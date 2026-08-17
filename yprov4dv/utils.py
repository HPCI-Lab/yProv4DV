
import subprocess
import os
import sys
from pathlib import Path
import base64
import io
import tarfile

def _get_compressed_source_b64(source_files: list[str]) -> str:
    buffer = io.BytesIO()
    
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for file_path in source_files:
            try:
                tar.add(file_path, arcname=file_path)
            except FileNotFoundError:
                continue

    compressed_bytes = buffer.getvalue()
    return base64.b64encode(compressed_bytes).decode("utf-8")

# def snapshot(root: Path):
#     if isinstance(root, str): 
#         root = Path(root)
#     return {p.resolve(): p.stat().st_mtime for p in root.rglob("*") if p.is_file()}

def _get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def _get_git_remote_url():
    try:
        remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], stderr=subprocess.DEVNULL).strip().decode()
        return remote_url
    except subprocess.CalledProcessError:
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

    for _, module in sys.modules.items():
        module_path = getattr(module, "__file__", None)
        
        if module_path and module_path.endswith(".py"):
            abs_module_path = os.path.realpath(module_path)
            
            is_in_project = abs_module_path.startswith(project_root)
            is_not_library = "site-packages" not in abs_module_path
            
            if is_in_project and is_not_library and os.path.exists(abs_module_path):
                rel_path = os.path.relpath(abs_module_path, project_root)
                source_files.add(rel_path)
        
    return {os.path.join("./", pre_rel_path, s) for s in source_files}
