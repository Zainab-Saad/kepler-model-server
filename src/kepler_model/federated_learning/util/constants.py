import os

CURRENT_DIR = os.path.dirname(__file__)
PREV_DIR = '..'
UTIL_DIR = 'util'
DATA_DIR = 'data'
MODELS_DIR = 'models'
ACPI_DIR = 'acpi'
ABS_POWER_DIR = 'AbsPower'
TRAINER_NAME = 'XgboostFitTrainer'
XGBOOST_TRAINER = 'XgboostFitTrainer_{}'
METADATA_FILE = 'metadata.json'
XGBOOST_MODEL_FILE = 'XgboostFitTrainer_platform_{}.json'
CHECKPOINT_DIR = 'checkpoint'
PROM_OUTPUT_DIR = 'prom_output'
SERVER_ADDRESS = "0.0.0.0:8081"
SPEC_DB_URL = "http://localhost:8080"
PROM_RESPONSE = "prom_response"
FEATURE_GROUP_TEST = "BPFOnly"
ARGUMENT_ASSERTION_ERROR = "Argument --{} is required"
ARGUMENT_PIPELINE_NAME = "pipeline_name"
ARGUMENT_NODE_TYPE = "node_type"
ARGUMENT_CLIENT = "client"