import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { secureStorage } from "@/features/store";

interface BiometricStore {
  isBiometricEnabled: boolean;
  setBiometricEnabled: (value: boolean) => Promise<void>;
  clearBiometricState: () => Promise<void>;
}

export const useBiometricStore = create<BiometricStore>()(
  persist(
    (set) => ({
      isBiometricEnabled: false,

      setBiometricEnabled: async (value) => {
        try {
          set({ isBiometricEnabled: value });
          await secureStorage.setItem(
            "biometric_enabled",
            JSON.stringify(value)
          );
        } catch (error) {
          console.error("Failed to set biometric preference:", error);
        }
      },

      clearBiometricState: async () => {
        try {
          set({ isBiometricEnabled: false });
          await secureStorage.removeItem("biometric_enabled");
        } catch (error) {
          console.error("Failed to clear biometric preference:", error);
        }
      },
    }),
    {
      name: "biometric-storage",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        isBiometricEnabled: state.isBiometricEnabled,
      }),
    }
  )
);
