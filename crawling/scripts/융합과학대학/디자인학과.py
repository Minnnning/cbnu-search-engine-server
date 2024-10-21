from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class 디자인학과:
    # 디자인학과 공지사항 설정
    url = "https://www.design.chungbuk.ac.kr/blog"
    site = "디자인학과"
    category = "공지사항"
    notice_list_selector = "div.item-link-wrapper"
    notice_contents_selector = "#articles"

class DepartmentofDesignNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []

        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "div")
            print(row[0].text)
            print(row[1].text)
            # 날짜 형식을 변환
            notice = {
                "site": self.site,
                "category": self.category,
                "title": "ddd",
                "url": "adsfa"
                
            }
            
            notices.append(notice)
        return notices