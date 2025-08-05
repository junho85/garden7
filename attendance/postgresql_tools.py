import configparser
import os
import psycopg2
from psycopg2.extras import RealDictCursor


class PostgreSQLTools:
    def __init__(self):
        config = configparser.ConfigParser()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, 'config.ini')
        config.read(path)

        self.pg_database = config['DATABASE']['DATABASE']
        self.pg_host = config['DATABASE']['HOST']
        self.pg_port = config['DATABASE']['PORT']
        self.pg_user = config['DATABASE']['USER']
        self.pg_password = config['DATABASE']['PASSWORD']
        self.pg_schema = config['DATABASE']['SCHEMA']

    def connect_db(self):
        """PostgreSQL 연결 생성"""
        conn = psycopg2.connect(
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_database,
            user=self.pg_user,
            password=self.pg_password,
            sslmode='require',
            gssencmode='disable'  # GSSAPI 오류 해결
        )
        return conn

    def get_cursor(self, conn=None):
        """커서 반환 (자동으로 스키마 설정)"""
        if conn is None:
            conn = self.connect_db()
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(f"SET search_path TO {self.pg_schema}")
        return cursor, conn

    def execute_query(self, query, params=None, fetch_all=True):
        """쿼리 실행 후 결과 반환"""
        cursor, conn = self.get_cursor()
        try:
            cursor.execute(query, params)
            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            return result
        finally:
            cursor.close()
            conn.close()

    def execute_insert(self, query, params=None):
        """INSERT/UPDATE/DELETE 쿼리 실행"""
        cursor, conn = self.get_cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()