from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class RussianLanguageAndCultureNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 2:
                continue
            
            title_element = row[2].find_element(By.TAG_NAME, "a")
            
            notice = {
                "site": self.site,
                "category": self.category,
                "title": title_element.text.strip(),
                "url": title_element.get_attribute("href").strip(),
                "date": None  
            }
            notices.append(notice)
        
        return notices

    def get_content_date(self):
        date_element = self.driver.find_element(By.CSS_SELECTOR, "#contents > div.bbs_info.clearfix > div.bbs_left.bbs_count > span:nth-child(1) > strong")
        raw_date = date_element.text.strip()
        formatted_date = raw_date.replace('.', '-')
        return formatted_date

class 러시아언어문화학과:
    # 러시아언어문화학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/russian/selectBbsNttList.do?bbsNo=93&key=339"
    site = "러시아언어문화학과"
    category = "공지사항" 
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(2) > td"
    