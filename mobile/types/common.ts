// types/api.ts

import { ReactNode } from "react";
import { AppStateStatus } from "react-native";

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  message?: string;
  error?: string;
  [key: string]: unknown;
}

// types/hooks.ts

export interface DeviceDetails {
  brand: string;
  model: string;
  os: string;
  osVersion: string;
  deviceType: string;
  deviceId: string;
  memory: string;
  batteryLevel: string;
  batteryState: string;
  ipAddress: string;
  connectionType: string;
  screenResolution: string;
  region: string;
  location: string;
  city: string;
  country: string;
  defaultcurrency: string;
  countryCallingCode: string;
}

export interface DeviceContextProps {
  deviceDetails: DeviceDetails;
}

export type NotificationType = "error" | "success" | "info" | "warning";

export interface NotificationProps {
  showNotification: (
    message: string,
    type?: NotificationType,
    duration?: number
  ) => void;
  hideNotification: () => void;
}

export interface PushNotificationContent {
  title: string;
  body: string;
  sound?: boolean;
  badge?: number;
  vibrate?: number[];
  data?: Record<string, any>;
}

export interface PushNotificationTrigger {
  seconds: number;
  repeats: boolean;
}

// App State Providers
export interface SessionAppStateContextProps {
  appState: AppStateStatus;
  isBackgroundSafe: boolean;
  setBackgroundSafe: (isBackgroundSafe: boolean) => void;
}

export interface SessionAppStateProviderProps {
  children: ReactNode;
}
