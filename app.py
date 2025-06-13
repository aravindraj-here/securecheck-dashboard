import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:yEydIHkrrBUXWsUcLXIvuiQydXlAiYGn@nozomi.proxy.rlwy.net:57537/railway")


# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM traffic_logs", engine)

df = load_data()

# --- Streamlit App UI ---
st.title("🚓 SecureCheck - Traffic Stops Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

gender = st.sidebar.multiselect("Driver Gender", df['driver_gender'].unique())
violation = st.sidebar.multiselect("Violation", df['violation'].unique())
country = st.sidebar.multiselect("Country", df['country_name'].unique())

filtered_df = df.copy()

if gender:
    filtered_df = filtered_df[filtered_df['driver_gender'].isin(gender)]
if violation:
    filtered_df = filtered_df[filtered_df['violation'].isin(violation)]
if country:
    filtered_df = filtered_df[filtered_df['country_name'].isin(country)]

# --- Main Table ---
st.dataframe(filtered_df)

# --- Basic Metrics ---
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Stops", len(filtered_df))
st.subheader("📊 Visual Analytics")

# 🚻 Gender Distribution
st.markdown("#### Gender Distribution (Pie Chart)")
gender_counts = filtered_df['driver_gender'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures pie is circular.
st.pyplot(fig1)
# ⚖️ Violation Types
st.markdown("#### Violation Types (Bar Chart)")
violation_counts = filtered_df['violation'].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=violation_counts.index, y=violation_counts.values, ax=ax2)
ax2.set_ylabel("Number of Stops")
ax2.set_xlabel("Violation")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)
# ⏱ Stops Over Time
if 'stop_datetime' in filtered_df.columns:
    st.markdown("#### Stops Over Time (Line Chart)")
    df_time = filtered_df.copy()
    df_time['date'] = pd.to_datetime(df_time['stop_datetime']).dt.date
    daily_counts = df_time.groupby('date').size()
    st.line_chart(daily_counts)

col2.metric("Arrests", filtered_df['is_arrested'].sum())
col3.metric("Drug Stops", filtered_df['drugs_related_stop'].sum())
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("📊 Visual Analytics")

# Gender distribution (Pie Chart)
st.markdown("#### 🚻 Gender Distribution")
gender_counts = filtered_df['driver_gender'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Violation count (Bar Chart)
st.markdown("#### ⚖️ Violation Types")
violation_counts = filtered_df['violation'].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=violation_counts.index, y=violation_counts.values, ax=ax2)
ax2.set_ylabel("Number of Stops")
ax2.set_xlabel("Violation")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# Stops Over Time (Line Chart)
if 'stop_datetime' in filtered_df.columns:
    st.markdown("#### ⏱ Stops Over Time")
    df_time = filtered_df.copy()
    df_time['date'] = pd.to_datetime(df_time['stop_datetime']).dt.date
    daily_counts = df_time.groupby('date').size()
    st.line_chart(daily_counts)
st.header("🧠 Advanced SQL Insights")
st.subheader("🚘 Top 10 Drug-Related Vehicles")

query1 = """
SELECT vehicle_number, COUNT(*) AS stop_count
FROM traffic_logs
WHERE drugs_related_stop = true AND vehicle_number IS NOT NULL
GROUP BY vehicle_number
ORDER BY stop_count DESC
LIMIT 10
"""
df1 = pd.read_sql(query1, engine)
st.dataframe(df1)
st.subheader("👥 Search Rate by Race & Gender")

query2 = """
SELECT driver_race, driver_gender,
       COUNT(*) AS total_stops,
       SUM(CASE WHEN search_conducted = true THEN 1 ELSE 0 END) AS searches,
       ROUND(100.0 * SUM(CASE WHEN search_conducted = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate
FROM traffic_logs
GROUP BY driver_race, driver_gender
ORDER BY search_rate DESC
"""
df2 = pd.read_sql(query2, engine)
st.dataframe(df2)
st.subheader("👮 Arrests by Age Group")

query3 = """
SELECT
  CASE
    WHEN driver_age < 18 THEN 'Under 18'
    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
    WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
    ELSE '60+'
  END AS age_group,
  COUNT(*) AS total_stops,
  SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) AS arrests,
  ROUND(100.0 * SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
FROM traffic_logs
WHERE driver_age IS NOT NULL
GROUP BY age_group
ORDER BY age_group
"""
df3 = pd.read_sql(query3, engine)
st.dataframe(df3)
st.subheader("🕒 Monthly Traffic Stops")

query4 = """
SELECT
  DATE_TRUNC('month', stop_datetime) AS month,
  COUNT(*) AS total_stops
FROM traffic_logs
GROUP BY month
ORDER BY month
"""
df4 = pd.read_sql(query4, engine)
df4['month'] = pd.to_datetime(df4['month'])
df4.set_index('month', inplace=True)
st.line_chart(df4)

