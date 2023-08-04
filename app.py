# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

def generate_time_travel_df(current_active_bytes, data_change_rate, time_periods):
    time_travel_df = pd.DataFrame()
    for days in time_periods:
        time_travel_df[f'{days} days'] = current_active_bytes * (1 + data_change_rate) ** (days / 30)
    return time_travel_df


# Write directly to the app
st.title('Snowflake Time-Travel Scenario Analysis')


# Get the current credentials
session = get_active_session()


#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
df = session.table("snowflake.account_usage.table_storage_metrics").to_pandas()

selected_table = st.selectbox('Select the designated table', df['TABLE_NAME'])
current_active_bytes = df[df['TABLE_NAME'] == selected_table]['ACTIVE_BYTES'].values[0]
st.write(f'Current Active Bytes for {selected_table}: {current_active_bytes}')

data_change_rate = st.number_input('Enter the expected data change rate (decimal)', min_value=0.0, max_value=1.0, value=0.1, step=0.01)
time_periods = st.multiselect('Select time periods for analysis (in days)', list(range(1, 91)), [30, 60])

if len(time_periods) > 0:
    # Generate DataFrame with time-travel options
    time_travel_df = generate_time_travel_df(current_active_bytes, data_change_rate, time_periods)
    
    # Plot bar graph using Streamlit
    st.subheader(f'Time-Travel Scenario for {selected_table}')
    st.bar_chart(time_travel_df)
    
    # Display DataFrame
    st.write('DataFrame with Time-Travel and Fail-Safe Options:')
    st.dataframe(time_travel_df)  
