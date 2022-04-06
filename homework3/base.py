import allure
import pytest

from generators.builder_base import BuilderBase
from api.client import ResponseStatusCodeException


class BaseApi:

    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.authorize()

    @allure.step("Campaign Creation")
    def create_campaing(self, payload, delete=False):
        response = self.api_client.post_campaing_create(payload)
        id_campaing = response['id']
        self.check_campaing(id_campaing, 'active')
        if delete:
            self.delete_campaing_by_id(id_campaing)
        return id_campaing

    def change_status_campaing_by_id(self, id_campaing, campaing_status_json):
        with allure.step(f"Campaign status changed to {campaing_status_json['status']}"):
            self.api_client.post_campaing_change_status(
                id_campaing, campaing_status_json
            )

    def delete_campaing_by_id(self, id_campaing):
        self.change_status_campaing_by_id(
            id_campaing, BuilderBase().update_inner_value("status", "deleted").build())
        self.check_campaing(id_campaing, 'deleted')

    @allure.step('Create a segment')
    def create_segment(self, payload, delete=False):
        response = self.api_client.post_create_segments(payload)
        id_segments = response['id']
        self.check_segment(id_segments)
        if delete:
            self.delete_segment_by_id(id_segments)
            return

        return id_segments

    @allure.step('Deleting a segment')
    def delete_segment_by_id(self, id_segment):
        self.api_client.delete_segments(id_segment)
        self.check_segment(id_segment, True)

    def check_campaing(self, id_campaing, status):
        try:
            response = self.api_client.get_info_campaing_by_id(id_campaing)
            with allure.step("Checking for the existence of a campaign with id"):
                assert response['id'] == id_campaing, \
                    f"Campaign with id {id_campaing} does not exist"
            with allure.step("Checking campaign status"):
                assert response['status'] == status, \
                    f"Campaign status should be {status}"
        except ResponseStatusCodeException:
            raise Exception(f"There is no campaign with this id ({id_campaing})")

    def check_segment(self, id_segment, deleted=False):
        try:
            response = self.api_client.get_info_segment_by_id(id_segment)
            with allure.step(f"Checking for the existence of a segment with an id {id_segment}"):
                assert isinstance(response['items'], list), \
                    f"Segment ID does not match {id_segment}"
        except ResponseStatusCodeException:
            if deleted:
                with allure.step(f"Segment deletion check"):
                    return
            raise Exception(f"There is no segment with this id ({id_segment})")

