#

# -------------------------------------------------------------------------- #

# File Name:        pyside6_qt_flame_functions.py
# Version:          1.1.0
# Created:          2024-01-19
# Modified:         2025-11-15

# -------------------------------------------------------------------------- #
# Setup sys.path
# -------------------------------------------------------------------------- #

import os
import sys

# Ensure the parent directory of 'src' is in sys.path for canonical imports
current_file = os.path.abspath(__file__)
src_parent = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if src_parent not in sys.path:
    sys.path.insert(0, src_parent)

# -------------------------------------------------------------------------- #
# Imports - Widget Functions
# -------------------------------------------------------------------------- #

from src.ui.widgets.functions.pyside6_qt_file_browser import pyside6_qt_file_browser
from src.ui.widgets.functions.pyside6_qt_get_flame_version import pyside6_qt_get_flame_version
from src.ui.widgets.functions.pyside6_qt_get_shot_name import pyside6_qt_get_shot_name
from src.ui.widgets.functions.pyside6_qt_load_config import pyside6_qt_load_config
from src.ui.widgets.functions.pyside6_qt_open_in_finder import pyside6_qt_open_in_finder
from src.ui.widgets.functions.pyside6_qt_print import pyside6_qt_print
from src.ui.widgets.functions.pyside6_qt_refresh_hooks import pyside6_qt_refresh_hooks
from src.ui.widgets.functions.pyside6_qt_resolve_path_tokens import pyside6_qt_resolve_path_tokens
from src.ui.widgets.functions.pyside6_qt_resolve_shot_name import pyside6_qt_resolve_shot_name
from src.ui.widgets.functions.pyside6_qt_save_config import pyside6_qt_save_config

# -------------------------------------------------------------------------- #
# Changelist
# -------------------------------------------------------------------------- #

# version:               1.1.0
# modified:              2025-11-15
# comments:              Verified imports use full package paths
# -------------------------------------------------------------------------- #