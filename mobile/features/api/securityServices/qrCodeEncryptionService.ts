import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";
import { QRCodeProps } from "@/types";

export const encryptSensitiveData = async (data: QRCodeProps) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ encrypted_data: string }>(
    "post",
    "/media/qrcode/encrypt/",
    data
  );
};

export const decryptSensitiveData = async (encryptedData: string) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<{ decrypted_data: QRCodeProps }>(
    "post",
    "/media/qrcode/decrypt/",
    { data: encryptedData }
  );
};
