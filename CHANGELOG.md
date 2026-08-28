# 📜 Changelog

All notable changes to the Nexus Tech Store project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
