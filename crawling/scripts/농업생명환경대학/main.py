# main.py
from notice_scraper import NoticeScraper
from 농업경제학과 import 농업경제학과
from 목재종이과학과 import 목재종이과학과
from 바이오시스템공학과 import 바이오시스템공학과
from 식물의학과 import 식물의학과, PlantMedicineNoticeScraper
from 식물자원학과 import 식물자원학과, PlantResourcesNoticeScraper
from 식품생명공학과 import 식품생명공학과, FoodLifeEngineeringNoticeScraper
from 원예학과 import 원예학과, HorticultureNoticeScraper
from 지역건설공학과 import 지역건설공학과
from 축산학과 import 축산학과
from 특용식물학과 import 특용식물학과
from 환경생명화학과 import 환경생명화학과
import time


def get_scraper(department):
    if department == 식물의학과:
        return PlantMedicineNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 식물자원학과:
        return PlantResourcesNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 식품생명공학과:
        return FoodLifeEngineeringNoticeScraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 원예학과 or department == 축산학과:
        return HorticultureNoticeScraper(
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
    departments = [농업경제학과, 목재종이과학과, 바이오시스템공학과, 식물의학과, 식물자원학과, 원예학과, 지역건설공학과, 축산학과, 특용식물학과, 환경생명화학과 ]

    for department in departments:
        if department == 원예학과 or department == 축산학과:
            print(f"스크래핑 시작: {department.site}")

            # 각 학과에 맞는 스크래퍼 인스턴스를 생성합니다.
            scraper = get_scraper(department)

            # notice_list를 가져와서 출력합니다.
            notice_list = scraper.get_notice_list()
            for notice in notice_list:
                scraper.driver.get(notice['url'])
                time.sleep(2)  # 페이지 로딩 대기
                notice['date'] = scraper.get_content_date()
                print(notice)

            scraper.close()
            print(f"스크래핑 완료 및 브라우저 종료: {department.site}\n")
        
        else:
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