class 축산학과:
    # 축산학과 공지사항 설정
    url = "https://animalscience.chungbuk.ac.kr/board/board.php?id=as_news"
    site = "축산학과"
    category = "공지사항"
    notice_list_selector = "#contentsArea > div > table.basicList > tbody > tr"
    notice_contents_selector = "#contentsArea > div > div.tableWrap > table > tbody > tr:nth-child(3)"