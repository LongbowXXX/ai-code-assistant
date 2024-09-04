#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from pathlib import Path

from pydantic import BaseModel

from ai_code_assistant.common.path import (
    APPLICATION_DATA_DIR,
    APPLICATION_DB_DIR,
    APPLICATION_REPOSITORY_DIR,
    APPLICATION_TOOLS_DIR,
)


class AppContext(BaseModel):
    data_dir: Path = APPLICATION_DATA_DIR
    db_dir: Path = APPLICATION_DB_DIR
    repository_dir: Path = APPLICATION_REPOSITORY_DIR
    tools_dir_path: Path = APPLICATION_TOOLS_DIR
