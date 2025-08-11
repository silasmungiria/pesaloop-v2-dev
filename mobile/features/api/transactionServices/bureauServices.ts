import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";
import {
  ExchangeRequest,
  PreviewExchangeResponse,
  ExecuteExchangeResponse,
  SupportedCurrenciesResponse,
} from "@/types";

export const previewExchange = async (data: ExchangeRequest) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  // Log response data
  return apiRequest<PreviewExchangeResponse>(
    "post",
    "/forex/exchange/preview/",
    data
  );
};

export const executeExchange = async (data: ExchangeRequest) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<ExecuteExchangeResponse>(
    "post",
    "/forex/exchange/execute/",
    data
  );
};

export const fetchCurrencies = async () => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<SupportedCurrenciesResponse>("get", "/wallets/currencies/");
};
