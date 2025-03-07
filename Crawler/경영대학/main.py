import sys
import os
import pymysql
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, '경영대학'))

from notice_scraper import NoticeScraper
from 경영정보학과 import 경영정보학과
from 경영학부 import 경영학부
from 국제경영학과 import 국제경영학과

# .env 파일 로드
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

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
    """텍스트에서 특수 문자 및 불필요한 공백을 제거"""
    if text:
        return text.replace("\n", " ").replace("\r", " ").replace("'", "\\'")
    return text

def is_duplicate(url):
    """데이터베이스에 이미 존재하는 url인지 확인"""
    sql = f"SELECT COUNT(*) FROM {table_N} WHERE url = %s"
    cursor.execute(sql, (url,))
    result = cursor.fetchone()
    return result[0] > 0

if __name__ == "__main__":
    departments = [경영정보학과, 경영학부, 국제경영학과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        scraper = NoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

        notice_list = scraper.get_notice_list()
        for notice in notice_list:
            if is_duplicate(notice['url']):
                print(f"중복된 데이터, 건너뜀: {notice['url']}")
                continue

            contents_text = clean_text(scraper.get_contents_text(notice['url']))
            try:
                sql = f"INSERT INTO {table_N} (title, content ,date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                cursor.execute(sql, values)
                db_connection.commit()
                print(f"Data inserted: title={notice['title']}, site={notice['site']}")

            except pymysql.Error as e:
                print(f"Error {e.args[0]}, {e.args[1]}")
                db_connection.rollback()

        scraper.close()
        print(f"스크래핑 완료: {department.site}\n")

    db_connection.close()
    print("경영대학 작업 완료.")
