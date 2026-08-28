# Nexus Tech Store - REST API Specification

This document details the REST API endpoints available in the Nexus Tech Store backend powered by Django REST Framework and JWT Authentication.

---

## Base URL
```
http://localhost:8000/api/
```

## Authentication & Authorization

Protected endpoints require a JSON Web Token passed in the `Authorization` header:
```http
Authorization: Bearer <access_token>
```

---

## Endpoints Overview

### 1. Authentication (`/api/auth/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user account | No |
| `POST` | `/api/auth/login/` | Authenticate and obtain JWT tokens | No |
| `POST` | `/api/auth/refresh/` | Refresh expired access token | No |
| `GET` | `/api/auth/profile/` | Retrieve current authenticated user profile | Yes |
| `PUT/PATCH` | `/api/auth/profile/` | Update current user profile | Yes |

#### Registration Payload Example:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

### 2. Categories & Products (`/api/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/categories/` | List all product categories | No |
| `GET` | `/api/categories/<id>/` | Retrieve specific category details | No |
| `GET` | `/api/products/` | List products (supports `search`, `category`, `featured`, `ordering`) | No |
| `GET` | `/api/products/<id>/` | Retrieve specific product details | No |
| `POST` | `/api/products/` | Create product | Admin |
| `PUT/PATCH` | `/api/products/<id>/` | Update product | Admin |
| `DELETE` | `/api/products/<id>/` | Remove product | Admin |

---

### 3. Reviews (`/api/products/<id>/reviews/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/products/<id>/reviews/` | List all customer reviews for product | No |
| `POST` | `/api/products/<id>/reviews/` | Submit a product review (rating 1-5 & comment) | Yes |

---

### 4. Orders & Checkout (`/api/orders/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/orders/` | List current user's order history | Yes |
| `POST` | `/api/orders/` | Place a new order with cart items | Yes |
| `GET` | `/api/orders/<id>/` | Retrieve single order details | Yes |
| `PATCH` | `/api/orders/<id>/status/` | Update order status (Pending, Processing, Shipped, Delivered) | Admin |

---

### 5. Admin Dashboard Analytics (`/api/admin/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/admin/metrics/` | Fetch aggregated revenue, order count, user count | Admin |
| `GET` | `/api/admin/recent-orders/` | List recent customer transactions | Admin |
| `GET` | `/api/admin/inventory-alerts/` | List items with low stock quantities | Admin |
