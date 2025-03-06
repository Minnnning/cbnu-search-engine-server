#!/bin/bash

# 가상환경 활성화
source crawling/venv/bin/activate

# 스크립트 목록 정의
scripts=("crawling/scripts/경영대학/main.py"
         "crawling/scripts/공과대학/main.py"
         "crawling/scripts/농업생명환경대학/main.py"
         "crawling/scripts/사범대학/main.py"
         "crawling/scripts/사회과학대학/main.py"
         "crawling/scripts/생활과학대학/main.py"
         "crawling/scripts/수의과대학/main.py"
         "crawling/scripts/약학대학/main.py"
         "crawling/scripts/의과대학/main.py"
         "crawling/scripts/인문대학/main.py"
         "crawling/scripts/자연과학대학/main.py"
         "crawling/scripts/전자정보대학/main.py"
         "crawling/scripts/공통/main.py")

# 각 스크립트 실행
for script in "${scripts[@]}"
do
    python "$script"
done

echo "공지사항 크롤링"

#가상 환경 종료
deactivate