import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page setup
st.set_page_config(page_title="Cold Mailing Agent Dashboard", layout="wide")

st.title("📧 Cold Mailing Agent Dashboard")


@st.cache_data(ttl=1)
def load_logs():
    response = supabase.table("outreach_logs").select("*").order("timestamp", desc=True).execute()
    return pd.DataFrame(response.data)

# Load data
logs_df = load_logs()

# KPIs
total_emails = len(logs_df)
last_run = logs_df['timestamp'].iloc[0] if not logs_df.empty else "No Data"

if not logs_df.empty and 'email' in logs_df.columns:
    unique_emails = logs_df['email'].nunique()
else:
    unique_emails = 0
    print("⚠️ No data or 'email' column missing in outreach_logs.")

col1, col2, col3 = st.columns(3)
col1.metric("📨 Total Emails Sent", total_emails)
col2.metric("⏱ Last Email Sent", last_run)
col3.metric("📧 Unique Recipients", unique_emails)

# Filters
with st.expander("🔍 Filter Logs"):
    search_email = st.text_input("Search by email")
    if search_email:
        logs_df = logs_df[logs_df['email'].str.contains(search_email, case=False)]

# Logs Table
st.subheader("📋 Outreach Logs")
if logs_df.empty:
    st.warning("No logs found.")
else:
    st.dataframe(logs_df , use_container_width=True)

# Download Option
csv = logs_df.to_csv(index=False)
st.download_button("📥 Download Logs as CSV", csv, "outreach_logs.csv", "text/csv")
