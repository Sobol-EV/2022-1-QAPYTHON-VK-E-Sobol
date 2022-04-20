import allure
import pytest

from generators.builder_base import BuilderBase
from generators.campaing_json_generator import AddMediatekaJson
import api.error_classes as error_cls


class BaseApi:

    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.authorize()

    @allure.step("Campaign Creation")
    def create_campaign(self, payload, delete=False):
        response = self.api_client.post_campaign_create(payload)
        id_campaign = response['id']
        if delete:
            self.delete_campaign_by_id(id_campaign)
        return id_campaign

    def change_status_campaign_by_id(self, id_campaign, campaign_status_json):
        with allure.step(f"Campaign status changed to {campaign_status_json['status']}"):
            self.api_client.post_campaign_change_status(id_campaign, campaign_status_json)

    def delete_campaign_by_id(self, id_campaign):
        self.change_status_campaign_by_id(id_campaign, BuilderBase().update_inner_value("status", "deleted").build())
        self.check_campaign(id_campaign, 'deleted')

    @allure.step('Create a segment')
    def create_segment(self, payload, delete=False):
        response = self.api_client.post_create_segments(payload)
        id_segments = response['id']
        if delete:
            self.delete_segment_by_id(id_segments)
            return

        return id_segments

    @allure.step('Deleting a segment')
    def delete_segment_by_id(self, id_segment):
        self.api_client.delete_segments(id_segment)
        self.check_segment(id_segment, True)

    def check_campaign(self, id_campaign, status):
        try:
            response = self.api_client.get_info_campaign_by_id(id_campaign)
            with allure.step("Checking for the existence of a campaign with id"):
                assert response['id'] == id_campaign, \
                    f"Campaign with id {id_campaign} does not exist"
            with allure.step("Checking campaign status"):
                assert response['status'] == status, \
                    f"Campaign status should be {status}"
        except error_cls.ResponseStatusCodeException:
            raise Exception(f"There is no campaign with this id ({id_campaign})")

    def check_segment(self, id_segment, deleted=False):
        try:
            response = self.api_client.get_info_segment_by_id(id_segment)
            with allure.step(f"Checking for the existence of a segment with an id {id_segment}"):
                assert isinstance(response['items'], list), \
                    f"Segment ID does not match {id_segment}"
        except error_cls.ResponseStatusCodeException:
            if deleted:
                with allure.step(f"Segment deletion check"):
                    return
            raise Exception(f"There is no segment with this id ({id_segment})")

    def upload_file_banner(self, file_path: str, repo_root):
        id_content = self.api_client.post_upload_file(file_path, repo_root)['id']
        id_primary = self.api_client.post_add_to_mediateka(
            AddMediatekaJson()
            .set_content(id_content)
            .set_description(file_path.split('/')[-1])
            .build()
        )['id']
        return id_content, id_primary
