from 한빛식당 import restaurant_hanbit
from 별빛식당 import restaurant_byulbit
from 은하수식당 import restaurant_eunhasu


import pymysql, json
# DB 설정 데이터 가져오기
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    driver_path = config['driver_path']
    hosturl = config['host']
    username = config['username']
    userpassword = config['password']
    dbname = config['db2']

table_N = 'menus'

# MariaDB 연결
db_connection = pymysql.connect(host=hosturl, user=username, password=userpassword, db=dbname, charset='utf8')
cursor = db_connection.cursor()


if __name__ == "__main__":
    restaurants = [restaurant_hanbit,restaurant_byulbit,restaurant_eunhasu]

    for  restaurant in restaurants:
        menus =restaurant.run()
        for menu in menus:
            try:
                # 데이터베이스에 저장
                sql = f"INSERT INTO {table_N} (restaurantId, restaurant_name ,menu, time, date) VALUES (%s, %s, %s, %s, %s)"
                values = (menu['restaurantId'], menu['restaurant_name'], menu['menu'], menu['time'], menu['date'])
                cursor.execute(sql, values)
                db_connection.commit()
                print(f"Data inserted successfully: title={menu['restaurant_name']}, site={menu['date']}")

            except pymysql.Error as e:
                print(f"Error {e.args[0]}, {e.args[1]}")
                db_connection.rollback()

    # WebDriver 및 DB 연결 닫기
    db_connection.close()
    print("학식 작업 완료.")