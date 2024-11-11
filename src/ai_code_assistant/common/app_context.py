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
    """
    AppContext is a configuration class that holds various directory paths used by the application.

    Attributes:
        data_dir: The directory path where application data is stored.
        db_dir: The directory path where the database files are stored.
        repository_dir: The directory path where repositories are stored.
        tools_dir_path: The directory path where tools are stored.
    """

    data_dir: Path = APPLICATION_DATA_DIR
    db_dir: Path = APPLICATION_DB_DIR
    repository_dir: Path = APPLICATION_REPOSITORY_DIR
    tools_dir_path: Path = APPLICATION_TOOLS_DIR
