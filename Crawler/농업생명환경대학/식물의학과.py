# 식물의학과.py
from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import datetime, time, re


class PlantMedicineNoticeScraper(NoticeScraper):
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        super().__init__(url, site, category, notice_list_selector, notice_contents_selector)

    def parse_date(self, raw_date):
        # 연도와 함께 주어진 날짜
        match_with_year = re.search(r'(\d{4})년 (\d{1,2})월 (\d{1,2})일', raw_date)
        if match_with_year:
            year = match_with_year.group(1)
            month = match_with_year.group(2).zfill(2)
            day = match_with_year.group(3).zfill(2)
            return f"{year}-{month}-{day}"

        # 연도가 없는 날짜
        match_without_year = re.search(r'(\d{1,2})월 (\d{1,2})일', raw_date)
        if match_without_year:
            year = datetime.datetime.now().year
            month = match_without_year.group(1).zfill(2)
            day = match_without_year.group(2).zfill(2)
            return f"{year}-{month}-{day}"

        # 변환 실패 시 원본 반환
        return raw_date

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기

        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        for item in list_items:
            td = item.find_elements(By.TAG_NAME, "td")
            if not td or len(td) < 5:
                continue

            raw_date = td[4].find_element(By.CSS_SELECTOR, 'span[data-hook="time-ago"]').text.strip()
            formatted_date = self.parse_date(raw_date)

            notice = {
                "site": self.site,
                "category": self.category,
                "title": td[0].find_element(By.TAG_NAME, "a").text.strip(),
                "url": td[0].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            notices.append(notice)
        
        return notices

    def get_contents_html(self, url):
        self.driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기
        contents_element = self.driver.find_element(By.CSS_SELECTOR, self.notice_contents_selector)
        return contents_element.get_attribute('outerHTML')


class 식물의학과:
    # 식물의학과 공지사항 설정
    url = "https://www.plantmed.chungbuk.ac.kr/forum/gongjisahang"
    site = "식물의학과"
    category = "공지사항"
    notice_list_selector = 'tr[data-hook="post-list-item"]'
    notice_contents_selector = ".post-content__body"
