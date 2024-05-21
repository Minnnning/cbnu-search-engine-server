from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import pymysql, time, json

# 학과별 크롤링 데이터를 가져와 실질적 크롤링을 실행하는 파일
# db설정 데이터 가져오기
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    driver_path = config['driver_path']
    hosturl = config['host'], 
    username = config['user'],
    userpassword = config['password'],
    dbname = config['db']


table_N = 'notice_board'

# MariaDB 연결
db_connection = pymysql.connect(host=hosturl, user=username, password=userpassword, db=dbname, charset='utf8')
cursor = db_connection.cursor()

# Firefox 옵션 설정 (예: headless 모드)
options = FirefoxOptions()
options.add_argument("--headless")  # GUI 없이 실행

# Geckodriver 서비스 설정
service = Service(executable_path = driver_path)

# Firefox 웹 드라이버 인스턴스 생성
driver = webdriver.Firefox(service=service, options=options)

url = 'https://inform.chungbuk.ac.kr/bbs/bbs.php?db=notice&search=&searchKey=&category=&pgID=ID12415888101&page=1'
driver.get(url)

# 정보를 저장할 리스트 초기화
notices = []

# <tr onmouseover> 태그를 모두 찾습니다.
rows = driver.find_elements(By.CSS_SELECTOR, 'tr[onmouseover]')

# 각 행에서 href, <b> 태그의 텍스트, 그리고 날짜를 추출하여 리스트에 저장합니다.
for row in rows:
    link = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    title = row.find_element(By.CSS_SELECTOR, 'b').text
    date = row.find_elements(By.CSS_SELECTOR, 'td')[-3].text
    notices.append((title, date, link))

# 각 링크에 대해 새로운 페이지로 이동하여 내용을 추출
for title, date, link in notices:
    driver.get(link)
    time.sleep(2)  # 페이지가 완전히 로드될 때까지 기다립니다.
    article_content = driver.find_element(By.ID, 'articles').text

    try:
        sql = f"INSERT INTO {table_N} (title, content, date, url, department) VALUES (%s, %s, %s, %s, %s)"
        values = (title, article_content, date, link, '정보통신공학부')
        cursor.execute(sql, values)
        db_connection.commit()
        print(f"Data inserted successfully: title={title}")
    except pymysql.Error as e:
        print(f"Error {e.args[0]}, {e.args[1]}")
        db_connection.rollback()

# WebDriver를 닫습니다.
driver.quit()

# 데이터베이스 연결을 닫습니다.
db_connection.close()
