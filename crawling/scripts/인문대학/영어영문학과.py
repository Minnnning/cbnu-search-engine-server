from 국어국문학과 import KoreanLiteratureNoticeScraper

if __name__ == "__main__":
    # 영어영문학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/ecbnu/selectBbsNttList.do?bbsNo=180&key=621"
    site = "영어영문학과"
    category = "공지사항"
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(3) > td"

    scraper = KoreanLiteratureNoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
    notice_list = scraper.get_notice_list()
    for notice in notice_list:
        print(f"Title: {notice['title']}")
        print(f"URL: {notice['url']}")
        print(f"Date: {notice['date']}")
        contents_text = scraper.get_contents_text(notice['url'])
        print(f"Contents:\n{contents_text}")
    scraper.close()
    print("close")
