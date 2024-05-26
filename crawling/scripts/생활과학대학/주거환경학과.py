from 소비자학과 import NoticeScraper

if __name__ == "__main__":
    # 주거환경학과 공지사항 설정
    url = "https://housing.cbnu.ac.kr/main/sub.html?pageCode=27"
    site = "주거환경학과"
    category = "학과공지사항"
    notice_list_selector = ".jmboardskin1 tr:not(.jTh):not(.jTh2)"
    notice_contents_selector = "#lightgallery"

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
