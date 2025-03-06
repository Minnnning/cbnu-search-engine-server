from notice_scraper import NoticeScraper

class 교육학과:
    # 교육학과 공지사항 설정
    url = "https://edu.chungbuk.ac.kr/edu/selectBbsNttList.do?key=170&bbsNo=8"
    site = "교육학과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(3) > div"

