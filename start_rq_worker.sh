#!/bin/bash

# Activate virtual environment
source env_lin/bin/activate

# Start Redis worker
python3 manage.py rqworker default
