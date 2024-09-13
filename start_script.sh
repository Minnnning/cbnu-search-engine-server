#!/bin/bash

# 실행할 특정 시간 (24시간 형식으로 입력)
target_hour1="21"
target_minute1="00"  

target_hour2="23"
target_minute2="00"

target_hour3="23"
target_minute3="30"

/backend/backend_run.sh

while true
do
    # 현재 시간 가져오기
    current_hour=$(date +"%H")
    current_minute=$(date +"%M")

    # 현재 시간이 목표 시간과 같으면 실행
    if [[ "$current_hour" == "$target_hour1" && "$current_minute" == "$target_minute1" ]]; then
        echo "공지사항 스크립트를 실행합니다."
        
        # 실행할 스크립트
        /crawling/notice_script_run.sh
        
        # 실행 후 1분 대기 (같은 스크립트가 반복 실행되지 않도록)
        sleep 60
    fi

    # 1분 대기 후 다시 확인
    sleep 1

    if [[ "$current_hour" == "$target_hour2" && "$current_minute" == "$target_minute2" ]]; then
        echo "메뉴 스크립트를 실행합니다."
        
        # 실행할 스크립트
        /crawling/menu_script_run.sh
        
        # 실행 후 1분 대기 (같은 스크립트가 반복 실행되지 않도록)
        sleep 60
    fi

    if [[ "$current_hour" == "$target_hour3" && "$current_minute" == "$target_minute3" ]]; then
        echo "es db 스크립트를 실행합니다."
        
        # 실행할 스크립트
        /backend/es_connect_run.sh
        
        # 실행 후 1분 대기 (같은 스크립트가 반복 실행되지 않도록)
        sleep 60
    fi
done
