import pytest
import os
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder
from models.models import (
    TotalRequestsModel,
    TopSizeRequests400Model,
    TotalUrlCountModel,
    TopUserCount500Model,
    TotalMethodCountModel,
)


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, repo_root):
        self.mysql: MysqlClient = mysql_client
        file_path = os.path.join(repo_root, "files/access.log")
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql, file_path)

        self.prepare()

    def get_total_requests(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TotalRequestsModel).filter_by(**filters)
        return res.all()

    def get_total_method_counts(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TotalMethodCountModel).filter_by(**filters)
        return res.all()

    def get_total_url_counts(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TotalUrlCountModel).filter_by(**filters)
        return res.all()

    def get_top_size_requests_400(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TopSizeRequests400Model).filter_by(**filters)
        return res.all()

    def get_top_user_count_500(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TopUserCount500Model).filter_by(**filters)
        return res.all()


class TestMySql(MyTest):

    def prepare(self):
        pass

    def test_total_requests(self):
        self.builder.create_total_requests()
        count = self.get_total_requests()
        assert len(count) == self.builder.checksums[0]

    def test_total_method_count(self):
        self.builder.create_total_method_count()
        count = self.get_total_method_counts()
        assert count

    def test_total_url_count(self):
        self.builder.create_total_url_count()
        count = self.get_total_url_counts()
        assert len(count) == self.builder.checksums[2]

    def test_top_size_requests_400(self):
        self.builder.create_top_size_requests_400()
        count = self.get_top_size_requests_400()
        assert len(count) == self.builder.checksums[3]

    def test_top_user_count_500(self):
        self.builder.create_top_user_count_500()
        count = self.get_top_user_count_500()
        assert len(count) == self.builder.checksums[4]
