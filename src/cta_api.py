import os
import requests
from typing import List, Dict, ClassVar
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class QueryLines:
    '''
        station ID: number associate with train station
        method: arrival/follow;
                arrival--check train arrival at specific station,
                follow--info about a specific train

    "L" routes (rapid transit train services) are identified as follows:
    • Red = Red Line (Howard-95th/Dan Ryan service)
    • Blue = Blue Line (O'Hare-Forest Park service)
    • Brn = Brown Line (Kimball-Loop service)
    • G = Green Line (Harlem/Lake-Ashland/63rd-Cottage Grove service)
    • Org = Orange Line (Midway-Loop service)
    • P = Purple Line (Linden-Howard shuttle service)
    • Pink = Pink Line (54th/Cermak-Loop service)
    • Y = Yellow Line (Skokie-Howard [Skokie Swift] shuttle service)
    '''
    api_key: ClassVar[str] = os.getenv('api_key')
    line: str = 'blue'

    def __post_init__(self):
        '"line" keyword check'
        self.line = self.line.lower()
        if self.line not in ['blue', 'red', 'brn', 'g', 'org', 'p', 'pink', 'y']:
            raise ValueError('Not a correct CTA L line')

        return None

    def query_api(self):
        ''' query the api by either target station info or
            follow trains
            return data in json format
        '''
        resp = requests.get(
            'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?' +
            f'key={self.api_key}&rt={self.line}&outputType=JSON',
            timeout=10
            )
        # check invalid api key error
        if resp.json()['ctatt']['errNm'] == "Invalid API key.":
            raise ValueError('Invalid API key')
        return resp.json()

    def api_output(self) -> List[Dict]:

        ''' fields of interests:
            prdt--date/time: when internal prediction was generated
            arrT--date/time: when train is expected to arrive/depart
            isApp--boolean that train tracker is now declaring "approaching/due"
            isDly--boolean flag to indicate whether train is late

        '''

        api_response = self.query_api()

        # time when response was received
        current_Time = api_response['ctatt']['tmst']

        # unpack API response
        fields = []
        for pred in api_response['ctatt']['route'][0]['train']:
            # nested json data, locate all active trains
            # on the blue line
            pred['resp_time'] = current_Time
            fields.append(pred)

        return fields


if __name__ == '__main__':
    None


'''
to do:
    -implement logging: https://cloud.google.com/logging/docs/setup/python
    https://stackoverflow.com/questions/74302649/log-to-cloud-logging-with-correct-severity-from-cloud-run-job-and-package-used-i


'''