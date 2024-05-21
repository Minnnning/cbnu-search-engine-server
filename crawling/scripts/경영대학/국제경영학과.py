# 국제경영학과.py

from 경영정보학과 import NoticeScraper

if __name__ == "__main__":
    # 국제경영학과 공지사항 설정
    url = "https://ib.chungbuk.ac.kr/master.php?pg_idx=33"
    site = "국제경영학과"
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
