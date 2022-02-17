# Import packages
import pandas as pd
import requests
from datetime import datetime
import altair as alt
import pandasql as ps
import streamlit as st
import pydata_google_auth

# Set GCP Credentials
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
]

credentials = pydata_google_auth.get_user_credentials(
    SCOPES,
    # Set auth_local_webserver to True to have a slightly more convienient
    # authorization flow. Note, this doesn't work if you're running from a
    # notebook on a remote sever, such as over SSH or with Google Colab.
    auth_local_webserver=True,
)

# Set Page Config
st.set_page_config(page_title='Orca Analytics Dashboard', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

qry = '''

select
    afp.epoch,
    e.start_date,
    e.end_date,
    afp.pool,
    (afp.reward_cost_usd * -1) as reward_cost_usd_neg,
    afp.reward_cost_usd,
    afp.pool_revenue_usd,
    afp.pool_profit_usd,
    case when afp.pool_profit_usd >= 0 then 1 else 0 end as is_profitable
from `m2-core-317116.transactions.aqua_farm_profitability` afp
    left join `m2-core-317116.key_tables.epoch` e on e.epoch = afp.epoch

'''

df = pd.read_gbq(qry, project_id='m2-core-317116', credentials=credentials)

st.dataframe(df)