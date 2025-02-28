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

# 사회과학대학 main.py 실행
def run_social_school():
    social_school_path = os.path.join(os.getcwd(), '사회과학대학', 'main.py')
    logging.info(f"사회과학대학 main.py 실행 시작: {social_school_path}")
    try:
        subprocess.run(['python', social_school_path], check=True)
        logging.info("사회과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"사회과학대학 main.py 실행 중 오류 발생: {e}")   

# 생활과학대학 main.py 실행
def run_life_sciences_school():
    life_sciences_school_path = os.path.join(os.getcwd(), '생활과학대학', 'main.py')
    logging.info(f"생활과학대학 main.py 실행 시작: {life_sciences_school_path}")
    try:
        subprocess.run(['python', life_sciences_school_path], check=True)
        logging.info("생활과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"생활과학대학 main.py 실행 중 오류 발생: {e}")   

# 수의과학대학 main.py 실행
def run_veterinary_medicine_school():
    veterinary_medicine_school_path = os.path.join(os.getcwd(), '수의과학대학', 'main.py')
    logging.info(f"수의과학대학 main.py 실행 시작: {veterinary_medicine_school_path}")
    try:
        subprocess.run(['python', veterinary_medicine_school_path], check=True)
        logging.info("수의과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"수의과학대학 main.py 실행 중 오류 발생: {e}")   

# 약학대학 main.py 실행
def run_pharmacy_school():
    pharmacy_school_path = os.path.join(os.getcwd(), '약학대학', 'main.py')
    logging.info(f"약학대학 main.py 실행 시작: {pharmacy_school_path}")
    try:
        subprocess.run(['python', pharmacy_school_path], check=True)
        logging.info("약학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"약학대학 main.py 실행 중 오류 발생: {e}")  

# 융합과학대학 main.py 실행
def run_convergence_science_school():
    convergence_science_school_path = os.path.join(os.getcwd(), '융합과학대학', 'main.py')
    logging.info(f"융합과학대학 main.py 실행 시작: {convergence_science_school_path}")
    try:
        subprocess.run(['python', convergence_science_school_path], check=True)
        logging.info("융합과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"융합과학대학 main.py 실행 중 오류 발생: {e}")  

# 의과대학 main.py 실행
def run_medicine_school():
    medicine_school_path = os.path.join(os.getcwd(), '의과대학', 'main.py')
    logging.info(f"의과대학 main.py 실행 시작: {medicine_school_path}")
    try:
        subprocess.run(['python', medicine_school_path], check=True)
        logging.info("의과대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"의과대학 main.py 실행 중 오류 발생: {e}")  

# 인문대학 main.py 실행
def run_humanities_school():
    humanities_school_path = os.path.join(os.getcwd(), '인문대학', 'main.py')
    logging.info(f"인문대학 main.py 실행 시작: {humanities_school_path}")
    try:
        subprocess.run(['python', humanities_school_path], check=True)
        logging.info("인문대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"인문대학 main.py 실행 중 오류 발생: {e}")  

# 자연과학대학 main.py 실행
def run_natural_sciences_school():
    natural_sciences_school_path = os.path.join(os.getcwd(), '자연과학대학', 'main.py')
    logging.info(f"자연과학대학 main.py 실행 시작: {natural_sciences_school_path}")
    try:
        subprocess.run(['python', natural_sciences_school_path], check=True)
        logging.info("자연과학대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"자연과학대학 main.py 실행 중 오류 발생: {e}")  

# 전자정보대학 main.py 실행
def run_electronics_information_school():
    electronics_information_school_path = os.path.join(os.getcwd(), '전자정보대학', 'main.py')
    logging.info(f"전자정보대학 main.py 실행 시작: {electronics_information_school_path}")
    try:
        subprocess.run(['python', electronics_information_school_path], check=True)
        logging.info("전자정보대학 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"전자정보대학 main.py 실행 중 오류 발생: {e}")  

# 학식 main.py 실행
def run_menu():
    menu_path = os.path.join(os.getcwd(), '학식', 'main.py')
    logging.info(f"학식 main.py 실행 시작: {menu_path}")
    try:
        subprocess.run(['python', menu_path], check=True)
        logging.info("학식 main.py 실행 완료")
    except subprocess.CalledProcessError as e:
        logging.error(f"학식 main.py 실행 중 오류 발생: {e}")  

if __name__ == "__main__":
    logging.info("프로그램 실행 시작")
    #run_business_school()
    #run_engineering_school()
    #run_public() # 충북대 사이트 1개만 되었음 확인 필요
    #run_agriculture_school()
    #run_education_school()
    #run_social_school()
    #run_life_sciences_school()
    #run_veterinary_medicine_school()
    #run_pharmacy_school()
    #run_convergence_science_school()
    #run_medicine_school()
    #run_humanities_school()
    #run_natural_sciences_school()
    #run_electronics_information_school()

    run_menu()
    logging.info("프로그램 실행 완료")
