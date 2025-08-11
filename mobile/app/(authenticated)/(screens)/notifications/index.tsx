import { View, Text, Button } from "react-native";
import React, { useEffect } from "react";
import * as Notifications from "expo-notifications";

import { useNotification } from "@/features/hooks";

export default function NotificationScreen() {
  const { scheduleVerificationReminder, scheduleNotification } =
    useNotification();

  useEffect(() => {
    scheduleVerificationReminder(); // Automatically schedule verification reminders
  }, []);

  return (
    <View className="flex-1 p-6 bg-gray-100 dark:bg-gray-900">
      <Text className="text-2xl font-semibold text-gray-800 dark:text-gray-200">
        Notifications
      </Text>

      <View className="gap-y-4 w-full">
        <Button
          title="Schedule Custom Notification"
          onPress={() =>
            scheduleNotification(
              {
                title: "Custom Reminder",
                body: "This is a custom reminder message.",
                sound: true,
                badge: 1,
                vibrate: [0, 300, 300, 300],
                data: { customData: "example" },
              },
              { seconds: 60, repeats: false }
            )
          }
        />
        <Button
          title="Clear Scheduled Notifications"
          onPress={Notifications.cancelAllScheduledNotificationsAsync}
        />
      </View>
    </View>
  );
}
