#원예학과.py
from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class HorticultureNoticeScraper(NoticeScraper):

    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 2:
                continue

            title = td[1].find_element(By.TAG_NAME, "a").text.strip().replace("new", "")
            url = td[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip()

            notice = {
                "site": self.site,
                "category": self.category,
                "title": title,
                "url": url,
                "date": None
            }
            notices.append(notice)
        
        return notices

    def get_content_date(self):
        date_element = self.driver.find_element(By.CSS_SELECTOR, 
            "#contentsArea > div > div.tableWrap > table > tbody > tr:nth-child(1) > td:nth-child(4)")
        date_text = date_element.text.strip()
        # 시간 부분 제거 (YYYY-MM-DD 형식으로 가정)
        return date_text.split()[0]

    def get_contents_html(self, url):
        self.driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기
        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')

class 원예학과:
    # 원예학과 공지사항 설정
    url = "https://hortisci.chungbuk.ac.kr/html/board/board.php?id=hor_news"
    site = "원예학과"
    category = "공지사항"
    notice_list_selector = "#contentsArea > div > table.basicList > tbody > tr"
    notice_contents_selector = "#contentsArea > div > div.tableWrap > table > tbody > tr:nth-child(3)"
