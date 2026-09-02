/**
 * Numeric and mathematical calculation helpers for animations, sliders, and statistics.
 */

/**
 * Clamps a number between a minimum and maximum boundary.
 * @param {number} value - The input value.
 * @param {number} min - Lower bound.
 * @param {number} max - Upper bound.
 * @returns {number} Clamped value.
 */
export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Linearly interpolates between two numbers.
 * @param {number} start - Beginning value.
 * @param {number} end - Target value.
 * @param {number} t - Interpolation factor (0 to 1).
 * @returns {number} Interpolated value.
 */
export function lerp(start, end, t) {
  return start * (1 - t) + end * t;
}

/**
 * Rounds a number to a specified decimal precision.
 * @param {number} value - The number to round.
 * @param {number} decimals - Decimal places (default: 2).
 * @returns {number} Rounded number.
 */
export function roundToPrecision(value, decimals = 2) {
  const factor = Math.pow(10, decimals);
  return Math.round((Number(value) + Number.EPSILON) * factor) / factor;
}

/**
 * Calculates percentage of a value relative to a total.
 * @param {number} value - Partial value.
 * @param {number} total - Total base value.
 * @param {number} decimals - Precision decimals.
 * @returns {number} Percentage value (0-100).
 */
export function calculatePercentage(value, total, decimals = 1) {
  if (!total || total === 0) return 0;
  const pct = (Number(value) / Number(total)) * 100;
  return roundToPrecision(pct, decimals);
}

/**
 * Checks if a value is strictly within a numeric range.
 * @param {number} value
 * @param {number} min
 * @param {number} max
 * @returns {boolean}
 */
export function inRange(value, min, max) {
  return value >= min && value <= max;
}

/**
 * Maps a number from one range to another.
 * @param {number} value
 * @param {number} inMin
 * @param {number} inMax
 * @param {number} outMin
 * @param {number} outMax
 * @returns {number}
 */
export function mapRange(value, inMin, inMax, outMin, outMax) {
  return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
}
