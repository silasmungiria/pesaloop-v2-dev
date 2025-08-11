import axios, { AxiosError, AxiosRequestConfig } from "axios";
import { QueryClient } from "@tanstack/react-query";
import { useSessionStore, useLogoutCleanup } from "@/features/store";

// Environment variables with fallbacks
const API_BASE_URL = process.env.API_BASE_URL ?? "https://api.pesaloop.com";
const API_RETRY = Number(process.env.API_RETRY ?? 3);
const API_WIN_FOCUS_REFETCH = process.env.API_WIN_FOCUS_REFETCH === "true";
const API_CONTENT_TYPE = process.env.API_CONTENT_TYPE ?? "application/json";
const API_ACCEPT_TYPE = process.env.API_ACCEPT_TYPE ?? "application/json";
const API_REFRESH_PATH = process.env.API_REFRESH_PATH ?? "/auth/refresh/";
const API_AUTH_KEY = process.env.API_AUTH_KEY ?? "Authorization";

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

interface ApiError {
  message?: string;
  error?: string;
  [key: string]: unknown;
}

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": API_CONTENT_TYPE,
    Accept: API_ACCEPT_TYPE,
  },
});

// Auth token management
export const setAuthorizationHeader = (accessToken: string | null): void => {
  if (accessToken) {
    axiosInstance.defaults.headers.common[
      API_AUTH_KEY
    ] = `Bearer ${accessToken}`;
  } else {
    delete axiosInstance.defaults.headers.common[API_AUTH_KEY];
  }
};

// Token refresh mechanism
let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

const onRefreshed = (token: string): void => {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
};

const refreshAccessToken = async (): Promise<string> => {
  const { refreshToken, setAccessToken, setRefreshToken } =
    useSessionStore.getState();
  const { performSessionLogout } = useLogoutCleanup();

  if (isRefreshing || !refreshToken) {
    throw new Error("No refresh token available");
  }

  isRefreshing = true;

  try {
    const response = await axios.post<{ access: string; refresh: string }>(
      `${API_BASE_URL}${API_REFRESH_PATH}`,
      { refresh: refreshToken }
    );

    const { access: newAccessToken, refresh: newRefreshToken } = response.data;

    setAccessToken(newAccessToken);
    setRefreshToken(newRefreshToken);
    setAuthorizationHeader(newAccessToken);

    onRefreshed(newAccessToken);
    return newAccessToken;
  } catch (error) {
    await performSessionLogout();
    console.error("Failed to refresh token. Logging out.");
    throw new Error("Session expired. Please log in again.");
  } finally {
    isRefreshing = false;
  }
};

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    if (!error.response) {
      console.error("Network error:", error.message);
      return Promise.reject(
        new Error("Network error. Please check your connection.")
      );
    }

    const { status, data, config } = error.response;
    const originalRequest = config;

    if (status === 401) {
      const { setSession, refreshToken } = useSessionStore.getState();

      if (!refreshToken) {
        setSession(false);
        return Promise.reject(new Error("Authentication required."));
      }

      if (!isRefreshing) {
        try {
          const newToken = await refreshAccessToken();
          if (originalRequest.headers) {
            originalRequest.headers[API_AUTH_KEY] = `Bearer ${newToken}`;
          }
          return axiosInstance(originalRequest);
        } catch (refreshError) {
          return Promise.reject(refreshError);
        }
      }

      return new Promise((resolve) => {
        refreshSubscribers.push((token: string) => {
          if (originalRequest.headers) {
            originalRequest.headers[API_AUTH_KEY] = `Bearer ${token}`;
          }
          resolve(axiosInstance(originalRequest));
        });
      });
    }

    const errorMessages: Record<number, string> = {
      400: data?.message || data?.error || "Invalid request.",
      404: data?.message || "The requested resource was not found.",
      500: data?.message || "Internal server error. Please try again later.",
    };

    if (errorMessages[status]) {
      console.error(`${status} error:`, errorMessages[status]);
      return Promise.reject(new Error(errorMessages[status]));
    }

    return Promise.reject(
      new Error(data?.message || "An unknown error occurred")
    );
  }
);

// API request helper
export const apiRequest = async <T>(
  method: "get" | "post" | "put" | "patch" | "delete",
  url: string,
  data?: unknown,
  config?: AxiosRequestConfig
): Promise<ApiResponse<T>> => {
  try {
    const response = await axiosInstance.request<T>({
      method,
      url,
      data,
      ...config,
    });

    return {
      success: true,
      data: response.data,
      message: (response.data as any)?.message || "Request successful",
    };
  } catch (error) {
    console.error("Request failed:", error);
    throw error;
  }
};

// Query client configuration
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: API_RETRY,
      refetchOnWindowFocus: API_WIN_FOCUS_REFETCH,
    },
  },
});

export default axiosInstance;
