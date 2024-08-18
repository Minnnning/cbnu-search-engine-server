from 원예학과 import NoticeScraper
import time

if __name__ == "__main__":
    # 축산학과 공지사항 설정
    url = "https://animalscience.chungbuk.ac.kr/board/board.php?id=as_news"
    site = "축산학과"
    category = "공지사항"
    notice_list_selector = "#contentsArea > div > table.basicList > tbody > tr"
    notice_contents_selector = "#contentsArea > div > div.tableWrap > table > tbody > tr:nth-child(3)"

    scraper = NoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        
        # Fetching the date from the content page
        scraper.driver.get(notice['url'])
        time.sleep(2)  # 페이지 로딩 대기
        date = scraper.get_content_date()
        print(f"Date: {date}")
        
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
