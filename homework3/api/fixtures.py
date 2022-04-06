import pytest

from generators.campaing_json_generator import CampaingJson
from generators.segments_json_generator import SegmentsJson


@pytest.fixture
def default_campaing_json():
    return CampaingJson().build()


@pytest.fixture()
def default_segments_json():
    return SegmentsJson().build()
