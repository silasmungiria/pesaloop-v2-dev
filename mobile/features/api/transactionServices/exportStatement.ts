import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

export const exportTransactionStatement = async ({
  exportFormat,
  deliveryMethod,
}: {
  exportFormat: string;
  deliveryMethod: string;
}) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);

  const params = new URLSearchParams({
    export_format: exportFormat,
    delivery_method: deliveryMethod,
  });

  return apiRequest(
    "get",
    `reports/transactions/download/?${params.toString()}`,
    {
      responseType: "blob",
    }
  );
};
