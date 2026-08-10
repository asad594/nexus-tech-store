# 🛡️ Nexus Tech Store Security Policy

## Authentication Architecture

Nexus Tech Store employs **JSON Web Tokens (JWT)** for authenticating API requests.

### Key Security Measures

1. **Password Hashing**: Django's PBKDF2 algorithm with SHA256 is used for secure password hashing.
2. **Role-Based Access Control (RBAC)**: Custom permissions (`IsAdminUserRole`, `IsOwnerOrAdmin`) prevent unauthorized access to sensitive endpoints.
3. **CORS Restrictions**: `django-cors-headers` restricts client origins strictly to trusted frontend domains.
4. **Token Expiration**: Access tokens expire after short intervals; refresh tokens are used for session renewal.

## Reporting Vulnerabilities

If you discover a security vulnerability, please send an email to `security@nexus.io` or open a confidential security advisory.
