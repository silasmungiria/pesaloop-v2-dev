import Constants from "expo-constants";

// ───────────────────────────────
// App Information
// ───────────────────────────────
export const appInfo = {
  APP_VERSION: Constants.expoConfig?.version,
  APP_NAME: Constants.expoConfig?.extra?.app_name,
  MIN_AGE: Constants.expoConfig?.extra?.app_minimum_age,
  APP_BUILD_NUMBER: Constants.expoConfig?.extra?.app_build_number,
};

// ───────────────────────────────
// API Configuration
// ───────────────────────────────
export const apiConfig = {
  AUTH_HEADER: Constants.expoConfig?.extra?.authorization_header,
  AUTH_SCHEME: Constants.expoConfig?.extra?.authentication_scheme,
  BASE_URL: Constants.expoConfig?.extra?.api_base_url,
  REFRESH_PATH: Constants.expoConfig?.extra?.api_refresh_path,
  RETRY: Constants.expoConfig?.extra?.api_retry,
  WIN_FOCUS_REFETCH: Constants.expoConfig?.extra?.api_win_focus_refetch,
  CONTENT_TYPE: Constants.expoConfig?.extra?.api_content_type,
  ACCEPT_TYPE: Constants.expoConfig?.extra?.api_accept_type,
};
