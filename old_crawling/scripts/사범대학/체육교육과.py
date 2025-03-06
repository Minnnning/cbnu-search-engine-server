class 체육교육과:
    # 체육교육과 공지사항 설정
    url = "http://edu.chungbuk.ac.kr/physicaledu/selectBbsNttList.do?key=479&bbsNo=96"
    site = "체육교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(3) > div"