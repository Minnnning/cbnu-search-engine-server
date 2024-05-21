import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

class SWCenterNotices:
    def __init__(self):
        self.url = "https://swapi.cbnu.ac.kr/v1/notice?page=1&limit=20&sort=-createdAt"
        self.site_id = boardTree['공통']['sw중심대학사업단']['공지사항']['id']
        self.site = "sw중심대학사업단"
        self.category = "공지사항"
        self.notice_list_selector = "pre"
        self.notice_contents_selector = ".ck-content"

    def get_notice_list(self):
        response = requests.get(self.url)
        data = response.json().get('data', {}).get('documents', [])

        notice_list = []
        for item in data:
            date = datetime.strptime(item['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
            notice = {
                "site": self.site,
                "category": self.category,
                "site_id": self.site_id,
                "title": item['title'],
                "url": f"https://sw7up.cbnu.ac.kr/community/notice/{item['_id']}",
                "date": f"{date.year}-{date.month}-{date.day}"
            }
            notice_list.append(notice)

        return notice_list

    def get_contents_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        content = soup.select_one(self.notice_contents_selector)
        return str(content) if content else ''

# Usage example
notices = SWCenterNotices()
notice_list = notices.get_notice_list()
for notice in notice_list:
    print(notice)
