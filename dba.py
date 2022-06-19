import psycopg2

from const import CONNECTION_STRING

"""singleton class to deal with db"""
'''same can be use for pymysql just replace the sqlite3 with pymysql'''


class DBConnection:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DBConnection)
            return cls.instance
        return cls.instance

    def __init__(self, db_name='you-db-name'):
        self.name = db_name
        # connect takes url, dbname, user-id, password
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            from sqlalchemy import create_engine

            # return psycopg2.connect(CONNECTION_STRING)
            return create_engine(CONNECTION_STRING)
        except psycopg2.Error as e:
            pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()


# db = SQLAlchemy(
#     engine_options={
#         "pool_pre_ping": True
#     }
# )
