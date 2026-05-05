import os
from ..config import IGNORE_DIRS, IGNORE_FILES

def build_file_tree(root):
    files = []

    for root, dirs, filenames in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for f in filenames:
            if any(f.endswith(x) for x in IGNORE_FILES):
                continue
            files.append(os.path.join(root, f))

    return files