# 소프트웨어학과.py

from 전기공학부 import NoticeScraper
from selenium.webdriver.common.by import By
import time
import datetime

class SoftwareDepartmentNoticeScraper(NoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 5:  # 데이터의 길이 확인
                continue

            # 날짜 형식을 2024.4.5에서 2024-4-5로 변환
            raw_date = row[4].text.strip()
            date_obj = datetime.datetime.strptime(raw_date, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[2].text.strip(),
                "url": row[2].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

if __name__ == "__main__":
    # 소프트웨어학과 공지사항 설정
    url = "https://software.cbnu.ac.kr/sub0401"
    site = "소프트웨어학과"
    category = "공지사항"
    notice_list_selector = "tbody tr"
    notice_contents_selector = ".rd_body"

    scraper = SoftwareDepartmentNoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        print(f"Date: {notice['date']}")
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
