<div align="center">

![Nexus Tech Store Banner](assets/nexus_banner.png)

# ⚡ NEXUS TECH STORE

**A Futuristic, Full-Stack E-Commerce Platform for Flagship Hardware & Quantum Gadgets**

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/asad594/nexus-tech-store/actions)
[![React](https://img.shields.io/badge/Frontend-React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite_8-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Django](https://img.shields.io/badge/Backend-Django_REST-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Container-Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[View Demo](#-getting-started) • [API Documentation](backend/API_DOCUMENTATION.md) • [Architecture Guide](frontend/ARCHITECTURE.md) • [Report Bug](https://github.com/asad594/nexus-tech-store/issues)

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
- 🐳 **Docker Ready**: One-command spinup using Docker and Docker Compose.
- 🧪 **Automated CI/CD & Testing**: GitHub Actions workflows for continuous integration, backend unit testing, and CodeQL security analysis.

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
| **SimpleJWT** | JSON Web Token authentication |
| **SQLite3 / MySQL** | Flexible relational database support |

---

## 🚀 Getting Started

### Option A: Running with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/asad594/nexus-tech-store.git
cd nexus-tech-store

# Launch backend and frontend containers
docker-compose up --build
```
- **Frontend App**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000/api/`

---

### Option B: Local Manual Setup

#### 1️⃣ Backend Setup (Django REST Framework)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Seed sample product catalog
python manage.py seed_data

# Start the Django development server
python manage.py runserver
```

The backend server will start at: `http://127.0.0.1:8000/`

#### 2️⃣ Frontend Setup (React + Vite)

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

## ⚡ Quick Command Reference

| Action | Command | Directory / Tool |
| :--- | :--- | :--- |
| **All-in-One Setup** | `make setup` | Root `Makefile` |
| **Backend Dev Server** | `make run-backend` or `python manage.py runserver` | `backend/` |
| **Seed Full Catalog** | `python manage.py seed_data` | `backend/` |
| **Seed Demo Data** | `python manage.py seed_demo_data` | `backend/` |
| **Export Catalog JSON**| `python manage.py export_catalog` | `backend/` |
| **Integrity Check** | `python manage.py check_integrity` | `backend/` |
| **Run Backend Tests** | `make test` or `python manage.py test store` | `backend/` |
| **Frontend Dev Server** | `make run-frontend` or `npm run dev` | `frontend/` |
| **Frontend Build** | `make build` or `npm run build` | `frontend/` |
| **Docker Compose** | `make docker-up` or `docker-compose up -d` | Root `/` |

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

1. **Fork** the Repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/asad594">Muhammad Asad</a> • ⚡ Nexus Tech Store Framework</sub>
</div>
