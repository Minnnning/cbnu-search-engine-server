# 건축학과.py

from 건축공학과 import NoticeScraper
from selenium.webdriver.common.by import By
import time, datetime

class ArchitectureDepartmentNoticeScraper(NoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.CSS_SELECTOR, "a > span")
            if not row or len(row) < 4:
                continue

            # 날짜 형식을 2024.4.5에서 2024-04-05로 변환
            raw_date = row[3].text.strip()
            date_obj = datetime.datetime.strptime(raw_date, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[1].text.strip(),
                "url": item.find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

if __name__ == "__main__":
    # 건축학과 공지사항 설정
    url = "https://cbnuarchi.cbnu.ac.kr/bbs/board.php?bo_table=news&sca=%EB%89%B4%EC%8A%A4"
    site = "건축학과"
    category = "공지사항"
    notice_list_selector = "#bo_list > div > ul:nth-child(2) > li"
    notice_contents_selector = "#bo_v_con"

    scraper = ArchitectureDepartmentNoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        print(f"Date: {notice['date']}")
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
