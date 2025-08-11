import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import * as Haptics from "expo-haptics";
import { secureStorage } from "@/features/store";

interface NotificationState {
  notificationsEnabled: boolean;
  smsNotifications: boolean;

  setNotificationsEnabled: (enabled: boolean) => void;
  toggleNotifications: () => void;
  setSMSNotifications: (enabled: boolean) => void;
  toggleSMSNotifications: () => void;
}

export const useNotificationStore = create<NotificationState>()(
  persist(
    (set) => ({
      notificationsEnabled: true,
      smsNotifications: false,

      setNotificationsEnabled: (enabled) =>
        set({ notificationsEnabled: enabled }),

      setSMSNotifications: (enabled) => set({ smsNotifications: enabled }),

      toggleNotifications: () => {
        set((state) => ({
          notificationsEnabled: !state.notificationsEnabled,
        }));
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      },

      toggleSMSNotifications: () => {
        set((state) => ({
          smsNotifications: !state.smsNotifications,
        }));
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      },
    }),
    {
      name: "notification-settings",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        notificationsEnabled: state.notificationsEnabled,
        smsNotifications: state.smsNotifications,
      }),
    }
  )
);
