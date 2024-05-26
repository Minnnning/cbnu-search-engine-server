from 경제학과 import NoticeScraper

if __name__ == "__main__":
    # 행정학과 공지사항 설정
    url = "https://public.chungbuk.ac.kr/board/department_notice"
    site = "행정학과"
    category = "학부/융합전공공지"
    notice_list_selector = "#fboardlist > table > tbody > tr"
    notice_contents_selector = "#post-content"

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
