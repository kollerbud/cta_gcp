import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from load import load_data


pd.options.mode.chained_assignment = None


@st.cache_data
def raw_data(weeks=1) -> pd.DataFrame:
    '''
    this step is to load data from bigquery
    data should be all arriving trains to stations on Wednesday & Thursday
    of THIS week
    caching to reduce Bigquery usage
    '''
    print('running bq raw data')
    return pd.DataFrame(load_data(week=weeks))


def ingest_df(num_weeks, station) -> pd.DataFrame:
    '''
    select columns of interest and staging for particular stations
    '''
    # load data from cache
    df = raw_data(weeks=num_weeks)
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


def arrival_freq(**kwargs) -> dict:
    '''
    rewrite this as a decorator function
    '''
    # ingested data
    _df = ingest_df(num_weeks=kwargs['weeks'],
                    station=kwargs['station'])

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
    df_morning['timeOnly'] = df_morning['arrT'].dt.time
    df_morning = (df_morning.groupby(by=['timeOnly', 'destNm'],
                                     as_index=False)['size'].sum()
                  )

    df_afternoon['timeOnly'] = df_afternoon['arrT'].dt.time
    df_afternoon = (df_afternoon.groupby(by=['timeOnly', 'destNm'],
                                         as_index=False)['size'].sum()
                    )
    # last step, sort values
    df_morning.sort_values(by=['destNm', 'timeOnly'], inplace=True)
    df_afternoon.sort_values(by=['destNm', 'timeOnly'], inplace=True)

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
    moring_station_picked = st.multiselect(
        label='morning commute station',
        options=list_of_stations,
        max_selections=3
        )
    afternoon_station_picked = st.multiselect(
        label='afternoon commute station',
        options=list_of_stations,
        max_selections=3
        )
    weeks_of_data = st.number_input(
        label='how many weeks of record to go back to?',
        min_value=1,
        max_value=3,
    )

    st.markdown('## About')
    st.write('''There is a limit on Bigquery query, so if data is not showing
                then we've probably hit the limit.
            ''')
    st.markdown('''More updates to come, 
                    check out my github [@kollerbud](https://github.com/kollerbud)'''
                )

# morning arrival information
morning = arrival_freq(weeks=weeks_of_data,
                       station=moring_station_picked)['morning']
# convert time to string for plotting
morning['timeOnly'] = morning['timeOnly'].astype(str)
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
ax1.set_title('NW bound')
ax1.bar(morning.loc[morning['destNm'] == 'NW', 'timeOnly'],
        morning.loc[morning['destNm'] == 'NW', 'size'])
ax1.set_xticklabels(morning['timeOnly'], rotation=90)
ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

ax2.set_title('W bound')
ax2.bar(morning.loc[morning['destNm'] == 'W', 'timeOnly'],
        morning.loc[morning['destNm'] == 'W', 'size'])
ax2.set_xticklabels(morning['timeOnly'], rotation=90)
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
st.pyplot(fig)


# afternoon arrival information
afternoon = arrival_freq(weeks=2,
                         station=afternoon_station_picked)['afternoon']
afternoon['timeOnly'] = afternoon['timeOnly'].astype(str)
fig, (ax3, ax4) = plt.subplots(nrows=1, ncols=2, sharey=True)
ax3.set_title('NW bound')
ax3.bar(afternoon.loc[afternoon['destNm'] == 'NW', 'timeOnly'],
        afternoon.loc[afternoon['destNm'] == 'NW', 'size'])
ax3.set_xticklabels(afternoon['timeOnly'], rotation=90)
ax3.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

ax4.set_title('W bound')
ax4.bar(afternoon.loc[afternoon['destNm'] == 'W', 'timeOnly'],
        afternoon.loc[afternoon['destNm'] == 'W', 'size'])
ax4.set_xticklabels(afternoon['timeOnly'], rotation=90)
ax4.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
st.pyplot(fig)

df_station = (ingest_df(num_weeks=weeks_of_data, station=moring_station_picked).
              sort_values(by=['destNm', 'arrT'], ascending=[True, False]))
st.dataframe(df_station)