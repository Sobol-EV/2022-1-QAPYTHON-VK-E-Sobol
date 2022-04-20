import pytest

from generators.segments_json_generator import SegmentsJson


@pytest.fixture()
def default_segments_json():
    return SegmentsJson().build()
