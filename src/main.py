from cta_api import QueryLines
from data_to_bq import StoreToBQ


def main():
    blue_line_data = QueryLines(line='blue').api_output()
    red_line_data = QueryLines(line='red').api_output()
    StoreToBQ().upload_data(data=blue_line_data, table_name='blue')
    StoreToBQ().upload_data(data=red_line_data, table_name='red')
    
main()
