// types/auth.ts

export interface SignupData {
  first_name: string;
  last_name: string;
  country_code: string;
  phone_number: string;
  email: string;
  password: string;
}

export interface VerifyUserData {
  identifier: string;
  otp: string;
}

export interface ResendOTPData {
  identifier: string;
}

export interface ForgotPasswordData {
  identifier: string;
}

export interface LoginPasswordData {
  identifier: string;
  password: string;
  send_otp: boolean;
  with_profile: boolean;
}

export interface AuthResponseMessage {
  message: string;
}

export interface UserVerificationStatus {
  is_email_verified: boolean;
  is_phone_verified: boolean;
}

export interface VerifyUserResponse extends AuthResponseMessage {
  user_verified?: UserVerificationStatus;
}

export interface SessionUser {
  account_number: string;
  email: string;
  is_email_verified: boolean;
  first_name: string;
  is_active: boolean;
  is_verified: boolean;
  last_name: string;
  phone_number: string;
  is_phone_verified: boolean;
  is_loan_qualified: boolean;
}

export interface CustomerProfile {
  id: string;
  id_type: string;
  id_number: string;
  selfie_image_url: string;
  is_id_front_uploaded: boolean;
  is_id_back_uploaded: boolean;
  is_face_uploaded: boolean;
  is_address_proof_image_uploaded: boolean;
  is_selfie_image_verified: boolean;
  is_id_front_verified: boolean;
  is_id_back_verified: boolean;
  is_address_proof_image_verified: boolean;
  verification_status: string;
  customer_verified: boolean;
  verification_date: string;
  remarks: string;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  user: SessionUser;
  customerProfile: CustomerProfile;
  access: string;
  refresh: string;
  message: string;
  success: boolean;
}
