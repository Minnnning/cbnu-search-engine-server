from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

class EmploymentSupportCenterNoticeScraper(NoticeScraper):

    def get_notice_list(self):
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        list_items = self.driver.find_elements(By.CSS_SELECTOR, self.notice_list_selector)
        notices = []
        
        for item in list_items:
            print(item.text)

            try:
                # 'div' 태그 찾기 시도
                row = item.find_element(By.TAG_NAME, "span")
                print(row.text)
                url = item.find_element(By.TAG_NAME, "a").get_attribute("href").strip()
                title = row.find_element(By.TAG_NAME, "span").text.strip()
                # 날짜 처리 및 공지 추가
                raw_date = row.find_element(By.TAG_NAME, "b").text.strip()  # 예시로 'span' 태그를 사용
                print(url, title,raw_date)
                notices.append({
                    "site": self.site,
                    "category": self.category,
                    "title": title,
                    "url": url,
                    "date": raw_date
                })
            
            except NoSuchElementException:
                # 요소가 없으면 무시하고 다음 항목으로 넘어감
                print("Element not found, skipping to the next item.")
                continue

        return notices

class 취업지원본부:
    # 취업지원본부 공지사항 설정
    url = "https://hrd.chungbuk.ac.kr/board_XuXE11"
    site = "취업지원본부"
    category = "공지사항"
    notice_list_selector = "li.clear"
    notice_contents_selector = "#bd_312_2935 > div.rd.clear > div.rd_body.clear > article > div"