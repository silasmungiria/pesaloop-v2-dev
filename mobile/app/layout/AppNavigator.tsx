import "react-native-reanimated";
import "@/global.css";

import { useEffect } from "react";
import {
  ActivityIndicator,
  TouchableOpacity,
  View,
  useColorScheme,
} from "react-native";
import FontAwesome from "@expo/vector-icons/build/FontAwesome";
import { useFonts } from "expo-font";
import { Link, Stack, router, useSegments } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { Ionicons } from "@expo/vector-icons";

import { defaultColors } from "@/features/constants";
import { useUserStore, useSessionStore } from "@/features/store";

SplashScreen.preventAutoHideAsync();

const AppNavigator = () => {
  const [loaded, error] = useFonts({
    SpaceMono: require("@/assets/fonts/SpaceMono-Regular.ttf"),
    ...FontAwesome.font,
  });

  const scheme = useColorScheme();
  const segments = useSegments();
  const { customerProfile, user, sessionVerified } = useUserStore();
  const { session, refreshToken, accessToken } = useSessionStore();

  const AUTH_GROUP = "(authenticated)";
  const HOME_ROUTE = "/(authenticated)/(tabs)/home";
  const LOCK_ROUTE = "/(authenticated)/lock";
  const ROOT_ROUTE = "/";

  // Splash screen hide handler
  useEffect(() => {
    if (error) throw error;
  }, [error]);

  useEffect(() => {
    const hideSplash = async () => {
      try {
        await SplashScreen.hideAsync();
      } catch (e) {
        console.warn("Splash screen hide failed", e);
      }
    };

    if (loaded || sessionVerified) hideSplash();
  }, [loaded, sessionVerified]);

  // Auth redirect logic
  useEffect(() => {
    if (!loaded || !sessionVerified) return;

    const inAuthGroup = segments[0] === AUTH_GROUP;

    const targetRoute =
      (!inAuthGroup && user && !session && sessionVerified && LOCK_ROUTE) ||
      (!inAuthGroup && user && session && sessionVerified && HOME_ROUTE) ||
      (inAuthGroup && !user && ROOT_ROUTE) ||
      (inAuthGroup && !session && sessionVerified && LOCK_ROUTE);

    if (targetRoute) {
      router.replace(targetRoute);
    }
  }, [user, session, sessionVerified, segments, loaded, router]);

  // Debug logs
  console.info("Login user", user);
  console.info("Login customerProfile", customerProfile);
  console.info("Login session", session);
  console.info("Login sessionVerified", sessionVerified);
  console.info("Login accessToken", accessToken);
  console.info("Login refreshToken", refreshToken);

  // Header button render helpers
  const getHeaderLeft = (onPress: () => void) => (
    <TouchableOpacity onPress={onPress} className="p-2 rounded-full">
      <Ionicons
        name="arrow-back"
        size={20}
        color={scheme === "dark" ? "#D1D5DB" : "#4B5563"}
      />
    </TouchableOpacity>
  );

  const getHelpIcon = () => (
    <Link href="/help" asChild>
      <TouchableOpacity className="p-2 rounded-full">
        <Ionicons
          name="help-circle-outline"
          size={20}
          color={scheme === "dark" ? "#D1D5DB" : "#4B5563"}
        />
      </TouchableOpacity>
    </Link>
  );

  if (!loaded) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color={defaultColors.green} />
      </View>
    );
  }

  return (
    <Stack
      screenOptions={{
        title: "",
        headerBackTitle: "",
        headerShown: false,
        headerShadowVisible: false,
        headerStyle: {
          backgroundColor: scheme === "dark" ? "#111827" : "#F3F4F6",
        },
        headerTitleStyle: {
          color: scheme === "dark" ? "#D1D5DB" : "#4B5563",
          fontSize: 18,
        },
        headerTitleAlign: "center",
        headerTintColor: scheme === "dark" ? "#D1D5DB" : "#4B5563",
      }}
    >
      <Stack.Screen name="index" />
      <Stack.Screen
        name="(public)/auth/signup/index"
        options={{
          headerShown: true,
          headerLeft: () => getHeaderLeft(() => router.replace("/")),
          headerRight: getHelpIcon,
        }}
      />
      <Stack.Screen
        name="(public)/auth/signup/password"
        options={{
          headerShown: true,
          headerLeft: () => getHeaderLeft(() => router.back()),
          headerRight: getHelpIcon,
        }}
      />
      <Stack.Screen
        name="(public)/auth/verify/otp"
        options={{
          headerShown: true,
          headerLeft: () => getHeaderLeft(() => router.back()),
        }}
      />
      <Stack.Screen
        name="(public)/auth/login/index"
        options={{
          headerShown: true,
          headerLeft: () => getHeaderLeft(() => router.replace("/")),
          headerRight: getHelpIcon,
        }}
      />
      <Stack.Screen
        name="(public)/auth/login/password"
        options={{
          headerShown: true,
          headerLeft: () => getHeaderLeft(() => router.back()),
          headerRight: getHelpIcon,
        }}
      />
      <Stack.Screen
        name="(public)/auth/forgot-password/index"
        options={{ presentation: "modal" }}
      />
      <Stack.Screen
        name="(public)/help/index"
        options={{ presentation: "modal" }}
      />
      <Stack.Screen name="(authenticated)" />
    </Stack>
  );
};

export default AppNavigator;
