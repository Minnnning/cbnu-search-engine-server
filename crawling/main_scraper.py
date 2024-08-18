import importlib
import pymysql
import json
from deprtments_list import departments

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


for department in departments:
    try:
        # 동적으로 학과별 모듈 가져오기
        module = importlib.import_module(department)
        
        # 스크래퍼 인스턴스 생성
        scraper = module.NoticeScraper(
            url=module.url,
            site=module.site,
            category=module.category,
            notice_list_selector=module.notice_list_selector,
            notice_contents_selector=module.notice_contents_selector
        )

        # 공지사항 리스트 가져오기
        notice_list = scraper.get_notice_list()
        
        for notice in notice_list:
            title = notice['title']
            url = notice['url']
            date = notice['date']
            contents_text = scraper.get_contents_text(url)

            try:
                # 데이터베이스에 저장
                sql = f"INSERT INTO {table_N} (title, content, date, url, department) VALUES (%s, %s, %s, %s, %s)"
                values = (title, contents_text, date, url, module.site)
                cursor.execute(sql, values)
                db_connection.commit()
                print(f"Data inserted successfully: title={title}, department={module.site}")
            except pymysql.Error as e:
                print(f"Error {e.args[0]}, {e.args[1]}")
                db_connection.rollback()
        
        # 스크래퍼 종료
        scraper.close()
    
    except ModuleNotFoundError:
        print(f"Module for {department} not found.")
    except Exception as e:
        print(f"An error occurred while processing {department}: {str(e)}")

# WebDriver 및 DB 연결 닫기
db_connection.close()

print("All departments processed successfully.")
