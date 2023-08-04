# Streamlit_Table_Metrics
Streamlit application to pull in table metrics from table and simulate time travel and failsafe metrics 


### Requirements
- Pull in ACCOUNT_USAGE.TABLE_STORAGE_METRICS table from SNOWFLAKE SCHEMA
- User can pick their designated table from a drop down menu and view current active bytes
- User can input how many times they expect their data to change from a daily/weekly/monthly basis
- A bar graph will be created of various time-travel scenarios from 1-90 days
- Dataframe will also be created with various time-travel options and fail-safe options
