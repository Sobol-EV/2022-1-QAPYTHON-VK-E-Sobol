import pytest
import json
from socket_client.base import SocketBase


class TestEndpointPOST(SocketBase):

    @pytest.mark.Mock
    def test_checking_the_created_user(self):
        user_data = self.create_user()
        response = self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        assert (json.loads(response[-1])['user_id']) == str(user_data['user_id']), \
            "User UUID does not match"

    @pytest.mark.Mock
    def test_creating_an_existing_user(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        assert '400 BAD REQUEST' in response[0], \
            "Error code does not match"


class TestEndpointGET(SocketBase):

    @pytest.mark.Mock
    def test_successful_user_request(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.last_name_for_user(
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        assert json.loads(response[-1])['last_name'] == user_data['last_name'], \
            "Incorrect user"

    @pytest.mark.Mock
    def test_request_with_non_existent_name(self):
        user_data = self.create_user()
        non_existent_name = 'TEST_NAME'
        response = self.last_name_for_user(
            first_name=non_existent_name,
            last_name=user_data['last_name']
        )
        assert f'Username {non_existent_name} not found' in response[-1], \
            "Incorrect error message when trying to get a non-existent user!"

    @pytest.mark.Mock
    def test_request_without_last_name(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.last_name_for_user(
            first_name=user_data['first_name'],
            last_name=None
        )
        assert f'Last name for username ' \
               f'{user_data["first_name"]} not found' in response[-1], \
            "Incorrect error message when trying to get a user without a last name!"


class TestEndpointPUT(SocketBase):

    @pytest.mark.Mock
    def test_successful_last_name_change(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.change_last_name_for_user(
            first_name=user_data['first_name'],
            old_last_name=user_data['last_name'],
            new_last_name=user_data['new_last_name']
        )
        assert json.loads(response[-1]).get('last_name') == user_data['new_last_name'], \
            "Name change failed!"

    @pytest.mark.Mock
    def test_changing_non_existing_user(self):
        user_data = self.create_user()
        non_existent_name = 'TEST_NAME'
        response = self.change_last_name_for_user(
            first_name=non_existent_name,
            old_last_name=user_data['last_name'],
            new_last_name=user_data['new_last_name']
        )
        assert f'Username {non_existent_name} not found' in response[-1], \
            "Incorrect error message when trying to change a non-existent user!"

    @pytest.mark.Mock
    def test_last_name_changes_without_existing_old(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.change_last_name_for_user(
            first_name=user_data['first_name'],
            old_last_name=None,
            new_last_name=user_data['new_last_name']
        )
        assert f'Last name for username ' \
               f'{user_data["first_name"]} not found' in response[-1], \
            "Incorrect error message when trying to change without the old last name!"


class TestEndpointDELETE(SocketBase):

    @pytest.mark.Mock
    def test_successful_user_deletion(self):
        user_data = self.create_user()
        self.add_user(
            first_name=user_data['first_name'],
            user_id=user_data['user_id']
        )
        response = self.delete_user(first_name=user_data['first_name'])
        assert json.loads(response[-1]).get(user_data['first_name']) is None, \
            "Unsuccessful removal"

    @pytest.mark.Mock
    def test_deleting_non_existing_user(self):
        non_existent_name = 'TEST_NAME'
        response = self.delete_user(first_name=non_existent_name)
        assert f'Username {non_existent_name} not found' in response[-1], \
            "Incorrect error message when trying to delete a non-existent user!"

