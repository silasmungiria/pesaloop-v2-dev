import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

import { secureStorage } from "@/features/store";
import { SessionUser, CustomerProfile } from "@/types";

interface UserStore {
  user: SessionUser | null;
  customerProfile: CustomerProfile | null;
  sessionVerified: boolean;

  setUserData: (data: Partial<SessionUser>) => Promise<void>;
  setCustomerProfile: (data: CustomerProfile) => Promise<void>;
  setSessionVerified: (value: boolean) => Promise<void>;
  clearUserState: () => Promise<void>;

  loadUserData: () => Promise<void>;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      user: null,
      customerProfile: null,
      sessionVerified: false,

      loadUserData: async () => {
        try {
          const storedUser = await secureStorage.getItem("platform_user_data");
          if (storedUser) {
            const parsedUser = JSON.parse(storedUser);
            // Merge with existing user like in setUserData
            set((state) => {
              const updatedUser = {
                ...(state.user ?? {}),
                ...parsedUser,
              };
              return { user: updatedUser as SessionUser };
            });
          }
        } catch (error) {
          console.error("Failed to load user data:", error);
        }
      },

      setUserData: async (data) => {
        set((state) => {
          const updatedUser = {
            ...(state.user ?? {}), // use empty object if null
            ...data,
          };

          secureStorage.setItem(
            "platform_user_data",
            JSON.stringify(updatedUser)
          );
          return { user: updatedUser as SessionUser };
        });
      },

      setCustomerProfile: async (data) => {
        set({ customerProfile: data });
      },

      setSessionVerified: async (value) => {
        set({ sessionVerified: value });
        await secureStorage.setItem(
          "platform_sessionVerified",
          JSON.stringify(value)
        );
      },

      clearUserState: async () => {
        set({ user: null, customerProfile: null, sessionVerified: false });
        await Promise.all([
          secureStorage.removeItem("platform_user_data"),
          secureStorage.removeItem("platform_sessionVerified"),
        ]);
      },
    }),
    {
      name: "platform_user-store",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        user: state.user,
        customerProfile: state.customerProfile,
        sessionVerified: state.sessionVerified,
      }),
    }
  )
);
