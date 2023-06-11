import os
import google
from dataclasses import dataclass
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
from typing import List, ClassVar
from cta_api import QueryLines


load_dotenv()


@dataclass
class StoreToBQ:
    '''
        contains all database operation
        may expand to cloud db later
    '''

    bq_client = None
    project_name: ClassVar[str] = os.getenv('project_name')
    dataset_name: ClassVar[str] = os.getenv('dataset_name')

    def __post_init__(self):
        'check if client secrects are available, if not then use default credentials'
        if os.getenv('private_key') is None:
            self.bq_client = bigquery.Client()

        self.bq_client = self._auth()

        return None

    def _auth(self):
        'authenticate Bigquery'
        secrets = {}
        for i in ['type', 'project_id', 'private_key_id',
                  'client_email', 'client_id', 'auth_uri', 'token_uri',
                  'auth_provider_x509_cert_url', 'client_x509_cert_url']:

            secrets[i] = os.getenv(i)
            # need to clean up private_key
        secrets['private_key'] = os.getenv('private_key').replace('\\n', '\n')
        cred = service_account.Credentials.from_service_account_info(secrets)

        client = bigquery.Client(credentials=cred)

        return client

    def create_table(self, table_name: str):

        # check table names
        table_name = table_name.lower()
        if table_name not in ['blue', 'red', 'brown', 'green',
                              'orange', 'purple', 'pink', 'yellow'
                              ]:
            raise KeyError("use table names match CTA's lines")

        table_id = bigquery.Table.from_string(
                   f'{self.project_name}.{self.dataset_name}.{table_name}'
                   )

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
            bigquery.SchemaField('isApp', 'STRING'),
            bigquery.SchemaField('isDly', 'STRING'),
            bigquery.SchemaField('flags', 'STRING'),
            bigquery.SchemaField('lat', 'FLOAT'),
            bigquery.SchemaField('lon', 'FLOAT'),
            bigquery.SchemaField('heading', 'STRING'),
            bigquery.SchemaField('resp_time', 'DATETIME')
        ]
        table = bigquery.Table(table_id, schema=schema)

        # check if table have already existed
        try:
            table = self.bq_client.create_table(table)
        except google.api_core.exceptions.Conflict:
            raise Exception('table already exists')

    def upload_data(self,
                    data: List[dict],
                    table_name: str) -> None:

        table_id = bigquery.Table.from_string(f'{self.project_name}.' +
                                              f'{self.dataset_name}.' +
                                              f'{table_name}'
                                              )

        rows_to_insert = data

        insert_errors = (self.bq_client
                         .insert_rows_json(table_id, rows_to_insert)
                         )

        if insert_errors == []:
            print('new rows added')
        else:
            print(f'encounter error {insert_errors}')


if __name__ == '__main__':
    data_to_upload = QueryLines(line='red').api_output()
    StoreToBQ().upload_data(data=data_to_upload, table_name='red')
