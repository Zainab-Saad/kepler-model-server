"""
- run the following command to serve kepler_spec_power_db
    docker run -it -p 8080:80 quay.io/sustainability/kepler_spec_power_db:v0.7
"""

import flwr as fl
import pandas as pd
import datetime

from imports import (
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

from fl_utils import (
    SERVER_ADDRESS,
    SPEC_DB_URL
)
from client import KeplerClient

args = parser.parse_args()

feature_group_test = "BPFOnly"

# this class overrides the KeplerClient train() method to train on individual node type data on each client
class SpecPowerTrainerClient(KeplerClient):
    def __init__(self, query_results, pipeline_name, node_type, abs_trainer_names=['XgboostFitTrainer'],
                 dyn_trainer_names=['XgboostFitTrainer'],
                 extractor=DefaultExtractor(), isolator=MinIdleIsolator(),
                 target_energy_sources=PowerSourceMap.keys(),
                 valid_feature_groups=FeatureGroups.keys()) -> None:

        super().__init__(query_results, pipeline_name, abs_trainer_names,
                         dyn_trainer_names, extractor, isolator,
                         target_energy_sources, valid_feature_groups)
        self.node_type = node_type
        self.power_labels = [component_to_col(self.energy_components[0])]

    # override this method
    def train(self):
        abs_data = pd.concat(self.query_results.values(), ignore_index=True)
        abs_data_node_type = abs_data[abs_data[node_info_column] == int(self.node_type)]
        self.pipeline._train(abs_data_node_type, None, self.power_labels,
                             self.target_energy_sources, FeatureGroup.BPFOnly.name)
        self.pipeline.print_pipeline_process_end(self.target_energy_sources,
                                                 FeatureGroup.BPFOnly.name, abs_data_node_type, None)
        self.pipeline.metadata["last_update_time"] = time_to_str(datetime.datetime.utcnow())
        self.pipeline.save_metadata()
        self.pipeline.node_collection.save()
        self.pipeline.archive_pipeline()
        self.datasize = len(abs_data)
        return True, abs_data, None

    def get_metdata_filename(self):
        filename = os.path.join('..', 'models', self.pipeline_name,
                                'acpi', 'AbsPower', feature_group_test,
                                'XgboostFitTrainer_'+self.node_type, 'metadata.json')
        return filename

    def get_model_filename(self):
        filename = os.path.join('..', 'models', self.pipeline_name,
                                'acpi', 'AbsPower', feature_group_test,
                                'checkpoint', 'XgboostFitTrainer_platform_'+self.node_type+'.json')
        return filename

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def init_specpower_client():
    assert args.pipeline_name, "Argument --pipeline_name is required"
    assert args.node_type, "Argument --node_type is required"
    node_type = args.node_type
    pipelinerun = SpecPipelineRun(args.pipeline_name)
    # same as the query_results var in init_kepler_client
    blockPrint()
    spec_extracted_data = pipelinerun.load_spec_data(SPEC_DB_URL)
    enablePrint()
    # valid_feature_groups = get_valid_feature_group_from_queries(spec_extracted_data.keys())

    client = SpecPowerTrainerClient(spec_extracted_data, args.pipeline_name,
                                    node_type, valid_feature_groups=[FeatureGroup.BPFOnly])
    # Start Flower client
    fl.client.start_numpy_client(server_address=SERVER_ADDRESS, client=client)

if __name__ == "__main__":
    init_specpower_client()
