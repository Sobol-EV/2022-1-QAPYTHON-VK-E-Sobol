import pytest

from base import BaseApi


class TestCampaing(BaseApi):

    @pytest.mark.API
    def test_campaing_create(self, default_campaing_json):
        """Checking Campaign Creation and Deletion"""
        self.create_campaing(default_campaing_json, True)


class TestSegments(BaseApi):

    @pytest.mark.API
    def test_segments_create(self, default_segments_json):
        """Checking Segment Creation and Deletion"""
        self.create_segment(default_segments_json, True)
