import pymysql
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# DB 설정 데이터 가져오기
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    db_config = {
        'host': config['host'],
        'user': config['username'],
        'password': config['password'],
        'db': config['db']
    }

# Elasticsearch 설정 데이터 가져오기
es_config = {
    'hosts': ['http://localhost:9200'],
    'http_auth': ('elastic', config['es_pw']),  # 기본 사용자와 비밀번호
    'scheme': 'http',
    'port': 9200
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
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        charset='utf8'
    )
    cursor = db_connection.cursor()

    # 데이터 조회 쿼리 (last_id 이후 데이터만 가져오기)
    query = "SELECT id, url, title, content, category, site, date FROM notice_board WHERE id > %s"
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
                "date": row[6].strftime('%Y-%m-%d %H:%M:%S')  # 날짜 형식 변환
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
