/**
 * Date and timestamp formatting utilities for Nexus Tech Store.
 */

/**
 * Formats a date into a human-readable string.
 * @param {Date|string|number} date - Date object or ISO string.
 * @param {Intl.DateTimeFormatOptions} options - Formatting options.
 * @param {string} locale - Locale string (default: 'en-US').
 * @returns {string} Formatted date string (e.g., 'Oct 14, 2026').
 */
export function formatDate(date, options = {}, locale = 'en-US') {
  if (!date) return '';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';

  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options,
  };

  return new Intl.DateTimeFormat(locale, defaultOptions).format(d);
}

/**
 * Formats a timestamp into a relative time description (e.g., '5 mins ago', 'yesterday').
 * @param {Date|string|number} date - Past date.
 * @returns {string} Relative time string.
 */
export function formatRelativeTime(date) {
  if (!date) return '';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';

  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - d.getTime()) / 1000);

  if (diffInSeconds < 0) return 'just now';
  if (diffInSeconds < 60) return `${diffInSeconds}s ago`;

  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`;

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours}h ago`;

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) return `${diffInDays}d ago`;

  const diffInMonths = Math.floor(diffInDays / 30);
  if (diffInMonths < 12) return `${diffInMonths}mo ago`;

  const diffInYears = Math.floor(diffInMonths / 12);
  return `${diffInYears}y ago`;
}

/**
 * Checks if a date has already passed.
 * @param {Date|string|number} date
 * @returns {boolean}
 */
export function isDateInPast(date) {
  if (!date) return false;
  const d = new Date(date);
  if (isNaN(d.getTime())) return false;
  return d.getTime() < Date.now();
}

/**
 * Formats date into standard ISO YYYY-MM-DD string.
 * @param {Date|string|number} date
 * @returns {string}
 */
export function formatIsoDate(date) {
  if (!date) return '';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';
  return d.toISOString().split('T')[0];
}
