import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

export interface NotificationPreferences {
  use_sms: boolean;
}

export const updateNotificationPreferences = async (
  data: NotificationPreferences
) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ message: string; use_sms: boolean }>(
    "post",
    "/users/preferences/notification",
    data
  );
};
