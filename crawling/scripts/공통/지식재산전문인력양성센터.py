from notice_scraper import NoticeScraper
import time, datetime
from selenium.webdriver.common.by import By

class IntellectualPropertyProfessionalTrainingCenterNoticeScraper(NoticeScraper):
    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 4:
                continue
            raw_date = row[3].text.strip()
            items = row[1].find_elements(By.TAG_NAME, "a")
            for item in items:
                if len(item.text) > 4 :
                    title = item.text
                    url = item.get_attribute("href").strip()
                    break

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title,
                "url": url,
                "date": raw_date
            }

            notices.append(notice)
        return notices

class 지식재산전문인력양성센터:
    # 지식재산전문인력양성센터 공지사항 설정
    url = "https://cip.chungbuk.ac.kr/board/notice"
    site = "지식재산전문인력양성센터"
    category = "공지사항"
    notice_list_selector = "tr"
    notice_contents_selector = "#post-content"

