// utils.js
import {
  validateEmail,
  validatePhoneNumber,
  formatPhoneNumberWithCountryCode,
} from "@/features/lib/validators";

export const getUserIdentifierWithUnformattedPhone = (
  email: string,
  phoneNumber: string,
  countryCode: string
) => {
  const formattedPhoneNumber = formatPhoneNumberWithCountryCode(
    countryCode,
    phoneNumber
  );

  const constructedIdentifier = validateEmail(email)
    ? email
    : validatePhoneNumber(formattedPhoneNumber)
    ? formattedPhoneNumber
    : null;

  return constructedIdentifier;
};

export const getUserIdentifierWithFormattedPhone = (
  email: string,
  phone: string
) => {
  const constructedIdentifier = validateEmail(email)
    ? email
    : validatePhoneNumber(phone)
    ? phone
    : null;

  return constructedIdentifier;
};
