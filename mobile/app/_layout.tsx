import "react-native-reanimated";
import "@/global.css";

import { useColorScheme } from "react-native";
import { StatusBar } from "expo-status-bar";
import { GestureHandlerRootView } from "react-native-gesture-handler";

import AppNavigator from "@/app/layout/AppNavigator";
import {
  DeviceDetailsProvider,
  NotificationProvider,
  SessionAppStateProvider,
  ThemeProvider,
} from "@/features/providers";

export { ErrorBoundary } from "expo-router";

const AppEntryLayout = () => {
  const scheme = useColorScheme();

  return (
    <GestureHandlerRootView className="flex-1 bg-gray-100 dark:bg-gray-900">
      <SessionAppStateProvider>
        <ThemeProvider>
          <NotificationProvider>
            <DeviceDetailsProvider>
              <StatusBar
                style={scheme === "dark" ? "light" : "dark"}
                translucent
              />
              <AppNavigator />
            </DeviceDetailsProvider>
          </NotificationProvider>
        </ThemeProvider>
      </SessionAppStateProvider>
    </GestureHandlerRootView>
  );
};

export default AppEntryLayout;
