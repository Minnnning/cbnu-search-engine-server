# 토목공학부.py

from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time, datetime

class CivilEngineeringNoticeScraper(NoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 4:
                continue

            # 날짜 형식을 2024.4.5에서 2024-04-05로 변환
            raw_date = td[3].text.strip()
            date_obj = datetime.datetime.strptime(raw_date, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[1].text.strip(),
                "url": td[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

class 토목공학부:
    # 토목공학부 공지사항 설정
    url = "https://civil.chungbuk.ac.kr/index.php?mid=civil_sub0301"
    site = "토목공학부"
    category = "공지사항"
    notice_list_selector = "#bd_300_0 > div.bd_lst_wrp > table > tbody > tr"
    notice_contents_selector = "#content > div.bd.hover_effect > div.rd.rd_nav_style2.clear > div.rd_body.clear"