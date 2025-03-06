#!/bin/bash

source backend/venv/bin/activate

nohup uvicorn backend.fast_api.main:app --host 0.0.0.0 --port 9334 > fastapi_output.log 2>&1 &

echo "백엔드 실행"