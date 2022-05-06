from models.models import (
    TotalRequestsModel,
    TopSizeRequests400Model,
    TotalUrlCountModel,
    TopUserCount500Model,
    TotalMethodCountModel,
)
from utils.parse import ParserLog


class MysqlBuilder:
    def __init__(self, client, log_file_path):
        self.client = client
        self.parser = ParserLog(log_file_path)
        self.log_result = self.parser.get_report()
        self.checksums = self.parser.get_checksums_report()

    def create_total_requests(self):
        total_requests = TotalRequestsModel(
            total_requests=self.log_result[0]['total_request'],
        )
        self.client.session.add(total_requests)
        self.client.session.commit()

        return total_requests

    def create_total_method_count(self):
        value = self.log_result[1]
        total_method_count = TotalMethodCountModel(
            GET=value['GET'],
            POST=value['POST'],
            PUT=value['PUT'],
            HEAD=value['HEAD'],
        )
        self.client.session.add(total_method_count)
        self.client.session.commit()

        return total_method_count

    def create_total_url_count(self):
        result = []
        value = self.log_result[2]
        for i in value.keys():
            total_url_count = TotalUrlCountModel(
                url=i,
                request_count=value[i],
            )
            self.client.session.add(total_url_count)
            result.append(total_url_count)

        self.client.session.commit()
        return result

    def create_top_size_requests_400(self):
        result = []
        value = self.log_result[3]
        for i in value.keys():
            top_size_requests_400 = TopSizeRequests400Model(
                ip=i,
                url=value[i][2],
                request_size=value[i][0],
                status_code=value[i][1],
            )
            self.client.session.add(top_size_requests_400)
            result.append(top_size_requests_400)

        self.client.session.commit()
        return result

    def create_top_user_count_500(self):
        result = []
        value = self.log_result[4]
        for i in value.keys():
            top_user_count_500 = TopUserCount500Model(
                ip=i,
                request_count=value[i],
            )
            self.client.session.add(top_user_count_500)
            result.append(top_user_count_500)

        self.client.session.commit()
        return result
