from 식물자원학과 import PlantResourcesNoticeScraper
from selenium.webdriver.common.by import By
import time

class FoodLifeEngineeringNoticeScraper(PlantResourcesNoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 3:
                continue

            raw_date = td[2].text.strip()
            formatted_date = self.parse_date(raw_date)

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[1].text.strip(),
                "url": td[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices
    
class 식품생명공학과:
    # 식품생명공학과 공지사항 설정
    url = "https://food.chungbuk.ac.kr/?pg_idx=239"
    site = "식품생명공학과"
    category = "공지사항"
    notice_list_selector = "#data_list > tbody > tr"
    notice_contents_selector = "#bbs_contnets > div.rd_body.clear"
