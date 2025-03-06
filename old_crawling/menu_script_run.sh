#!/bin/bash

# 가상환경 활성화
source crawling/venv/bin/activate

python crawling/scripts/학식/main.py

echo "학식 크롤링"

deactivate