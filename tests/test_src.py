import pytest
import sys
sys.path += ['../cta_gcp']
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


@pytest.mark.parametrize('param', ['random', 547, None])
def test_api_incorr_var(param):
    # test if incorrect inputs are caught
    with pytest.raises(ValueError):
        TrainStop(method=param)


def test_bq_table():
    # make sure table already exist when try to create table
    with pytest.raises(Exception):
        StoreToDB().create_table()
