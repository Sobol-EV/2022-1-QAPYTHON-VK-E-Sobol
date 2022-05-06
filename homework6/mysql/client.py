import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from models.models import Base


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = 3306
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name
        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):

        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        print(url)
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table_total_requests(self):
        if not inspect(self.engine).has_table('total_requests'):
            Base.metadata.tables['total_requests'].create(self.engine)

    def create_table_total_method_count(self):
        if not inspect(self.engine).has_table('total_method_count'):
            Base.metadata.tables['total_method_count'].create(self.engine)

    def create_table_total_url_count(self):
        if not inspect(self.engine).has_table('total_url_count'):
            Base.metadata.tables['total_url_count'].create(self.engine)

    def create_table_top_size_requests_400(self):
        if not inspect(self.engine).has_table('top_size_requests_400'):
            Base.metadata.tables['top_size_requests_400'].create(self.engine)

    def create_table_top_user_count_500(self):
        if not inspect(self.engine).has_table('top_user_count_500'):
            Base.metadata.tables['top_user_count_500'].create(self.engine)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
