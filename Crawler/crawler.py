import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from tasks import (
    run_business_school,
    run_engineering_school,
    run_public,
    run_agriculture_school,
    run_education_school,
    run_social_school,
    run_life_sciences_school,
    run_veterinary_medicine_school,
    run_pharmacy_school,
    run_convergence_science_school,
    run_medicine_school,
    run_humanities_school,
    run_natural_sciences_school,
    run_electronics_information_school,
    run_menu,
    sync_db_to_es
)

# 로그 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


if __name__ == '__main__':
    scheduler = BlockingScheduler({'apscheduler.timezone':'Asia/Seoul'})

    scheduler.add_job(run_business_school, 'cron', hour=0, minute=0, id='business_school')
    scheduler.add_job(run_engineering_school, 'cron', hour=0, minute=20, id='engineering_school')
    scheduler.add_job(run_public, 'cron', hour=0, minute=40, id='public')
    scheduler.add_job(run_agriculture_school, 'cron', hour=1, minute=0, id='agriculture_school')
    scheduler.add_job(run_education_school, 'cron', hour=1, minute=20, id='education_school')
    scheduler.add_job(run_social_school, 'cron', hour=1, minute=40, id='social_school')
    scheduler.add_job(run_life_sciences_school, 'cron', hour=2, minute=0, id='life_sciences_school')
    scheduler.add_job(run_veterinary_medicine_school, 'cron', hour=2, minute=20, id='veterinary_medicine_school')
    scheduler.add_job(run_pharmacy_school, 'cron', hour=2, minute=40, id='pharmacy_school')
    scheduler.add_job(run_convergence_science_school, 'cron', hour=3, minute=0, id='convergence_science_school')
    scheduler.add_job(run_medicine_school, 'cron', hour=3, minute=20, id='medicine_school')
    scheduler.add_job(run_humanities_school, 'cron', hour=3, minute=40, id='humanities_school')
    scheduler.add_job(run_natural_sciences_school, 'cron', hour=4, minute=0, id='natural_sciences_school')
    scheduler.add_job(run_electronics_information_school, 'cron', hour=4, minute=20, id='electronics_information_school')

    # DB -> ES 동기화 작업
    scheduler.add_job(sync_db_to_es, 'cron', hour=4, minute=40, id='sync_db_to_es')

    # 메뉴 크롤링은 매주 토요일에만 실행
    scheduler.add_job(run_menu, 'cron', day_of_week='sat', hour=12, minute=0, id='menu')
    
    logging.info('스케줄러 시작')
    scheduler.start()
