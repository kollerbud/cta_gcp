import pandas as pd
import streamlit as st
from load import load_data


st.cache_data()
def raw_data() -> pd.DataFrame:
    '''
    this step is to load data from bigquery
    data should be all arriving trains to stations on Wednesday & Thursday
    of THIS week
    caching to reduce Bigquery usage
    '''
    return pd.DataFrame(load_data())


def ingest_df(station=None) -> pd.DataFrame:
    '''
    '''

    # load data from cache
    df = raw_data()
    # remove extra columns
    df = df.loc[:, ['rn', 'destNM', 'nextStaNm',
                    'arrT', 'resp_time', 'isApp',
                    ]
                ]
    # return only when the train is approaching station
    df = df.query('`isApp`=="1" & `nextStaNm`==@station')
    return df


list_of_stations = ["O'Hare", 'Rosemont', 'Cumberland', "Harlem (O'Hare Branch)",
                    "Jefferson Park", "Montrose", 'Irving Park', 'Addison', 'Belmont',
                    'Logan Square', 'California', "Western (O'Hare Branch)", 'Damen', 'Division',
                    'Chicago', 'Grand', 'Clark/Lake', 'Washington', 'Monroe', 'Jackson',
                    'LaSalle', 'Clinton', 'UIC-Halsted', 'Racine', 'Illinois Medical District',
                    'Western (Forest Park Branch)', 'Kedzie-Homan', 'Pulaski', 'Cicero', 'Austin',
                    'Oak Park', 'Harlem (Forest Park Branch)', 'Forest Park'
                    ]

st.title('Looking for my blueline')


with st.sidebar:
    station_picked = st.selectbox(
        label='Pick a station to check arrival',
        index=13,
        options= list_of_stations,
        )

df_station = (ingest_df(station=station_picked).
              sort_values(by=['destNM', 'arrT'], ascending=[True, False]))
st.dataframe(df_station)