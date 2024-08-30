import os
import sys

from .helpers import build_path_append, build_path
from .constants import (
    CURRENT_DIR,
    PREV_DIR,
    UTIL_DIR,
    DATA_DIR,
    MODELS_DIR,
    ACPI_DIR,
    ABS_POWER_DIR,
    XGBOOST_TRAINER,
    METADATA_FILE,
    XGBOOST_MODEL_FILE,
    CHECKPOINT_DIR,
    PROM_OUTPUT_DIR,
    PROM_RESPONSE,
    FEATURE_GROUP_TEST,
    SERVER_ADDRESS,
    SPEC_DB_URL,
    TRAINER_NAME,
    ARGUMENT_ASSERTION_ERROR,
    ARGUMENT_PIPELINE_NAME,
    ARGUMENT_NODE_TYPE,
    ARGUMENT_CLIENT
)

from kepler_model.util.loader import load_json
from kepler_model.util.prom_types import prom_responses_to_results

prom_output_path = build_path(CURRENT_DIR, PREV_DIR, DATA_DIR, PROM_OUTPUT_DIR)
prom_output_filename = PROM_RESPONSE

def get_query_results(save_path=prom_output_path, save_name=prom_output_filename):
    response = load_json(save_path, save_name)
    return prom_responses_to_results(response)

def get_metrics_from_dict(contents):
    return contents["mae"], contents["mape"], contents["mse"], contents["rmse"], contents["r2"]

def get_eval_metrics(mae, mape, mse, rmse, r2):
    metrics = dict()
    metrics["mae"] = mae
    metrics["mape"] = mape
    metrics["mse"] = mse
    metrics["rmse"] = rmse
    metrics["r2"] = r2
    return metrics

def get_metadata_filename(pipeline_name, feature_group, node_type=0):
    filename = build_path(PREV_DIR, PREV_DIR, MODELS_DIR, pipeline_name, ACPI_DIR,
                          ABS_POWER_DIR, feature_group, XGBOOST_TRAINER.format(str(node_type)),
                          METADATA_FILE)
    return filename

def get_model_filename(pipeline_name, feature_group, node_type=0):
    filename = build_path(PREV_DIR, PREV_DIR, MODELS_DIR, pipeline_name, ACPI_DIR,
                          ABS_POWER_DIR, feature_group, CHECKPOINT_DIR,
                          XGBOOST_MODEL_FILE.format(str(node_type)))
    return filename

# TODO: remove these functions - only for testing
# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__