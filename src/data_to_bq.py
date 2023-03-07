import os
import google
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
from typing import List


load_dotenv()


class StoreToDB:
    '''
        contains all database operation
        may expand to cloud db later
    '''

    def __init__(self) -> None:

        self.project_name = os.getenv('project_name')
        self.dataset_name = os.getenv('dataset_name')
        secrets = {}
        for i in ['type', 'project_id', 'private_key_id',
                  'client_email', 'client_id', 'auth_uri', 'token_uri',
                  'auth_provider_x509_cert_url', 'client_x509_cert_url']:

            secrets[i] = os.getenv(i)
            # need to clean up private_key
            secrets['private_key'] = os.getenv('private_key').replace('\\n', '\n')
        cred = service_account.Credentials.from_service_account_info(secrets)
        self.client = bigquery.Client(credentials=cred)

    def create_table(self):

        table_id = bigquery.Table.from_string(f'{self.project_name}.{self.dataset_name}.blue')

        schema = [
            bigquery.SchemaField('rn', 'STRING'),
            bigquery.SchemaField('destSt', 'STRING'),
            bigquery.SchemaField('destNm', 'STRING'),
            bigquery.SchemaField('trDr', 'STRING'),
            bigquery.SchemaField('nextStaId', 'STRING'),
            bigquery.SchemaField('nextStpId', 'STRING'),
            bigquery.SchemaField('nextStaNm', 'STRING'),
            bigquery.SchemaField('prdt', 'DATETIME'),
            bigquery.SchemaField('arrT', 'DATETIME'),
            bigquery.SchemaField('isApp', 'STRING'), # if use boolean then raw data should be converted
            bigquery.SchemaField('isDly', 'STRING'), # if use boolean then raw data should be converted
            bigquery.SchemaField('flags', 'STRING'),
            bigquery.SchemaField('lat', 'FLOAT'),
            bigquery.SchemaField('lon', 'FLOAT'),
            bigquery.SchemaField('heading', 'STRING'),
            bigquery.SchemaField('resp_time', 'DATETIME')
        ]
        table = bigquery.Table(table_id, schema=schema)

        # check if table have already existed
        try:
            table = self.client.create_table(table)
        except google.api_core.exceptions.Conflict:
            raise Exception('table already exists')

    def upload_data(self, data: List) -> None:

        table_id = bigquery.Table.from_string(f'{self.project_name}.'\
                                              f'{self.dataset_name}.blue'
                                              )
        rows_to_insert = data

        errors = self.client.insert_rows_json(table_id, rows_to_insert)

        if errors == []:
            print('new rows added')
        else:
            print(f'encounter error {errors}')


if __name__ == '__main__':
   print(StoreToDB().create_table())

