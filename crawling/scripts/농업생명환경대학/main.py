# main.py
import pymysql
from notice_scraper import NoticeScraper
from 농업경제학과 import 농업경제학과
from 목재종이과학과 import 목재종이과학과
from 바이오시스템공학과 import 바이오시스템공학과
from 식물의학과 import 식물의학과, PlantMedicineNoticeScraper
from 식물자원학과 import 식물자원학과, PlantResourcesNoticeScraper
from 식품생명공학과 import 식품생명공학과, FoodLifeEngineeringNoticeScraper
from 원예학과 import 원예학과, HorticultureNoticeScraper
from 지역건설공학과 import 지역건설공학과
from 축산학과 import 축산학과
from 특용식물학과 import 특용식물학과
from 환경생명화학과 import 환경생명화학과
import time

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
    if department == 식물의학과:
        return PlantMedicineNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 식물자원학과:
        return PlantResourcesNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 식품생명공학과:
        return FoodLifeEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 원예학과 or department == 축산학과:
        return HorticultureNoticeScraper(
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
    departments = [농업경제학과, 목재종이과학과, 바이오시스템공학과, 식물의학과, 식물자원학과, 원예학과, 지역건설공학과, 축산학과, 특용식물학과, 환경생명화학과 ]

    for department in departments:
        if department == 원예학과 or department == 축산학과:
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

            scraper.close()
            print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")
        
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
    print("농대 작업 완료.")