import axios, { AxiosError, AxiosRequestConfig } from "axios";
import { QueryClient } from "@tanstack/react-query";

import { apiConfig } from "@/features/constants";
import { useSessionStore, useLogoutCleanup } from "@/features/store";
import { ApiResponse, ApiError } from "@/types";

const axiosInstance = axios.create({
  baseURL: apiConfig.BASE_URL,
  headers: {
    "Content-Type": apiConfig.CONTENT_TYPE,
    Accept: apiConfig.ACCEPT_TYPE,
  },
});

// Auth token management
export const setAuthorizationHeader = (accessToken: string | null): void => {
  if (accessToken) {
    axiosInstance.defaults.headers.common[
      apiConfig.AUTH_HEADER
    ] = `${apiConfig.AUTH_SCHEME} ${accessToken}`;
  } else {
    delete axiosInstance.defaults.headers.common[apiConfig.AUTH_HEADER];
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
      `${apiConfig.BASE_URL}${apiConfig.REFRESH_PATH}`,
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
            originalRequest.headers[
              apiConfig.AUTH_HEADER
            ] = `${apiConfig.AUTH_SCHEME} ${newToken}`;
          }
          return axiosInstance(originalRequest);
        } catch (refreshError) {
          return Promise.reject(refreshError);
        }
      }

      return new Promise((resolve) => {
        refreshSubscribers.push((token: string) => {
          if (originalRequest.headers) {
            originalRequest.headers[
              apiConfig.AUTH_HEADER
            ] = `${apiConfig.AUTH_SCHEME} ${token}`;
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
      retry: Number(apiConfig.RETRY),
      refetchOnWindowFocus: apiConfig.WIN_FOCUS_REFETCH,
    },
  },
});

export default axiosInstance;
