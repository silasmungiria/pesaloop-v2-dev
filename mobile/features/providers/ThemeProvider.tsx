import React, { useEffect } from "react";
import {
  DefaultTheme,
  DarkTheme,
  ThemeProvider as NavigationThemeProvider,
} from "@react-navigation/native";
import { Appearance, AppState } from "react-native";
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import * as Haptics from "expo-haptics";
import { secureStorage } from "@/features/store";

const THEME_KEY = "app-theme";

interface ThemeStore {
  darkModeEnabled: boolean;
  theme: typeof DefaultTheme | typeof DarkTheme;
  originalSystemTheme: "light" | "dark" | null;
  setDarkModeEnabled: (value: boolean) => void;
  setTheme: (value: typeof DefaultTheme | typeof DarkTheme) => void;
  setOriginalSystemTheme: (value: "light" | "dark" | null) => void;
  toggleTheme: () => Promise<void>;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      darkModeEnabled: false,
      theme: DarkTheme,
      originalSystemTheme: null,
      setDarkModeEnabled: (value) => set({ darkModeEnabled: value }),
      setTheme: (value) => set({ theme: value }),
      setOriginalSystemTheme: (value) => set({ originalSystemTheme: value }),
      toggleTheme: async () => {
        const currentState = useThemeStore.getState();
        const newDarkMode = !currentState.darkModeEnabled;

        // Only update if the state actually changes
        if (newDarkMode !== currentState.darkModeEnabled) {
          set({
            darkModeEnabled: newDarkMode,
            theme: newDarkMode ? DarkTheme : DefaultTheme,
          });
          await secureStorage.setItem(
            THEME_KEY,
            newDarkMode ? "dark" : "light"
          );
          Appearance.setColorScheme(newDarkMode ? "dark" : "light");
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        }
      },
    }),
    {
      name: "app-theme-storage",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        darkModeEnabled: state.darkModeEnabled,
        theme: state.theme,
      }),
    }
  )
);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const {
    darkModeEnabled,
    theme,
    setDarkModeEnabled,
    setTheme,
    setOriginalSystemTheme,
  } = useThemeStore();

  useEffect(() => {
    const loadTheme = async () => {
      const savedTheme = await secureStorage.getItem(THEME_KEY);
      if (savedTheme !== null) {
        const darkModeEnabled = savedTheme === "dark";
        if (darkModeEnabled !== darkModeEnabled) {
          setDarkModeEnabled(darkModeEnabled);
        }
        setTheme(darkModeEnabled ? DarkTheme : DefaultTheme);

        const systemTheme = Appearance.getColorScheme() ?? "light";
        setOriginalSystemTheme(systemTheme);
        Appearance.setColorScheme(darkModeEnabled ? "dark" : "light");
      }
    };
    loadTheme();
  }, [darkModeEnabled, setDarkModeEnabled, setTheme, setOriginalSystemTheme]);

  useEffect(() => {
    const handleAppStateChange = (nextAppState: string) => {
      if (nextAppState === "inactive" || nextAppState === "background") {
        const originalTheme = useThemeStore.getState().originalSystemTheme;
        if (originalTheme) {
          Appearance.setColorScheme(originalTheme);
        }
      }
    };

    const subscription = AppState.addEventListener(
      "change",
      handleAppStateChange
    );
    return () => {
      subscription.remove();
    };
  }, []);

  return (
    <NavigationThemeProvider value={theme}>{children}</NavigationThemeProvider>
  );
};

export const useTheme = () => {
  const context = useThemeStore();
  return context;
};
