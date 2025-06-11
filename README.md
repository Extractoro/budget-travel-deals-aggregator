# Flight & Hotel Deal Tracker

A full-stack FastAPI-based web service to monitor flight and hotel deals using Scrapy, Celery, and Playwright. Users can initiate searches, view results, subscribe to updates, and receive email alerts on changes. Integrated with Docker, Redis, and PostgreSQL for scalable deployment.

## Table of Contents

* [✨ Features](#-features)
* [🛠 Project Structure](#-project-structure)
* [⚙️ Getting Started](#-getting-started)

  * [1. Clone the Repository](#1-clone-the-repository)
  * [2. Configure Environment](#2-configure-environment)
  * [3. Run with Docker](#3-run-with-docker)
* [🧪 Testing](#-testing)
* [📊 API Endpoints](#-api-endpoints)

  * [🔐 Authentication](#-authentication)
  * [👤 Profile](#-profile)
  * [✈️ Flights](#-flights)
  * [🏨 Hotels](#-hotels)
  * [📅 Subscription](#-subscription)
* [🔍 Interactive Docs](#-interactive-docs)

## ✨ Features

* 🔐 JWT-based authentication
* ✈️ Flight search (Ryanair, Playwright-powered)
* 🏨 Hotel search (Booking.com, Scrapy)
* 📅 Email notifications on price or availability changes
* ✅ Celery workers for async task processing
* 📧 Subscription to search results
* 🛠 Dockerized environment with PostgreSQL, Redis, and Celery
* ⚡ Test coverage with pytest

## 🛠 Project Structure

```
├── app/
│   ├── api/                 # Route handlers
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── tasks/               # Celery tasks (flights, hotels)
│   ├── tests/               # Test suite
│   ├── utils/               # Helpers (token, parsing, email)
│   ├── scrapy/              # Scrapy spiders and pipelines
│   ├── service/             # Business logic
│   └── main.py              # FastAPI entry point
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Extractoro/budget-travel-deals-aggregator.git
cd budget-travel-deals-aggregator
```

### 2. Configure Environment

Create a `.env` file:

```
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
SECRET_KEY=your_secret_key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your_password
MAIL_FROM=your@email.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

### 3. Run with Docker

```bash
docker-compose up --build
```

## 🧪 Testing

```bash
docker-compose exec web pytest
pytest .
flake8 .
```

## 📊 API Endpoints

### 🔐 Authentication

| Method | Endpoint     | Description   |
| ------ | ------------ | ------------- |
| POST   | /auth/signup | Register user |
| POST   | /auth/login  | Login user    |

### 👤 Profile

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| GET    | /profile/ | Current user profile |

### ✈️ Flights

| Method | Endpoint                            | Description              |
| ------ | ----------------------------------- | ------------------------ |
| POST   | /flights/oneway\_fare/start         | Start oneway fare search |
| GET    | /flights/oneway\_fare/{task\_id}    | Get results by task\_id  |
| POST   | /flights/search\_flights/start      | Start full flight search |
| GET    | /flights/search\_flights/{task\_id} | Get results by task\_id  |

### 🏨 Hotels

| Method | Endpoint                          | Description             |
| ------ | --------------------------------- | ----------------------- |
| POST   | /hotels/search\_hotels/start      | Start hotel search      |
| GET    | /hotels/search\_hotels/{task\_id} | Get results by task\_id |

### 📅 Subscription

| Method | Endpoint                         | Description                   |
| ------ | -------------------------------- | ----------------------------- |
| POST   | /subscription/subscribe          | Subscribe to search result    |
| POST   | /subscription/{task\_id}/refresh | Refresh and check for changes |
| DELETE | /subscription/unsubscribe        | Unsubscribe from updates      |

## 🔍 Interactive Docs

* Swagger → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)
