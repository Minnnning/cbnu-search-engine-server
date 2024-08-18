from notice_scraper import NoticeScraper
from 수의예과 import 수의예과
from 수의학과 import 수의학과
from 연구실험실 import 수의학과연구실험실
from 수의대학원 import 수의대학원

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [수의예과, 수의학과, 수의학과연구실험실, 수의대학원]

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

