from pathlib import Path
from PIL import Image
import tarfile
import io
import base64

def restore_source_files_from_image(image_path: str, output_dir: str = "."):
    """Extracts and decompresses embedded source files from a PNG image."""
    image = Image.open(image_path)
    b64_data = image.info.get("CompressedSource")
    
    if not b64_data:
        raise ValueError(f"No 'CompressedSource' metadata found in {image_path}")

    compressed_bytes = base64.b64decode(b64_data)
    buffer = io.BytesIO(compressed_bytes)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    with tarfile.open(fileobj=buffer, mode="r:gz") as tar:
        tar.extractall(path=out_path)
        extracted_files = tar.getnames()

    print(f"Successfully restored {len(extracted_files)} files to '{out_path.resolve()}':")
    for name in extracted_files:
        print(f" - {name}")