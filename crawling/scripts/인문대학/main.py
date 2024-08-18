# main.py
from notice_scraper import NoticeScraper
import time
from 국어국문학과 import 국어국문학과
from 고고미술사학과 import 고고미술사학과, ArchaeologyAndArtHistoryNoticescraper
from 독일언어문화학과 import 독일언어문화학과
from 사학과 import 사학과
from 영어영문학과 import 영어영문학과
from 중어중문학과 import 중어중문학과
from 철학과 import 철학과
from 프랑스언어문화학과 import 프랑스언어문화학과
from 러시아언어문화학과 import 러시아언어문화학과, RussianLanguageAndCultureNoticeScraper

def get_scraper(department):
    if department == 고고미술사학과:
        return ArchaeologyAndArtHistoryNoticescraper(
            department.url,
            department.site,
            department.category,
            department.notice_list_selector,
            department.notice_contents_selector
        )
    
    elif department == 러시아언어문화학과:
        return RussianLanguageAndCultureNoticeScraper(
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
    departments = [국어국문학과, 고고미술사학과, 독일언어문화학과, 사학과, 영어영문학과, 중어중문학과, 철학과, 프랑스언어문화학과, 러시아언어문화학과]

    for department in departments:
        if department == 러시아언어문화학과:
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