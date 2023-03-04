from cta_api import TrainStop
from data_to_bq import StoreToDB

def main():
    data = TrainStop(method='blueline').method_response()
    StoreToDB().upload_data(data=data)
    
main()
print('trigger workflow')
