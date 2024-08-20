# notice_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import datetime, time, json

class NoticeScraper:
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        self.url = url
        self.site = site
        self.category = category
        self.notice_list_selector = notice_list_selector
        self.notice_contents_selector = notice_contents_selector
        self.driver = self._init_driver()

    def _init_driver(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            driver_path = config['driver_path']
        
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

            # 날짜 형식을 2024.4.5에서 2024-04-05로 변환
            raw_date = td[3].text.strip()
            date_obj = datetime.datetime.strptime(raw_date, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[1].text.strip(),
                "url": td[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

    def get_contents_html(self, url):
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기
        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')

    def get_contents_text(self, url):
        html_content = self.get_contents_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator="\n").strip()

    def close(self):
        self.driver.quit()
