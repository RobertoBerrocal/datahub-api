# 📊 DataHub API

A modular **FastAPI-based Data Engineering and Backend project** designed to integrate external public APIs, process them through ETL pipelines, and store results in a local SQLite database.

Currently, the system ingests data from:

- **Frankfurter Exchange Rates API**
- **OpenWeather Air Pollution API (Historical)**

---

## ⚙️ Environment Setup

### 1️⃣ Environment Variables

Create a `.env` file in the project root:

    # General
    APP_NAME="DataHub API"
    DEBUG=True

    # Database
    DATABASE_URL=sqlite:///./data/datahub.db

    # API Keys
    OPENWEATHER_API_KEY=your_openweather_api_key_here

> The Exchange Rates module uses the Frankfurter API, which does not require an API key.

---

### 2️⃣ Local Installation (Recommended for Development)

    # Clone the repository
    git clone https://github.com/RobertoBerrocal/datahub-api.git
    cd datahub-api

    # Create virtual environment (Python 3.11 recommended)
    python3.11 -m venv .venv

    # Activate environment
    # macOS/Linux
    source .venv/bin/activate
    # Windows (PowerShell)
    # .venv\Scripts\Activate.ps1

    # Install dependencies
    python -m pip install -r requirements.txt

Run the application:

    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Access:

- API: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs

---

### 3️⃣ Run with Docker

    docker-compose up --build

This will:

- Build the Docker image
- Mount the SQLite database (`./data/datahub.db`)
- Load environment variables from `.env`
- Expose FastAPI on port `8000`

Stop containers:

    docker-compose down

---

## 🔄 ETL Pipelines

### 💱 Exchange Rates

- Source: **Frankfurter API**  
  https://www.frankfurter.app

- Base currencies:
  - `USD`
  - `EUR`

- Target currencies:
  - `GBP`
  - `AUD`
  - `CAD`
  - `CHF`
  - `JPY`
  - `MXN`
  - `PEN`
  - `SEK`
  - `BRL`

- Historical range:
  - From **2025-01-01**
  - Until current date

#### ETL Flow

- **Extract**
  - HTTP requests to Frankfurter historical endpoint
- **Transform**
  - Normalize response into tabular format:
    - `date`
    - `base_currency`
    - `target_currency`
    - `exchange_rate`
- **Load**
  - Append to SQLite table: `exchange_rates`

---

### 🌫️ Air Pollution

- Source: **OpenWeather Air Pollution (Historical)**  
  https://openweathermap.org/api/air-pollution

- Endpoint used:

    /data/2.5/air_pollution/history

- Cities:
  - Berlin
  - Munich
  - Frankfurt

- Time range:
  - Last **5 days**
  - Hourly granularity

#### ETL Flow

- **Extract**
  - Fetch hourly pollution data per city
- **Transform**
  - Flatten JSON into structured format:
    - `city`
    - `timestamp`
    - `aqi`
    - `co`
    - `no`
    - `no2`
    - `o3`
    - `so2`
    - `pm2_5`
    - `pm10`
    - `nh3`
- **Load**
  - Insert deduplicated rows (city + timestamp unique key) into SQLite table: `air_pollution`

---

## 📡 API Endpoints

### `GET /`

Welcome endpoint.

### `GET /health`

Operational health endpoint with database and scheduler status.

### `POST /data/update/exchange_rates`

Runs the Exchange Rates ETL pipeline and updates:

    exchange_rates

### `POST /data/update/air_pollution`

Runs the Air Pollution ETL pipeline for Berlin, Munich, and Frankfurt and updates:

    air_pollution

---

## 🧰 Tech Stack

- **FastAPI** — Backend framework  
- **Pandas** — Data transformation  
- **SQLAlchemy** — ORM & DB engine  
- **SQLite** — Embedded relational database  
- **APScheduler** — Scheduled ETL execution  
- **Docker & Docker Compose** — Containerization  
- **Uvicorn** — ASGI server  

---

## 🧠 Future Enhancements

- Incremental ETL updates  
- Data validation layer  
- Additional cities & currencies  
- Authentication for ETL endpoints  
- Optional visualization layer (React or BI tool)  

---

## ✅ Testing

Run tests with:

    .venv/bin/python -m pytest -q

---

## 👨‍💻 Author

**Roberto Berrocal**  
Data Analyst & Engineer — Berlin, Germany  

GitHub:  
https://github.com/RobertoBerrocal  

LinkedIn:  
https://www.linkedin.com/in/roberto-berrocal  

---

📦 **Version 2.0**  
Last updated: November 2025
