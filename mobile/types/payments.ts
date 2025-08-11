// types/payments.d.ts
import { Currency } from "./wallets";

export interface VerifyRecipientParams {
  email?: string;
  phone?: string;
}

export interface InitiateTransferParams {
  recipient_user: string;
  transfer_amount: string;
  reason: string;
}

export interface TransferRequestParams {
  requested_user: string;
  request_amount: string;
  reason: string;
}

export interface ActionTransferRequestParams {
  request_id: string;
  action: string;
}

export interface Wallet {
  wallet_id: string;
  wallet_owner: string;
  currency: Currency;
  is_default: boolean;
}

export interface User {
  id: string;
  full_name: string;
  email: string;
  phone_number: string;
  wallet: Wallet;
}

// Recipient verification
export interface VerifyRecipientResponse {
  email: string;
  first_name: string;
  id: string;
  last_name: string;
  phone_number: string;
}

export interface PaginationMetadata {
  count: number;
  total_pages: number;
  current_page: number;
  next: string | null;
  previous: string | null;
}

// Payment and transfer details
export interface TransferMetadata {
  payment_provider: string;
}

export interface Transfer {
  id: string;
  sender: User;
  recipient: User;
  amount: number;
  reference_id: string;
  transaction_charge: string;
  currency: string;
  status: string;
  type: string;
  metadata: TransferMetadata;
  created_at: string;
  updated_at: string;
}

// Payment and transfer details
interface ResponseWallet {
  wallet_id: string;
  wallet_owner: string;
  currency: string;
  currency_name: string;
  is_default: boolean;
}

export interface InitiateTransferResponse {
  id: string;
  sender_wallet: ResponseWallet;
  receiver_wallet: ResponseWallet;
  amount: number;
  currency: string;
  status: string;
  reference_id: string;
  transaction_charge: string;
  transaction_type: string;
  payment_provider: string;
  reason: string;
  created_at: string;
  updated_at: string;
}

// Transfer Requests
export interface TransfersResponse {
  metadata: PaginationMetadata;
  results: Transfer[];
}

export interface UserProfile {
  id: string;
  full_name: string;
  email: string;
  phone_number: string;
}

export interface TransferRequest {
  id: string;
  requesting_user: UserProfile;
  requested_user: UserProfile;
  amount: string;
  currency: string;
  status: string;
  reference_id: string;
  payment_provider: string;
  action: string;
  reason: string;
  created_at: string;
  updated_at: string;
}

export interface TransferRequestsResponse {
  metadata: PaginationMetadata;
  results: TransferRequest[];
}
