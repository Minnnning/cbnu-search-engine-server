# 컴퓨터공학과.py

from 전기공학부 import NoticeScraper

if __name__ == "__main__":
    # 컴퓨터공학과 공지사항 설정
    url = "https://computer.chungbuk.ac.kr/bbs/bbs.php?db=notice"
    site = "컴퓨터공학과"
    category = "공지사항"
    notice_list_selector = "#content > table:nth-child(9) > tbody > tr"
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
