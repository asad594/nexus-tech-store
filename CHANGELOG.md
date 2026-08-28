# 📜 Changelog

All notable changes to the Nexus Tech Store project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-08-29

### Added
- **Backend Response Time Middleware**: Added `ResponseTimeMiddleware` providing request duration monitoring and `X-Process-Time-ms` headers.
- **Dynamic Pagination**: Added `NexusStandardPagination` supporting customizable `page_size` query limits.
- **Signals & Auditing**: Added product stock monitoring signals (`signals.py`) for low-inventory alerts.
- **Management Commands**: Added `export_catalog` for JSON snapshots and `check_integrity` for database health diagnostics.
- **Security Hardening Guide**: Created `backend/SECURITY_CONFIG.md` for production HSTS, SSL, and CORS setup.
- **Advanced Frontend Hooks**: Added `useMediaQuery`, `useBreakpoints`, `useClipboard`, `useIntersectionObserver`, and `useOnClickOutside`.
- **UI Components & Motion**: Added `Badge` (with 6 glowing status themes), `BackToTop` floating button, `Toast` HUD notification system, and Framer Motion animation presets (`animations.js`).
- **Developer Automation**: Added root `Makefile` for one-line environment initialization and task running.
- **Expanded Test Coverage**: Added automated tests for products filtering, wishlist management, cart operations, and diagnostic endpoints.

## [1.1.0] - 2026-08-28

### Added
- **Continuous Integration (CI/CD)**: GitHub Actions workflows for frontend builds, backend test runners, and CodeQL security analysis.
- **Docker Containerization**: Multi-stage Dockerfiles for backend and frontend with unified `docker-compose.yml`.
- **System Diagnostics**: Detailed `/api/diagnostics/` endpoint providing database connection and uptime metrics.
- **Backend Domain Constants & Standard Responses**: Centralized status enums, response envelopes, and custom DRF exception handling.
- **Demo Seeder**: Lightweight `seed_demo_data` Django management command for fast sandbox setup.
- **Extended Test Suite**: Unit test suites for serializers, authentication, order processing, and review aggregations.
- **Frontend Custom Hook Suite**: Added `useLocalStorage`, `useDebounce`, `useWindowSize`, `useDocumentTitle`, and `useScrollLock`.
- **Frontend Components & Helpers**: Added `ErrorBoundary`, `SkeletonLoader`, formatters, and validators.
- **Project Governance & Tooling**: Added MIT `LICENSE`, `CODE_OF_CONDUCT.md`, `.editorconfig`, `.prettierrc`, and GitHub Issue/PR templates.

## [1.0.0] - 2026-08-11

### Added
- **Dark Glassmorphism UI**: High performance React storefront with Lenis scroll integration.
- **Scroll Video Hero**: Interactive canvas frame scrubbing for flagship laptop and audio products.
- **Django REST Framework Backend**: Complete REST API with JWT authentication (`simplejwt`).
- **Catalog Seed Management**: Seed command populating 30 authentic laptop models, accessories, and user profiles.
- **Admin Dashboard**: Real-time sales statistics, stock qty management, product editing, and order status updates.
- **Health Check Endpoint**: `/api/health/` status monitoring endpoint.
- **Comprehensive Documentation**: Setup guides, architecture schemas (`ARCHITECTURE.md`), security notes (`SECURITY.md`), and contributing guidelines (`CONTRIBUTING.md`).
- **Unit Test Suite**: Backend test cases covering Django models, API viewsets, and helper utility calculations.
