<div align="center">

![Nexus Tech Store Banner](assets/nexus_banner.png)

# ⚡ NEXUS TECH STORE

**A Futuristic, Full-Stack E-Commerce Platform for Flagship Hardware & Quantum Gadgets**

[![React](https://img.shields.io/badge/Frontend-React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite_8-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Django](https://img.shields.io/badge/Backend-Django_REST-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Language-Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[View Demo](#-getting-started) • [API Documentation](#-api-endpoints) • [Report Bug](https://github.com/asad594/nexus-tech-store/issues)

</div>

---

## 📖 Overview

**Nexus Tech Store** is an ultra-modern, high-performance e-commerce platform designed for selling next-generation electronics, laptops, smartphones, quantum hardware, and premium audio accessories. 

Built with a dark-glassmorphism aesthetic, interactive scroll-driven video showcases, custom JWT authentication, customer cart & checkout flows, and a feature-complete Admin Control Dashboard powered by **Django REST Framework** and **React 19**.

---

## ✨ Key Features

- 🌌 **Futuristic Dark-Glass UI**: Built with glassmorphism cards, vibrant HSL gradients, dynamic particle confetti, and smooth Lenis scrolling.
- 🎬 **Interactive Scroll-Scrubbed Video Hero**: Framer Motion scroll-bound video hero section featuring flagship products.
- 🔐 **Role-Based Authentication**: Seamless login and signup with JWT support, dividing access into **Customer** and **Admin** personas.
- 🛍️ **Interactive Shopping Experience**: Dynamic filtering by category/brand, real-time search, spec modals, and shopping cart persistence.
- 🎉 **Confetti Checkout Flow**: Smooth order processing accompanied by dynamic canvas confetti animations.
- 🛠️ **Admin Control Dashboard**: Full CRUD panel for store administrators to add/edit products, manage stock levels, manage categories, and update order statuses.
- ⚡ **RESTful API Backend**: Powered by Django REST Framework with customizable models, CORS headers, and relational SQLite schema.

---

## 🛠️ Tech Stack & Architecture

### **Frontend**
| Technology | Description |
| :--- | :--- |
| **React 19** | Latest UI component library with concurrent rendering |
| **Vite 8** | Lightning-fast build tool and dev server |
| **Tailwind CSS v4** | Modern utility-first CSS framework |
| **Framer Motion** | Fluid animations and scroll-triggered transitions |
| **Lenis Scroll** | Ultra-smooth wheel scrolling engine |
| **Lucide React** | Clean, customizable modern icon set |
| **Canvas Confetti** | Celebration feedback upon order completion |

### **Backend**
| Technology | Description |
| :--- | :--- |
| **Python 3.x** | Core backend language |
| **Django 5.x** | High-level Python web framework |
| **Django REST Framework** | Robust toolkit for building RESTful APIs |
| **SQLite3** | Relational database engine |
| **django-cors-headers** | Cross-Origin Resource Sharing handling for React client |

---

## 📂 Project Structure

```bash
nexus-tech-store/
├── assets/
│   └── nexus_banner.png             # GitHub Repository Banner
├── backend/
│   ├── manage.py                    # Django Management Script
│   ├── nexus_backend/               # Core Project Configuration
│   │   ├── settings.py              # Settings & CORS config
│   │   ├── urls.py                  # Main API Router
│   │   └── wsgi.py
│   └── store/                       # E-Commerce App Module
│       ├── models.py                # User, Product, Category, Order models
│       ├── serializers.py           # REST Serializers
│       ├── views.py                 # API Viewsets & Controllers
│       └── urls.py                  # Store API endpoints
├── frontend/
│   ├── public/                      # Static assets & sample videos
│   ├── src/
│   │   ├── api.js                   # Axios client instance
│   │   ├── components/              # Reusable UI Components
│   │   ├── context/                 # AuthContext & State management
│   │   ├── pages/                   # Storefront Pages (Home, Products, Admin, etc.)
│   │   ├── index.css                # Global Tailwind CSS directives
│   │   └── main.jsx                 # Application Entry Point
│   ├── package.json
│   └── vite.config.js
└── README.md                        # Documentation
```

---

## 🚀 Getting Started

Follow these steps to run the application locally on your system.

### 📋 Prerequisites
- **Node.js** (v18.x or higher)
- **Python** (v3.10 or higher)
- **Git**

---

### 1️⃣ Backend Setup (Django REST Framework)

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django djangorestframework django-cors-headers

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# (Optional) Create a superuser for Admin Panel access
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

The backend server will start at: `http://127.0.0.1:8000/`

---

### 2️⃣ Frontend Setup (React + Vite)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Start Vite development server
npm run dev
```

The frontend web application will start at: `http://localhost:5173/`

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/login/` | Public | Authenticate user & return token/user data |
| `POST` | `/api/register/` | Public | Register new customer account |
| `GET` | `/api/products/` | Public | List all tech products |
| `POST` | `/api/products/` | Admin | Create a new product |
| `PUT/PATCH`| `/api/products/{id}/` | Admin | Update existing product |
| `DELETE` | `/api/products/{id}/` | Admin | Delete product |
| `GET` | `/api/categories/` | Public | List categories with product counts |
| `GET` | `/api/orders/` | Authenticated | List user orders (Admin sees all) |
| `POST` | `/api/orders/` | Authenticated | Checkout cart & create order |

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the Repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git checkout -b feature/AmazingFeature` -> `git push origin feature/AmazingFeature`)
5. Open a **Pull Request**


---

## ⚡ Quick Command Reference

| Action | Command | Directory |
| :--- | :--- | :--- |
| **Backend Dev Server** | `python manage.py runserver` | `backend/` |
| **Seed Sample Data** | `python manage.py seed_data` | `backend/` |
| **Run Backend Tests** | `python manage.py test store` | `backend/` |
| **Frontend Dev Server** | `npm run dev` | `frontend/` |
| **Frontend Build** | `npm run build` | `frontend/` |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/asad594">Muhammad Asad</a> • ⚡ Nexus Tech Store Framework</sub>
</div>

