import pymysql
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='backend/test.env')

hosturl =  os.getenv('DB_HOST')
username = os.getenv('DB_USER')
userpassword = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME1')
es_pw = os.getenv('ES_PASS')
es_host = os.getenv('ES_HOST')
es_port = os.getenv('ES_PORT')

# Elasticsearch 설정 데이터 가져오기
es_config = {
    'hosts': [es_host],
    'http_auth': ('elastic', es_pw),  # 기본 사용자와 비밀번호
    'scheme': 'http',
    'port': es_port
}

# Elasticsearch 클라이언트 설정
es = Elasticsearch(
    es_config['hosts'],
    http_auth=es_config['http_auth']
)

# Elasticsearch에서 가장 최근의 `id` 가져오기
def get_last_indexed_id():
    query = {
        "size": 1,
        "sort": [
            {
                "id": {
                    "order": "desc"
                }
            }
        ],
        "_source": ["id"]
    }
    response = es.search(index="notice_index", body=query)
    hits = response['hits']['hits']
    if hits:
        return hits[0]['_id']
    return 0

# DB에서 데이터 읽기 (최신 `id` 이후 데이터만)
def fetch_data_from_db(last_id):
    db_connection = pymysql.connect(
        host=hosturl,
        user=username,
        password=userpassword,
        db=dbname,
        charset='utf8'
    )
    cursor = db_connection.cursor()

    # 데이터 조회 쿼리 (last_id 이후 데이터만 가져오기)
    query = "SELECT id, url, title, content, category, site, date, latitude, longitude FROM notice_board WHERE id > %s"
    cursor.execute(query, (last_id,))

    # 결과 가져오기
    data = cursor.fetchall()
    db_connection.close()
    return data

# DB에서 가져온 데이터를 Elasticsearch 도큐먼트로 변환
def generate_docs(data):
    for row in data:
        yield {
            "_index": 'notice_index',  # Elasticsearch 인덱스 이름
            "_id": row[0],  # id를 문서 ID로 사용
            "_source": {
                "url": row[1],
                "title": row[2],
                "content": row[3],
                "category": row[4],
                "site": row[5],
                "date": row[6].strftime('%Y-%m-%d %H:%M:%S'),  # 날짜 형식 변환
                "latitude": row[7],
                "longitude": row[8]
            }
        }

# Elasticsearch에 데이터 전송
def index_data():
    last_id = get_last_indexed_id()# 가장 최근의 id 가져오기
    data = fetch_data_from_db(last_id)
    success, failed = bulk(es, generate_docs(data))
    print(f"Successfully indexed {success} documents.")
    print(f"Failed to index {failed} documents.")

# 메인 실행
if __name__ == "__main__":
    index_data()
