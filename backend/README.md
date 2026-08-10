# ⚡ Nexus Tech Store Backend API Documentation

The backend service is built using **Django 5** and **Django REST Framework (DRF)**.

## 🔑 Authentication

Authentication uses JWT tokens (JSON Web Tokens).

- **Token Obtain**: `POST /api/auth/token/`
  - Body: `{"username": "your_username", "password": "your_password"}`
  - Response: `{"access": "<access_token>", "refresh": "<refresh_token>"}`
- **Token Refresh**: `POST /api/auth/token/refresh/`
  - Body: `{"refresh": "<refresh_token>"}`
- **User Profile**: `GET /api/auth/me/`
  - Header: `Authorization: Bearer <access_token>`

## 📦 Core Endpoints

### 1. Categories
- `GET /api/categories/` - Retrieve list of all categories with product counts.
- `POST /api/categories/` - Create a category (Admin only).

### 2. Products
- `GET /api/products/` - List products with optional search and category filters.
- `GET /api/products/{id}/` - Retrieve single product details with variants and reviews.
- `POST /api/products/` - Create new product (Admin only).

### 3. Cart & Orders
- `GET /api/cart/` - Retrieve active user cart items.
- `POST /api/cart/` - Add item to cart.
- `POST /api/checkout/` - Process order checkout from cart.

## 🛠️ Management Commands
- `python manage.py seed_data` - Populate initial categories, products, and admin accounts.
