import React from "react";
import { Link, Stack, router } from "expo-router";
import { TouchableOpacity, useColorScheme } from "react-native";
import { Ionicons } from "@expo/vector-icons";

const StacksLayout = () => {
  const scheme = useColorScheme();

  return (
    <Stack
      screenOptions={{
        headerShown: false,
        headerShadowVisible: false,
        headerStyle: {
          backgroundColor: scheme === "dark" ? "#111827" : "#F3F4F6",
        },
        headerTitleStyle: {
          color: scheme === "dark" ? "#D1D5DB" : "#4B5563",
          fontSize: 20,
        },
        headerTitleAlign: "center",
        headerTintColor: scheme === "dark" ? "#D1D5DB" : "#4B5563",
      }}
    >
      <Stack.Screen name="lock/index" />
      <Stack.Screen name="(tabs)" />

      <Stack.Screen
        name="(screens)/transactions/forex/index"
        options={{
          headerShown: true,
          headerTitle: "Currency Exchange",
        }}
      />
      <Stack.Screen name="(screens)/transactions/requests/InternalRequest" />
      <Stack.Screen
        name="(screens)/transactions/requests/ExternalRequest"
        options={{
          headerShown: true,
          headerTitle: "Request Funds",
        }}
      />
      <Stack.Screen name="(screens)/transactions/send/InternalTransfer" />
      <Stack.Screen
        name="(screens)/transactions/send/ExternalTransfer"
        options={{
          headerShown: true,
          headerTitle: "Send Out",
        }}
      />
      <Stack.Screen name="(screens)/qr-codes/index" />
      <Stack.Screen
        name="(screens)/qr-codes/screens/CreateQRCodeScreen"
        options={{
          headerShown: true,
          headerTitle: "Scan to Pay",
        }}
      />
      <Stack.Screen
        name="(screens)/credits/index"
        options={{
          headerShown: true,
          headerTitle: "Credit Issuance",
          headerRight: () => {
            const iconColor = scheme === "dark" ? "#D1D5DB" : "#4B5563";
            return (
              <Link href="/(authenticated)/(screens)/settings" asChild>
                <TouchableOpacity className="p-2 rounded-full bg-gray-200 dark:bg-gray-800">
                  <Ionicons
                    name="settings-outline"
                    size={20}
                    color={iconColor}
                  />
                </TouchableOpacity>
              </Link>
            );
          },
        }}
      />

      <Stack.Screen
        name="(screens)/settings/index"
        options={{
          headerShown: true,
          headerTitle: "Account Settings",
        }}
      />
      <Stack.Screen name="(screens)/settings/profile/index" />
      <Stack.Screen
        name="(screens)/settings/security/index"
        options={{
          headerShown: true,
          headerTitle: "Security",
        }}
      />
      <Stack.Screen
        name="(screens)/activity-center/index"
        options={{
          headerShown: true,
          headerTitle: "Activity Center",
          headerStyle: {
            backgroundColor: scheme === "dark" ? "#111827" : "#F3F4F6",
          },
        }}
      />
      <Stack.Screen
        name="(screens)/settings/cards/index"
        options={{
          headerShown: true,
          headerTitle: "Manage payment cards",
        }}
      />

      <Stack.Screen
        name="(screens)/notifications/index"
        options={{
          headerShown: true,
          headerTitle: "Notifications",
        }}
      />
      <Stack.Screen
        name="(screens)/(devSamples)/useDeviceDetails"
        options={{
          headerShown: true,
          headerTitle: "Device Info",
        }}
      />
    </Stack>
  );
};

export default StacksLayout;
