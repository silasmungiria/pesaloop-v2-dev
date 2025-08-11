export interface ExchangeRequest {
  source_currency: string;
  target_currency: string;
  source_amount: string;
}

export interface PreviewExchangeResponse {
  source_currency: string;
  target_currency: string;
  source_amount: number;
  platform_exchange_rate: number;
  charged_amount: number;
  converted_amount_with_fee: number;
}

export interface ExecuteExchangeResponse {
  message: string;
}

export interface SupportedCurrenciesResponse {
  count: number;
  next: string;
  previous: string;
  results: {
    id: string;
    name: string;
    code: string;
  }[];
}
