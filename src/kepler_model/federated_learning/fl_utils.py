import os
import sys

trainer_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(trainer_path)

util_path = os.path.join(os.path.dirname(__file__), '..', 'util')
sys.path.append(util_path)


prom_output_path = os.path.join(os.path.dirname(__file__), 'data', 'prom_output')
prom_output_filename = "prom_response"

from util.loader import load_json
from util.prom_types import prom_responses_to_results

def get_query_results(save_path=prom_output_path, save_name=prom_output_filename):
    response = load_json(save_path, save_name)
    return prom_responses_to_results(response)

SERVER_ADDRESS = "0.0.0.0:8081"
SPEC_DB_URL = "http://localhost:8080"
