from notice_scraper import NoticeScraper
import time, datetime
from selenium.webdriver.common.by import By

class InternationalExchangeCenterNoticeScraper(NoticeScraper):
    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 4:
                continue
            # 날짜 형식을 변환
            raw_date = row[2].text.strip()
            formatted_date = raw_date.replace(".", "-")
            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[1].find_element(By.TAG_NAME, "a").text.strip(),
                "url": row[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        return notices


class 국제교류본부:
    # 국제교류본부 공지사항 설정
    url = "https://cia.chungbuk.ac.kr/board/notice/lists/key/180"
    site = "국제교류본부"
    category = "공지사항"
    notice_list_selector = ".adm_table tr"
    notice_contents_selector = ".board_content"
