class 생물교육과:
    # 생물교육과 공지사항 설정
    url = "http://edu.chungbuk.ac.kr/bio/selectBbsNttList.do?key=399&bbsNo=2"
    site = "생물교육과"
    category = "공지사항"
    notice_list_selector = "#board > div.tableA > table > tbody > tr"
    notice_contents_selector = "#board > div > div.tit_area > ul > li:nth-child(4)"