#!/bin/bash

# Set environment variables
export PROJECT_ROOT=$(pwd)
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH

# Install dependencies
pip install -r requirements.txt

# Any other setup commands...
