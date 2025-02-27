from notice_scraper import NoticeScraper
import time
from datetime import datetime
from selenium.webdriver.common.by import By

class LibraryNoticeScraper(NoticeScraper):
    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 2:
                continue
            # 날짜 형식을 변환
            raw_date = row[2].find_element(By.TAG_NAME, "li").text[-7:]
            month, day = raw_date.replace("월", "").replace("일", "").split()
            formatted_date = f"{datetime.now().year}-{month.zfill(2)}-{day.zfill(2)}"
            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[2].find_element(By.TAG_NAME, "span").text.strip(),
                "url": "https://cbnul.chungbuk.ac.kr/library-guide/community/notice",
                "date": formatted_date
            }
            print(notice["title"],notice["url"])
            notices.append(notice)
        return notices

class 도서관:
    # 도서관 공지사항 설정
    url = "https://cbnul.chungbuk.ac.kr/library-guide/community/notice"
    site = "도서관"
    category = "공지사항"
    notice_list_selector = ".ikc-bulletins tr"
    notice_contents_selector = ".board_content"
