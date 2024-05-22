from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json

# Config 파일에서 드라이버 경로 읽기
with open('../../config.json', 'r') as config_file:
    config = json.load(config_file)
    driver_path = config['driver_path']

class NoticeScraper:
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector, date_selector):
        self.url = url
        self.site = site
        self.category = category
        self.notice_list_selector = notice_list_selector
        self.notice_contents_selector = notice_contents_selector
        self.date_selector = date_selector
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
        print(list_items)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 2:
                continue

            title_element = row[1].find_element(By.TAG_NAME, "a")

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title_element.text.strip(),
                "url": title_element.get_attribute("href").strip(),
                "date": ""  # Date is in the detail page
            }
            notices.append(notice)
        
        return notices

    def get_content_date(self):
        date_element = self.driver.find_element(By.CSS_SELECTOR, self.date_selector)
        raw_date = date_element.text.strip()
        formatted_date = raw_date.replace('.', '-')
        return formatted_date

    def get_contents_html(self, url):
        self.driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기
        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')

    def get_contents_text(self, url):
        self.driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기
        date = self.get_content_date()
        html_content = self.get_contents_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return date, soup.get_text(separator="\n").strip()

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    # 러시아언어문화학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/russian/selectBbsNttList.do?bbsNo=93&key=339"
    site = "러시아언어문화학과"
    category = "공지사항"
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(2) > td"
    date_selector = "#contents > div.bbs_info.clearfix > div.bbs_left.bbs_count > span:nth-child(1) > strong"

    scraper = NoticeScraper(url, site, category, notice_list_selector, notice_contents_selector, date_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        date, contents_text = scraper.get_contents_text(notice['url'])
        print(f"Date: {date}")
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
