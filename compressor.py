import os
import base64
from hac_core import hac_compress

def encode_file_to_base64(path: str, rel_path: str = None) -> str:
    with open(path, 'rb') as f:
        raw = f.read()
    name = rel_path if rel_path else os.path.basename(path)
    encoded = base64.b64encode(raw).decode('utf-8')
    return f"__FILE_START__::{name}\n{encoded}\n__FILE_END__"

def read_folder_binary(folder: str) -> list[str]:
    encoded_files = []
    for root, _, files in os.walk(folder):
        for fname in files:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, start=os.path.dirname(folder))
            try:
                encoded_files.append(encode_file_to_base64(full_path, rel_path))
            except Exception as e:
                print(f"[!] Пропущен файл {full_path}: {e}")
    return encoded_files

def compress_files(paths: list[str], level: int = 1) -> str:
    all_encoded = []
    archive_name = "archive"

    if len(paths) == 1:
        base = os.path.basename(paths[0])
        archive_name = os.path.splitext(base)[0] if os.path.isfile(paths[0]) else base
    else:
        archive_name = "MultipleFiles"

    for path in paths:
        if os.path.isfile(path):
            all_encoded.append(encode_file_to_base64(path))
        elif os.path.isdir(path):
            all_encoded += read_folder_binary(path)
        else:
            print(f"[!] Пропущен путь: {path}")

    joined_data = "\n".join(all_encoded)
    compressed = hac_compress(joined_data)
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output = os.path.join(desktop, f"{archive_name}.hac")

    with open(output, 'w', encoding="utf-8") as f:
        f.write(compressed)

    return output
