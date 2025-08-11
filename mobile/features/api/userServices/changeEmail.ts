import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

interface ChangeEmail {
  email: string;
  currentPassword: string;
}

export const changeEmail = async (data: ChangeEmail) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ message: string }>(
    "post",
    "/users/security/change-email/",
    data
  );
};
