# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

def generate_time_travel_df(current_active_bytes, data_change_rate):
    time_travel_data = []
    for days in range(1, 91):
        time_travel_bytes = current_active_bytes * (1 + data_change_rate) ** (days / 30)
        fail_safe_bytes = time_travel_bytes*7
        time_travel_data.append([days, time_travel_bytes,fail_safe_bytes])
    return pd.DataFrame(time_travel_data, columns=['day', 'time-travel bytes', 'fail_safe_bytes'])



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


# Generate DataFrame with time-travel options
time_travel_df = generate_time_travel_df(current_active_bytes, data_change_rate)    
# Plot bar graph using Streamlit
st.subheader(f'Time-Travel Scenario for {selected_table}')
st.bar_chart(time_travel_df.set_index('day'))    
# Display DataFrame
st.write('DataFrame with Time-Travel and Fail-Safe Options:')
st.dataframe(time_travel_df)
