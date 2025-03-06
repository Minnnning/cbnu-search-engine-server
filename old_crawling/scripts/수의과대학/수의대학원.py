class 수의대학원:
    # 수의학과 대학원 공지사항 설정
    url = "https://vetmed.chungbuk.ac.kr/board/graduateschool-notice.do"
    site = "수의대학원"
    category = "공지사항"
    notice_list_selector = "#container > div > div.content_body > div > div.boardList > table > tbody > tr"
    notice_contents_selector = ".boardViewContent"
