/**
 * Input & Form Validation Utilities
 * Lightweight validation helpers for client-side forms and UI fields.
 */

export const isValidEmail = (email) => {
  if (!email || typeof email !== 'string') return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
};

export const isValidPassword = (password, minLength = 6) => {
  if (!password || typeof password !== 'string') return false;
  return password.length >= minLength;
};

export const isValidPhoneNumber = (phone) => {
  if (!phone) return true; // Optional field
  const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s./0-9]*$/;
  return phoneRegex.test(phone.trim());
};

export const validateRequiredFields = (formData, requiredKeys = []) => {
  const errors = {};
  requiredKeys.forEach((key) => {
    const value = formData[key];
    if (value === undefined || value === null || (typeof value === 'string' && value.trim() === '')) {
      errors[key] = 'This field is required.';
    }
  });
  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};
