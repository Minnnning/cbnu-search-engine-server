from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class SocialEducationNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 6:
                continue

            raw_date = td[5].text.strip()
            formatted_date = self.parse_date(raw_date)

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[2].find_element(By.TAG_NAME, "a").text.strip(),
                "url": td[2].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

class 사회교육과:
    # 사회교육과 공지사항 설정
    url = "http://edu.chungbuk.ac.kr/soc/selectBbsNttList.do?key=297&bbsNo=40"
    site = "사회교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(4)"
