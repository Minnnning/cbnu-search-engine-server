from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os

SELENIUM_URL = os.getenv("SELENIUM_URL", "http://localhost:4444/wd/hub")

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

        return webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=firefox_options
        )

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            title_element = item.find_element(By.CSS_SELECTOR, "a[href*='/main/sub.html?Mode=view&boardID=']")

            if not td or not title_element:
                continue

            raw_date = td[3].text.strip()
            # 날짜 형식 처리 (YYYY-MM-DD 형식으로 가정)
            formatted_date = raw_date.replace('.', '-')

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title_element.text.strip(),
                "url": title_element.get_attribute("href").strip(),
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
