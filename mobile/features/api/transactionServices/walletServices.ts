// services/walletServices.ts

import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";
import {
  WalletResponse,
  WalletActionResponse,
  SetDefaultWalletData,
  ActivateWalletData,
} from "@/types";

export const fetchUserWallets = async () => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<WalletResponse>("get", "/wallets/wallets/");
};

export const setDefaultWallet = async (
  walletId: string,
  data: SetDefaultWalletData
) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<WalletActionResponse>(
    "put",
    `/wallets/wallets/${walletId}/set-default/`,
    data
  );
};

export const activateWallet = async (
  walletId: string,
  data: ActivateWalletData
) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<WalletActionResponse>(
    "put",
    `/wallets/wallets/${walletId}/activate/`,
    data
  );
};
