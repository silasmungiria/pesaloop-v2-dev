import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

export interface MpesaSTKPushRequest {
  phone_number: string;
  amount: number;
  reason?: string;
  metadata?: Record<string, any>;
}

export const initiateMpesaSTKPush = async (data: MpesaSTKPushRequest) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ message: string }>(
    "post",
    "/mpesaservice/stk-push/top-up/",
    data
  );
};
