#noticescraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time, re
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='test.env')

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
            if not td or len(td) < 3:
                continue

            url_tag = td[1].find_element(By.TAG_NAME, "a")
            url = url_tag.get_attribute("href").strip()

            if url_tag.get_attribute("onclick"):
                onclick_content = url_tag.get_attribute("onclick")
                id_match = re.search(r'(\d+)', onclick_content)
                if id_match:
                    id_value = id_match.group(1)
                    url = f"{self.url}&mod=view&pidx={id_value}&page=1"
            
            if self.site == "농업경제학과":
                raw_date = td[2].text.strip()
                # 날짜 형식을 2024.2.1에서 2024-2-1로 변환
                date_parts = raw_date.split('.')
                formatted_date = f"{date_parts[0]}-{date_parts[1]}-{date_parts[2]}"
            else:
                formatted_date = td[3].text.strip()

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[1].find_element(By.TAG_NAME, "a").text.strip(),
                "url": url,
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

    def get_contents_html(self, url):
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        # link_sns 클래스를 가진 요소의 부모 요소 제거
        self.driver.execute_script("""
            var elements = document.getElementsByClassName('link_sns');
            while(elements.length > 0){
                var parentElement = elements[0].parentNode;
                parentElement.parentNode.removeChild(parentElement);
            }
        """)

        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')

    def get_contents_text(self, url):
        html_content = self.get_contents_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator="\n").strip()

    def close(self):
        self.driver.quit()
