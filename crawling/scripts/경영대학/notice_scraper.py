from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time, json

with open('../../config.json', 'r') as config_file:
    config = json.load(config_file)
    driver_path = config['driver_path']

class NoticeScraper:
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        self.url = url
        self.site = site
        self.category = self.category = category
        self.notice_list_selector = notice_list_selector
        self.notice_contents_selector = notice_contents_selector
        self.driver = self._init_driver()

    def _init_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        service = Service(executable_path=driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "div")
            if not td or len(td) < 4:
                continue

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[1].text.strip(),
                "url": td[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": td[3].text.strip()
            }
            notices.append(notice)
        
        return notices

    def get_contents_html(self, url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.notice_contents_selector))
            )
        except TimeoutException:
            print(f"Timeout while waiting for element: {self.notice_contents_selector}")
            return ""

        try:
            attached_list = self.driver.find_element(By.CSS_SELECTOR, "#attachedList")
            self.driver.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
            """, attached_list)
        except:
            pass

        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')

    def get_contents_text(self, url):
        html_content = self.get_contents_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator="\n").strip()

    def close(self):
        self.driver.quit()

# NoticeScraper는 이제 다른 파이썬 파일에서 import하여 사용됩니다.
