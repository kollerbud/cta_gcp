from dotenv import load_dotenv
from collections import defaultdict
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime, timedelta


load_dotenv()


def load_data(week=1):
    '''
    read data from Bigquery,
    query for week to now data
    return data in a dictionary format
    '''
    secrets = {}
    for i in ['type', 'project_id', 'private_key_id', 'private_key',
              'client_email', 'client_id', 'auth_uri', 'token_uri',
              'auth_provider_x509_cert_url', 'client_x509_cert_url']:
        secrets[i] = os.getenv(i)

    cred = service_account.Credentials.from_service_account_info(secrets)

    client = bigquery.Client(credentials=cred)

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