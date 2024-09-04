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
