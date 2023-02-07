from dotenv import load_dotenv
import os
import streamlit as st
from google.cloud import bigquery

load_dotenv()

def bq_data():
    '''
    read data from Bigquery
    '''
    client = bigquery.Client()
    
    
    