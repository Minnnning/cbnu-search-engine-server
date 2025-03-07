import os
import runpy
import logging
import pymysql
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_business_school():
    path = os.path.join(os.getcwd(), '경영대학', 'main.py')
    logging.info(f"경영대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("경영대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"경영대학 main.py 실행 중 오류 발생: {e}")

def run_engineering_school():
    path = os.path.join(os.getcwd(), '공과대학', 'main.py')
    logging.info(f"공과대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("공과대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"공과대학 main.py 실행 중 오류 발생: {e}")

def run_public():
    path = os.path.join(os.getcwd(), '공통', 'main.py')
    logging.info(f"공통 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("공통 main.py 실행 완료")
    except Exception as e:
        logging.error(f"공통 main.py 실행 중 오류 발생: {e}")

def run_agriculture_school():
    path = os.path.join(os.getcwd(), '농업생명환경대학', 'main.py')
    logging.info(f"농업생명환경대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("농업생명환경대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"농업생명환경대학 main.py 실행 중 오류 발생: {e}")

def run_education_school():
    path = os.path.join(os.getcwd(), '사범대학', 'main.py')
    logging.info(f"사범대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("사범대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"사범대학 main.py 실행 중 오류 발생: {e}")

def run_social_school():
    path = os.path.join(os.getcwd(), '사회과학대학', 'main.py')
    logging.info(f"사회과학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("사회과학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"사회과학대학 main.py 실행 중 오류 발생: {e}")

def run_life_sciences_school():
    path = os.path.join(os.getcwd(), '생활과학대학', 'main.py')
    logging.info(f"생활과학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("생활과학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"생활과학대학 main.py 실행 중 오류 발생: {e}")

def run_veterinary_medicine_school():
    path = os.path.join(os.getcwd(), '수의과학대학', 'main.py')
    logging.info(f"수의과학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("수의과학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"수의과학대학 main.py 실행 중 오류 발생: {e}")

def run_pharmacy_school():
    path = os.path.join(os.getcwd(), '약학대학', 'main.py')
    logging.info(f"약학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("약학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"약학대학 main.py 실행 중 오류 발생: {e}")

def run_convergence_science_school():
    path = os.path.join(os.getcwd(), '융합과학대학', 'main.py')
    logging.info(f"융합과학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("융합과학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"융합과학대학 main.py 실행 중 오류 발생: {e}")

def run_medicine_school():
    path = os.path.join(os.getcwd(), '의과대학', 'main.py')
    logging.info(f"의과대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("의과대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"의과대학 main.py 실행 중 오류 발생: {e}")

def run_humanities_school():
    path = os.path.join(os.getcwd(), '인문대학', 'main.py')
    logging.info(f"인문대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("인문대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"인문대학 main.py 실행 중 오류 발생: {e}")

def run_natural_sciences_school():
    path = os.path.join(os.getcwd(), '자연과학대학', 'main.py')
    logging.info(f"자연과학대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("자연과학대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"자연과학대학 main.py 실행 중 오류 발생: {e}")

def run_electronics_information_school():
    path = os.path.join(os.getcwd(), '전자정보대학', 'main.py')
    logging.info(f"전자정보대학 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("전자정보대학 main.py 실행 완료")
    except Exception as e:
        logging.error(f"전자정보대학 main.py 실행 중 오류 발생: {e}")

def run_menu():
    path = os.path.join(os.getcwd(), '학식', 'main.py')
    logging.info(f"학식 main.py 실행 시작: {path}")
    try:
        runpy.run_path(path, run_name="__main__")
        logging.info("학식 main.py 실행 완료")
    except Exception as e:
        logging.error(f"학식 main.py 실행 중 오류 발생: {e}")

# ---------- DB -> ES 동기화 함수 ----------
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

# 환경변수에서 DB 및 ES 연결 정보 읽기
hosturl = os.getenv('DB_HOST')
username = os.getenv('DB_USER')
userpassword = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME')
es_host = os.getenv('ES_HOST')
es_port = os.getenv('ES_PORT')

# Elasticsearch 클라이언트 생성 (비밀번호 없이)
es = Elasticsearch([es_host])

def get_last_indexed_id():
    query = {
        "size": 1,
        "sort": [
            {"id": {"order": "desc"}}
        ],
        "_source": ["id"]
    }
    response = es.search(index="notice_index", body=query)
    hits = response['hits']['hits']
    if hits:
        return int(hits[0]['_id'])
    return 0

def fetch_data_from_db(last_id):
    db_connection = pymysql.connect(
        host=hosturl,
        user=username,
        password=userpassword,
        db=dbname,
        charset='utf8'
    )
    cursor = db_connection.cursor()
    query = """SELECT id, url, title, content, category, site, date, latitude, longitude 
               FROM notice_board WHERE id > %s"""
    cursor.execute(query, (last_id,))
    data = cursor.fetchall()
    db_connection.close()
    return data

def generate_docs(data):
    for row in data:
        yield {
            "_index": 'notice_index',
            "_id": row[0],
            "_source": {
                "url": row[1],
                "title": row[2],
                "content": row[3],
                "category": row[4],
                "site": row[5],
                "date": row[6].strftime('%Y-%m-%d %H:%M:%S'),
                "latitude": row[7],
                "longitude": row[8]
            }
        }

def sync_db_to_es():
    """
    DB에서 새로운 데이터를 읽어와 Elasticsearch에 색인합니다.
    이미 색인된 문서와 동일한 id가 있을 경우 덮어씁니다.
    """
    try:
        last_id = get_last_indexed_id() # 마지막id
        data = fetch_data_from_db(last_id) #마지막 id 이후
        if data:
            success, _ = bulk(es, generate_docs(data))
            logging.info(f"Successfully indexed {success} documents.")
        else:
            logging.info("색인할 새로운 데이터가 없습니다.")
    except Exception as e:
        logging.error(f"DB에서 ES로 데이터 동기화 중 오류 발생: {e}")
