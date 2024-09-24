from fastapi import FastAPI, HTTPException, Query
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
load_dotenv(dotenv_path='backend/test.env')

# MariaDB 설정
DB_HOST = os.getenv('DB_HOST')
DB_PORT = 3306
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASS')
DB_NAME_NOTICE = os.getenv('DB_NAME1')
DB_NAME_RESTAURANT = os.getenv('DB_NAME2')  
DB_NAME_SEARCH = os.getenv('DB_NAME3')

# Elasticsearch 설정
ES_HOST = os.getenv('ES_HOST')
ES_INDEX = os.getenv('ES_INDEX')
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASS')

# SQLAlchemy 엔진 생성 및 세션 설정
engine_notice = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_NOTICE}")
engine_search_term = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_SEARCH}")
engine_restaurant = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_RESTAURANT}")
SessionLocalNotice = sessionmaker(autocommit=False, autoflush=False, bind=engine_notice)
SessionLocalSearchTerm = sessionmaker(autocommit=False, autoflush=False, bind=engine_search_term)
SessionLocalRestaurant = sessionmaker(autocommit=False, autoflush=False, bind=engine_restaurant)

app = FastAPI()

# 학과 목록 예시
departments = ["경영정보학과대학원", "경영정보학과", "국제경영학과", "경영학부",
               "기계공학부", "환경공학과", "도시공학과", "화학공학과", "건축학과", "토목공학부", "신소재공학과", "공업화학과", "건축공학과", "안전공학과",
               "식물의학과", "환경생명화학과", "바이오시스템공학과", "지역건설공학과", "식품생명공학과", "특용식물학과", "원예학과", "산림학과", "축산학과", "목재종이과학과", "식물자원학과", "농업경제학과",
               "수학교육과", "교육학과", "물리교육과", "윤리교육과", "생물교육과", "국어교육과", "화학교육과", "지구과학교육과", "지리교육과", "역사교육과", "사회교육과", "영어교육과", "체육교육과",
               "사회학과", "경제학과", "행정학과", "정치외교학과", "심리학과",
               "주거환경학과", "소비자학과", "식품영양학과", "의류학과", "아동복지학과",
               "수의예과", "수의학과", "약학과", "간호학과", "의학과",
               "디자인학과", "조형예술학과",
               "철학과", "러시아언어문화학과", "국어국문학과", "프랑스언어문화학과", "영어영문학과", "중어중문학과", "독일언어문화학과", "고고미술사학과",
               "수학과", "생물학과", "화학과", "정보통계학과", "미생물학과", "천문우주학과", "물리학과", "생화학과", "지구환경과학과",
               "전자공학부", "정보통신공학부", "전기공학부", "지능로봇공학과", "반도체공학부", "소프트웨어학과", "컴퓨터공학과",
               "학생생활관", "sw중심사업단", "충북대취업지원본부", "국제교류본부", "linc사업단", "충북대공지사항"]

# 요청 바디 모델
class SearchRequest(BaseModel):
    query: str

# SearchResult와 일치하는 Pydantic 모델 정의
class SearchResult(BaseModel):
    id: str
    site: str
    title: str
    url: str
    date: str
    contentPreview: str = None  # 내용 미리보기는 옵션

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
    db_session = SessionLocalSearchTerm()
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
    
    with engine_search_term.connect() as connection:
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
    
# 학과별 공지사항을 notice_board에서 가져오는 함수
def get_notices_by_department(department: str, page: int = 0, size: int = 10) -> List[SearchResult]:
    db_session = SessionLocalNotice()
    page = page + 1
    try:
        # 페이지네이션을 위한 LIMIT과 OFFSET 설정
        query = text("""
            SELECT * FROM notice_board WHERE site = :department
            ORDER BY date DESC
            LIMIT :limit OFFSET :offset
        """)
        result = db_session.execute(query, {"department": department, "limit": size, "offset": page * size}).fetchall()
        
        # 결과를 SearchResult 리스트로 변환
        notices = []
        for row in result:
            date_str = row._mapping['date'].strftime("%Y-%m-%d")  # 날짜 형식 변환
            content_preview = (row._mapping['content'][:100].strip() if row._mapping['content'] else None)
            notice = SearchResult(
                id=str(row._mapping['id']),
                site=row._mapping['site'],
                title=row._mapping['title'],
                url=row._mapping['url'],
                date=date_str,
                content=content_preview
            )
            notices.append(notice)

        return notices
    except Exception as e:
        raise HTTPException(status_code=500, detail="학과 공지사항을 가져오는 중 오류가 발생했습니다.")
    finally:
        db_session.close()

# 검색어에 학과명을 포함하는지 확인하는 함수
def extract_department_from_query(query: str) -> str:
    for department in departments:
        if department in query:
            return department
    return None

# 검색 API 엔드포인트 수정
@app.post("/search")
def search(request: SearchRequest, page: int = 0, size: int = 10):
    # 학과명 추출
    department = extract_department_from_query(request.query)
    
    if department:
        # 학과명이 포함된 경우 해당 학과 공지사항 조회
        notices = get_notices_by_department(department, page, size)
        # 실시간 검색어 저장
        store_search_terms_in_db(department)
        
        if not notices:
            raise HTTPException(status_code=404, detail="해당 학과의 공지사항을 찾을 수 없습니다.")
        
        # 공지사항 반환
        return {
            "query": department,
            "results": notices
        }

    # 검색어 토큰화 및 저장
    store_search_terms_in_db(request.query)
    
    # Elasticsearch로 검색 요청
    search_results = search_elasticsearch(request.query, page=page, size=size)

    # Elasticsearch 응답에서 필요한 정보만 추출
    results = []
    for hit in search_results['hits']['hits']:
        source = hit['_source']
        results.append({
            "id": hit['_id'],
            "site": source.get('site', ''),
            "title": source.get('title', ''),
            "url": source.get('url', ''),
            "date": source.get('date', ''),
            "contentPreview": source.get('content', '')
        })
    
    return {
        "query": request.query,
        "results": results
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
    store_search_terms_in_db("학식")
    menus = get_menus_from_db()
    return menus

