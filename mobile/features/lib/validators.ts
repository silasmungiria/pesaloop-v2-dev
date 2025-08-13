// validators.ts

// Validate first name (non-empty and contains only letters)
export const validateFirstName = (firstName: string) => {
  return /^[a-zA-Z]+(?: [a-zA-Z]+)*$/.test(firstName.trim());
};

// Validate last name (non-empty and contains only letters)
export const validateLastName = (lastName: string) => {
  return /^[a-zA-Z]+(?: [a-zA-Z]+)*$/.test(lastName.trim());
};

// Validate country code (e.g., +1, +254)
export const validateCountryCode = (countryCode: string) => {
  return /^\+\d{1,4}$/.test(countryCode.trim());
};

// Validate phone number format
export const validatePhoneNumber = (phoneNumber: string) => {
  const phoneRegex = /^[+]?[0-9]{1,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}$/;
  return phoneRegex.test(phoneNumber.trim());
};

// Validate email address
export const validateEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
};

// Format phone number (e.g., +1 123 456 7890 becomes +11234567890)
export const formatPhoneNumberWithCountryCode = (
  countryCode: string,
  phoneNumber: string
) => {
  return `${countryCode}${phoneNumber}`.replace(/[\s\(\)\-]/g, "");
};

// Validate amount (decimal format, non-negative, up to two decimal places)
export const validateAmount = (amount: string) => {
  const amountRegex = /^\d+(\.\d{1,2})?$/;
  return amountRegex.test(amount) && parseFloat(amount) > 0;
};

// Format phone number (e.g., +1405-535-1262 becomes +14055351262)
export const sanitizePhoneNumber = (phoneNumber: string) => {
  return phoneNumber.replace(/[\s\(\)\-]/g, "");
};

// Format currency (e.g., 1234567.89 becomes 1,234,567.89)
export const formatCurrency = (value: number) => {
  return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

// Combine all validators into a single object for cleaner imports
export const validators = {
  validateFirstName,
  validateLastName,
  validateCountryCode,
  validatePhoneNumber,
  validateEmail,
  validateAmount,
  formatPhoneNumberWithCountryCode,
  formatCurrency,
};
