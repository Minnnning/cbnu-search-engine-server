#!/bin/bash

source venv/bin/activate

nohup uvicorn fast_api.main:app --host 0.0.0.0 --port 9334 > fastapi_output.log 2>&1 &
