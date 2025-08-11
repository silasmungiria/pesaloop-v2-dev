import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

interface ChangePassword {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

export const changePassword = async (data: ChangePassword) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ message: string }>(
    "post",
    "/users/security/change-password/",
    data
  );
};
