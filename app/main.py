import pandas as pd
import streamlit as st
from load import load_data


def ingest_to_df():
    df = pd.DataFrame(load_data())
    
    return df

def list_of_stations():
    return ["O'Hare", 'Rosemont', 'Cumberland', "Harlem (O'Hare Branch)",
            "Jefferson Park", "Montrose", 'Irving Park', 'Addison', 'Belmont',
            'Logan Square', 'California', "Western (O'Hare Branch)", 'Damen', 'Division',
            'Chicago', 'Grand', 'Clark/Lake', 'Washington', 'Monroe', 'Jackson',
            'LaSalle', 'Clinton', 'UIC-Halsted', 'Racine', 'Illinois Medical District',
            'Western (Forest Park Branch)', 'Kedzie-Homan', 'Pulaski', 'Cicero', 'Austin',
            'Oak Park', 'Harlem (Forest Park Branch)', 'Forest Park'
            ]

ingest_to_df()