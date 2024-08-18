# main.py
from notice_scraper import NoticeScraper
from 건축공학과 import 건축공학과
from 건축학과 import 건축학과, ArchitectureDepartmentNoticeScraper
from 공업화학과 import 공업화학과
from 기계공학부 import 기계공학부, MechanicalEngineeringNoticeScraper
from 도시공학과 import 도시공학과
from 신소재공학과 import 신소재공학과
from 안전공학과 import 안전공학과
from 토목공학부 import 토목공학부, CivilEngineeringNoticeScraper
from 화학공학과 import 화학공학과, ChemicalEngineeringNoticeScraper
from 환경공학과 import 환경공학과

def get_scraper(department):
    if department == 건축학과:
        return ArchitectureDepartmentNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 기계공학부:
        return MechanicalEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 토목공학부:
        return CivilEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 화학공학과:
        return ChemicalEngineeringNoticeScraper(
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
    departments = [건축공학과, 건축학과, 공업화학과, 기계공학부, 도시공학과, 신소재공학과, 안전공학과, 토목공학부, 화학공학과, 환경공학과]

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