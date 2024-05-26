from 물리학과 import NoticeScraper

if __name__ == "__main__":
    # 정보통계학과 공지사항 설정
    url = "https://stat.chungbuk.ac.kr/?pg_idx=145"
    site = "정보통계학과"
    category = "공지사항"
    notice_list_selector = ".dambbs_notice_list > table > tbody > tr"
    notice_contents_selector = ".dambbs_body"

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
