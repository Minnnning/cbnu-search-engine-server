#!/bin/bash

# 가상환경 활성화
source backend/venv/bin/activate

python backend/es/db_to_es_connector.py

deactivate