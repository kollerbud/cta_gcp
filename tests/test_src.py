import pytest
import sys
sys.path.append('../cta_gcp/src')
from cta_api import QueryLines
from data_to_bq import StoreToBQ


def test_api_output():
    # test fields return from API call

    # blueline fields
    blue = QueryLines(line='blue').api_output()

    assert list(blue[0].keys()) == ['rn', 'destSt', 'destNm', 'trDr',
                                    'nextStaId', 'nextStpId', 'nextStaNm',
                                    'prdt', 'arrT', 'isApp', 'isDly', 'flags',
                                    'lat', 'lon', 'heading', 'resp_time']


def test_bq_table():
    # make sure table already exist when try to create table
    with pytest.raises(Exception):
        StoreToBQ().create_table(table_name='blue')
