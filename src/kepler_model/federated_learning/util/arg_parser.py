import argparse

from .fl_utils import (
    prom_output_path,
    prom_output_filename
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--save_path",
    default=prom_output_path,
    type=str,
    help="Save path of the input kepler query response"
)
parser.add_argument(
    "--save_name",
    default=prom_output_filename,
    type=str,
    help="Filename of the input kepler query response that can be found at the save_path"
)
# required argument
parser.add_argument(
    "--pipeline_name",
    type=str,
    help="Name of the power model pipeline at the client"
)
parser.add_argument(
    "--node_type",
    type=int,
    help="For specpower training; Node type on which this client local model is trained"
)
parser.add_argument(
    "--client",
    type=int,
    help="For specpower training; the client number for quick prototyping: TODO (change it to more meaningful argument)"
)