#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
from dataclasses import dataclass
from typing import Literal

TOOL_NAME = Literal["google-search"]


@dataclass
class ToolSettings:
    name: TOOL_NAME
