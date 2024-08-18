# main.py
from notice_scraper import NoticeScraper
from 전기공학부 import 전기공학부
from 전자공학부 import 전자공학부, ElectronicEngineeringNoticeScraper
from 정보통신공학부 import 정보통신공학부
from 컴퓨터공학과 import 컴퓨터공학과
from 지능로봇공학과 import 지능로봇공학과, IntelligentRoboticsNoticeScraper
from 반도체공학부 import 반도체공학부
from 소프트웨어학과 import 소프트웨어학과, SoftwareDepartmentNoticeScraper

def get_scraper(department):
    if department == 전자공학부:
        return ElectronicEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 지능로봇공학과 or department == 반도체공학부:
        return IntelligentRoboticsNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 소프트웨어학과:
        return SoftwareDepartmentNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

    else:
        return NoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )

if __name__ == "__main__":
    # 각 학과 설정들을 리스트에 담습니다.
    departments = [전기공학부, 전자공학부, 정보통신공학부, 컴퓨터공학과, 지능로봇공학과, 반도체공학부, 소프트웨어학과]

    for department in departments:
        print(f"스크래핑 시작: {department.site}")

        # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
        scraper = get_scraper(department)

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