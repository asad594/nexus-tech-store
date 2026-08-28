# Frontend Architecture & Design Guide

Nexus Tech Store's frontend is constructed with React 19, Tailwind CSS v4, Framer Motion, and Lenis Smooth Scroll.

---

## Directory Structure Overview

```
frontend/src/
├── assets/          # Static brand icons and images
├── components/      # Modular, reusable presentation components
│   ├── AdminDashboard.jsx
│   ├── AuthModal.jsx
│   ├── CartDrawer.jsx
│   ├── CheckoutModal.jsx
│   ├── HeroSection.jsx
│   ├── Navbar.jsx
│   ├── ProductCard.jsx
│   ├── ProductCarousel.jsx
│   ├── ProductDetailModal.jsx
│   └── ScrollVideoHero.jsx
├── context/         # Global state providers
│   ├── AuthContext.jsx   # User authentication, tokens, roles
│   ├── CartContext.jsx   # Local storage cart items, totals
│   └── LenisContext.jsx  # Smooth inertia scroll synchronization
├── pages/           # High-level route views
│   ├── AdminPage.jsx
│   ├── CartPage.jsx
│   ├── CheckoutPage.jsx
│   ├── HomePage.jsx
│   ├── LoginPage.jsx
│   ├── OrdersPage.jsx
│   ├── ProductDetailPage.jsx
│   ├── ProductsPage.jsx
│   └── RegisterPage.jsx
├── App.jsx          # Top-level Router layout and Provider wrapping
└── main.jsx         # DOM Mounting entry point
```

---

## State Management Principles
1. **Auth Context**: Persists JWT Access and Refresh tokens in `localStorage`. Automatically handles token validation and role-based route guarding.
2. **Cart Context**: Reactive cart state saved in `localStorage`. Provides methods `addToCart`, `removeFromCart`, `updateQuantity`, and `clearCart`.
3. **Smooth Scrolling**: Lenis virtual scrolling handles frame-accurate canvas and video playback scrub synchronization on the landing page.

---

## Styling Architecture
- **Theme Palette**: Deep dark cyber aesthetics (`#0a0a0f`, `#12121e`) accented with neon cyan (`#00f0ff`) and electric purple (`#7000ff`).
- **Glassmorphism**: Backdrop blur filters (`backdrop-blur-xl`), translucent dark borders (`border-white/10`), and subtle radial gradient glows.
