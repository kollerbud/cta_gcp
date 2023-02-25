import datetime
import pandas as pd
import streamlit as st
from load import load_data


pd.options.mode.chained_assignment = None


@st.cache_data
def raw_data() -> pd.DataFrame:
    '''
    this step is to load data from bigquery
    data should be all arriving trains to stations on Wednesday & Thursday
    of THIS week
    caching to reduce Bigquery usage
    '''
    print('running bq raw data')
    return pd.DataFrame(load_data())


def ingest_df(station=None) -> pd.DataFrame:
    '''
    select columns of interest and staging for particular stations
    '''
    # load data from cache
    df = raw_data()
    # remove extra columns
    df = df.loc[:, ['rn', 'destNm', 'nextStaNm',
                    'arrT', 'isApp',
                    ]
                ]
    # return only when the train is approaching station
    df = df.query('`isApp`=="1" & `nextStaNm`==@station')
    # re-define destination to NW & W, since not all route
    # goes to the end
    df.loc[:, 'destNm'] = df.loc[:, 'destNm'].map(
                             {"O'Hare": 'NW',
                              'Forest Park': 'W',
                              'UIC-Halsted': 'NW',
                              })

    return df.reset_index(drop=True)


def arrival_freq(station):
    '''
    rewrite this as a decorator function
    '''
    # ingested data
    _df = ingest_df(station=station)

    # groupby dataframe by arrival time every 10mins
    df_group = _df.groupby([pd.Grouper(key='arrT', freq='10min'), 'destNm'],
                           as_index=False)['isApp'].size()

    # split into morning and afternoon
    df_morning = df_group.loc[
        (df_group['arrT'].dt.time >= datetime.time(hour=8)) &
        (df_group['arrT'].dt.time <= datetime.time(hour=10))
    ].sort_values(by=['destNm', 'arrT'], ascending=[True, False])

    df_afternoon = df_group.loc[
        (df_group['arrT'].dt.time >= datetime.time(hour=16)) &
        (df_group['arrT'].dt.time <= datetime.time(hour=18))
    ].sort_values(by=['destNm', 'arrT'], ascending=[True, False])

    # remove dates in both morning and afternoon dataframe
    df_morning['timeNoDate'] = df_morning['arrT'].dt.time
    df_morning = (df_morning.groupby(by=['timeNoDate', 'destNm'],
                                     as_index=False)['size'].sum()
                  )

    df_afternoon['timeNoDate'] = df_afternoon['arrT'].dt.time
    df_afternoon = (df_afternoon.groupby(by=['timeNoDate', 'destNm'],
                                         as_index=False)['size'].sum()
                    )
    # last step, sort values
    df_morning.sort_values(by=['destNm', 'timeNoDate'], inplace=True)
    df_afternoon.sort_values(by=['destNm', 'timeNoDate'], inplace=True)

    return {'morning': df_morning,
            'afternoon': df_afternoon,
            }


list_of_stations = ["O'Hare", 'Rosemont', 'Cumberland',
                    "Harlem (O'Hare Branch)",
                    "Jefferson Park", "Montrose", 'Irving Park', 'Addison',
                    'Belmont', 'Logan Square', 'California',
                    "Western (O'Hare Branch)", 'Damen', 'Division',
                    'Chicago', 'Grand', 'Clark/Lake', 'Washington', 'Monroe',
                    'Jackson', 'LaSalle', 'Clinton', 'UIC-Halsted', 'Racine',
                    'Illinois Medical District',
                    'Western (Forest Park Branch)',
                    'Kedzie-Homan', 'Pulaski', 'Cicero', 'Austin',
                    'Oak Park', 'Harlem (Forest Park Branch)', 'Forest Park'
                    ]

st.title('Looking for my blueline')


with st.sidebar:
    station_picked = st.multiselect(
        label='Pick a station to check arrival',
        #index=13,
        options=list_of_stations,
        max_selections=3
        )

df_station = (ingest_df(station=station_picked).
              sort_values(by=['destNm', 'arrT'], ascending=[True, False]))
st.dataframe(df_station)

# morning arrival information
st.dataframe(arrival_freq(station=station_picked)['morning'])

# afternoon arrival information
st.dataframe(arrival_freq(station=station_picked)['afternoon'])
