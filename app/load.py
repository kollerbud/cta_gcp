from dotenv import load_dotenv
from collections import defaultdict
from google.cloud import bigquery
import os
from datetime import datetime, timedelta


load_dotenv()


def load_data(week=1):
    '''
    read data from Bigquery,
    query for week to now data
    return data in a dictionary format
    '''
    client = bigquery.Client(project=os.getenv('project_name'))

    # query statement
    query_string = '''
                    SELECT rn, destNm, nextStaNm, prdt, arrT, lat, lon, resp_time, isApp, isDly
                    FROM line_stops.blue
                    WHERE resp_time BETWEEN @monday and @current
                    ORDER BY resp_time DESC
                    ;
                    '''
    # define Monday and Friday of the week
    
    now = datetime.now()
    back_days = week * 7
    m = now - timedelta(days=back_days)
    # modify sql query
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('monday', 'DATETIME', m),
            bigquery.ScalarQueryParameter('current', 'DATETIME', now)
        ]
    )

    rows = client.query(query=query_string, job_config=job_config)
    # organize return rows into usage dict format
    data_dict = defaultdict(list)
    for row in rows:
        for key in row.keys():
            data_dict[key] += [row[key]]

    return dict(data_dict)


def main():

    return load_data()

if __name__ == '__main__':
    print(main())