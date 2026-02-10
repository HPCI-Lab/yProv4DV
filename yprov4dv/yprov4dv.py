import atexit
import os
import time
import sys
from prov.model import ProvDocument
from pathlib import Path
import shutil
import shlex
import pandas as pd
import xarray as xr
import geopandas as gpd
import rasterio as rio
import numpy as np
import torch
import matplotlib.pyplot as plt
import seaborn as sns

from . import utils
from . import file_utils

class ProvTracker:
    def _track_read_calls(self): 
        pd.read_csv = self._track_read_path(pd.read_csv)
        pd.read_parquet = self._track_read_path(pd.read_parquet)
        pd.read_excel = self._track_read_path(pd.read_excel)
        pd.read_json = self._track_read_path(pd.read_json)
        xr.open_dataset = self._track_read_path(xr.open_dataset)
        xr.open_mfdataset = self._track_read_path(xr.open_mfdataset)
        gpd.read_file = self._track_read_path(gpd.read_file)
        rio.open = self._track_read_path(rio.open)
        np.load = self._track_read_path(np.load)
        torch.load = self._track_read_path(torch.load)

    def _track_plot_calls(self): 
        self._orig_plot = plt.plot
        plt.plot = self._wrapped_plt_plot

        self._orig_pandas_call = pd.plotting._core.PlotAccessor.__call__
        tracker_instance = self
        def pandas_stub(accessor, *args, **kwargs):
            data = accessor._parent 
            tracker_instance._wrapped_pd_plot(data)
            return tracker_instance._orig_pandas_call(accessor, *args, **kwargs)
        pd.plotting._core.PlotAccessor.__call__ = pandas_stub

        sns_plots = ['scatterplot', 'lineplot', 'barplot', 'histplot', 'boxplot']
        for func_name in sns_plots:
            orig_func = getattr(sns, func_name)
            setattr(sns, func_name, self._make_sns_wrapper(orig_func))
        
    def __init__(
            self, 
            run_name : str = "experiment_run", 
            provenance_directory : str = "prov", 
            prefix : str = "yProv4DA", 
            default_namespace : str = "http://example.org/", 
            create_json_file : bool = False, 
            create_dot_file : bool = False, 
            create_svg_file : bool = False, 
            create_rocrate : bool = True,
            save_input_files_full : bool = True, 
            save_input_files_subset : bool = False,
            skip_files_larger_than : int = 50,
            verbose : bool = False, 
        ): 

        self.accessed_files = {}
        self.plot_count = 0

        self.PREFIX = prefix
        self.RUN_ID = 0
        self.EXPERIMENT_DIR = f"{provenance_directory}_{self.RUN_ID}"
        
        self.doc = ProvDocument()
        self.doc.set_default_namespace(default_namespace)
        self.doc.add_namespace(self.PREFIX, self.PREFIX)

        if os.path.exists(self.EXPERIMENT_DIR):
            prev_exps = os.listdir(".") 
            experiment_name = self.EXPERIMENT_DIR.removesuffix("_0")
            matching_files = [int(exp.split("_")[-1].split(".")[0]) for exp in prev_exps if utils.experiment_matches(experiment_name, exp)]
            self.RUN_ID = max(matching_files)+1  if len(matching_files) > 0 else 0
            self.EXPERIMENT_DIR = f"{experiment_name}_{self.RUN_ID}"
        os.makedirs(self.EXPERIMENT_DIR, exist_ok=True)

        self.INPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "inputs")
        self.SRC_DIR = os.path.join(self.EXPERIMENT_DIR, "src")
        self.OUTPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "outputs")
        self.PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))

        if not os.path.exists(self.INPUTS_DIR):
            os.makedirs(self.INPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.OUTPUTS_DIR):
            os.makedirs(self.OUTPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.SRC_DIR):
            os.makedirs(self.SRC_DIR, exist_ok=True)

        self.RUN_NAME = run_name
        self.verbose = verbose
        self.create_json = create_json_file
        self.create_graph = create_dot_file
        if self.create_graph and not self.create_json: 
            self.create_json = True
            if self.verbose: 
                print("[ProvTracker] YPROV4DV_CREATE_JSON_FILE cannot be False when requesting YPROV4DV_CREATE_DOT_FILE, turning it to True")
        self.create_svg = create_svg_file
        if self.create_svg and not (self.create_json and self.create_graph): 
            self.create_json, self.create_graph = True, True
            if self.verbose: 
                print("[ProvTracker] YPROV4DV_CREATE_JSON_FILE and YPROV4DV_CREATE_DOT_FILE cannot be False when requesting YPROV4DV_CREATE_SVG_FILE, turning them to True")
        self.crate_ro_crate = create_rocrate

        self.skip_files_larger_than = skip_files_larger_than
        self.save_input_files_full = save_input_files_full
        if self.save_input_files_full: 
            self._track_read_calls()
        self.save_input_files_subset = save_input_files_subset
        if self.save_input_files_subset: 
            self._track_plot_calls()

        self.start_time = time.time()
        self.start_snapshot = file_utils.snapshot(".")

        if self.verbose: 
            print("[ProvTracker] Monitoring started...")

    def _track_read_path(self, func):
        def wrapper(path, *a, **kw):
            try:
                self.accessed_files[Path(path).resolve()] = "r"
            except TypeError:
                pass  # file-like objects, buffers, URLs, etc.
            return func(path, *a, **kw)
        return wrapper
    
    
    def _make_sns_wrapper(self, orig_func):
        def wrapper(*args, **kwargs):
            # Seaborn usually takes data via the 'data' keyword argument
            data = kwargs.get('data')
            x = kwargs.get('x')
            y = kwargs.get('y')
            if data is None and x is None and y is None: 
                data = args[0]
            if x is not None and isinstance(x, str): 
                data = args[0]
                xdata = data[x]
            if y is not None and isinstance(y, str): 
                data = args[0]
                ydata = data[y]
            if data is not None:
                self._wrapped_pd_plot(data)
            if xdata is not None and ydata is not None: 
                self._wrapped_plt_plot(xdata, ydata)
            return orig_func(*args, **kwargs)
        return wrapper
    
    def _wrapped_pd_plot(self, *args, **kwargs): 
        self.plot_count += 1
        if self.verbose: 
            print(f"[ProvTracker] Tracking pandas or seaborn plot...")

        x_data = args[0]            
        if isinstance(x_data, (pd.DataFrame, pd.Series, np.ndarray)):
            xfilename = os.path.join(self.INPUTS_DIR, f"data_{self.plot_count}.csv")
            pd.DataFrame(x_data).to_csv(xfilename)
            self.accessed_files[Path(xfilename).resolve()] = "r"

        return self._orig_plot(*args, **kwargs)

    def _wrapped_plt_plot(self, *args, **kwargs):
        self.plot_count += 1
        if self.verbose: 
            print(f"[ProvTracker] Tracking matplotlib plot...")

        print(len(args))
        if len(args) >= 2:
            x_data = args[0]            
            if isinstance(x_data, (pd.Series, np.ndarray)):
                xfilename = os.path.join(self.INPUTS_DIR, f"xdata_{self.plot_count}.csv")
                pd.DataFrame(x_data).to_csv(xfilename)
                self.accessed_files[Path(xfilename).resolve()] = "r"

            y_data = args[1]
            if isinstance(y_data, (pd.Series, np.ndarray)):
                yfilename = os.path.join(self.INPUTS_DIR, f"ydata_{self.plot_count}.csv")
                pd.DataFrame(y_data).to_csv(yfilename)
                self.accessed_files[Path(yfilename).resolve()] = "r"

        return self._orig_plot(*args, **kwargs)

    def copy_file_to(self, file, _dir): 
        if self.verbose: 
            print(f"[ProvTracker] Copy File {file} to {_dir}...")
        filename = Path(file).name
        file_dst = os.path.join(_dir, filename)
        if file != Path(file_dst).resolve(): 
            shutil.copyfile(file, file_dst)
        return file_dst

    def finalize(self):
        if self.verbose: 
            print("[ProvTracker] Script ending. Analyzing changes...")

        end_snapshot = file_utils.snapshot(".")
        created = end_snapshot.keys() - self.start_snapshot.keys()
        modified = {p for p in self.start_snapshot.keys() & end_snapshot.keys() if self.start_snapshot[p] != end_snapshot[p]}
        for c in created: 
            log_output(c)
        for m in modified: 
            log_output(m)

        activity = self.doc.activity(f'{self.PREFIX}:{self.RUN_NAME}', time.ctime(self.start_time), time.ctime())

        repo = file_utils._get_git_remote_url()
        if repo is not None:
            commit_hash = file_utils._get_git_revision_hash()
            activity.add_attributes({f"{self.PREFIX}:source_code": os.path.join(repo, commit_hash)})
        reqs = file_utils._requirements_lookup(".")
        if reqs: 
            activity.add_attributes({f"{self.PREFIX}:requirements": reqs})
            log_input(reqs)
        activity.add_attributes({f"{self.PREFIX}:execution_command": " ".join(shlex.quote(c) for c in [sys.executable] + sys.argv)})
        
        for file, perm in self.accessed_files.items(): 
            if  "r" in perm: 
                size = os.path.getsize(file) // (1024**2)
                if size > self.skip_files_larger_than: 
                    if self.verbose: 
                        print(f"[ProvTracker] Skipped saving file {file} since larger than {self.skip_files_larger_than} Mb ({size} Mb)")
                    continue
                file_dst = self.copy_file_to(file, self.INPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.used(activity, entity)
            elif "w" in perm: 
                file_dst = self.copy_file_to(file, self.OUTPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.wasGeneratedBy(entity, activity)
            
        file_sources = file_utils._get_source_files()
        for file in file_sources: 
            file_dst = self.copy_file_to(file, self.SRC_DIR)
            entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
            self.doc.used(activity, entity)

        output_file = f'{self.RUN_NAME}.json'
        path_json = os.path.join(self.EXPERIMENT_DIR, output_file)
        if self.create_json: 
            with open(path_json, 'w') as f:
                f.write(self.doc.serialize())
            if self.verbose: 
                print(f"[ProvTracker] Provenance saved to {path_json}")

        if self.create_graph: 
            path_graph = os.path.join(self.EXPERIMENT_DIR, output_file)
            utils.save_prov_file(self.doc, self.EXPERIMENT_DIR, path_graph, self.create_graph, self.create_svg)
            if self.verbose: 
                print(f"[ProvTracker] Provenance graph to {path_graph}")

        if self.crate_ro_crate: 
            file_utils.create_rocrate_in_dir(self.EXPERIMENT_DIR)

_instance = None
    
def start_run(
    run_name : str = "experiment_run", 
    provenance_directory : str = "prov", 
    prefix : str = "yProv4DA", 
    default_namespace : str = "http://example.org/", 
    create_json_file : bool = False, 
    create_dot_file : bool = False, 
    create_svg_file : bool = False, 
    create_rocrate : bool = True,
    save_input_files_full : bool = True, 
    save_input_files_subset : bool = False,
    skip_files_larger_than : int = 50, 
    verbose : bool = False, 
): 
    global _instance
    _instance = ProvTracker(run_name, provenance_directory, prefix, default_namespace, create_json_file, create_dot_file, create_svg_file, create_rocrate, save_input_files_full, save_input_files_subset, skip_files_larger_than, verbose)
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
                print(f"[ProvTracker] Attempt to log {path} when {p} has already been logged with mode \"{mode}\"")
                return
    _instance.accessed_files[path] = mode
