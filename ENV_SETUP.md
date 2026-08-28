# Nexus Tech Store - Environment Variables Guide

This repository contains two primary subsystems requiring environment configuration:
1. **Backend (Django REST Framework)**
2. **Frontend (Vite + React)**

---

## 1. Backend Configuration (`backend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `SECRET_KEY` | string | `django-insecure-...` | Django security cryptographic secret key |
| `DEBUG` | boolean | `True` | Enable/disable debug mode (Set `False` in production) |
| `ALLOWED_HOSTS` | string | `*` | Comma-separated list of allowed host domains |
| `USE_MYSQL` | boolean | `False` | Toggle between SQLite (`False`) and MySQL (`True`) |
| `MYSQL_DATABASE` | string | `nexus_db` | MySQL database name |
| `MYSQL_USER` | string | `root` | MySQL database user |
| `MYSQL_PASSWORD` | string | `root` | MySQL database password |
| `MYSQL_HOST` | string | `localhost` | MySQL host server address |
| `MYSQL_PORT` | integer | `3306` | MySQL port |

---

## 2. Frontend Configuration (`frontend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | string | `http://localhost:8000/api` | Base URL for REST API communication |

---

## Quick Start Setup Command

Copy sample files into your local `.env` files:
```bash
# In backend directory
cp .env.example .env

# In frontend directory
cp .env.example .env
```
