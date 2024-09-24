# menu_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import re
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='crawling/test.env')

driver_path = os.getenv('DR_PATH')

class MenuScraper:
    def __init__(self, url, tab, restaurant_id, restaurant_name):
        self.url = url
        self.tab = tab
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.driver = None

    def setup_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        service = Service(executable_path = driver_path)  # geckodriver 경로 설정
        self.driver = webdriver.Firefox(service=service, options=firefox_options)  

    def fetch_page(self):
        self.driver.get(self.url)
        time.sleep(2)  

        tabs = self.driver.find_elements(By.CSS_SELECTOR, "#restaurant-menu > div.navbar.navbar-bg.mb-3.nav.nav-pills > nav > a")
        if tabs:
            tabs[self.tab - 1].click()
            time.sleep(2)

    def get_menus(self):
        week_menus = self.driver.find_elements(By.CSS_SELECTOR, ".active table > tbody > tr")
        week_titles = self.driver.find_elements(By.CLASS_NAME, "weekday-title")
        
        result = []
        time_slot = 1

        for week_menu_index, week_menu in enumerate(week_menus):
            if re.search(r'아점|아침', week_menu.text):
                time_slot = 1
            elif re.search(r'점심|중식', week_menu.text):
                time_slot = 2
            elif re.search(r'저녁|석식', week_menu.text):
                time_slot = 3

            if week_menu_index % 2 == 1:
                days = week_menu.find_elements(By.TAG_NAME, "td")
                for index, day in enumerate(days):
                    try:
                        card_header = day.find_element(By.CLASS_NAME, "card-header")
                        if card_header:
                            MMDD = re.sub(r'\(.*요일\)', '', week_titles[index + (self.tab -1) * 5 ].text).strip().replace('.','-')
                            main_menu = card_header.text
                            sub_menus = ','.join([m.text for m in day.find_elements(By.CSS_SELECTOR, ".card-body .side")])
                            menu = f"{main_menu},{sub_menus}".replace('\\n', '').strip()

                            if menu and menu != ".":
                                result.append({
                                    "restaurantId": self.restaurant_id,
                                    "restaurant_name": self.restaurant_name,
                                    "menu": menu,
                                    "time": time_slot,
                                    "date": f"{time.strftime('%Y')}-{MMDD}"
                                })
                    except Exception as e:
                        print(e, day)
        return result

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def run(self):
        self.setup_driver()
        self.fetch_page()
        menus = self.get_menus()
        self.close_driver()
        return menus
