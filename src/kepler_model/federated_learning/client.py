import flwr as fl
import os
import json

from flwr.common import (
    Code,
    FitRes,
    FitIns,
    GetParametersIns,
    GetParametersRes,
    Parameters,
    Status,
    EvaluateIns,
    EvaluateRes
)

from imports import (
    NewPipeline,
    DefaultExtractor,
    MinIdleIsolator,
    FeatureGroups,
    PowerSourceMap,
    get_valid_feature_group_from_queries,
    parser
)

from fl_utils import (
    get_query_results,
    prom_output_path,
    prom_output_filename,
    SERVER_ADDRESS
)

feature_group_test = "BPFOnly"

args = parser.parse_args()

class KeplerClient(fl.client.Client):
    # TODO the pipeline_name should be some id generated by the aggregator for client
    def __init__(self, query_results, pipeline_name, abs_trainer_names=['XgboostFitTrainer'],
                 dyn_trainer_names=['XgboostFitTrainer'],
                 extractor=DefaultExtractor(), isolator=MinIdleIsolator(),
                 target_energy_sources=PowerSourceMap.keys(),
                 valid_feature_groups=FeatureGroups.keys()) -> None:
        super().__init__()

        # initialize the training pipeline
        self.pipeline = NewPipeline(pipeline_name, abs_trainer_names, dyn_trainer_names,
                                    extractor, isolator, list(target_energy_sources),
                                    valid_feature_groups)
        self.query_results = query_results
        self.valid_feature_groups = valid_feature_groups
        # TODO if target_energy_sources is ['acpi', 'intel_rapl'] => train the model for each of the energy source seperately
        self.target_energy_sources = list(target_energy_sources)[1]
        self.energy_components = PowerSourceMap[self.target_energy_sources]
        self.pipeline_name = pipeline_name
        self.datasize = -1

    def train(self):
        # self.pipeline.node_collection.index_train_machine("test", spec)
        success, abs_data, dyn_data = self.pipeline.process(self.query_results, self.energy_components,
                                                            self.target_energy_sources, feature_group_test)
        self.pipeline.save_metadata()
        self.pipeline.node_collection.save()
        self.pipeline.archive_pipeline()
        self.datasize = len(abs_data)
        return success, abs_data, dyn_data

    def get_parameters(self, ins: GetParametersIns) -> GetParametersRes:
        return GetParametersRes(
            status=Status(
                code=Code.OK,
                message="OK",
            ),
            parameters=Parameters(tensor_type="", tensors=[]),
        )

    def fit(self, ins: FitIns) -> FitRes:
        global_round = int(ins.config["global_round"])

        if global_round  != 1:
            global_model = ins.parameters.tensors
            dict_obj = json.loads(global_model[0])
            json_obj = json.dumps(dict_obj, separators=(',', ':'))
            filename = self.get_model_filename()
            with open(filename, 'w') as outfile:
                outfile.write(json_obj)

        sucess, abs_data, dyn_data = self.train()
        filename = self.get_model_filename()
        with open(filename, "r") as f:
            contents = f.read()
        json_bytes = contents.encode('utf-8')
        json_bytearray = bytearray(json_bytes)
        encoded_weights = bytes(json_bytearray)
        self.datasize = len(abs_data)
        return FitRes(
            status=Status(
                code=Code.OK,
                message="OK",
            ),
            parameters=Parameters(tensor_type="", tensors=[encoded_weights]),
            num_examples=self.datasize,
            metrics={},
        )

    def evaluate(self, ins: EvaluateIns) -> EvaluateRes:
        filename = self.get_metdata_filename()
        with open(filename, "r") as f:
            contents = f.read()
        contents = json.loads(contents)

        return EvaluateRes(
            status=Status(
                code=Code.OK,
                message="OK",
            ),
            loss=0.0,
            num_examples=contents["test_dataset_size"],
            metrics={"mae": contents["mae"]},
        )

    def get_metdata_filename(self):
        filename = os.path.join('..', 'models', self.pipeline_name,
                                'acpi', 'AbsPower', feature_group_test,
                                'XgboostFitTrainer_0', 'metadata.json')
        return filename

    def get_model_filename(self):
        filename = os.path.join('..', 'models', self.pipeline_name,
                                'acpi', 'AbsPower', feature_group_test,
                                'checkpoint', 'XgboostFitTrainer_platform_0.json')
        return filename

def init_kepler_client(save_path=prom_output_path, save_name=prom_output_filename):
    query_results = get_query_results(save_path, save_name)
    valid_feature_groups = get_valid_feature_group_from_queries(query_results.keys())
    assert args.pipeline_name, "Argument --pipeline_name is required"
    client = KeplerClient(query_results, args.pipeline_name, valid_feature_groups=valid_feature_groups)
    # Start Flower client
    fl.client.start_numpy_client(server_address=SERVER_ADDRESS, client=client)

if __name__ == "__main__":
    init_kepler_client(args.save_path, args.save_name)
