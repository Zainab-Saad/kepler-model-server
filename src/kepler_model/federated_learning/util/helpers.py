import os
import sys

def build_path(*args):
    return os.path.join(*args)

def build_path_append(*args):
    path = build_path(*args)
    sys.path.append(path)
