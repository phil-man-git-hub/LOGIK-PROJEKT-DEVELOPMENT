#!/bin/bash

# This script will sort the output of the du command in a human readable format.

# The folder to be analyzed
folder=/samsung_850_2tb_backup/backup/pman

# The du command
du -h $folder | sort -h

# The du command with the total size
du -h --max-depth=1 $folder | sort -h

# The du command with the total size and the total size of the folder
du -h --max-depth=1 $folder | sort -h | awk '{s+=$1} END
{print "Total size: " s}'

# The du command with the output sorted by name
du -h --max-depth=1 $folder | sort -h | awk '{s+=$1} END
{print "Total size: " s}' | sort -k 2

# The du command including hidden files, the output sorted by name
du -h --max-depth=1 $folder | sort -h | awk '{s+=$1} END
{print "Total size: " s}' | sort -k 2

# A bash one-liner to sort the output of the du command
du -h --max-depth=1 $folder | sort -h | awk '{s+=$1} END \
{print "Total size: " s}' | sort -k 2

du -ah --max-depth=1 | sort -k2
