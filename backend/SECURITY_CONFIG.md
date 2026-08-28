# Security Configuration & Hardening Guide

This document outlines recommended security settings and configurations for production deployments of Nexus Tech Store.

---

## 1. Django Security Settings (`nexus_backend/settings.py`)

In production environments (`DEBUG=False`), ensure the following parameters are enabled:

```python
# Force HTTPS redirection
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Browser Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## 2. JWT Token Lifetime & Refresh Rotation

Configured via `SIMPLE_JWT`:
- **Access Tokens**: Short-lived (7 days in staging, recommended 15-60 minutes in enterprise production).
- **Refresh Tokens**: Long-lived (30 days) with token blacklisting and rotation enabled on every refresh request.

---

## 3. CORS & Origin Whitelisting

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://your-production-domain.com",
]
```
