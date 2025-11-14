#

# -------------------------------------------------------------------------- #

# File Name:        concatenate_2_files.py
# Version:          0.0.1
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section defines the import statements and directory paths.
# ========================================================================== #

ft1 = ocio.FileTransform("<Path to first CTF file>")
ft2 = ocio.FileTransform("<Path to second CTF file>")
gt = ocio.GroupTransform([ft1, ft2])
gt.write("Color Transform Format","test.ctf",config)

# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4D 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #

# Changelist:     

# -------------------------------------------------------------------------- #
# version:          0.0.1
# modified:         2024-08-31 - 16:51:09
# comments:         prep for release - code appears to be functional
# -------------------------------------------------------------------------- #
