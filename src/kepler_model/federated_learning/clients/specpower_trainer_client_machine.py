"""
- run the following command to serve kepler_spec_power_db
    docker run -it -p 8080:80 quay.io/sustainability/kepler_spec_power_db:v0.7
"""

import flwr as fl
import pandas as pd
import datetime

from kepler_model.federated_learning.util.imports import (
    DefaultExtractor,
    MinIdleIsolator,
    SpecPipelineRun,
    FeatureGroups,
    FeatureGroup,
    PowerSourceMap,
    get_valid_feature_group_from_queries,
    time_to_str,
    component_to_col,
    node_info_column,
    parser
)

from kepler_model.federated_learning.util.fl_utils import (
    blockPrint,
    enablePrint,
    SERVER_ADDRESS,
    SPEC_DB_URL,
    TRAINER_NAME,
    ARGUMENT_ASSERTION_ERROR,
    ARGUMENT_PIPELINE_NAME,
    ARGUMENT_NODE_TYPE,
    ARGUMENT_CLIENT
)

from kepler_model.federated_learning.clients.client import KeplerClient

args = parser.parse_args()

feature_group_test = "BPFOnly"

# this class overrides the KeplerClient train() method to train on individual node type data on each client
class SpecPowerTrainerClient(KeplerClient):
    def __init__(self, query_results, pipeline_name, node_type, abs_trainer_names=[TRAINER_NAME],
                 dyn_trainer_names=[TRAINER_NAME],
                 extractor=DefaultExtractor(), isolator=MinIdleIsolator(),
                 target_energy_sources=PowerSourceMap.keys(),
                 valid_feature_groups=FeatureGroups.keys()) -> None:

        super().__init__(query_results, pipeline_name, abs_trainer_names,
                         dyn_trainer_names, extractor, isolator,
                         target_energy_sources, valid_feature_groups)
        self.node_type = str(node_type)
        self.power_labels = [component_to_col(self.energy_components[0])]

    # override this method
    def train(self):
        abs_data = pd.concat(self.query_results.values(), ignore_index=True)
        self.pipeline._train(abs_data, None, self.power_labels,
                             self.target_energy_sources, FeatureGroup.BPFOnly.name)
        self.pipeline.print_pipeline_process_end(self.target_energy_sources,
                                                 FeatureGroup.BPFOnly.name, abs_data, None)
        self.pipeline.metadata["last_update_time"] = time_to_str(datetime.datetime.utcnow())
        self.pipeline.save_metadata()
        self.pipeline.node_collection.save()
        self.pipeline.archive_pipeline()
        self.datasize = len(abs_data)
        return True, abs_data, None

def init_specpower_client():
    assert args.pipeline_name, ARGUMENT_ASSERTION_ERROR.format(ARGUMENT_PIPELINE_NAME)
    assert args.node_type, ARGUMENT_ASSERTION_ERROR.format(ARGUMENT_NODE_TYPE)
    assert args.client, ARGUMENT_ASSERTION_ERROR.format(ARGUMENT_CLIENT)
    client_no = args.client
    node_type = args.node_type
    pipelinerun = SpecPipelineRun(args.pipeline_name)
    blockPrint()
    # spec_extracted_data = pipelinerun.load_spec_machine_data(client_no, node_type, SPEC_DB_URL)
    spec_extracted_data = pipelinerun.load_spec_machine_data(client_no, node_type, SPEC_DB_URL)
    enablePrint()
    # valid_feature_groups = get_valid_feature_group_from_queries(spec_extracted_data.keys())
    client = SpecPowerTrainerClient(spec_extracted_data, args.pipeline_name,
                                    node_type, valid_feature_groups=[FeatureGroup.BPFOnly])
    # Start Flower client
    fl.client.start_numpy_client(server_address=SERVER_ADDRESS, client=client)

if __name__ == "__main__":
    init_specpower_client()