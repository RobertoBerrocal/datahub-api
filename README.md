# 📊 DataHub API

A modular **FastAPI-based Data Engineering and Backend project** designed to integrate external public APIs, process them through ETL pipelines, and store results in a local SQLite database.  
Currently, the system ingests data from **Frankfurter Exchange Rates** and **OpenWeather Air Pollution** APIs.

---

## ⚙️ Environment Setup

### 1️⃣ Environment Variables

Create a `.env` file in the project root with the following keys:

```bash
# General
APP_NAME="DataHub API"
DEBUG=True

# Database
DATABASE_URL=sqlite:///datahub.db

# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

_Note: The Exchange Rates module uses the Frankfurter API, which does not require an API key._

---

### 2️⃣ Local Installation

```bash
# Create a virtual environment
python3 -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows (PowerShell):
# .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

Start the API locally:

```bash
uvicorn app.main:app --reload
```

- App: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs

---

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

This will:
- Build the image from the `Dockerfile`
- Mount the SQLite database file (`data/datahub.db`)
- Expose the FastAPI service on port `8000`

Stop containers:

```bash
docker-compose down
```

---

## 🔄 ETL Pipelines

### 💱 Exchange Rates

- Source: **Frankfurter API** (https://www.frankfurter.app)
- Base currencies: **USD**, **EUR**
- Target currencies: `GBP`, `AUD`, `CAD`, `CHF`, `JPY`, `MXN`, `PEN`, `SEK`, `BRL`
- Historical range: **2025-01-01 → current date**
- Stages:
  - **Extract**: HTTP GET requests to Frankfurter endpoints for historical rates
  - **Transform**: Normalize pairs into tabular structure (base, target, rate, date)
  - **Load**: Append into SQLite table `exchange_rates`

---

### 🌫️ Air Pollution

- Source: **OpenWeather Air Pollution (Historical)** (https://openweathermap.org/api/air-pollution)
- Endpoint used: `https://api.openweathermap.org/data/2.5/air_pollution/history`
- Cities: **Berlin**, **Munich**, **Frankfurt**
- Time range: **Last 5 days** (hourly)
- Stages:
  - **Extract**: Fetch hourly pollutant data for each city
  - **Transform**: Flatten JSON into tabular structure (city, AQI, CO, NO, NO2, O3, SO2, PM2_5, PM10, NH3, date)
  - **Load**: Append into SQLite table `air_pollution_data`

---

## 📡 API Endpoints

### GET `/`
Returns a simple health/status payload.

### POST `/data/update/exchange_rates`
Runs the Exchange Rates ETL and updates `exchange_rates`.

### POST `/data/update/air_pollution`
Runs the Air Pollution ETL for Berlin, Munich, and Frankfurt (last 5 days) and updates `air_pollution_data`.

---

## 🧰 Tech Stack

- **FastAPI** — web framework
- **Pandas** — data processing & loading to SQLite
- **SQLAlchemy** — ORM/engine
- **SQLite** — local relational database
- **Docker & Docker Compose** — containerized runtime
- **Uvicorn** — ASGI server

---

## 🧠 Future Enhancements

- [ ] Daily incremental updates for both pipelines
- [ ] Data validation & error handling in ETL
- [ ] Additional cities and currencies
- [ ] Auth for ETL endpoints (JWT/API Key)
- [ ] Optional visualization layer (React or BI)

---

## 👨‍💻 Author

**Roberto Berrocal**  
Data & Software Engineer — Berlin, Germany  
GitHub: https://github.com/RobertoBerrocal  
LinkedIn: https://www.linkedin.com/in/roberto-berrocal

---

📦 Version 2.0 — Last updated: November 2025
