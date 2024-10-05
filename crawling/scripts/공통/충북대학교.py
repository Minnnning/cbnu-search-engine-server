# 충북대학교.py
from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time
import datetime

class ChungbukUniversityNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []

        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 6:
                continue
            print(row[2].text)
            # 날짜 형식을 2024.4.5에서 2024-04-05로 변환
            raw_date = row[5].text.strip()

            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[2].find_element(By.TAG_NAME, "a").text.strip(),
                "url": row[2].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": raw_date
            }
            notices.append(notice)
        
        return notices

class 충북대학교:
    # 충북대학교 공지사항 설정
    url = "https://www.chungbuk.ac.kr/www/selectBbsNttList.do?bbsNo=8&key=813"
    site = "충북대학교"
    category = "공지사항"
    notice_list_selector = "div.table-responsive > table > tbody > tr:nth-child(1)"
    notice_contents_selector = "#contents > div > div > div:nth-child(3) > div"
