🌍 DataHub API

DataHub API es un backend modular construido con FastAPI y Docker, diseñado para extraer, limpiar, almacenar y servir datos públicos mediante endpoints REST.

Este proyecto combina conceptos de Backend Development y Data Engineering, con una arquitectura escalable que permite agregar nuevas fuentes de datos fácilmente.

🚀 Características principales

🔹 API desarrollada con FastAPI

🔹 Base de datos SQLite (por defecto, extensible a PostgreSQL)

🔹 Arquitectura modular ETL (Extract, Transform, Load)

🔹 Configuración por entorno usando .env

🔹 Totalmente Dockerized

🔹 Endpoints REST documentados automáticamente con Swagger UI

🧱 Arquitectura general
                ┌────────────────────────────┐
                │  External Data Sources     │
                │ (APIs públicas, CSVs, etc) │
                └──────────────┬─────────────┘
                               │
                      (ETL Pipeline)
                               │
                   ┌───────────▼───────────┐
                   │      SQLite DB        │
                   │   (datahub.db)        │
                   └───────────┬───────────┘
                               │
                        (FastAPI Layer)
                               │
                   ┌───────────▼───────────┐
                   │   REST API Endpoints  │
                   │  /, /data/sources, …  │
                   └───────────┬───────────┘
                               │
                           (Client)
                               │
                   ┌───────────▼───────────┐
                   │ React / BI / cURL / … │
                   └───────────────────────┘

⚙️ Configuración del entorno

1️⃣ Clonar el repositorio

git clone https://github.com/RobertoBerrocal/datahub-api.git
cd datahub-api


2️⃣ Crear el archivo .env

Puedes copiar el ejemplo incluido:

cp .env.example .env


3️⃣ Construir y ejecutar con Docker

docker-compose up --build


La API quedará corriendo en:

🌐 http://localhost:8000

📘 Documentación Swagger → http://localhost:8000/docs

🧩 Endpoints actuales (Fase 1)
Endpoint	Método	Descripción
/	GET	Prueba de conexión
/data/sources	GET	Lista las fuentes de datos disponibles
🔜 Próximas Fases
💱 Fase 2: Exchange Rates API

Integración con una API gratuita de tasas de cambio (EUR/USD, etc.)
→ Descarga diaria automática y almacenamiento en la base de datos.

🌦️ Fase 3: OpenWeather API

Integración con una API gratuita de clima (OpenWeatherMap).
→ Información meteorológica actualizada por ciudad.

🕒 Fase 4: Scheduler y automatización

Automatización de los pipelines ETL con APScheduler.

🧑‍💻 Autor

Roberto Berrocal
Data Analyst & Full-Stack Developer
📍 Berlín, Alemania
🔗 GitHub Profile

📜 Licencia

MIT License © 2025 Roberto Berrocal