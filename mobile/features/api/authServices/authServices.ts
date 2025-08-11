import { apiRequest } from "@/features/api/apiClient";
import {
  SignupData,
  VerifyUserData,
  ResendOTPData,
  ForgotPasswordData,
  LoginPasswordData,
  AuthResponseMessage,
  VerifyUserResponse,
  LoginResponse,
} from "@/types";

export const signupUser = async (data: SignupData) => {
  return apiRequest<AuthResponseMessage>("post", "/auth/register/", data);
};

export const verifyUser = async (data: VerifyUserData) => {
  return apiRequest<VerifyUserResponse>(
    "post",
    "/auth/account/activation/otp/activate/",
    data
  );
};

export const resendOTP = async (data: ResendOTPData) => {
  return apiRequest<AuthResponseMessage>(
    "post",
    "/auth/account/activation/resend/otp/",
    data
  );
};

export const forgotPassword = async (data: ForgotPasswordData) => {
  return apiRequest<AuthResponseMessage>(
    "post",
    "/auth/password/forgot/",
    data
  );
};

export const loginPassword = async (data: LoginPasswordData) => {
  return apiRequest<LoginResponse>("post", "/auth/token/create/", data);
};

export const revokeAuthToken = async (refreshToken: string) => {
  return apiRequest<AuthResponseMessage>("post", "/auth/token/logout/", {
    refresh: refreshToken,
  });
};
