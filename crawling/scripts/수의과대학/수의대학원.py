from 수의예과 import NoticeScraper

if __name__ == "__main__":
    # 수의학과 대학원 공지사항 설정
    url = "https://vetmed.chungbuk.ac.kr/board/graduateschool-notice.do"
    site = "수의대학원"
    category = "공지사항"
    notice_list_selector = "#container > div > div.content_body > div > div.boardList > table > tbody > tr"
    notice_contents_selector = ".boardViewContent"

    scraper = NoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        print(f"Date: {notice['date']}")
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
