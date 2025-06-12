import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --- PostgreSQL Connection ---
db_user = 'postgres'          # 👉 use your actual DB user
db_pass = 'guvi2025'      # 👉 use your PostgreSQL password
db_host = 'localhost'         # keep this if using locally
db_port = '5432'              # default PostgreSQL port
db_name = 'traffic_db'        # your DB name

conn_str = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_engine(conn_str)

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
