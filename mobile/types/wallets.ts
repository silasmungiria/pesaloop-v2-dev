export interface WalletOwner {
  user_id: string;
  name: string;
  email: string;
  phone_number: string;
}

export interface Currency {
  name: string;
  code: string;
}

export interface DefaultWallet {
  id: string;
  wallet_owner: WalletOwner;
  balance: number;
  currency: Currency;
  is_default: boolean;
  is_active: boolean;
  last_updated: string;
  created_at: string;
}

export interface WalletMetadata {
  count: number;
  total_pages: number;
  current_page: number;
  next: null;
  previous: null;
}

export interface WalletResponse {
  metadata: WalletMetadata;
  results: DefaultWallet[];
}

export interface WalletActionResponse {
  message: string;
}

export interface SetDefaultWalletData {
  is_default: boolean;
}

export interface ActivateWalletData {
  is_active: boolean;
}
