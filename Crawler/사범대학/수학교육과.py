class 수학교육과:
    # 수학교육과 공지사항 설정
    url = "http://edu.chungbuk.ac.kr/mathedu/selectBbsNttList.do?key=763&bbsNo=88"
    site = "수학교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(3) > div"