// apis/paymentServices.ts

import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";
import { validateEmail, validatePhoneNumber } from "@/features/lib";
import {
  VerifyRecipientResponse,
  InitiateTransferResponse,
  TransfersResponse,
  TransferRequest,
  TransferRequestsResponse,
  VerifyRecipientParams,
  InitiateTransferParams,
  TransferRequestParams,
  ActionTransferRequestParams,
} from "@/types";

export const verifyRecipient = async (data: VerifyRecipientParams) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);

  let params = new URLSearchParams();
  if (data.email && validateEmail(data.email)) {
    params.append("email", data.email);
  } else if (data.phone && validatePhoneNumber(data.phone)) {
    params.append("phone", data.phone);
  } else {
    throw new Error("Invalid email or phone number format");
  }

  return apiRequest<VerifyRecipientResponse>(
    "get",
    `/payments/recipient/verify/?${params.toString()}`
  );
};

export const initiateTransfer = async (data: InitiateTransferParams) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<InitiateTransferResponse>(
    "post",
    "/payments/transactions/initiate/",
    data
  );
};

export const fetchTransactions = async () => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<TransfersResponse>("get", "/payments/transactions/");
};

export const initiateTransferRequest = async (data: TransferRequestParams) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<TransferRequest>(
    "post",
    "/payments/transfer-requests/initiate/",
    data
  );
};

export const fetchTransferRequests = async () => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<TransferRequestsResponse>(
    "get",
    "/payments/transfer-requests/"
  );
};

export const actionTransferRequest = async (
  data: ActionTransferRequestParams
) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<TransferRequest>(
    "post",
    "/payments/transfer-requests/action/",
    data
  );
};
