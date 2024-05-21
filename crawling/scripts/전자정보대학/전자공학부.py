# 전자공학부.py

from 전기공학부 import NoticeScraper
from selenium.webdriver.common.by import By
import time

class ElectronicEngineeringNoticeScraper(NoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for index, item in enumerate(list_items):
            if index < 4:
                continue

            row = item.find_elements(By.TAG_NAME, "td")
            if not row:
                continue

            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[2].text.strip(),
                "url": row[2].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": row[6].text.strip()
            }
            notices.append(notice)
        
        return notices

if __name__ == "__main__":
    # 전자공학부 공지사항 설정
    url = "https://elec.chungbuk.ac.kr/bbs/bbs.php?db=notice"
    site = "전자공학부"
    category = "공지사항"
    notice_list_selector = "#subContent > table:nth-child(7) > tbody > tr"
    notice_contents_selector = "#articles"  # 필요에 맞게 설정

    scraper = ElectronicEngineeringNoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        print(f"Date: {notice['date']}")
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
