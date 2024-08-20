from elasticsearch import Elasticsearch

# Elasticsearch 설정 데이터 가져오기
es_config = {
    'hosts': ['http://localhost:9200'],
    'http_auth': ('elastic', 'Pw'),  # 기본 사용자와 비밀번호
    'scheme': 'http',
    'port': 9200
}

# Elasticsearch 클라이언트 설정
es = Elasticsearch(
    es_config['hosts'],
    http_auth=es_config['http_auth']
)
# 모든 문서 조회 (기본적으로 상위 10개)
response = es.search(index="notice_index", body={"query": {"match_all": {}}})

# 검색 결과 출력
for hit in response['hits']['hits']:
    print(hit['_source'])


response = es.count(index="notice_index")

# 저장된 문서 개수 출력
print("Stored document count:", response['count'])