from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class TotalRequestsModel(Base):

    __tablename__ = 'total_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalRequests: id={self.id}, total_requests={self.total_requests}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_requests = Column(Integer, nullable=False)


class TotalMethodCountModel(Base):

    __tablename__ = 'total_method_count'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalMethodCount: id={self.id}, GET={self.GET}," \
               f" POST={self.POST}, PUT={self.PUT}, HEAD={self.HEAD}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    GET = Column(Integer, nullable=False)
    POST = Column(Integer, nullable=False)
    PUT = Column(Integer, nullable=False)
    HEAD = Column(Integer, nullable=False)


class TotalUrlCountModel(Base):
    __tablename__ = 'total_url_count'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):

        return f"<TotalUrlCount: id={self.id}, url={self.url}, request_count={self.request_count}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    request_count = Column(Integer, nullable=False)


class TopSizeRequests400Model(Base):
    __tablename__ = 'top_size_requests_400'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalUrlCount: id={self.id}, url={self.url}," \
               f" request_size={self.request_size}, status_code={self.status_code}," \
               f" ip={self.ip}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    request_size = Column(Integer, nullable=False)
    status_code = Column(String(3), nullable=False)
    ip = Column(String(15), nullable=False)


class TopUserCount500Model(Base):
    __tablename__ = 'top_user_count_500'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopUserCount500: id={self.id}, ip={self.ip}, request_count={self.request_count}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    request_count = Column(Integer, nullable=False)
