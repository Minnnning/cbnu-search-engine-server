#!/bin/bash

# 가상환경 활성화
source venv/bin/activate

# 스크립트 목록 정의
scripts=("scripts/경영대학/main.py"
         "scripts/공과대학/main.py"
         "scripts/농업생명환경대학/main.py"
         "scripts/사범대학/main.py"
         "scripts/사회과학대학/main.py"
         "scripts/생활과학대학/main.py"
         "scripts/수의과대학/main.py"
         "scripts/약학대학/main.py"
         "scripts/의과대학/main.py"
         "scripts/인문대학/main.py"
         "scripts/자연과학대학/main.py"
         "scripts/전자정보대학/main.py")

# 각 스크립트 실행
for script in "${scripts[@]}"
do
    python "$script"
done

#가상 환경 종료
deactivate