#

# -------------------------------------------------------------------------- #

# File Name:        concatenate_3_files.py
# Version:          0.0.1
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section defines the import statements and directory paths.
# ========================================================================== #
import PyOpenColorIO as ocio

# Create FileTransform objects for each CTF file
ft1 = ocio.FileTransform("<Path to first CTF file>")
ft2 = ocio.FileTransform("<Path to second CTF file>")
ft3 = ocio.FileTransform("<Path to third CTF file>")

# Create a GroupTransform object with all three FileTransforms
gt = ocio.GroupTransform([ft1, ft2, ft3])

# Write the GroupTransform to a new CTF file
gt.write("Color Transform Format", "test.ctf", config)

# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4D 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #

# Changelist:     

# -------------------------------------------------------------------------- #
# version:          0.0.1
# modified:         2024-08-31 - 16:51:09
# comments:         prep for release - code appears to be functional
# -------------------------------------------------------------------------- #
