from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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
DB_NAME_SEARCH = os.getenv('DB_NAME3')
DB_NAME_RESTAURANT = os.getenv('DB_NAME2')  

# Elasticsearch 설정
ES_HOST = os.getenv('ES_HOST')
ES_INDEX = os.getenv('ES_INDEX')
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASS')

# SQLAlchemy 엔진 생성 및 세션 설정
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_SEARCH}")
engine_restaurant = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_RESTAURANT}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalRestaurant = sessionmaker(autocommit=False, autoflush=False, bind=engine_restaurant)

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
        f"{ES_HOST}/{ES_INDEX}/_analyze",
        json=analyze_request_body,
        auth=(ES_USER, ES_PASSWORD)
    )
    
    if response.status_code == 200:
        tokens = [token['token'] for token in response.json().get('tokens', [])]
        return tokens
    else:
        raise HTTPException(status_code=response.status_code, detail="Nori 분석기를 사용한 토큰화 실패")

# Elasticsearch에 검색 요청을 보내는 함수 (페이지네이션 포함)
def search_elasticsearch(query_string, page: int = 0, size: int = 10):
    #query_string = " ".join(tokens)
    es_query = {
        "query": {
            "multi_match": {
                "query": query_string,
                "fields": ["title^2", "content"],  # 검색할 필드 목록 및 가중치
                "fuzziness": "AUTO"  # 오타 허용
            }
        },
        "highlight": {
            "fields": {
                "title": {},  # 제목에서 매칭된 단어 하이라이트
                "content": {}  # 본문에서 매칭된 단어 하이라이트
            }
        },
        "from": page * size,  # 어느 결과부터 가져올지
        "size": size  # 몇 개의 결과를 가져올지
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
def store_search_terms_in_db(tokens: str):
    current_time = datetime.now()
    db_session = SessionLocal()
    tokens = tokens.split()
    try:
        for token in tokens:
            query = text("INSERT INTO search_tokens (token, search_time) VALUES (:token, :search_time)")
            db_session.execute(query, {"token": token, "search_time": current_time})
        
        db_session.commit()  # 데이터베이스에 변경 사항 커밋
    except Exception as e:
        db_session.rollback()  # 오류 발생 시 롤백
        raise HTTPException(status_code=500, detail="데이터 저장 중 오류가 발생했습니다.")
    finally:
        db_session.close()  # 세션 종료

# restaurant DB의 menus 테이블에서 모든 데이터를 가져오는 함수
def get_menus_from_db():
    db_session = SessionLocalRestaurant()
    
    try:
        query = text("SELECT * FROM menus")
        result = db_session.execute(query).fetchall()  # 모든 결과 행을 가져옴
        menus = [dict(row._mapping) for row in result]  # 각 행을 딕셔너리로 변환
        return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail="메뉴 데이터를 가져오는 중 오류가 발생했습니다.")
    finally:
        db_session.close()

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
        
        result_dict = result.mappings().all()
        return [{"token": row["token"], "count": row["count"]} for row in result_dict]
    
# 학과별 공지사항을 notice_table에서 가져오는 함수
def get_notices_by_department(department: str):
    db_session = SessionLocal()  # Using the same session for the search database

    try:
        # SQL query to fetch notices based on the department (site field)
        query = text("SELECT * FROM notice_table WHERE site = :department")
        result = db_session.execute(query, {"department": department}).fetchall()
        
        # Convert the result to a list of dictionaries
        notices = [dict(row._mapping) for row in result]
        return notices
    except Exception as e:
        raise HTTPException(status_code=500, detail="학과 공지사항을 가져오는 중 오류가 발생했습니다.")
    finally:
        db_session.close()

# 검색 API 엔드포인트
@app.post("/search")
def search(request: SearchRequest, page: int = 0, size: int = 10):
    
    # 검색어 토큰화 (Nori 분석기 사용)
    # tokens = tokenize_query_with_nori(request.query)
    
    # 검색어 저장 (MariaDB)
    store_search_terms_in_db(request.query)
    
    # Elasticsearch로 검색 요청
    search_results = search_elasticsearch(request.query, page=page, size=size)
    
    return {
        #"tokens": tokens,
        "query": request.query,
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

# 학식을 조회하는 API 엔드포인트
@app.get("/menus")
def get_menus():
    store_search_terms_in_db(["학식"])
    menus = get_menus_from_db()
    return menus

# 학과 공지사항 조회 API 엔드포인트
@app.get("/notices/{department}")
def get_notices(department: str):
    # 학과별 공지사항 가져오기
    notices = get_notices_by_department(department)
    
    if not notices:
        raise HTTPException(status_code=404, detail="해당 학과의 공지사항을 찾을 수 없습니다.")
    
    # 공지사항 반환
    return {
        "department": department,
        "notices": notices
    }
