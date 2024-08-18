class 철학과:
    # 철학과 공지사항 설정
    url = "https://humanum.chungbuk.ac.kr/philosophy/selectBbsNttList.do?bbsNo=99&key=366"
    site = "철학과"
    category = "공지사항"
    notice_list_selector = "#contents > table > tbody > tr"
    notice_contents_selector = "#contents > table > tbody > tr:nth-child(2) > td"

