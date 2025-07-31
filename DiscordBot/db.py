import mysql.connector #모듈 설치 필요 : pip install mysql-connector-python
import json

from mysql.connector.pooling import MySQLConnectionPool

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

# 커넥션 풀
cnx_pool = None #MySQLConnectionPool(pool_name="discord_bot", pool_size=10, **DB_CONFIG)

# MySQL 데이터베이스에 연결
async def connect_db():
    """데이터베이스 연결을 설정하고 연결 객체를 반환합니다."""
    try:
        # cnx = await mysql.connector.connect(**DB_CONFIG)
        cnx_pool = await MySQLConnectionPool(pool_name="discord_bot", pool_size=10, **DB_CONFIG)
        print("데이터베이스 연결 성공!")
        # return cnx
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 오류: {err}")
        return connect_db()
        # return None
    
async def record_channel_id(id: str):
    connection: mysql.connector.MySQLConnection = None
    cursor = None
    try:
        connection = cnx_pool.get_connection()
        cursor = connection.cursor()
        query = '''

                '''
        
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close() #풀로 반환됨
    


#memo aiomysql로 변경해야 할듯