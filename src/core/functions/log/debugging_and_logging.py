#

# -------------------------------------------------------------------------- #

# File Name:        debugging_and_logging.py
# Version:          2.2.7
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section imports the necessary modules.
# ========================================================================== #

import os
import logging
from datetime import datetime

# ========================================================================== #
# This section enables debugging.
# ========================================================================== #

# Initiate script logging for debugging
def setup_logging(*args, **kwargs):
    script_path = os.path.abspath(__file__)
    script_name = os.path.basename(script_path)
    script_name_without_extension = os.path.splitext(script_name)[0]
    script_directory = os.path.dirname(script_path)
    log_directory = os.path.join(script_directory, 'log')

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}_{script_name}.debug.log"
    log_filepath = os.path.join(log_directory, log_filename)
    print("Log filepath:", log_filepath)  # Add this line for debugging
    
    # Configure logging
    logging.basicConfig(filename=log_filepath, level=logging.DEBUG, *args, **kwargs)
    
    # Return the configured logger instance
    return logging.getLogger()

# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4M 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #