
# 🚓 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

SecureCheck is a real-time, Streamlit-powered dashboard and PostgreSQL database system designed for police check post monitoring. It enables officers to log, track, analyze, and predict vehicle stops, violations, and outcomes at multiple check posts.

## 📌 Project Overview

**Problem Statement:**  
Police check posts require a centralized, digitized system to log and monitor vehicle movements. Manual entry leads to inefficiencies and data loss. SecureCheck addresses this gap with a clean, scalable, and analytical web dashboard.

**Goal:**  
To create a centralized database with SQL and a Python dashboard to visualize logs, detect violation patterns, and predict stop outcomes.

## 💡 Features

- 📊 Streamlit dashboard with gender, violation, and time-based filters
- ✅ SQL-backed analytics on arrests, searches, and violations
- 🧠 Complex queries with subqueries and window functions
- 📅 Time-based pattern recognition by hour, month, and year
- 🔮 Form-based prediction (simulated) for violation and outcome
- 🛡️ Built with role-based access in mind (can be extended)

## 🛠️ Tech Stack

| Component   | Tools Used                   |
|-------------|------------------------------|
| Language    | Python 3                     |
| Database    | PostgreSQL (via Railway)     |
| Framework   | Streamlit                    |
| ORM         | SQLAlchemy                   |
| Data Viz    | Matplotlib, Pandas           |
| IDE         | VS Code                      |
| Hosting     | Railway for DB, Streamlit locally |

## 🗂️ Folder Structure

```
SecureCheck/
│
├── app.py                  # Main Streamlit dashboard
├── traffic_stops.csv       # Original dataset
├── cleaned_data.csv        # Cleaned dataset
├── README.md               # You're here
├── requirements.txt        # Python dependencies
```

## 📈 Sample SQL Queries Included

- 🔍 Top 10 vehicles involved in drug-related stops
- 📊 Gender and race-based search frequency
- 🕐 Hourly traffic stop trends
- ⚖️ Arrest rate per violation per country
- 🧠 Ranked violations using window functions

## 📋 Key Tables (PostgreSQL)

- `traffic_logs`
  - stop_datetime (timestamp)
  - driver_age, gender, race
  - violation, search_conducted, is_arrested
  - stop_duration, drugs_related_stop
  - country_name, vehicle_number

## 🧪 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SecureCheck.git
cd SecureCheck
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Connect to Your PostgreSQL DB

Edit `app.py`:

```python
engine = create_engine("postgresql+psycopg2://<user>:<password>@<host>/<db>")
```

Or use `.env` for secure storage.

### 4. Launch Streamlit Dashboard

```bash
streamlit run app.py
```

## ✅ Sample Use Case

> A 44-year-old female driver was stopped at 16:37 on 2025-06-14.  
> Predicted violation: **Speeding**  
> Predicted outcome: **Warning**  
> Country: **US**

## 🔐 Optional Enhancements

- Add authentication (officer login)
- Deploy dashboard on Streamlit Cloud
- Replace simulated prediction with a trained ML model
- Real-time alerts for flagged vehicles

## 📌 Project Status

✅ Completed:
- Data ingestion and cleaning  
- PostgreSQL schema setup  
- Dashboard development  
- SQL analytics  
- Complex queries  
- Form-based prediction

🚧 In Progress (Optional):
- ML model integration  
- Database write-back (logs/predictions)

## 📃 License

MIT License. Use freely for learning, law enforcement education, or demonstration.

## 🤝 Contributors

- 👨‍💻 Aravind Raj
- 👩‍🏫 Guided by: GUVI x HCL Capstone Team

## 📎 References

- [Streamlit Docs](https://docs.streamlit.io/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- Dataset: Provided in capstone
