/**
 * String and text manipulation utility functions for Nexus Tech Store.
 */

/**
 * Truncates a string to a specified max length and appends an ellipsis.
 * @param {string} text - The input text to truncate.
 * @param {number} maxLength - Maximum allowable length.
 * @param {string} suffix - Suffix to append (default: '...').
 * @returns {string} Truncated string.
 */
export function truncateText(text, maxLength = 80, suffix = '...') {
  if (!text || typeof text !== 'string') return '';
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength).trim()}${suffix}`;
}

/**
 * Capitalizes the first letter of a string or words.
 * @param {string} text - The input string.
 * @param {boolean} allWords - Whether to capitalize every word.
 * @returns {string} Capitalized string.
 */
export function capitalize(text, allWords = false) {
  if (!text || typeof text !== 'string') return '';
  if (allWords) {
    return text.replace(/\b\w/g, (char) => char.toUpperCase());
  }
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/**
 * Converts a string into a URL-friendly slug.
 * @param {string} text - The input string.
 * @returns {string} Slugified string.
 */
export function slugify(text) {
  if (!text || typeof text !== 'string') return '';
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * Strips HTML tags from an input string.
 * @param {string} html - HTML string.
 * @returns {string} Clean plain text.
 */
export function stripHtml(html) {
  if (!html || typeof html !== 'string') return '';
  return html.replace(/<[^>]*>?/gm, '');
}

/**
 * Masks an email address for privacy display (e.g. j***@domain.com).
 * @param {string} email - Email address.
 * @returns {string} Masked email.
 */
export function maskEmail(email) {
  if (!email || !email.includes('@')) return email || '';
  const [username, domain] = email.split('@');
  if (username.length <= 2) {
    return `${username[0]}***@${domain}`;
  }
  return `${username[0]}${'*'.repeat(username.length - 2)}${username.slice(-1)}@${domain}`;
}

/**
 * Formats a byte size into human-readable representation.
 * @param {number} bytes - Number of bytes.
 * @param {number} decimals - Number of decimal places.
 * @returns {string} Formatted size (e.g., '1.5 MB').
 */
export function formatBytes(bytes, decimals = 2) {
  if (!bytes || bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

/**
 * Pluralizes a word based on count.
 * @param {number} count - Item count.
 * @param {string} singular - Singular form.
 * @param {string} plural - Plural form (optional).
 * @returns {string} Formatted count and word.
 */
export function pluralize(count, singular, plural = `${singular}s`) {
  return `${count} ${count === 1 ? singular : plural}`;
}
