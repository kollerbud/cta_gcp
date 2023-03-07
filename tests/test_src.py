import pytest
import sys
sys.path.append('/workspaces/cta_gcp')
from src.cta_api import TrainStop
from src.data_to_bq import StoreToDB


def test_api_output():
    # test fields return from API call

    # blueline fields
    blue = TrainStop(method='blueline').method_response()

    assert list(blue[0].keys()) == ['rn', 'destSt', 'destNm', 'trDr',
                            'nextStaId', 'nextStpId', 'nextStaNm',
                            'prdt', 'arrT', 'isApp', 'isDly', 'flags',
                            'lat', 'lon', 'heading', 'resp_time']


def test_bq_table():
    # make sure table already exist when try to create table
    with pytest.raises(Exception):
        StoreToDB().create_table()


def test_branch():
    assert 1==1