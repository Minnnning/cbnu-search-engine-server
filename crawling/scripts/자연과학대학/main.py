from notice_scraper import NoticeScraper
from 물리학과 import 물리학과
from 미생물학과 import 미생물학과
from 생물학과 import 생물학과
from 생화학과 import 생화학과
from 수학과 import 수학과
from 정보통계학과 import 정보통계학과
from 지구환경과학과 import 지구환경과학과
from 천문우주학과 import 천문우주학과
from 화학과 import 화학과

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [물리학과, 미생물학과, 생물학과, 생화학과, 수학과, 정보통계학과, 지구환경과학과, 천문우주학과, 화학과]

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

