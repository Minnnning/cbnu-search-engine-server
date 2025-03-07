import sys
import os
import pymysql
from dotenv import load_dotenv

# 현재 파일(main.py)이 위치한 디렉토리 기준으로 학과 모듈이 있는 경로를 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 전자정보대학 폴더를 모듈 검색 경로에 추가
sys.path.append(os.path.join(BASE_DIR, '전자정보대학'))

# 모듈 임포트
from notice_scraper import NoticeScraper
from 전기공학부 import 전기공학부
from 전자공학부 import 전자공학부, ElectronicEngineeringNoticeScraper
from 정보통신공학부 import 정보통신공학부, InformationAndCommunicationEngineeringNoticeScraper
from 컴퓨터공학과 import 컴퓨터공학과
from 지능로봇공학과 import 지능로봇공학과, IntelligentRoboticsNoticeScraper
from 반도체공학부 import 반도체공학부
from 소프트웨어학과 import 소프트웨어학과, SoftwareDepartmentNoticeScraper

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
    if department == 전자공학부:
        return ElectronicEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    elif department in [지능로봇공학과, 반도체공학부]:
        return IntelligentRoboticsNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    elif department == 소프트웨어학과:
        return SoftwareDepartmentNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    elif department == 정보통신공학부:
        return InformationAndCommunicationEngineeringNoticeScraper(
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
    departments = [정보통신공학부, 전자공학부, 전기공학부, 컴퓨터공학과, 지능로봇공학과, 반도체공학부, 소프트웨어학과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")
        scraper = get_scraper(department)
        notice_list = scraper.get_notice_list()
        
        for notice in notice_list:
            if is_duplicate(notice['url']):
                print(f"중복된 데이터, 건너뜀: {notice['url']}")
                continue
            
            contents_text = clean_text(scraper.get_contents_text(notice['url']))
            try:
                sql = f"INSERT INTO {table_N} (title, content, date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                cursor.execute(sql, values)
                db_connection.commit()
                print(f"Data inserted successfully: title={notice['title']}, site={notice['site']}")
            except pymysql.Error as e:
                print(f"Error {e.args[0]}, {e.args[1]}")
                db_connection.rollback()

        scraper.close()
        print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")

    db_connection.close()
    print("전정대학 작업 완료.")
