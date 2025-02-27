import subprocess
import os
import logging

# 로그 설정
logging.basicConfig(
    level=logging.DEBUG,  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # 로그 메시지 형식
    handlers=[
        logging.StreamHandler()  # 콘솔에 로그 출력
        # logging.FileHandler('app.log')  # 파일에 로그 출력
    ]
)

# 경영대학 main.py 실행
def run_business_school():
    business_school_path = os.path.join(os.getcwd(), '경영대학', 'main.py')
    logging.info(f"경영대학 main.py 실행 시작: {business_school_path}")
    try:
        subprocess.run(['python', business_school_path], check=True)
        logging.info("경영대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"경영대학 main.py 실행 중 오류 발생: {e}")

# 공학대학 main.py 실행
def run_engineering_school():
    engineering_school_path = os.path.join(os.getcwd(), '공과대학', 'main.py')
    logging.info(f"공과대학 main.py 실행 시작: {engineering_school_path}")
    try:
        subprocess.run(['python', engineering_school_path], check=True)
        logging.info("공과대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"공과대학 main.py 실행 중 오류 발생: {e}")

# 공통 main.py 실행
def run_public():
    public_path = os.path.join(os.getcwd(), '공통', 'main.py')
    logging.info(f"공통 main.py 실행 시작: {public_path}")
    try:
        subprocess.run(['python', public_path], check=True)
        logging.info("공통 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"공통 main.py 실행 중 오류 발생: {e}")

# 농업생명환경대학 main.py 실행
def run_agriculture_school():
    agriculture_school_path = os.path.join(os.getcwd(), '농업생명환경대학', 'main.py')
    logging.info(f"농업생명환경대학 main.py 실행 시작: {agriculture_school_path}")
    try:
        subprocess.run(['python', agriculture_school_path], check=True)
        logging.info("농업생명환경대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"농업생명환경대학 main.py 실행 중 오류 발생: {e}")

# 사범대학 main.py 실행
def run_education_school():
    education_school_path = os.path.join(os.getcwd(), '사범대학', 'main.py')
    logging.info(f"사범대학 main.py 실행 시작: {education_school_path}")
    try:
        subprocess.run(['python', education_school_path], check=True)
        logging.info("사범대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"사범대학 main.py 실행 중 오류 발생: {e}")       

if __name__ == "__main__":
    logging.info("프로그램 실행 시작")
    #run_business_school()
    #run_engineering_school()
    #run_public()
    #run_agriculture_school()
    run_education_school()

    logging.info("프로그램 실행 완료")
