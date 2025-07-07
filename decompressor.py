import base64
import os
from hac_core import hac_decompress

def decompress_file(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        compressed = f.read()

    decompressed = hac_decompress(compressed)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = base_name
    os.makedirs(out_dir, exist_ok=True)

    blocks = decompressed.split("__FILE_START__::")
    for block in blocks[1:]:
        try:
            header, rest = block.split('\n', 1)
            encoded_data, _ = rest.split("__FILE_END__", 1)
            rel_path = header.strip()
            raw_data = base64.b64decode(encoded_data)

            full_out_path = os.path.join(out_dir, rel_path)
            os.makedirs(os.path.dirname(full_out_path), exist_ok=True)
            with open(full_out_path, 'wb') as f:
                f.write(raw_data)
        except Exception as e:
            print(f"[!] Ошибка при извлечении файла: {e}")

    return out_dir
