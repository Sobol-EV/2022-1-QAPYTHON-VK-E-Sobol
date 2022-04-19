import pytest

from base import BaseApi
from generators.campaing_json_generator import CampaingJson


class TestCampaing(BaseApi):

    @pytest.mark.API
    def test_campaing_create(self):
        """Checking Campaign Creation and Deletion"""
        campaing_json = CampaingJson(*self.upload_file_banner(
            'files/campaign/240x400.png'
        )).build()
        id_campaign = self.create_campaign(campaing_json)
        self.check_campaign(id_campaign, 'active')
        self.delete_campaign_by_id(id_campaign)


class TestSegments(BaseApi):

    @pytest.mark.API
    def test_segments_create(self, default_segments_json):
        """Checking Segment Creation"""
        id_segment = self.create_segment(default_segments_json)
        self.check_segment(id_segment)
        self.delete_segment_by_id(id_segment)

    @pytest.mark.API
    def test_segment_delete(self, default_segments_json):
        """Checking Segment Deletion"""
        id_segment = self.create_segment(default_segments_json)
        self.delete_segment_by_id(id_segment)
        self.check_segment(id_segment, True)
