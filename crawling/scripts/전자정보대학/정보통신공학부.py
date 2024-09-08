from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time, datetime

class InformationAndCommunicationEngineeringNoticeScraper(NoticeScraper):

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
            raw_date = td[4].text.strip()
            date_obj = datetime.datetime.strptime(raw_date, "%Y.%m.%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[2].text.strip(),
                "url": td[2].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

class 정보통신공학부:
    # 정보통신공학부 공지사항 설정
    url = "https://inform.chungbuk.ac.kr/cisub5_2"
    site = "정보통신공학부"
    category = "공지사항"
    notice_list_selector = "#bd_378_0 > div.bd_lst_wrp > table > tbody > tr"
    notice_contents_selector = "div.rd_body.clear > article"
