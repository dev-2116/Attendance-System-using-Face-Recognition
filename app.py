# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime

st.set_page_config(page_title="Face Attendance System", page_icon="📋", layout="centered")

st.title("📋 Real-Time Attendance System")

os.makedirs("Attendance", exist_ok=True)
today_date = datetime.now().strftime("%d-%m-%Y")

# Scan available dates in Attendance directory and sort by latest date
attendance_files = glob.glob("Attendance/Attendance_*.csv")
available_dates = []

for f in attendance_files:
    date_str = os.path.basename(f).replace("Attendance_", "").replace(".csv", "")
    available_dates.append(date_str)

# Sort dates in descending order (latest date first)
def parse_date(d):
    try:
        return datetime.strptime(d, "%d-%m-%Y")
    except Exception:
        return datetime.min

available_dates = sorted(set(available_dates), key=parse_date, reverse=True)

if today_date not in available_dates:
    available_dates.insert(0, today_date)

selected_date = st.selectbox("📅 Select Date:", available_dates, index=0)

# Real-time auto-refreshing section using Streamlit's native @st.fragment
@st.fragment(run_every="2s")
def display_attendance():
    file_path = f"Attendance/Attendance_{selected_date}.csv"
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                st.info(f"No records logged yet for {selected_date}.")
            else:
                st.success(f"Total Records: {len(df)}")
                st.dataframe(df, width="stretch")
        except Exception as e:
            st.error(f"Error reading attendance file: {e}")
    else:
        st.info(f"No attendance marked yet for {selected_date}.")

display_attendance()