from notice_scraper import NoticeScraper
import time, datetime
from selenium.webdriver.common.by import By

class DormitoryNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []

        for item in list_items:
            row = item.find_elements(By.TAG_NAME, "td")
            if not row or len(row) < 4:
                continue
            # 날짜 형식을 변환
            raw_date = row[3].text.strip()
            formatted_date = raw_date.replace("/", "-")
            notice = {
                "site": self.site,
                "category": self.category,
                "title": row[1].find_element(By.TAG_NAME, "a").text.strip(),
                "url": row[1].find_element(By.TAG_NAME, "a").get_attribute("href").strip(),
                "date": formatted_date
            }
            print(notice['title'],notice['date'],notice['url'])
            notices.append(notice)
        return notices

class 학생생활관:
    # 학생생활관 공지사항 설정
    url = "https://dorm.chungbuk.ac.kr/home/sub.php?menukey=20039"
    site = "학생생활관"
    category = "공지사항"
    notice_list_selector = "tbody tr"
    notice_contents_selector = ".substance"
