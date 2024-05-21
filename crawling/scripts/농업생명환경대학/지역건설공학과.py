from 농업경제학과 import NoticeScraper

if __name__ == "__main__":
    # 지역건설공학과 공지사항 설정
    url = "https://jigong.chungbuk.ac.kr/index.html?pg_idx=23"
    site = "지역건설공학과"
    category = "공지사항"
    notice_list_selector = "#bbs_contnets tbody > tr"  
    notice_contents_selector = ".rd_body"

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
