import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class NoticeScraper:
    def __init__(self, url, site, category, notice_list_selector, notice_contents_selector):
        self.url = url
        self.site = site
        self.category = category
        self.notice_list_selector = notice_list_selector
        self.notice_contents_selector = notice_contents_selector

    def get_notice_list(self):
        response = requests.get(self.url)
        data = json.loads(response.text)
        list = data['data']['documents']
        notice_list = []

        for item in list:
            row = item
            date = datetime.strptime(row['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

            notice = {
                'site': self.site,
                'category': self.category,
                'title': row['title'],
                'url': f"https://sw7up.cbnu.ac.kr/community/notice/{row['_id']}",
                'date': f"{date.year}-{date.month}-{date.day}",
            }
            notice_list.append(notice)

        return notice_list

    def get_contents_text(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.select_one(self.notice_contents_selector).get_text(strip=True)
        return contents

# Usage
url = "https://swapi.cbnu.ac.kr/v1/notice?page=1&limit=20&sort=-createdAt"
site = "sw중심대학사업단"
category = "공지사항"
notice_list_selector = "pre"
notice_contents_selector = ".ck-content"

scraper = NoticeScraper(url, site, category, notice_list_selector, notice_contents_selector)
notice_list = scraper.get_notice_list()

for notice in notice_list:
    print(f"Title: {notice['title']}")
    print(f"URL: {notice['url']}")
    print(f"Date: {notice['date']}")
    contents_text = scraper.get_contents_text(notice['url'])
    print(f"Contents:\n{contents_text}")
