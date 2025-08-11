import React, { useState, useMemo, useCallback } from "react";
import {
  FlatList,
  Text,
  View,
  TouchableOpacity,
  Switch,
  ActivityIndicator,
} from "react-native";
import Animated, {
  FadeIn,
  FadeInDown,
  FadeInUp,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import * as Haptics from "expo-haptics";

import { updateNotificationPreferences } from "@/features/api";
import {
  AccountDeactivationModal,
  AccountDeletionModal,
  Biometric2FAModal,
} from "@/features/components";
import { useTheme } from "@/features/providers";
import {
  useNotificationStore,
  useUserStore,
  useLogoutCleanup,
  useBiometricStore,
} from "@/features/store";
import { ExportStatementModal } from "./overlays";

interface Link {
  section: "general" | "preference" | "danger";
  name: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  action: () => void;
}

const renderSectionHeader = (section: string) => {
  const headers: Record<string, string> = {
    general: "Account Settings",
    preference: "Preference Settings",
    danger: "Danger Zone",
  };
  return (
    <Text
      className={`font-bold mt-8 mb-4 px-3 text-base ${
        section === "danger" ? "text-red-600" : "text-gray-400"
      }`}
    >
      {headers[section]}
    </Text>
  );
};

export default function Settings() {
  const { user } = useUserStore();
  const { performFullLogout } = useLogoutCleanup();
  const { darkModeEnabled, toggleTheme } = useTheme();
  const {
    notificationsEnabled,
    toggleNotifications,
    smsNotifications,
    setSMSNotifications,
  } = useNotificationStore();
  const { isBiometricEnabled } = useBiometricStore();

  const [deactivateVisible, setDeactivateVisible] = useState(false);
  const [deleteVisible, setDeleteVisible] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [showBiometricModal, setShowBiometricModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const togglesmsNotifications = async () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    const newValue = !smsNotifications;
    setIsLoading(true);
    try {
      const { data } = await updateNotificationPreferences({
        use_sms: newValue,
      });

      console.log("Notification channel updated:", data);
      setSMSNotifications(data.use_sms);
    } catch (error) {
      console.error("Error toggling SMS notifications:", error);
    } finally {
      setIsLoading(false);
    }
  };

  console.info("Biometric Enabled:", isBiometricEnabled);

  const handle2FAToggle = useCallback(() => {
    setShowBiometricModal(true);
  }, []);

  const settings: Link[] = useMemo(
    () => [
      {
        section: "general",
        name: "My Profile",
        icon: "person",
        color: "#4a90e2",
        action: () =>
          router.push("/(authenticated)/(screens)/settings/profile"),
      },
      {
        section: "general",
        name: "Security Settings",
        icon: "lock-closed",
        color: "#e94e77",
        action: () =>
          router.push("/(authenticated)/(screens)/settings/security"),
      },
      {
        section: "general",
        name: "Recent Activity",
        icon: "time",
        color: "#9b59d6",
        action: () => router.push("/(authenticated)/(screens)/activity-center"),
      },
      {
        section: "general",
        name: "Linked Payment Cards",
        icon: "card",
        color: "#f39c12",
        action: () => router.push("/(authenticated)/(screens)/settings/cards"),
      },
      {
        section: "general",
        name: "Download Statement",
        icon: "document-text",
        color: "#2ecc71",
        action: () => setShowExportModal(true),
      },
      {
        section: "preference",
        name: `Switch to ${darkModeEnabled ? "Light" : "Dark"} Mode`,
        icon: darkModeEnabled ? "sunny" : "moon",
        color: darkModeEnabled ? "#2980b9" : "#f1c40f",
        action: toggleTheme,
      },
      {
        section: "preference",
        name: "App Notifications",
        icon: notificationsEnabled ? "notifications" : "notifications-off",
        color: notificationsEnabled ? "#27ae60" : "#c0392b",
        action: toggleNotifications,
      },
      {
        section: "preference",
        name: "Notification Channel",
        icon: smsNotifications ? "chatbubbles" : "mail",
        color: smsNotifications ? "#f39c12" : "#3498db",
        action: togglesmsNotifications,
      },
      {
        section: "preference",
        name: isBiometricEnabled
          ? "Disable Biometric 2FA"
          : "Enable Biometric 2FA",
        icon: "finger-print",
        color: "#8e44ad",
        action: handle2FAToggle,
      },
      {
        section: "danger",
        name: "Sign Out",
        icon: "log-out",
        color: "#c0392b",
        action: performFullLogout,
      },
      {
        section: "danger",
        name: "Temporarily Deactivate Account",
        icon: "alert-circle",
        color: "#e74c3c",
        action: () => setDeactivateVisible(true),
      },
      {
        section: "danger",
        name: "Permanently Delete Account",
        icon: "trash",
        color: "#c0392b",
        action: () => setDeleteVisible(true),
      },
    ],
    [
      darkModeEnabled,
      notificationsEnabled,
      smsNotifications,
      togglesmsNotifications,
      toggleTheme,
      toggleNotifications,
      isBiometricEnabled,
      handle2FAToggle,
      performFullLogout,
    ]
  );

  const getSwitchValue = (action: any) => {
    switch (action) {
      case toggleTheme:
        return darkModeEnabled;
      case toggleNotifications:
        return notificationsEnabled;
      case togglesmsNotifications:
        return smsNotifications;
      case handle2FAToggle:
        return isBiometricEnabled;
      default:
        return false;
    }
  };

  const renderItem = useCallback(
    ({ item, index }: { item: Link; index: number }) => {
      const isFirstInSection =
        index === 0 || settings[index - 1].section !== item.section;
      const isPreference = item.section === "preference";

      return (
        <Animated.View
          entering={FadeInDown.delay(Math.min(index * 100, 300)).springify()}
          exiting={FadeOutUp.springify()}
          layout={Layout.springify()}
          className="mb-2"
        >
          {isFirstInSection && renderSectionHeader(item.section)}
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={isPreference ? undefined : item.action}
            className={`flex-row rounded-xl justify-between bg-white/90 dark:bg-gray-800 p-4 ${
              isPreference ? "" : "py-8"
            }`}
          >
            <View className="flex-row items-center">
              <Ionicons name={item.icon} size={20} color={item.color} />
              <Text className="ml-3 text-base text-gray-800 dark:text-gray-300">
                {item.name === "Notification Channel"
                  ? `${item.name} (${smsNotifications ? "SMS" : "Email"})`
                  : item.name}
              </Text>
            </View>

            {isPreference ? (
              <View>
                {item.name === "Notification Channel" && isLoading ? (
                  <View className="p-3 justify-center items-center">
                    <ActivityIndicator size={27} color={item.color} />
                  </View>
                ) : (
                  <Switch
                    trackColor={{ false: "#d3d3d3", true: item.color }}
                    thumbColor="#ffffff"
                    ios_backgroundColor="#3e3e3e"
                    onValueChange={item.action}
                    value={getSwitchValue(item.action)}
                    disabled={item.name === "Notification Channel" && isLoading}
                  />
                )}
              </View>
            ) : (
              <Ionicons name="chevron-forward" size={20} color="lightgray" />
            )}
          </TouchableOpacity>
        </Animated.View>
      );
    },
    [
      settings,
      darkModeEnabled,
      notificationsEnabled,
      isBiometricEnabled,
      isLoading,
    ]
  );

  return (
    <View className="flex-1 bg-gray-100 dark:bg-gray-900">
      <FlatList
        data={settings}
        keyExtractor={(item) => item.name}
        renderItem={renderItem}
        className="p-3"
        contentContainerStyle={{ paddingBottom: 80 }}
      />

      <AccountDeactivationModal
        visible={deactivateVisible}
        onClose={() => setDeactivateVisible(false)}
      />
      <AccountDeletionModal
        visible={deleteVisible}
        onClose={() => setDeleteVisible(false)}
      />
      <Biometric2FAModal
        visible={showBiometricModal}
        onClose={() => setShowBiometricModal(false)}
        launchedFromSettings={true}
      />
      <ExportStatementModal
        visible={showExportModal}
        onClose={() => setShowExportModal(false)}
      />
    </View>
  );
}
