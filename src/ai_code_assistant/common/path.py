#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import os
from pathlib import Path

APPLICATION_DATA_DIR = Path(f"{os.getenv('APPDATA')}/ai-code-assistant").resolve()
APPLICATION_DB_DIR = Path(APPLICATION_DATA_DIR, "db").resolve()
APPLICATION_REPOSITORY_DIR = Path(APPLICATION_DATA_DIR, "repository").resolve()
APPLICATION_TOOLS_DIR = Path(APPLICATION_DATA_DIR, "tools").resolve()

os.makedirs(APPLICATION_DB_DIR, exist_ok=True)


def remove_dir_contents(dir_path: Path) -> None:
    """
    Remove all contents of the given directory.
    Args:
        dir_path: Directory path.
    """
    if not dir_path.exists():
        return

    for item in dir_path.iterdir():
        if item.is_dir():
            remove_dir_contents(item)
        else:
            item.unlink()
    dir_path.rmdir()
