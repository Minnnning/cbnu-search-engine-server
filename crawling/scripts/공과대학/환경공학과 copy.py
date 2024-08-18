# 환경공학과.py

from 건축공학과 import NoticeScraper

if __name__ == "__main__":
    # 공업화학과 공지사항 설정
    url = "https://env.cbnu.ac.kr/index.php?mid=env_sub05"
    site = "환경공학과"
    category = "공지사항"
    notice_list_selector = "div.bd_lst_wrp > table > tbody > tr"
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
