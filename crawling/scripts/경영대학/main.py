from notice_scraper import NoticeScraper
from 경영정보학과 import 경영정보학과
from 경영학부 import 경영학부
from 국제경영학과 import 국제경영학과

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [경영정보학과, 경영학부, 국제경영학과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        # NoticeScraper 인스턴스를 생성합니다.
        scraper = NoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

        # notice_list를 가져와서 출력합니다.
        notice_list = scraper.get_notice_list()
        for notice in notice_list:
            # print(f"Title: {notice['title']}")
            # print(f"URL: {notice['url']}")
            # print(f"Date: {notice['date']}")
            # contents_text = scraper.get_contents_text(notice['url']) # 내용까지 스크래핑하는 코드 추가
            # print(f"Contents:\n{contents_text}")
            print(notice)

        scraper.close()
        print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")

    print("모든 학과 스크래핑 작업 완료.")

