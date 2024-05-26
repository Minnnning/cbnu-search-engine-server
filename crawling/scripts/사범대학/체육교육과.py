from 교육학과 import NoticeScraper

if __name__ == "__main__":
    # 체육교육과 공지사항 설정
    url = "http://edu.chungbuk.ac.kr/physicaledu/selectBbsNttList.do?key=479&bbsNo=96"
    site = "체육교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(3) > div"

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
