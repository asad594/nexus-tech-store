/**
 * Application Constants
 * Centralized mapping for navigation routes, local storage keys, and API defaults.
 */

export const APP_ROUTES = {
  HOME: '/',
  PRODUCTS: '/products',
  PRODUCT_DETAIL: '/products/:id',
  CART: '/cart',
  CHECKOUT: '/checkout',
  ORDERS: '/orders',
  LOGIN: '/login',
  REGISTER: '/register',
  ADMIN: '/admin',
};

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'nexus_access_token',
  REFRESH_TOKEN: 'nexus_refresh_token',
  USER: 'nexus_user',
  CART: 'nexus_cart',
  THEME: 'nexus_theme',
};

export const ORDER_STATUS_LABELS = {
  pending: 'Pending Approval',
  processing: 'Processing Order',
  shipped: 'Shipped & En Route',
  delivered: 'Delivered',
  cancelled: 'Cancelled',
};

export const ORDER_STATUS_COLORS = {
  pending: 'text-amber-400 border-amber-500/30 bg-amber-500/10',
  processing: 'text-cyan-400 border-cyan-500/30 bg-cyan-500/10',
  shipped: 'text-blue-400 border-blue-500/30 bg-blue-500/10',
  delivered: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
  cancelled: 'text-rose-400 border-rose-500/30 bg-rose-500/10',
};
