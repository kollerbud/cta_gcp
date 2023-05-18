from __future__ import absolute_import
import os
import datetime as dt
from dataclasses import dataclass
from typing import List, Dict
import requests
from dotenv import load_dotenv


load_dotenv()


@dataclass
class TrainStop:
    '''
        station ID: number associate with train station
        method: arrival/follow;
                arrival--check train arrival at specific station,
                follow--info about a specific train

    '''
    stationID: str = '40320'
    method: str = 'arrival'

    def __post_init__(self):
        # remind myself to use the right keywords
        if self.method not in ['arrival', 'follow', 'blueline']:
            raise ValueError('use "arrival", "follow", "blueline"')

    def query_api(self, run_num=None):
        ''' query the api by either target station info or
            follow trains
            return data in json format
        '''
        apiKey = os.getenv('api_key')
        resp = None

        if self.method == 'arrival':
            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?'\
                                f'key={apiKey}'\
                                f'&max=10&mapid={self.stationID}&outputType=JSON',
                                timeout=10
                                )

        if self.method == 'follow':

            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0.b/ttfollow.aspx?'\
                                f'key={apiKey}'\
                                f'&runnumber={run_num}&outputType=JSON',
                                timeout=10
                                )

        if self.method == 'blueline':

            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?'\
                                f'key={apiKey}&rt=blue&outputType=JSON',
                                timeout=10
                                )

        # check invalid api key error
        if resp.json()['ctatt']['errNm'] == "Invalid API key.":
            raise ValueError('Invalid API key')
        return resp.json()

    def method_response(self) -> List[Dict]:

        ''' fields of interests:
            prdt--date/time: when internal prediction was generated
            arrT--date/time: when train is expected to arrive/depart
            isApp--boolean that train tracker is now declaring "approaching/due"
            isDly--boolean flag to indicate whether train is late

        '''

        data = self.query_api()

        # time when response was received
        current_Time = data['ctatt']['tmst']

        fields = []
        for pred in data['ctatt']['route'][0]['train']:
            # nested json data, locate all active trains
            # on the blue line
            pred['resp_time'] = current_Time
            fields.append(pred)

        return fields


def main():
    '''
    main function
    '''
    return TrainStop(method='blueline').method_response()

if __name__ == '__main__':
    print(TrainStop(method='blueline').method_response())


'''
to do:
    -implement logging: https://cloud.google.com/logging/docs/setup/python
    https://stackoverflow.com/questions/74302649/log-to-cloud-logging-with-correct-severity-from-cloud-run-job-and-package-used-i


'''