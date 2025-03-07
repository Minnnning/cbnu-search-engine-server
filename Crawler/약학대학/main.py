import sys
import os
import pymysql
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, '약학대학'))

from notice_scraper import NoticeScraper
from 약학과 import 약학과

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

def is_duplicate(title):
    """데이터베이스에 이미 존재하는 제목 인지 확인합니다."""
    sql = f"SELECT COUNT(*) FROM {table_N} WHERE title = %s"
    cursor.execute(sql, (title,))
    result = cursor.fetchone()
    return result[0] > 0

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [약학과]

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
            if is_duplicate(notice['title']):
                print(f"중복된 데이터, 건너뜀: {notice['title']}")
                continue
            
            try:
                # 데이터베이스에 저장
                sql = f"INSERT INTO {table_N} (title, date, url, site, category) VALUES (%s, %s, %s, %s, %s)"
                values = (notice['title'], notice['date'], notice['url'], notice['site'], department.category)
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
    print("약학대학 작업 완료.")

