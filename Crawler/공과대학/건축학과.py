# 건축학과.py
from notice_scraper import NoticeScraper
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

class 건축학과:
    url = "https://cbnuarchi.cbnu.ac.kr/bbs/board.php?bo_table=news&sca=학과소식%20및%20정보"
    site = "건축학과"
    category = "공지사항"
    notice_list_selector = "#bo_list > div > ul:nth-child(2) > li"
    notice_contents_selector = "#bo_v_con"
