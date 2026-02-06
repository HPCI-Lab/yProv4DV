import atexit
import os
import time
import sys
from prov.model import ProvDocument
from pathlib import Path
import shutil
import shlex
import warnings
import pandas as pd
import xarray as xr
import geopandas as gpd
import rasterio as rio
import numpy as np
import torch

from . import utils
from . import file_utils

class ProvTracker:
    def __init__(self):
        self.PREFIX = os.environ.get('YPROV4DS_PREFIX', "yProv4DA")
        self.RUN_ID = 0
        self.EXPERIMENT_DIR = f"{os.environ.get('YPROV4DS_PROVENANCE_DIRECTORY', "prov")}_{self.RUN_ID}"
        self.INPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "inputs")
        self.SRC_DIR = os.path.join(self.EXPERIMENT_DIR, "src")
        self.OUTPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "outputs")
        self.PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))

        if not os.path.exists(self.EXPERIMENT_DIR):
            os.makedirs(self.EXPERIMENT_DIR, exist_ok=True)

        self.RUN_NAME = os.environ.get('YPROV4DS_RUN_NAME', "experiment_run")
        self.verbose = utils.parse_bool(os.environ.get('YPROV4DS_VERBOSE', "False"))
        self.create_json = utils.parse_bool(os.environ.get('YPROV4DS_CREATE_JSON_FILE', "False"))
        self.create_graph = utils.parse_bool(os.environ.get('YPROV4DS_CREATE_DOT_FILE', "False"))
        if self.create_graph and not self.create_json: 
            self.create_json = True
            if self.verbose: 
                warnings.warn("[ProvTracker] YPROV4DS_CREATE_JSON_FILE cannot be False when requesting YPROV4DS_CREATE_DOT_FILE, turning it to True")
        self.create_svg = utils.parse_bool(os.environ.get('YPROV4DS_CREATE_SVG_FILE', "False"))
        if self.create_svg and not (self.create_json and self.create_graph): 
            self.create_json, self.create_graph = True, True
            if self.verbose: 
                warnings.warn("[ProvTracker] YPROV4DS_CREATE_JSON_FILE and YPROV4DS_CREATE_DOT_FILE cannot be False when requesting YPROV4DS_CREATE_SVG_FILE, turning them to True")

        self.crate_ro_crate = utils.parse_bool(os.environ.get('YPROV4DS_CREATE_RO_CRATE', "True"))

        self.accessed_files = {}

        self.doc = ProvDocument()
        self.doc.set_default_namespace(os.environ.get('YPROV4DS_DEFAULT_NAMESPACE', 'http://example.org/'))
        self.doc.add_namespace(self.PREFIX, self.PREFIX)
        self.start_time = time.time()

        self.start_snapshot = file_utils.snapshot(".")

        pd.read_csv = self.track_path(pd.read_csv)
        pd.read_parquet = self.track_path(pd.read_parquet)
        pd.read_excel = self.track_path(pd.read_excel)
        pd.read_json = self.track_path(pd.read_json)
        xr.open_dataset = self.track_path(xr.open_dataset)
        xr.open_mfdataset = self.track_path(xr.open_mfdataset)
        gpd.read_file = self.track_path(gpd.read_file)
        rio.open = self.track_path(rio.open)
        np.load = self.track_path(np.load)
        torch.load = self.track_path(torch.load)

        if self.verbose: 
            warnings.warn("[ProvTracker] Monitoring started...")

    def track_path(self, func):
        def wrapper(path, *a, **kw):
            try:
                self.accessed_files[Path(path).resolve()] = "r"
            except TypeError:
                pass  # file-like objects, buffers, URLs, etc.
            return func(path, *a, **kw)
        return wrapper

    def copy_file_to(self, file, _dir): 
        if self.verbose: 
            warnings.warn(f"[ProvTracker] Copy File {file} to {_dir}...")
        filename = Path(file).name
        file_dst = os.path.join(_dir, filename)
        shutil.copyfile(file, file_dst)
        return file_dst

    def finalize(self):
        if self.verbose: 
            warnings.warn("[ProvTracker] Script ending. Analyzing changes...")

        end_snapshot = file_utils.snapshot(".")
        created = end_snapshot.keys() - self.start_snapshot.keys()
        modified = {p for p in self.start_snapshot.keys() & end_snapshot.keys() if self.start_snapshot[p] != end_snapshot[p]}
        for c in created: 
            log_output(c)
        for m in modified: 
            log_output(m)

        activity = self.doc.activity(f'{self.PREFIX}:{self.RUN_NAME}', time.ctime(self.start_time), time.ctime())

        if os.path.exists(self.EXPERIMENT_DIR):
            prev_exps = os.listdir(".") 
            experiment_name = self.EXPERIMENT_DIR.removesuffix("_0")
            matching_files = [int(exp.split("_")[-1].split(".")[0]) for exp in prev_exps if utils.experiment_matches(experiment_name, exp)]
            self.RUN_ID = max(matching_files)+1  if len(matching_files) > 0 else 0
            self.EXPERIMENT_DIR = f"{experiment_name}_{self.RUN_ID}"
        os.makedirs(self.EXPERIMENT_DIR, exist_ok=True)

        if not os.path.exists(self.INPUTS_DIR):
            os.makedirs(self.INPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.OUTPUTS_DIR):
            os.makedirs(self.OUTPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.SRC_DIR):
            os.makedirs(self.SRC_DIR, exist_ok=True)

        repo = file_utils._get_git_remote_url()
        if repo is not None:
            commit_hash = file_utils._get_git_revision_hash()
            activity.add_attributes({f"{self.PREFIX}:source_code": os.path.join(repo, commit_hash)})
        reqs = file_utils._requirements_lookup(".")
        if reqs: 
            activity.add_attributes({f"{self.PREFIX}:requirements": reqs})
        activity.add_attributes({f"{self.PREFIX}:execution_command": " ".join(shlex.quote(c) for c in [sys.executable] + sys.argv)})
        
        for file, perm in self.accessed_files.items(): 
            if  "r" in perm: 
                file_dst = self.copy_file_to(file, self.INPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.used(entity, activity)
            elif "w" in perm: 
                file_dst = self.copy_file_to(file, self.OUTPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.wasGeneratedBy(entity, activity)
            
        file_sources = file_utils._get_source_files()
        for file in file_sources: 
            file_dst = self.copy_file_to(file, self.SRC_DIR)
            entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
            self.doc.used(entity, activity)

        output_file = f'{self.RUN_NAME}.json'
        path_json = os.path.join(self.EXPERIMENT_DIR, output_file)
        if self.create_json: 
            with open(path_json, 'w') as f:
                f.write(self.doc.serialize())
            if self.verbose: 
                warnings.warn(f"[ProvTracker] Provenance saved to {path_json}")

        if self.create_graph: 
            path_graph = os.path.join(self.EXPERIMENT_DIR, output_file)
            utils.save_prov_file(self.doc, self.EXPERIMENT_DIR, path_graph, self.create_graph, self.create_svg)
            if self.verbose: 
                warnings.warn(f"[ProvTracker] Provenance graph to {path_graph}")

        if self.crate_ro_crate: 
            file_utils.create_rocrate_in_dir(self.EXPERIMENT_DIR)

_instance = ProvTracker()
atexit.register(_instance.finalize)
    
def log_input(path): 
    log_file(path, "r")

def log_output(path): 
    log_file(path, "w")

def log_file(path, mode): 
    global _instance
    path = Path(path)
    for p in _instance.accessed_files.keys(): 
        if p.name in path.name or path.name in p.name: 
            if utils.paths_are_same(p, path): 
                warnings.warn(f"[ProvTracker] Attempt to log {path} when {p} has already been logged with mode \"{mode}\"")
                return
    _instance.accessed_files[path] = mode
