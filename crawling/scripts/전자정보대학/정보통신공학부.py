# 정보통신공학부.py

from 전기공학부 import NoticeScraper

if __name__ == "__main__":
    # 정보통신공학부 공지사항 설정
    url = "https://inform.chungbuk.ac.kr/bbs/bbs.php?db=notice"
    site = "정보통신공학부"
    category = "공지사항"
    notice_list_selector = "#content1 > div.section.clear > table:nth-child(6) > tbody > tr"
    notice_contents_selector = "#articles"

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
