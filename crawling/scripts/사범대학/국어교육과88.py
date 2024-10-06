from notice_scraper import NoticeScraper
from selenium.webdriver.common.by import By
import time

class 국어교육과:
    # 국어교육과 공지사항 설정
    url = "https://edu.chungbuk.ac.kr/korean/selectBbsNttList.do?bbsNo=58&key=496"
    site = "국어교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(3) > div"
