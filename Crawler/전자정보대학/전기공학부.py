class 전기공학부:
    # 전기공학부 공지사항 설정
    url = "https://koamma.chungbuk.ac.kr/bbs/bbs.php?db=notice"
    site = "전기공학부"
    category = "공지사항"
    notice_list_selector = "#subContent > div.section > table:nth-child(6) > tbody > tr"
    notice_contents_selector = "#articles" 