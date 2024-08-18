class 소비자학과:
    # 소비자학과 공지사항 설정
    url = "https://consumer.cbnu.ac.kr/main/sub.html?pageCode=39"
    site = "소비자학과"
    category = "학과공지사항"
    notice_list_selector = ".jmboardskin1 tr:not(.jTh):not(.jTh2)"
    notice_contents_selector = "#lightgallery"
