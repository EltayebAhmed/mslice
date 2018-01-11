#!/bin/bash
#
# Basic wrapper script for running in development mode. It assumes the current
# working directory is the directory containing this script.
#
env QT_API=pyqt python setup.py
env PYTHONPATH=$(dirname $0):$PYTHONPATH /bin/bash scripts/mslice
