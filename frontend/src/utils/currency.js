/**
 * Currency, pricing, and number formatting utilities for Nexus Tech Store.
 */

/**
 * Formats a numeric value into a localized currency string.
 * @param {number|string} amount - The amount to format.
 * @param {string} currency - Currency code (default: 'USD').
 * @param {string} locale - Locale code (default: 'en-US').
 * @returns {string} Formatted currency string (e.g. '$1,299.00').
 */
export function formatPrice(amount, currency = 'USD', locale = 'en-US') {
  const num = typeof amount === 'string' ? parseFloat(amount) : Number(amount);
  if (isNaN(num)) return '$0.00';

  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
}

/**
 * Computes discount percentage savings between base and discounted prices.
 * @param {number} originalPrice - Base regular price.
 * @param {number} salePrice - Discounted price.
 * @returns {number} Integer discount percentage.
 */
export function calculateDiscount(originalPrice, salePrice) {
  const orig = Number(originalPrice);
  const sale = Number(salePrice);
  if (isNaN(orig) || isNaN(sale) || orig <= 0 || sale >= orig) return 0;
  return Math.round(((orig - sale) / orig) * 100);
}

/**
 * Formats large numeric amounts into compact readable format (e.g., '1.2K', '3.4M').
 * @param {number} number - The number to convert.
 * @returns {string} Compact string representation.
 */
export function formatCompactNumber(number) {
  const num = Number(number);
  if (isNaN(num)) return '0';
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'short',
    maximumFractionDigits: 1,
  }).format(num);
}

/**
 * Parses a currency string back into a pure float number.
 * @param {string} currencyStr - Formatted string (e.g. '$1,250.50').
 * @returns {number} Parsed float number.
 */
export function parseCurrencyToNumber(currencyStr) {
  if (typeof currencyStr !== 'string') return Number(currencyStr) || 0;
  const cleaned = currencyStr.replace(/[^0-9.-]+/g, '');
  const parsed = parseFloat(cleaned);
  return isNaN(parsed) ? 0 : parsed;
}

/**
 * Calculates cart totals including subtotals, calculated taxes, and free shipping tiers.
 * @param {Array<{ price: number, quantity: number }>} items
 * @param {number} taxRate - Default 0.08 (8%)
 * @param {number} freeShippingThreshold - Default $100
 * @param {number} baseShippingFee - Default $15
 * @returns {{ subtotal: number, tax: number, shipping: number, total: number, freeShippingRemaining: number }}
 */
export function calculateCartSummary(
  items = [],
  taxRate = 0.08,
  freeShippingThreshold = 100,
  baseShippingFee = 15
) {
  const subtotal = items.reduce((acc, item) => {
    const p = Number(item.price || item.price_at_purchase || 0);
    const q = Number(item.quantity || 1);
    return acc + p * q;
  }, 0);

  const shipping = subtotal >= freeShippingThreshold || subtotal === 0 ? 0 : baseShippingFee;
  const tax = Number((subtotal * taxRate).toFixed(2));
  const total = Number((subtotal + tax + shipping).toFixed(2));
  const freeShippingRemaining = Math.max(0, freeShippingThreshold - subtotal);

  return {
    subtotal: Number(subtotal.toFixed(2)),
    tax,
    shipping,
    total,
    freeShippingRemaining: Number(freeShippingRemaining.toFixed(2)),
    qualifiesForFreeShipping: subtotal >= freeShippingThreshold,
  };
}
