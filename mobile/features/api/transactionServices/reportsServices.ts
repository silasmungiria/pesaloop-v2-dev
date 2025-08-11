import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";

export interface PaginationMetadata {
  count: number;
  total_pages: number;
  current_page: number;
  next: string | null;
  previous: string | null;
}

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface Currency {
  code: string;
  name: string;
}

export interface Wallet {
  id: string;
  wallet_owner: User;
  currency: Currency;
}

export interface ExchangeRecord {
  id: string;
  user: User;
  source_currency: string;
  target_currency: string;
  source_amount: string;
  platform_exchange_rate: string;
  converted_amount_with_fee: string;
  charged_amount: string;
  charged_amount_currency: string;
  reference_id: string;
  transaction_type: string;
  status: string;
  is_debit: boolean;
  payment_provider: string;
  metadata: any | null;
  created_at: string;
  updated_at: string;
}

export interface PaymentRequest {
  id: string;
  requesting_user: User;
  requested_user: User;
  amount: number;
  reference_id: string;
  currency: string;
  is_debit: boolean;
  status: string;
  action: string | null;
  payment_provider: string;
  reason: string;
  transaction_type: string;
  created_at: string;
  updated_at: string;
}

export interface TransactionRecord {
  id: string;
  sender_wallet: Wallet;
  receiver_wallet: Wallet;
  amount: number;
  currency: string;
  reference_id: string;
  transaction_charge: string | null;
  transaction_type: string;
  is_debit: boolean;
  status: string;
  payment_provider: string;
  reason: string;
  created_at: string;
  updated_at: string;
}

export interface AccountActivitiesResults {
  exchange_records: ExchangeRecord[];
  transfer_requests: PaymentRequest[];
  transaction_records: TransactionRecord[];
}

export interface ActivitiesResponse {
  metadata: PaginationMetadata;
  results: AccountActivitiesResults;
}

export const fetchAccountActivitiesReport = async () => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<ActivitiesResponse>("get", "/reports/account/activities/");
};
