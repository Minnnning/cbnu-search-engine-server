from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import pymysql
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='test.env')

# MariaDB 설정
DB_HOST = os.getenv('DB_HOST')
DB_PORT = 3306
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASS')
DB_NAME3 = os.getenv('DB_NAME3') 

# Elasticsearch 설정
ES_HOST = os.getenv('ES_HOST')
ES_INDEX = os.getenv('ES_INDEX')
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASS')

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME3}")

app = FastAPI()

# 요청 바디 모델
class SearchRequest(BaseModel):
    query: str

# 검색어를 Nori 분석기를 통해 토큰화하는 함수
def tokenize_query_with_nori(query: str) -> List[str]:
    analyze_request_body = {
        "analyzer": "nori_analyzer",  # Nori 분석기 사용
        "text": query
    }
    
    response = requests.post(
        f"{ES_HOST}/_analyze",
        json=analyze_request_body,
        auth=(ES_USER, ES_PASSWORD)
    )
    
    if response.status_code == 200:
        tokens = [token['token'] for token in response.json().get('tokens', [])]
        return tokens
    else:
        raise HTTPException(status_code=response.status_code, detail="Nori 분석기를 사용한 토큰화 실패")

# Elasticsearch에 검색 요청을 보내는 함수
def search_elasticsearch(tokens: List[str]):
    query_string = " ".join(tokens)
    es_query = {
        "query": {
            "multi_match": {
                "query": query_string,
                "fields": ["title", "content"]
            }
        }
    }
    
    response = requests.get(
        f"{ES_HOST}/{ES_INDEX}/_search",
        json=es_query,
        auth=(ES_USER, ES_PASSWORD)
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Elasticsearch 검색에 실패했습니다.")

# 검색어와 검색 시간을 MariaDB에 저장하는 함수
def store_search_terms_in_db(tokens: List[str]):
    current_time = datetime.now()
    
    with engine.connect() as connection:
        for token in tokens:
            query = text("INSERT INTO search_tokens (token, search_time) VALUES (:token, :search_time)")
            connection.execute(query, {"token": token, "search_time": current_time})

# 최근 24시간 이내에 가장 많이 검색된 토큰 상위 5개를 조회하는 함수
def get_top_search_terms_from_db(limit: int = 5) -> List[str]:  # 기본값을 5로 설정
    past_24_hours = datetime.now() - timedelta(hours=24)
    
    with engine.connect() as connection:
        query = text("""
            SELECT token, COUNT(*) as count 
            FROM search_tokens 
            WHERE search_time >= :past_24_hours
            GROUP BY token 
            ORDER BY count DESC 
            LIMIT :limit
        """)
        result = connection.execute(query, {"past_24_hours": past_24_hours, "limit": limit})
        return [{"token": row["token"], "count": row["count"]} for row in result]

# 검색 API 엔드포인트
@app.post("/search")
def search(request: SearchRequest):
    # 검색어 토큰화 (Nori 분석기 사용)
    tokens = tokenize_query_with_nori(request.query)
    
    # 검색어 토큰 저장 (MariaDB)
    store_search_terms_in_db(tokens)
    
    # Elasticsearch로 검색 요청
    search_results = search_elasticsearch(tokens)
    
    return {
        "tokens": tokens,
        "results": search_results
    }

# 실시간 검색어를 조회하는 API 엔드포인트
@app.get("/search-terms")
def get_search_terms():
    # 가장 많이 검색된 검색어 상위 5개 반환 (최근 24시간 기준)
    top_search_terms = get_top_search_terms_from_db(limit=5)
    return {
        "realtime_search_terms": top_search_terms
    }
