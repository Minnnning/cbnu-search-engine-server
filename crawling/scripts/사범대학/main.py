# main.py
from notice_scraper import NoticeScraper
from 교육학과 import 교육학과
from 사회교육과 import 사회교육과, SocialEducationNoticeScraper
from 생물교육과 import 생물교육과
from 수학교육과 import 수학교육과
from 역사교육과 import 역사교육과
from 지구과학교육과 import 지구과학교육과
from 체육교육과 import 체육교육과
from 화학교육과 import 화학교육과

def get_scraper(department):
    if department == 사회교육과 or department == 생물교육과:
        return SocialEducationNoticeScraper(
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
    departments = [교육학과, 사회교육과, 생물교육과, 수학교육과, 역사교육과, 지구과학교육과, 체육교육과, 화학교육과]

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