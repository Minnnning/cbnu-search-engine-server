import subprocess
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# 로그 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 각 대학 및 기능별 main.py 실행 함수들
def run_business_school():
    path = os.path.join(os.getcwd(), '경영대학', 'main.py')
    logging.info(f"경영대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("경영대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"경영대학 main.py 실행 중 오류 발생: {e}")

def run_engineering_school():
    path = os.path.join(os.getcwd(), '공과대학', 'main.py')
    logging.info(f"공과대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("공과대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"공과대학 main.py 실행 중 오류 발생: {e}")

def run_public():
    path = os.path.join(os.getcwd(), '공통', 'main.py')
    logging.info(f"공통 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("공통 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"공통 main.py 실행 중 오류 발생: {e}")

def run_agriculture_school():
    path = os.path.join(os.getcwd(), '농업생명환경대학', 'main.py')
    logging.info(f"농업생명환경대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("농업생명환경대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"농업생명환경대학 main.py 실행 중 오류 발생: {e}")

def run_education_school():
    path = os.path.join(os.getcwd(), '사범대학', 'main.py')
    logging.info(f"사범대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("사범대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"사범대학 main.py 실행 중 오류 발생: {e}")

def run_social_school():
    path = os.path.join(os.getcwd(), '사회과학대학', 'main.py')
    logging.info(f"사회과학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("사회과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"사회과학대학 main.py 실행 중 오류 발생: {e}")

def run_life_sciences_school():
    path = os.path.join(os.getcwd(), '생활과학대학', 'main.py')
    logging.info(f"생활과학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("생활과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"생활과학대학 main.py 실행 중 오류 발생: {e}")

def run_veterinary_medicine_school():
    path = os.path.join(os.getcwd(), '수의과학대학', 'main.py')
    logging.info(f"수의과학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("수의과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"수의과학대학 main.py 실행 중 오류 발생: {e}")

def run_pharmacy_school():
    path = os.path.join(os.getcwd(), '약학대학', 'main.py')
    logging.info(f"약학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("약학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"약학대학 main.py 실행 중 오류 발생: {e}")

def run_convergence_science_school():
    path = os.path.join(os.getcwd(), '융합과학대학', 'main.py')
    logging.info(f"융합과학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("융합과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"융합과학대학 main.py 실행 중 오류 발생: {e}")

def run_medicine_school():
    path = os.path.join(os.getcwd(), '의과대학', 'main.py')
    logging.info(f"의과대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("의과대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"의과대학 main.py 실행 중 오류 발생: {e}")

def run_humanities_school():
    path = os.path.join(os.getcwd(), '인문대학', 'main.py')
    logging.info(f"인문대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("인문대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"인문대학 main.py 실행 중 오류 발생: {e}")

def run_natural_sciences_school():
    path = os.path.join(os.getcwd(), '자연과학대학', 'main.py')
    logging.info(f"자연과학대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("자연과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"자연과학대학 main.py 실행 중 오류 발생: {e}")

def run_electronics_information_school():
    path = os.path.join(os.getcwd(), '전자정보대학', 'main.py')
    logging.info(f"전자정보대학 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("전자정보대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"전자정보대학 main.py 실행 중 오류 발생: {e}")

def run_menu():
    path = os.path.join(os.getcwd(), '학식', 'main.py')
    logging.info(f"학식 main.py 실행 시작: {path}")
    try:
        subprocess.run(['python', path], check=True)
        logging.info("학식 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"학식 main.py 실행 중 오류 발생: {e}")

if __name__ == '__main__':
    scheduler = BlockingScheduler({'apscheduler.timezone':'Asia/Seoul'})

    # 아래 작업들은 하루에 한 번씩 실행되며, 각각 30분 간격으로 시간대를 달리하여 실행합니다.
    scheduler.add_job(run_business_school, 'cron', hour=0, minute=0, id='business_school')
    scheduler.add_job(run_engineering_school, 'cron', hour=0, minute=30, id='engineering_school')
    scheduler.add_job(run_public, 'cron', hour=1, minute=0, id='public')
    scheduler.add_job(run_agriculture_school, 'cron', hour=1, minute=30, id='agriculture_school')
    scheduler.add_job(run_education_school, 'cron', hour=2, minute=0, id='education_school')
    scheduler.add_job(run_social_school, 'cron', hour=2, minute=30, id='social_school')
    scheduler.add_job(run_life_sciences_school, 'cron', hour=3, minute=0, id='life_sciences_school')
    scheduler.add_job(run_veterinary_medicine_school, 'cron', hour=3, minute=30, id='veterinary_medicine_school')
    scheduler.add_job(run_pharmacy_school, 'cron', hour=4, minute=0, id='pharmacy_school')
    scheduler.add_job(run_convergence_science_school, 'cron', hour=4, minute=30, id='convergence_science_school')
    scheduler.add_job(run_medicine_school, 'cron', hour=5, minute=0, id='medicine_school')
    scheduler.add_job(run_humanities_school, 'cron', hour=5, minute=30, id='humanities_school')
    scheduler.add_job(run_natural_sciences_school, 'cron', hour=6, minute=0, id='natural_sciences_school')
    scheduler.add_job(run_electronics_information_school, 'cron', hour=6, minute=30, id='electronics_information_school')
    
    # 메뉴 크롤링은 매주 토요일에만 실행 (예: 토요일 자정)
    scheduler.add_job(run_menu, 'cron', day_of_week='sat', hour=7, minute=0, id='menu')
    
    logging.info('스케줄러 시작')
    scheduler.start()
