import mysql.connector #모듈 설치 필요 : pip install mysql-connector-python
import json

with open('config.json', 'r') as f:
    config = json.load(f)

# MySQL 서버 연결 정보
DB_CONFIG = {
    'host': config['database']['host'],
    'port' : config['database']['port'],
    'database' : config['database']['dbname'],
    'user' : config['database']['user'],
    'password' : config['database']['password']
}

# MySQL 데이터베이스에 연결
async def connect_db():
    """데이터베이스 연결을 설정하고 연결 객체를 반환합니다."""
    try:
        cnx = await mysql.connector.connect(**DB_CONFIG)
        print("데이터베이스 연결 성공!")
        return cnx
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 오류: {err}")
        return None
    
    

    



# 데이터베이스 커서 생성
# cursor = connection.cursor()

# def insert_data(name, age):
#     # 데이터 삽입 쿼리
#     query = "INSERT INTO users (name, age) VALUES (%s, %s)"
#     # 쿼리 실행
#     cursor.execute(query, (name, age))
#     # 변경 사항을 데이터베이스에 반영
#     connection.commit()

# # 데이터 삽입 예제
# name = 'John'
# age = 30
# insert_data(name, age)
