# 경영학부.py

from 경영정보학과 import NoticeScraper

if __name__ == "__main__":
    # 경영학부 공지사항 설정
    url = "https://biz.chungbuk.ac.kr/?pg_idx=7"
    site = "경영학부"
    category = "공지사항"
    notice_list_selector = ".bbs_body>#rows"
    notice_contents_selector = "#bbs_contnets > div.rd_body.row"

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
