import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity, useColorScheme } from "react-native";
import { Tabs, router } from "expo-router";
import { BlurView } from "expo-blur";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";

import { ActionsModal } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { useNotification } from "@/features/hooks";
import { useUserStore } from "@/features/store";

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning,";
  if (hour < 18) return "Good Afternoon,";
  return "Good Evening,";
};

const TabsLayout = () => {
  const scheme = useColorScheme();

  const { scheduleVerificationReminder } = useNotification();
  const { user } = useUserStore();

  useEffect(() => {
    if (!user) {
      router.replace("/");
    }

    scheduleVerificationReminder();
  }, [user]);

  const [modalVisible, setModalVisible] = useState(false);

  const handleAction = (path: string) => {
    setModalVisible(false);
    router.push(path as unknown as (typeof router.push.arguments)[0]);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const onProfilePress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push("/(authenticated)/(screens)/settings/profile");
  };

  const onActivityCenterPress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push("/(authenticated)/(screens)/activity-center");
  };

  const onNotificationsPress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push("/(authenticated)/(screens)/notifications");
  };

  const onSettingsPress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push("/(authenticated)/(screens)/settings");
  };

  const onScanToPay = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    // router.push(
    //   "/(authenticated)/(screens)/qr-codes/screens/ScanToPayScreen" as unknown as (typeof router.push.arguments)[0]
    // );
    router.push("/(authenticated)/(screens)/qr-codes/screens/ScanToPay");
  };

  return (
    <SafeAreaProvider>
      <SafeAreaView className="flex-1 bg-gray-100 dark:bg-gray-900">
        {/* Main Tabs */}
        <Tabs
          screenOptions={{
            headerShown: false,
            tabBarShowLabel: false,
            tabBarStyle: {
              backgroundColor:
                scheme === "dark"
                  ? "rgba(17, 24, 39, 0.9)"
                  : "rgba(243, 244, 246, 0.9)",
              position: "absolute",
              bottom: 0,
              left: 0,
              right: 0,
              height: 72,
              width: "100%",
              elevation: 0,
              borderTopWidth: 0,
            },
            tabBarBackground: () => (
              <BlurView
                intensity={10}
                // tint={"extraLight"}
                tint={scheme === "dark" ? "dark" : "light"}
                className="flex-1 bg-white/90 dark:bg-gray-900"
              />
            ),
          }}
        >
          <Tabs.Screen
            name="home/index"
            options={{
              headerShown: true,
              headerShadowVisible: false,
              header: () => (
                <View className="flex-row justify-between items-center py-3 px-5 bg-gray-100 dark:bg-gray-900">
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={onProfilePress}
                    className="p-2 rounded-full"
                  >
                    <Text className="font-medium text-base text-gray-800 dark:text-gray-200">
                      {getGreeting()}
                    </Text>
                    <Text className="font-bold text-lg text-indigo-600 dark:text-indigo-400">
                      {user?.first_name}
                    </Text>
                  </TouchableOpacity>

                  <View className="flex-row justify-between items-center gap-x-3">
                    <TouchableOpacity
                      activeOpacity={0.8}
                      onPress={onNotificationsPress}
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons
                        name="notifications-outline"
                        size={20}
                        color="gray"
                      />
                    </TouchableOpacity>

                    <TouchableOpacity
                      activeOpacity={0.8}
                      onPress={onActivityCenterPress}
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons
                        name="bar-chart-outline"
                        size={20}
                        color="gray"
                      />
                    </TouchableOpacity>

                    <TouchableOpacity
                      activeOpacity={0.8}
                      onPress={onSettingsPress}
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons
                        name="settings-outline"
                        size={20}
                        color="gray"
                      />
                    </TouchableOpacity>

                    <TouchableOpacity
                      activeOpacity={0.8}
                      onPress={onScanToPay}
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons name="barcode-outline" size={20} color="gray" />
                    </TouchableOpacity>
                  </View>
                </View>
              ),
              tabBarIcon: ({ focused }) => (
                <View className="justify-center items-center pt-4">
                  <Ionicons
                    name={focused ? "home" : "home-outline"}
                    color={focused ? defaultColors.primary : defaultColors.gray}
                    size={20}
                  />
                  <Text
                    className={`text-sm mt-2 ${
                      focused
                        ? "text-indigo-600 dark:text-indigo-400"
                        : "text-gray-800 dark:text-gray-400"
                    }`}
                  >
                    Home
                  </Text>
                </View>
              ),
            }}
            listeners={() => ({
              tabPress: () => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              },
            })}
          />

          <Tabs.Screen
            name="actions/index"
            options={{
              title: "Actions",
              tabBarIcon: ({ focused }) => (
                <View
                  className="justify-center items-center h-16 w-16 rounded-full"
                  style={{ backgroundColor: defaultColors.primary }}
                >
                  <Ionicons
                    name="add"
                    color={focused ? "gray" : "white"}
                    size={20}
                  />
                </View>
              ),
            }}
            listeners={() => ({
              tabPress: (e) => {
                e.preventDefault();
                setModalVisible(true);
              },
            })}
          />

          <Tabs.Screen
            name="wallets/index"
            options={{
              headerShown: true,
              headerShadowVisible: false,
              headerStyle: { backgroundColor: defaultColors.background },
              header: () => (
                <View className="flex-row justify-between items-center py-3 px-5 bg-gray-100 dark:bg-gray-900">
                  <View className="rounded-full p-2 flex-row gap-2 justify-center items-center bg-gray-100 dark:bg-gray-900">
                    <Ionicons name="wallet-outline" size={20} color="gray" />
                    <Text className="text-lg font-semibold text-gray-700 dark:text-gray-200">
                      Wallet
                    </Text>
                  </View>

                  <View className="flex-row justify-between items-center gap-x-2">
                    <TouchableOpacity
                      onPress={() =>
                        router.push(
                          "/(authenticated)/(screens)/activity-center"
                        )
                      }
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons
                        name="bar-chart-outline"
                        size={20}
                        color="gray"
                      />
                    </TouchableOpacity>

                    <TouchableOpacity
                      activeOpacity={0.8}
                      onPress={() =>
                        router.push("/(authenticated)/(screens)/settings")
                      }
                      className="rounded-full p-2 justify-center items-center bg-gray-200 dark:bg-gray-800"
                    >
                      <Ionicons
                        name="settings-outline"
                        size={20}
                        color="gray"
                      />
                    </TouchableOpacity>
                  </View>
                </View>
              ),
              tabBarIcon: ({ focused }) => (
                <View className="justify-center items-center pt-4">
                  <Ionicons
                    name={focused ? "wallet" : "wallet-outline"}
                    color={focused ? defaultColors.primary : defaultColors.gray}
                    size={20}
                  />
                  <Text
                    className={`text-sm mt-2 ${
                      focused
                        ? "text-indigo-600 dark:text-indigo-400"
                        : "text-gray-800 dark:text-gray-400"
                    }`}
                  >
                    Wallet
                  </Text>
                </View>
              ),
            }}
            listeners={() => ({
              tabPress: () => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              },
            })}
          />
        </Tabs>

        {/* Modal for Actions */}
        <ActionsModal
          visible={modalVisible}
          onClose={() => setModalVisible(false)}
          onActionSelect={handleAction}
        />
      </SafeAreaView>
    </SafeAreaProvider>
  );
};

export default TabsLayout;
