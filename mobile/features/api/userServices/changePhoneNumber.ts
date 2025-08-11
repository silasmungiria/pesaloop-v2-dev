import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

interface ChangePhoneNumber {
  phoneNumber: string;
  currentPassword: string;
}

export const changePhoneNumber = async (data: ChangePhoneNumber) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ message: string }>(
    "post",
    "/users/security/change-phone-number/",
    data
  );
};
