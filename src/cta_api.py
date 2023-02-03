from __future__ import absolute_import
import requests
import os
import csv
import datetime as dt
from dataclasses import dataclass
from typing import List, Dict
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
        
        if self.method=='arrival':
            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?'\
                                f'key={apiKey}'\
                                f'&max=10&mapid={self.stationID}&outputType=JSON',
                                )
            return resp.json()
        
        if self.method=='follow':

            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0.b/ttfollow.aspx?'\
                                f'key={apiKey}'\
                                f'&runnumber={run_num}&outputType=JSON',
                                )
            return resp.json()

        if self.method=='blueline':
            
            resp = requests.get(f'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?'\
                                f'key={apiKey}&rt=blue&outputType=JSON'
                                )
            
            return resp.json()
        
    
    def method_response(self) -> List[Dict]:
        
        ''' fields of interests: prdt--date/time: when internal prediction was generated
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


def write_to_local(dict_data: List[Dict],
                   write_to=None):
    ''' for option to output a csv file in local disk,
        mostly for testing output purpose
    '''
    
    # type check
    if type(dict_data) is not list:
        raise TypeError('data is not in list format')
    
    # current time
    curr_time = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    
    keys = [i for s in [d.keys() for d in dict_data] for i in s]
    
    if write_to is None:
        write_to = os.getcwd()+'/example_data/'
    
    with open(write_to+curr_time+'.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, restval='-',
                                        fieldnames=keys, delimiter=',')
        dict_writer.writeheader()
        dict_writer.writerows(dict_data)

def main():
    
    print(TrainStop(method='blueline').method_response())

if __name__ == '__main__':
    main()
