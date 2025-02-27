import pymysql
from notice_scraper import NoticeScraper
from 경제학과 import 경제학과
from 사회학과 import 사회학과
from 심리학과 import 심리학과
from 정치외교학과 import 정치외교학과
from 행정학과 import 행정학과

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv(dotenv_path='.env')

# 환경 변수 설정
hosturl = os.getenv('DB_HOST')
username = os.getenv('DB_USER')
userpassword = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME')

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

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [경제학과, 사회학과, 심리학과, 정치외교학과, 행정학과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        # NoticeScraper 인스턴스를 생성합니다.
        scraper = NoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

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
    print("사과대학 작업 완료.")

