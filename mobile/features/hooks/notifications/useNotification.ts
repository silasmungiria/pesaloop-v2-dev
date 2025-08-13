import { useEffect } from "react";
import * as Notifications from "expo-notifications";
import { Platform } from "react-native";

import { useSessionAppState } from "@/features/providers";
import { useUserStore, useNotificationStore } from "@/features/store";
import { PushNotificationContent, PushNotificationTrigger } from "@/types";

export function useNotification() {
  const { setBackgroundSafe } = useSessionAppState();
  const { notificationsEnabled } = useNotificationStore();
  const { user } = useUserStore();

  useEffect(() => {
    const requestPermissions = async () => {
      if (!notificationsEnabled) return;

      setBackgroundSafe(true);

      let status;
      if (Platform.OS === "ios") {
        const { status: iosStatus } =
          await Notifications.requestPermissionsAsync();
        status = iosStatus;
      } else if (Platform.OS === "android") {
        const { status: androidStatus } =
          await Notifications.requestPermissionsAsync();
        status = androidStatus;
      }

      if (status !== "granted") {
        alert("Permission to receive notifications was denied!");
      }

      setBackgroundSafe(false);
    };

    requestPermissions();

    // Set notification handler to improve notification display
    Notifications.setNotificationHandler({
      handleNotification: async (notification) => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
        shouldShowBanner: true,
        shouldShowList: true,
        priority: Notifications.AndroidNotificationPriority.HIGH,
        data: notification.request.content.data,
      }),
    });
  }, [setBackgroundSafe, notificationsEnabled]);

  // Function to schedule a dynamic notification
  const scheduleNotification = async (
    content: PushNotificationContent,
    trigger: PushNotificationTrigger
  ) => {
    if (!notificationsEnabled) return;

    await Notifications.scheduleNotificationAsync({
      content: {
        title: content.title,
        body: content.body,
        sound: content.sound || true,
        badge: content.badge || 1,
        vibrate: content.vibrate || [0, 250, 250, 250],
        data: content.data || {},
      },
      trigger: {
        type: Notifications.SchedulableTriggerInputTypes.TIME_INTERVAL,
        seconds: trigger.seconds,
        repeats: trigger.repeats,
      },
    });
  };

  // Function to schedule a verification reminder notification based on user data
  const scheduleVerificationReminder = async () => {
    const delay = 1 * 60;

    if (!user?.is_email_verified) {
      await scheduleNotification(
        {
          title: "Email Verification Reminder",
          body: "Please verify your email to fully activate your account.",
        },
        {
          seconds: 3 * 60,
          repeats: false,
        }
      );
      await new Promise((resolve) => setTimeout(resolve, delay * 1000));
    }

    if (!user?.is_phone_verified) {
      await scheduleNotification(
        {
          title: "Phone Verification Reminder",
          body: "Please verify your phone number to fully activate your account.",
        },
        {
          seconds: 3 * 60,
          repeats: false,
        }
      );
      await new Promise((resolve) => setTimeout(resolve, delay * 1000));
    }

    if (!user?.is_verified) {
      await scheduleNotification(
        {
          title: "Account Verification Reminder",
          body: "Please verify your account to enjoy all features. Your account is currently limited.",
        },
        {
          seconds: 3 * 60,
          repeats: false,
        }
      );
    }
  };

  return { scheduleVerificationReminder, scheduleNotification };
}
