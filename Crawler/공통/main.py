# main.py
import pymysql
from notice_scraper import NoticeScraper
from 국제교류본부 import 국제교류본부, InternationalExchangeCenterNoticeScraper
from linc사업단 import linc사업단
from sw중심사업단 import sw중심사업단, SWCenterNoticeScraper
from 도서관 import 도서관, LibraryNoticeScraper
from 지식재산전문인력양성센터 import 지식재산전문인력양성센터,IntellectualPropertyProfessionalTrainingCenterNoticeScraper
from 충북대학교 import 충북대학교, ChungbukUniversityNoticeScraper
from 학생생활관 import 학생생활관, DormitoryNoticeScraper
from 스포츠센터 import 스포츠센터, SportCenterNoticeScraper
from 충북대취업지원본부 import 취업지원본부, EmploymentSupportCenterNoticeScraper

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv(dotenv_path='.env')

hosturl =  os.getenv('DB_HOST')
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

def is_duplicate(title):
    """데이터베이스에 이미 존재하는 제목 인지 확인합니다."""
    sql = f"SELECT COUNT(*) FROM {table_N} WHERE title = %s"
    cursor.execute(sql, (title,))
    result = cursor.fetchone()
    return result[0] > 0

def get_scraper(department):
    if department == sw중심사업단:
        return SWCenterNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 도서관:
        return LibraryNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 지식재산전문인력양성센터:
        return IntellectualPropertyProfessionalTrainingCenterNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 국제교류본부:
        return InternationalExchangeCenterNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 충북대학교:
        return ChungbukUniversityNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 학생생활관:
        return DormitoryNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 스포츠센터:
        return SportCenterNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 취업지원본부:
        return EmploymentSupportCenterNoticeScraper(
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
    departments = [취업지원본부, 스포츠센터, 학생생활관, 충북대학교, 지식재산전문인력양성센터, 도서관, 국제교류본부, linc사업단, sw중심사업단]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
        scraper = get_scraper(department)

        # notice_list를 가져와서 출력합니다.
        notice_list = scraper.get_notice_list()

        if department.site == "도서관":
            for notice in notice_list:
                if is_duplicate(notice['title']):
                    print(f"중복된 데이터, 건너뜀: {notice['title']}")
                    continue
                
                contents_text = " " # 내용 없음
                try:
                    sql = f"INSERT INTO {table_N} (title, content ,date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                    cursor.execute(sql, values)
                    db_connection.commit()
                    print(f"Data inserted successfully: title={notice['title']}, site={notice['site']}, {notice['date']}")

                except pymysql.Error as e:
                    print(f"Error {e.args[0]}, {e.args[1]}")
                    db_connection.rollback()

        else:
            for notice in notice_list:
                if is_duplicate(notice['url']):
                    print(f"중복된 데이터, 건너뜀: {notice['url']}")
                    continue
                
                contents_text = clean_text(scraper.get_contents_text(notice['url'])) # 내용까지 스크래핑하는 코드 추가
                #print(contents_text)
                try:
                    sql = f"INSERT INTO {table_N} (title, content ,date, url, site, category) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (notice['title'], contents_text, notice['date'], notice['url'], notice['site'], department.category)
                    cursor.execute(sql, values)
                    db_connection.commit()
                    print(f"Data inserted successfully: title={notice['title']}, site={notice['site']}, {notice['date']}")

                except pymysql.Error as e:
                    print(f"Error {e.args[0]}, {e.args[1]}")
                    db_connection.rollback()

        scraper.close()
        print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")

    # WebDriver 및 DB 연결 닫기
    db_connection.close()
    print("공통 작업 완료.")




