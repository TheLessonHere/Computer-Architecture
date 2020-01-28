#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# Get the file name out of the cmd line request
file_to_run = sys.argv[1]
cpu = CPU()
# Load it with our emulator
cpu.load(file_to_run)
cpu.run()