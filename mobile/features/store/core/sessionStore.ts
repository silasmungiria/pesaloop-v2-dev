import { create } from "zustand";
import { secureStorage } from "@/features/store";

interface UserSessioonStore {
  accessToken: string | null;
  refreshToken: string | null;
  session: boolean;
  setAccessToken: (token: string) => Promise<void>;
  setRefreshToken: (token: string) => Promise<void>;
  setSession: (value: boolean) => Promise<void>;
  clearSessionState: () => Promise<void>;
}

export const useSessionStore = create<UserSessioonStore>((set) => ({
  accessToken: null,
  refreshToken: null,
  session: false,

  setAccessToken: async (token) => {
    set({ accessToken: token });
    await secureStorage.setItem("platform_access_token", token);
  },

  setRefreshToken: async (token) => {
    set({ refreshToken: token });
    await secureStorage.setItem("platform_refresh_token", token);
  },

  setSession: async (value) => {
    set({ session: value });
    await secureStorage.setItem("platform_session", JSON.stringify(value));
  },

  clearSessionState: async () => {
    set({ session: false, accessToken: null, refreshToken: null });
    await Promise.all([
      secureStorage.removeItem("platform_session"),
      secureStorage.removeItem("platform_access_token"),
      secureStorage.removeItem("platform_refresh_token"),
    ]);
  },
}));
