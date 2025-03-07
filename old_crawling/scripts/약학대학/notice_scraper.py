from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='crawling/test.env')

driver_path = os.getenv('DR_PATH')

class NoticeScraper:
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        self.url = url
        self.site = site
        self.category = category
        self.notice_list_selector = notice_list_selector
        self.notice_contents_selector = notice_contents_selector
        self.driver = self._init_driver()

    def _init_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        service = Service(executable_path=driver_path)  # geckodriver 경로 설정
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 4:
                continue

            title_element = td[1].find_element(By.TAG_NAME, "a")
            notice_url = 'https://pharm.chungbuk.ac.kr/app/index.html?pg_idx=21'

            raw_date = td[3].text.strip()
            # 날짜 형식 처리 (YYYY-MM-DD 형식으로 가정)
            formatted_date = raw_date.replace('.', '-')

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title_element.text.strip(),
                "url": notice_url,
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

    def close(self):
        self.driver.quit()