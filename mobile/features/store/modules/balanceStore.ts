import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { secureStorage } from "@/features/store";

interface BalanceStore {
  currency: string;
  balance: number;

  setCurrency: (value: string) => Promise<void>;
  setBalance: (value: number) => Promise<void>;
  resetBalanceState: () => Promise<void>;
}

export const useBalanceStore = create<BalanceStore>()(
  persist(
    (set) => ({
      currency: "USD",
      balance: 0,

      setCurrency: async (value) => {
        try {
          set({ currency: value });
          await secureStorage.setItem("platform_currency", value);
        } catch (error) {
          console.error("Failed to set currency:", error);
        }
      },

      setBalance: async (value) => {
        try {
          set({ balance: value });
          await secureStorage.setItem(
            "platform_balance",
            JSON.stringify(value)
          );
        } catch (error) {
          console.error("Failed to set balance:", error);
        }
      },

      resetBalanceState: async () => {
        try {
          set({ currency: "USD", balance: 0 });
          await secureStorage.removeItem("platform_currency");
          await secureStorage.removeItem("platform_balance");
        } catch (error) {
          console.error("Failed to clear secure storage:", error);
        }
      },
    }),
    {
      name: "platform_balance-storage",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        currency: state.currency,
        balance: state.balance,
      }),
    }
  )
);
