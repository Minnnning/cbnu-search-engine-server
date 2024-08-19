import schedule
import time
import os

def run_scripts():
    # 실행할 파이썬 파일들
    scripts = ["scripts/경영대학/main.py",
               "scripts/공과대학/main.py",
               "scripts/농업생명환경대학/main.py",
               "scripts/사범대학/main.py",
               "scripts/사회과학대학/main.py",
               "scripts/생활과학대학/main.py",
               "scripts/수의과대학/main.py",
               "scripts/약학대학/main.py",
               "scripts/의과대학/main.py",
               "scripts/인문대학/main.py",
               "scripts/자연과학대학/main.py",
               "scripts/전자정보대학/main.py"]
    
    for script in scripts:
        os.system(f"python {script}")
        print(f"{script} 실행 완료")

# 매일 오후 2시에 실행
schedule.every().day.at("09:08").do(run_scripts)

while True:
    schedule.run_pending()
    time.sleep(100)


# import subprocess

# def run_scripts():
#     # 실행할 파이썬 파일들
#     scripts = ["script1.py", "script2.py", "script3.py"]
    
#     for script in scripts:
#         # subprocess.run을 사용하여 Python 파일 실행
#         result = subprocess.run(["python", script], capture_output=True, text=True)
#         if result.returncode == 0:
#             print(f"{script} 실행 완료")
#         else:
#             print(f"{script} 실행 중 오류 발생")
#             print(f"오류 메시지: {result.stderr}")

# # 예시로 run_scripts 호출
# run_scripts()
