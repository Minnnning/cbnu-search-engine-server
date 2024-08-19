# main.py
import pymysql, json
from notice_scraper import NoticeScraper
from 교육학과 import 교육학과
from 사회교육과 import 사회교육과, SocialEducationNoticeScraper
from 생물교육과 import 생물교육과
from 수학교육과 import 수학교육과
from 역사교육과 import 역사교육과
from 지구과학교육과 import 지구과학교육과
from 체육교육과 import 체육교육과
from 화학교육과 import 화학교육과

# DB 설정 데이터 가져오기
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    driver_path = config['driver_path']
    hosturl = config['host']
    username = config['username']
    userpassword = config['password']
    dbname = config['db']

table_N = 'notice_board'

# MariaDB 연결
db_connection = pymysql.connect(host=hosturl, user=username, password=userpassword, db=dbname, charset='utf8')
cursor = db_connection.cursor()

def clean_text(text):
    """텍스트에서 특수 문자 및 불필요한 공백을 제거합니다."""
    if text:
        return text.replace("\n", " ").replace("\r", " ").replace("'", "\\'")
    return text

def get_scraper(department):
    if department == 사회교육과 or department == 생물교육과:
        return SocialEducationNoticeScraper(
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
    departments = [교육학과, 사회교육과, 생물교육과, 수학교육과, 역사교육과, 지구과학교육과, 체육교육과, 화학교육과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
        scraper = get_scraper(department)

        # notice_list를 가져와서 출력합니다.
        notice_list = scraper.get_notice_list()
        for notice in notice_list:
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
    print("사범대학 작업 완료.")