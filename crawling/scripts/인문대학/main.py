# main.py
from notice_scraper import NoticeScraper
import time
from 국어국문학과 import 국어국문학과
from 고고미술사학과 import 고고미술사학과, ArchaeologyAndArtHistoryNoticescraper
from 독일언어문화학과 import 독일언어문화학과
from 사학과 import 사학과
from 영어영문학과 import 영어영문학과
from 중어중문학과 import 중어중문학과
from 철학과 import 철학과
from 프랑스언어문화학과 import 프랑스언어문화학과
from 러시아언어문화학과 import 러시아언어문화학과, RussianLanguageAndCultureNoticeScraper

import pymysql
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='test.env')

hosturl =  os.getenv('DB_HOST')
username = os.getenv('DB_USER')
userpassword = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME1')

table_N = 'notice_board'

# MariaDB 연결
db_connection = pymysql.connect(host=hosturl, user=username, password=userpassword, db=dbname, charset='utf8')
cursor = db_connection.cursor()

def clean_text(text):
    """텍스트에서 특수 문자 및 불필요한 공백을 제거합니다."""
    if text:
        return text.replace("\n", " ").replace("\r", " ").replace("'", "\\'")
    return text

def is_duplicate(url):
    """데이터베이스에 이미 존재하는 url인지 확인합니다."""
    sql = f"SELECT COUNT(*) FROM {table_N} WHERE url = %s"
    cursor.execute(sql, (url,))
    result = cursor.fetchone()
    return result[0] > 0

def get_scraper(department):
    if department == 고고미술사학과:
        return ArchaeologyAndArtHistoryNoticescraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 러시아언어문화학과:
        return RussianLanguageAndCultureNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    else:
        return NoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [국어국문학과, 고고미술사학과, 독일언어문화학과, 사학과, 영어영문학과, 중어중문학과, 철학과, 프랑스언어문화학과, 러시아언어문화학과]

    for department in departments:
        if department == 러시아언어문화학과:
            print(f"스크래핑 시작: {department.site}")

            # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
            scraper = get_scraper(department)

            # notice_list를 가져와서 출력합니다.
            notice_list = scraper.get_notice_list()
            for notice in notice_list:
                if is_duplicate(notice['url']):
                    print(f"중복된 데이터, 건너뜀: {notice['url']}")
                    continue

                scraper.driver.get(notice['url'])
                time.sleep(2)  # 페이지 로딩 대기
                notice['date'] = scraper.get_content_date()
                contents_text = clean_text(scraper.get_contents_text(notice['url'])) # 내용까지 스크래핑하는 코드 추가
                try:
                    # 데이터베이스에 저장
                    sql = f"INSERT INTO {table_N} (title, content ,date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                    cursor.execute(sql, values)
                    db_connection.commit()
                    print(f"Data inserted successfully: title={notice['title']}, site={notice['site']}")

                except pymysql.Error as e:
                    print(f"Error {e.args[0]}, {e.args[1]}")
                    db_connection.rollback()

        else:
            print(f"스크래핑 시작: {department.site}")

            # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
            scraper = get_scraper(department)

            # notice_list를 가져와서 출력합니다.
            notice_list = scraper.get_notice_list()
            for notice in notice_list:
                if is_duplicate(notice['url']):
                    print(f"중복된 데이터, 건너뜀: {notice['url']}")
                    continue
                
                contents_text = clean_text(scraper.get_contents_text(notice['url'])) # 내용까지 스크래핑하는 코드 추가
                try:
                    # 데이터베이스에 저장
                    sql = f"INSERT INTO {table_N} (title, content ,date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                    cursor.execute(sql, values)
                    db_connection.commit()
                    print(f"Data inserted successfully: title={notice['title']}, site={notice['site']}")

                except pymysql.Error as e:
                    print(f"Error {e.args[0]}, {e.args[1]}")
                    db_connection.rollback()

        scraper.close()
        print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")

    # WebDriver 및 DB 연결 닫기
    db_connection.close()
    print("인문대학 작업 완료.")