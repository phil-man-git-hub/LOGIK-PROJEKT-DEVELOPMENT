#

# -------------------------------------------------------------------------- #

# File Name:        pyside6_qt_flame_modules.py
# Version:          1.1.1
# Created:          2024-01-19
# Modified:         2025-11-15

# ========================================================================== #
# Imports - Standard Library
# ========================================================================== #

import ast
import os
import sys

# Ensure the parent directory of 'src' is in sys.path for canonical imports
current_file = os.path.abspath(__file__)
src_parent = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if src_parent not in sys.path:
    sys.path.insert(0, src_parent)

# ========================================================================== #
# Imports - Third Party
# ========================================================================== #

try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui

# ========================================================================== #
# Imports - LOGIK-PROJEKT UI Classes (Direct from widgets)
# ========================================================================== #

from src.ui.widgets.classes.pyside6_qt_button import pyside6_qt_button
from src.ui.widgets.classes.pyside6_qt_clickable_line_edit import pyside6_qt_clickable_line_edit
from src.ui.widgets.classes.pyside6_qt_label import pyside6_qt_label
from src.ui.widgets.classes.pyside6_qt_line_edit import pyside6_qt_line_edit
from src.ui.widgets.classes.pyside6_qt_list_widget import pyside6_qt_list_widget
from src.ui.widgets.classes.pyside6_qt_message_window import pyside6_qt_message_window
from src.ui.widgets.classes.pyside6_qt_password_window import pyside6_qt_password_window
from src.ui.widgets.classes.pyside6_qt_preset_window import pyside6_qt_preset_window
from src.ui.widgets.classes.pyside6_qt_progress_window import pyside6_qt_progress_window
from src.ui.widgets.classes.pyside6_qt_push_button import pyside6_qt_push_button
from src.ui.widgets.classes.pyside6_qt_push_button_menu import pyside6_qt_push_button_menu
from src.ui.widgets.classes.pyside6_qt_qdialog import pyside6_qt_qdialog
from src.ui.widgets.classes.pyside6_qt_slider import pyside6_qt_slider
from src.ui.widgets.classes.pyside6_qt_text_edit import pyside6_qt_text_edit
from src.ui.widgets.classes.pyside6_qt_token_push_button import pyside6_qt_token_push_button
from src.ui.widgets.classes.pyside6_qt_tree_widget import pyside6_qt_tree_widget
from src.ui.widgets.classes.pyside6_qt_window import pyside6_qt_window

# ========================================================================== #
# Imports - LOGIK-PROJEKT UI Functions (Direct from widgets)
# ========================================================================== #

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

# ========================================================================== #
# Imports - LOGIK-PROJEKT UI Components
# ========================================================================== #

from src.ui.methods.pyside6_qt_output_config_ui import (
    pyside6_qt_output_config_ui
)

# ========================================================================== #
# Changelist
# ========================================================================== #

# version:               1.1.1
# modified:              2025-11-15
# comments:              Fixed circular imports - import directly from widgets
# -------------------------------------------------------------------------- #
# version:               1.1.0
# modified:              2025-11-14
# comments:              Refactored imports - removed sys.path manipulation
# -------------------------------------------------------------------------- #
# version:               1.0.3
# modified:              2025-02-25 - 07:01:22
# comments:              Added legacy support for PySide2 imports
# -------------------------------------------------------------------------- #
# version:               1.0.2
# modified:              2025-01-19 - 17:47:49
# comments:              Changed import statements to fix shell errors.
# -------------------------------------------------------------------------- #
# version:               1.0.1
# modified:              2024-11-16 - 16:52:07
# comments:              Fixed circular import statements
# -------------------------------------------------------------------------- #
# version:               1.0.0
# modified:              2024-10-30 - 07:35:27
# comments:              Refactored PySide6 Output Node Config UI.
# -------------------------------------------------------------------------- #