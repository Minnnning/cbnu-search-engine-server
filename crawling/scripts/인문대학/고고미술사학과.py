from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class ArchaeologyAndArtHistoryNoticescraper(NoticeScraper):
    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 6:
                continue

            title_element = row[2].find_element(By.TAG_NAME, "a")
            raw_date = row[5].text.strip()
            formatted_date = raw_date.replace('.', '-')

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title_element.text.strip(),
                "url": title_element.get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

class 고고미술사학과:
    # 고고미술사학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/gomisa/selectBbsNttList.do?bbsNo=218&key=683"
    site = "고고미술사학과"
    category = "공지사항"
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(3) > td"

