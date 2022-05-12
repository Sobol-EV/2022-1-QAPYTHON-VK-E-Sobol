import json

import pytest

from mock.flask_mock import (
    LAST_NAME_DATA,
    ID_DATA,
)
from generators.builder import MockData


class SocketBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client, logger):
        self.builder = MockData()
        self.socket_client = client
        self.logger = logger

    def create_user(self):
        data = self.builder.build()
        user_id = data['user_id']
        first_name = data['first_name']
        last_name = data['last_name']
        new_last_name = data['new_last_name']
        user_data = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'new_last_name': new_last_name,
        }
        return user_data

    def add_user(self, first_name, user_id):
        ID_DATA[first_name] = user_id
        data_response = self.socket_client.post_request(name=first_name)
        self.logger.info(json.dumps(
            self.log_writer(
                data_response=data_response,
                response='POST'
            )
        ))

        return data_response

    def last_name_for_user(self, first_name, last_name):
        LAST_NAME_DATA[first_name] = last_name
        data_response = self.socket_client.get_request(name=first_name)
        self.logger.info(json.dumps(
            self.log_writer(
                data_response=data_response,
                response='GET'
            )
        ))

        return data_response

    def change_last_name_for_user(self, first_name, old_last_name, new_last_name):
        LAST_NAME_DATA[first_name] = old_last_name
        data_response = self.socket_client.put_request(
            name=first_name, new_last_name=new_last_name
        )
        self.logger.info(json.dumps(
            self.log_writer(
                data_response=data_response,
                response='PUT'
            )
        ))

        return data_response

    def delete_user(self, first_name):
        data_response = self.socket_client.delete_request(name=first_name)
        self.logger.info(json.dumps(
            self.log_writer(
                data_response=data_response,
                response='DELETE'
            )
        ))

        return data_response

    @staticmethod
    def log_writer(data_response, response):
        data_log = {}
        data_log.update({'Response': response})
        data_log.update({'Response Code': data_response[0].split(' ', maxsplit=1)[1]})
        for i in range(1, len(data_response) - 2):
            data_log.update({
                data_response[i].split(':')[0]: data_response[i].split(':')[1]
            })
        data_log.update({
            'Response Body': json.loads(data_response[-1])
        })
        return data_log

