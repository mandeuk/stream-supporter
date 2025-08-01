import mysql.connector #모듈 설치 필요 : pip install mysql-connector-python
import json
from datetime import datetime

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
cnx_pool = None

async def connect_db():
    """데이터베이스 연결을 설정하고 연결 풀을 초기화합니다."""
    global cnx_pool
    try:
        cnx_pool = MySQLConnectionPool(pool_name="discord_bot", pool_size=10, **DB_CONFIG)
        print("데이터베이스 연결 성공!")
        # Ensure the table exists
        await create_chzzk_stream_status_table()
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 오류: {err}")
        # Consider more robust error handling or retry mechanism
        # For now, re-raising to prevent further operations on a failed connection
        raise

async def create_chzzk_stream_status_table():
    connection = None
    cursor = None
    try:
        connection = cnx_pool.get_connection()
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS chzzk_stream_status (
            channel_id VARCHAR(255) PRIMARY KEY,
            is_live BOOLEAN NOT NULL,
            last_notified_at DATETIME,
            discord_channel_id VARCHAR(255)
        );
        """
        cursor.execute(query)
        connection.commit()
        print("Table 'chzzk_stream_status' checked/created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

async def get_chzzk_stream_status(chzzk_channel_id: str):
    connection = None
    cursor = None
    try:
        connection = cnx_pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT channel_id, is_live, last_notified_at, discord_channel_id
        FROM chzzk_stream_status
        WHERE channel_id = %s;
        """
        cursor.execute(query, (chzzk_channel_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"Error getting Chzzk stream status: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

async def update_chzzk_stream_status(chzzk_channel_id: str, is_live: bool, discord_channel_id: str, last_notified_at: datetime = None):
    connection = None
    cursor = None
    try:
        connection = cnx_pool.get_connection()
        cursor = connection.cursor()
        if last_notified_at:
            query = """
            INSERT INTO chzzk_stream_status (channel_id, is_live, last_notified_at, discord_channel_id)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                is_live = VALUES(is_live),
                last_notified_at = VALUES(last_notified_at),
                discord_channel_id = VALUES(discord_channel_id);
            """
            cursor.execute(query, (chzzk_channel_id, is_live, last_notified_at, discord_channel_id))
        else:
            query = """
            INSERT INTO chzzk_stream_status (channel_id, is_live, discord_channel_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                is_live = VALUES(is_live),
                discord_channel_id = VALUES(discord_channel_id);
            """
            cursor.execute(query, (chzzk_channel_id, is_live, discord_channel_id))
        connection.commit()
        print(f"Chzzk stream status for {chzzk_channel_id} updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating Chzzk stream status: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

#memo aiomysql로 변경해야 할듯