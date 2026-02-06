
import subprocess
import os
import sys
from rocrate.rocrate import ROCrate
from pathlib import Path

def snapshot(root: Path):
    if isinstance(root, str): 
        root = Path(root)
    return {p.resolve(): p.stat().st_mtime for p in root.rglob("*") if p.is_file()}

def _get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def _get_git_remote_url():
    try:
        remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], stderr=subprocess.DEVNULL).strip().decode()
        return remote_url
    except subprocess.CalledProcessError:
        print("> get_git_remote_url() Repository not found")
        return None  # No remote found
    
def _requirements_lookup(path): 
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename == "requirements.txt": 
                return os.path.join(root, filename)
    return None
    
def _get_source_files():
    entry_script = os.path.realpath(sys.argv[0])
    project_root = os.path.dirname(entry_script)
    cwd = os.getcwd()
    pre_rel_path = project_root.replace(cwd + "/", "")

    source_files = set()
    if os.path.exists(entry_script) and entry_script.endswith('.py'):
        source_files.add(os.path.relpath(entry_script, project_root))

    for name, module in sys.modules.items():
        module_path = getattr(module, "__file__", None)
        
        if module_path and module_path.endswith(".py"):
            abs_module_path = os.path.realpath(module_path)
            
            is_in_project = abs_module_path.startswith(project_root)
            is_not_library = "site-packages" not in abs_module_path
            
            if is_in_project and is_not_library:
                rel_path = os.path.relpath(abs_module_path, project_root)
                source_files.add(rel_path)
        
    return {os.path.join("./", pre_rel_path, s) for s in source_files}

def get_properties_from_file(file : str):
    if file.endswith(".dot"): 
        return {
            "name": "pygraphviz provenance graph file",
            "encodingFormat": "application/dot"
        }
    elif file.endswith(".csv"): 
        return {
            "name": "metric",
            "encodingFormat": "text/csv"
        }
    elif file.endswith(".svg"): 
        return {
            "name": "pygraphviz svg provenance graph file",
            "encodingFormat": "image/svg+xml"
        }
    elif file.endswith(".json") and "/" not in file: 
        return {
            "name": "provenance JSON file",
            "encodingFormat": "text/json"
        }
    elif file.endswith(".json") and "/" in file: 
        return {
            "name": "JSON property description",
            "encodingFormat": "text/json"
        }
    elif file.endswith(".pt") or file.endswith(".pth"): 
        return {
            "name": "pytorch model checkpoint",
            "encodingFormat": "application/octet-stream"
        }
    elif file.endswith(".py"): 
        return {
            "name": "python source file",
            "encodingFormat": "text/plain"
        }
    else: 
        return {
            "name": file,
            "encodingFormat": f"{file.split('.')[-1]}",
        }

def create_rocrate_in_dir(directory): 
    crate = ROCrate()

    for (d, _, fs) in os.walk(directory): 
        for f in fs: 
            file_path = d + "/" + f
            if os.path.exists(file_path):
                property = get_properties_from_file(file_path)
                property["@type"] = "File" 
                property["@id"] = file_path
                crate.add_file(file_path, dest_path=file_path, properties=property)

    # crate.write("exp_crate")
    crate.write_zip(f"{directory}.zip")