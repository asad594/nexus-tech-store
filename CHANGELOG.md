# 📜 Changelog

All notable changes to the Nexus Tech Store project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-08-31

### Added
- **SKU & Discount Utilities**: Added `validate_sku_format`, `calculate_discount_percentage`, `apply_discount`, and `generate_order_reference` with test coverage in `backend/store/utils.py`.
- **Frontend Text & String Toolkit**: Added `truncateText`, `capitalize`, `slugify`, `stripHtml`, `maskEmail`, `formatBytes`, and `pluralize` in `frontend/src/utils/text.js`.
- **API Request Throttling**: Added DRF rate-limiting classes (`BurstRateThrottle`, `SustainedRateThrottle`, `AuthRateThrottle`, `OrderCreationThrottle`) in `backend/store/throttling.py`.
- **Keyboard Shortcut Hooks**: Added `useKeyPress` and `useHotkeys` in `frontend/src/hooks/useKeyPress.js`.
- **Serializer Test Suite**: Expanded unit tests covering `ProductSerializer`, `OrderItemSerializer`, and registration edge cases.
- **Store Sales Report Command**: Added `sales_report` management command calculating revenue, order volumes, and average order values with `--json` export support.
- **Financial & Currency Helpers**: Added `formatPrice`, `calculateDiscount`, `formatCompactNumber`, and `calculateCartSummary` in `frontend/src/utils/currency.js`.
- **Custom Model QuerySets**: Added `ProductQuerySet` and `OrderQuerySet` in `backend/store/managers.py`.
- **Timing & Declarative Interval Hooks**: Added `useInterval` and `useTimeout` hooks with automatic lifecycle teardown.
- **Cart Maintenance Command**: Added `prune_stale_carts` command with `--dry-run` and `--days` options.
- **RatingStars Component**: Added accessible interactive and presentation star rating UI component in `frontend/src/components/RatingStars.jsx`.
- **Command Test Suite**: Added automated tests for all management commands in `backend/store/tests/test_commands.py`.
- **Network Status Hook**: Added `useOnlineStatus` hook monitoring real-time browser connectivity.
- **Structured Error Handling**: Added domain exceptions and structured error envelopes in `backend/store/exceptions.py`.
- **Tooltip Component**: Added floating dark-glassmorphism tooltip component in `frontend/src/components/Tooltip.jsx`.
- **Repository Quality Tooling**: Added `.pre-commit-config.yaml` and `.github/workflows/markdown-lint.yml`.
- **Persistent Storage Wrapper**: Added `safeGet`, `safeSet` with TTL expiry, and in-memory fallbacks in `frontend/src/utils/storage.js`.
- **Health Check Latency Metrics**: Enhanced `/api/diagnostics/` with real-time database query latency metrics.
- **OpenAPI 3.0.3 Specification**: Created `backend/API_SPECIFICATION.json` covering all REST endpoints, schemas, and parameters.

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
