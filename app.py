import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:LmPKGwdHCXBEFWHJLJsEirdEitllEHST@interchange.proxy.rlwy.net:23897/railway")


@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM traffic_logs", engine)

df = load_data()


st.title("🚓 SecureCheck - Traffic Stops Dashboard")


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


st.dataframe(filtered_df)


st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Stops", len(filtered_df))
st.subheader("📊 Visual Analytics")

st.markdown("#### Gender Distribution (Pie Chart)")
gender_counts = filtered_df['driver_gender'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  
st.pyplot(fig1)

st.markdown("#### Violation Types (Bar Chart)")
violation_counts = filtered_df['violation'].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=violation_counts.index, y=violation_counts.values, ax=ax2)
ax2.set_ylabel("Number of Stops")
ax2.set_xlabel("Violation")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

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
  DATE_TRUNC('month', stop_datetime::timestamp) AS month,
  COUNT(*) AS total_stops
FROM traffic_logs
GROUP BY month
ORDER BY month
"""
df4 = pd.read_sql(query4, engine)
df4['month'] = pd.to_datetime(df4['month'])
df4.set_index('month', inplace=True)
st.line_chart(df4)

st.markdown("## 📊 SQL-Based Analytics")


with st.expander("🚗 Vehicle-Based Queries"):
    st.markdown("**1. Top 10 vehicles involved in drug-related stops**")
    q1 = """
    SELECT vehicle_number, COUNT(*) AS stop_count
    FROM traffic_logs
    WHERE drugs_related_stop = TRUE AND vehicle_number IS NOT NULL
    GROUP BY vehicle_number
    ORDER BY stop_count DESC
    LIMIT 10;
    """
    st.dataframe(pd.read_sql(q1, engine))

    st.markdown("**2. Most frequently searched vehicles**")
    q2 = """
    SELECT vehicle_number, COUNT(*) AS search_count
    FROM traffic_logs
    WHERE search_conducted = TRUE AND vehicle_number IS NOT NULL
    GROUP BY vehicle_number
    ORDER BY search_count DESC
    LIMIT 10;
    """
    st.dataframe(pd.read_sql(q2, engine))


with st.expander("🧍 Demographic-Based Queries"):
    st.markdown("**3. Age group with highest arrest rate**")
    q3 = """
    SELECT driver_age, COUNT(*) AS arrest_count
    FROM traffic_logs
    WHERE is_arrested = TRUE
    GROUP BY driver_age
    ORDER BY arrest_count DESC
    LIMIT 10;
    """
    st.dataframe(pd.read_sql(q3, engine))

    st.markdown("**4. Gender distribution by country**")
    q4 = """
    SELECT country_name, driver_gender, COUNT(*) AS count
    FROM traffic_logs
    GROUP BY country_name, driver_gender;
    """
    st.dataframe(pd.read_sql(q4, engine))

    st.markdown("**5. Highest search rate by Race & Gender**")
    q5 = """
    SELECT driver_race, driver_gender, COUNT(*) AS search_count
    FROM traffic_logs
    WHERE search_conducted = TRUE
    GROUP BY driver_race, driver_gender
    ORDER BY search_count DESC
    LIMIT 5;
    """
    st.dataframe(pd.read_sql(q5, engine))


with st.expander("🕒 Time & Duration-Based Queries"):
    st.markdown("**6. Time of day with most stops**")
    q6 = """
SELECT 
    EXTRACT(HOUR FROM stop_datetime::timestamp) AS hour,
    COUNT(*) AS stop_count
FROM traffic_logs
GROUP BY hour
ORDER BY stop_count DESC;
"""

    st.dataframe(pd.read_sql(q6, engine))

    st.markdown("**7. Avg stop duration per violation**")
    q7 = """
    SELECT violation, AVG(CASE 
        WHEN stop_duration = '<5 Min' THEN 3 
        WHEN stop_duration = '6-15 Min' THEN 10 
        WHEN stop_duration = '16-30 Min' THEN 20 
        WHEN stop_duration = '30+ Min' THEN 35 
        ELSE NULL END) AS avg_duration
    FROM traffic_logs
    GROUP BY violation;
    """
    st.dataframe(pd.read_sql(q7, engine))

    st.markdown("**8. Night vs Day Arrests**")
    q8 = """
SELECT 
    CASE 
        WHEN EXTRACT(HOUR FROM stop_datetime::timestamp) BETWEEN 0 AND 6 THEN 'Night'
        ELSE 'Day'
    END AS time_period,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests
FROM traffic_logs
GROUP BY time_period;
"""


    st.dataframe(pd.read_sql(q8, engine))


with st.expander("⚖️ Violation-Based Queries"):
    st.markdown("**9. Violations linked to searches or arrests**")
    q9 = """
    SELECT violation, 
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count,
        SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_count
    FROM traffic_logs
    GROUP BY violation
    ORDER BY arrest_count DESC, search_count DESC;
    """
    st.dataframe(pd.read_sql(q9, engine))

    st.markdown("**10. Common violations among drivers < 25**")
    q10 = """
    SELECT violation, COUNT(*) AS count
    FROM traffic_logs
    WHERE driver_age < 25
    GROUP BY violation
    ORDER BY count DESC
    LIMIT 5;
    """
    st.dataframe(pd.read_sql(q10, engine))

    st.markdown("**11. Violations with no arrests or searches**")
    q11 = """
SELECT *
FROM (
    SELECT violation,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count,
        SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_count,
        COUNT(*) AS total
    FROM traffic_logs
    GROUP BY violation
) AS subquery
WHERE arrest_count = 0 AND search_count = 0;
"""
    st.dataframe(pd.read_sql(q11, engine))


with st.expander("🌍 Location-Based Queries"):
    st.markdown("**12. Countries with most drug-related stops**")
    q12 = """
    SELECT country_name, COUNT(*) AS count
    FROM traffic_logs
    WHERE drugs_related_stop = TRUE
    GROUP BY country_name
    ORDER BY count DESC
    LIMIT 5;
    """
    st.dataframe(pd.read_sql(q12, engine))

    st.markdown("**13. Arrest rate by country and violation**")
    q13 = """
    SELECT country_name, violation,
        ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS arrest_rate
    FROM traffic_logs
    GROUP BY country_name, violation
    ORDER BY arrest_rate DESC
    LIMIT 10;
    """
    st.dataframe(pd.read_sql(q13, engine))

    st.markdown("**14. Countries with most searches**")
    q14 = """
    SELECT country_name, COUNT(*) AS search_count
    FROM traffic_logs
    WHERE search_conducted = TRUE
    GROUP BY country_name
    ORDER BY search_count DESC
    LIMIT 5;
    """
    st.dataframe(pd.read_sql(q14, engine))

with st.expander("🧠 Complex Queries: Trends & Insights"):
    
    st.markdown("**1. Yearly Breakdown of Stops and Arrests by Country**")
    cq1 = """
    SELECT 
        country_name,
        EXTRACT(YEAR FROM stop_datetime::timestamp) AS year,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
        ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
    FROM traffic_logs
    GROUP BY country_name, year
    ORDER BY country_name, year;
    """
    st.dataframe(pd.read_sql(cq1, engine))

    st.markdown("**2. Driver Violation Trends by Age and Race**")
    cq2 = """
    SELECT 
        driver_race,
        driver_age,
        violation,
        COUNT(*) AS violation_count
    FROM traffic_logs
    GROUP BY driver_race, driver_age, violation
    ORDER BY driver_race, driver_age;
    """
    st.dataframe(pd.read_sql(cq2, engine))

    st.markdown("**3. Time Series: Stops by Year, Month, and Hour**")
    cq3 = """
    SELECT 
        EXTRACT(YEAR FROM stop_datetime::timestamp) AS year,
        EXTRACT(MONTH FROM stop_datetime::timestamp) AS month,
        EXTRACT(HOUR FROM stop_datetime::timestamp) AS hour,
        COUNT(*) AS stops
    FROM traffic_logs
    GROUP BY year, month, hour
    ORDER BY year, month, hour;
    """
    st.dataframe(pd.read_sql(cq3, engine))

    st.markdown("**4. Violations with Highest Search and Arrest Ratios (Ranked)**")
    cq4 = """
    SELECT violation, 
           COUNT(*) AS total_stops,
           SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
           SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
           ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)/COUNT(*), 2) AS arrest_rate,
           ROUND(100.0 * SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)/COUNT(*), 2) AS search_rate,
           RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) DESC) AS arrest_rank,
           RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) DESC) AS search_rank
    FROM traffic_logs
    GROUP BY violation
    LIMIT 10;
    """
    st.dataframe(pd.read_sql(cq4, engine))

    st.markdown("**5. Driver Demographics by Country**")
    cq5 = """
    SELECT 
        country_name,
        AVG(driver_age) AS avg_age,
        COUNT(*) FILTER (WHERE driver_gender = 'M') AS male_count,
        COUNT(*) FILTER (WHERE driver_gender = 'F') AS female_count,
        COUNT(*) FILTER (WHERE driver_race IS NOT NULL) AS race_known_count
    FROM traffic_logs
    GROUP BY country_name
    ORDER BY country_name;
    """
    st.dataframe(pd.read_sql(cq5, engine))

    st.markdown("**6. Top 5 Violations by Arrest Rate**")
    cq6 = """
    SELECT violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count,
        ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
    FROM traffic_logs
    GROUP BY violation
    ORDER BY arrest_rate DESC
    LIMIT 5;
    """
    st.dataframe(pd.read_sql(cq6, engine))

st.sidebar.header("Add New Police Log & Predict Outcome and Violation")

with st.sidebar.form("add_new_log_form"):
    
    stop_date = st.date_input("Stop Date")
  
    stop_time = st.time_input("Stop Time")
   
    country_name = st.text_input("Country Name")
    
    driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
  
    driver_age = st.number_input("Driver Age", min_value=18, max_value=100, value=30)
    
    violation = st.text_input("Violation")
   
    vehicle_number = st.text_input("Vehicle Number")
    
    was_drug_related = st.selectbox("Was it Drug Related?", [0, 1])

  
    submit = st.form_submit_button("Predict Stop Outcome & Violation")
if submit:
    
    new_data = pd.DataFrame([{
        "stop_date": stop_date,
        "stop_time": stop_time,
        "country_name": country_name,
        "driver_gender": driver_gender,
        "driver_age": driver_age,
        "violation": violation,
        "vehicle_number": vehicle_number,
        "was_drug_related": was_drug_related
    }])

   
    predicted_outcome = "Warning"
    predicted_violation = "Speeding"

    st.success(f"Predicted Violation: {predicted_violation}")
    st.success(f"Predicted Stop Outcome: {predicted_outcome}")

    st.write("**Details of the new entry:**")
    st.write(new_data)



stop_date = st.date_input("Stop Date")
stop_time = st.time_input("Stop Time")
driver_age = st.number_input("Driver Age", min_value=10, max_value=100)
driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])

violation = st.selectbox("Violation", [
    "Speeding", "DUI", "Equipment", "Registration", "Moving violation", "Other"
])

country = st.selectbox("Country", [
    "US", "UK", "Canada", "Germany", "India", "Australia", "Other"
])


if st.button("Predict Stop Outcome & Violation"):
  
    predicted_violation = violation
    predicted_outcome = "Warning" 

  
    st.success("✅ Prediction Summary")
    st.markdown(
        f"A {driver_age}-year-old {driver_gender} driver was stopped at {stop_time} on {stop_date}. "
        f"The predicted violation was **{predicted_violation.lower()}**, and the predicted outcome was **{predicted_outcome.lower()}**. "
        f"The stop occurred in **{country}**. "
    )
