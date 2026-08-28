/**
 * Frontend Formatting Utilities
 * Provides formatting functions for prices, currencies, dates, and numbers.
 */

export const formatCurrency = (amount, currency = 'USD') => {
  const numericAmount = Number(amount) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numericAmount);
};

export const formatDate = (dateString, options = {}) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options,
  }).format(date);
};

export const calculateDiscountPercentage = (originalPrice, discountedPrice) => {
  const orig = Number(originalPrice);
  const disc = Number(discountedPrice);
  if (!orig || !disc || disc >= orig) return 0;
  return Math.round(((orig - disc) / orig) * 100);
};

export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text || '';
  return `${text.slice(0, maxLength)}...`;
};
