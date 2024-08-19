import os
import sys

trainer_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(trainer_path)

util_path = os.path.join(os.path.dirname(__file__), '..', 'util')
sys.path.append(util_path)

from train.pipeline import NewPipeline
from train.extractor.extractor import DefaultExtractor
from train.isolator.isolator import MinIdleIsolator
from train.specpower_pipeline import SpecPipelineRun

from util.prom_types import node_info_column, get_valid_feature_group_from_queries
from util.train_types import (
    FeatureGroups,
    FeatureGroup,
    PowerSourceMap
)
from util.format import time_to_str
from util.extract_types import component_to_col

from arg_parser import parser