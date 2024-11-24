class 사학과:
    # 사학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/cbnuhistory/selectBbsNttList.do?bbsNo=98&key=388"
    site = "사학과"
    category = "공지사항"
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(2) > td"
