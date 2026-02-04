import atexit
import os
import time
import sys
from prov.model import ProvDocument
from pathlib import Path
import shutil

from yprov4dv.utils import save_prov_file
from yprov4dv.file_utils import _get_git_revision_hash, _get_git_remote_url, _requirements_lookup, _get_source_files, create_rocrate_in_dir

class ProvTracker:
    def __init__(self):
        self.PREFIX = os.environ.get('YPROV4DS_PREFIX', "yProv4DA")
        self.EXPERIMENT_DIR = os.environ.get('YPROV4DS_PROVENANCE_DIRECTORY', "prov")
        self.INPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "inputs")
        self.SRC_DIR = os.path.join(self.EXPERIMENT_DIR, "src")
        self.OUTPUTS_DIR = os.path.join(self.EXPERIMENT_DIR, "outputs")
        self.PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))

        self.RUN_NAME = os.environ.get('YPROV4DS_RUN_NAME', "experiment_run")
        self.verbose = bool(os.environ.get('YPROV4DS_VERBOSE', "False"))
        self.create_json = bool(os.environ.get('YPROV4DS_CREATE_JSON_FILE', "False"))
        self.create_graph = bool(os.environ.get('YPROV4DS_CREATE_DOT_FILE', "False"))
        self.create_svg = bool(os.environ.get('YPROV4DS_CREATE_SVG_FILE', "False"))
        self.crate_ro_crate = bool(os.environ.get('YPROV4DS_CREATE_RO_CRATE', "True"))

        self.accessed_files = {}

        self.doc = ProvDocument()
        self.doc.set_default_namespace(os.environ.get('YPROV4DS_DEFAULT_NAMESPACE', 'http://example.org/'))
        self.doc.add_namespace(self.PREFIX, self.PREFIX)
        self.start_time = time.time()
        if self.verbose: 
            print("[ProvTracker] Monitoring started...")

    def copy_file_to(self, file, _dir): 
        if self.verbose: 
            print(f"[ProvTracker] Copy File {file} to {_dir}...")
        filename = Path(file).name
        file_dst = os.path.join(_dir, filename)
        shutil.copyfile(file, file_dst)
        return file_dst

    def finalize(self):
        if self.verbose: 
            print("\n[ProvTracker] Script ending. Analyzing changes...")

        activity = self.doc.activity(f'{self.PREFIX}:{self.RUN_NAME}', time.ctime(self.start_time), time.ctime())

        if not os.path.exists(self.EXPERIMENT_DIR):
            os.makedirs(self.EXPERIMENT_DIR, exist_ok=True)
        if not os.path.exists(self.INPUTS_DIR):
            os.makedirs(self.INPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.OUTPUTS_DIR):
            os.makedirs(self.OUTPUTS_DIR, exist_ok=True)
        if not os.path.exists(self.SRC_DIR):
            os.makedirs(self.SRC_DIR, exist_ok=True)

        repo = _get_git_remote_url()
        if repo is not None:
            commit_hash = _get_git_revision_hash()
            activity.add_attributes({f"{self.PREFIX}:source_code", os.path.join(repo, commit_hash)})
        reqs = _requirements_lookup(".")
        if reqs: 
            activity.add_attributes({f"{self.PREFIX}:requirements": reqs})
        
        for file, perm in self.accessed_files.items(): 
            if  "r" in perm: 
                file_dst = self.copy_file_to(file, self.INPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.used(entity, activity)
            elif "w" in perm: 
                file_dst = self.copy_file_to(file, self.OUTPUTS_DIR)
                entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
                self.doc.wasGeneratedBy(entity, activity)
            
        file_sources = _get_source_files()
        for file in file_sources: 
            file_dst = self.copy_file_to(file, self.SRC_DIR)
            entity = self.doc.entity(f'{self.PREFIX}:{file_dst}')
            self.doc.used(entity, activity)

        output_file = 'provenance_log.json'
        path_json = os.path.join(self.EXPERIMENT_DIR, output_file)
        if self.create_json: 
            with open(path_json, 'w') as f:
                f.write(self.doc.serialize())
            if self.verbose: 
                print(f"[ProvTracker] Provenance saved to {path_json}")

        if self.create_graph: 
            path_graph = os.path.join(self.EXPERIMENT_DIR, output_file)
            save_prov_file(self.doc, self.EXPERIMENT_DIR, path_graph, self.create_graph, self.create_svg)
            if self.verbose: 
                print(f"[ProvTracker] Provenance graph to {path_graph}")

        if self.crate_ro_crate: 
            create_rocrate_in_dir(self.EXPERIMENT_DIR)

_instance = ProvTracker()
atexit.register(_instance.finalize)
    
def log_input(path): 
    global _instance
    _instance.accessed_files[path] = "r"

def log_output(path): 
    global _instance
    _instance.accessed_files[path] = "w"