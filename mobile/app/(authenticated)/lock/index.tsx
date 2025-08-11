import { useState, useEffect } from "react";
import {
  ActivityIndicator,
  StyleSheet,
  Text,
  TouchableOpacity,
  useColorScheme,
  View,
} from "react-native";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { router } from "expo-router";
import * as Haptics from "expo-haptics";
import { Ionicons } from "@expo/vector-icons";
import { SafeAreaView } from "react-native-safe-area-context";

import { loginPassword } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { useNotificationToast } from "@/features/providers";
import {
  useUserStore,
  useSessionStore,
  useLogoutCleanup,
} from "@/features/store";

export default function Lock() {
  const scheme = useColorScheme();

  const { session, setSession, setAccessToken, setRefreshToken } =
    useSessionStore();
  const { user, customerProfile, setCustomerProfile } = useUserStore();
  const { performFullLogout } = useLogoutCleanup();

  const { showNotification } = useNotificationToast();

  useEffect(() => {
    if (!user?.email || !user?.phone_number) {
      performFullLogout();
      router.replace("/(public)/auth/login");
    }
  }, [user]);

  const [password, setPassword] = useState<number[]>([]);
  const [submittingLoginData, setSubmittingLoginData] = useState(false);
  const passwordLength = Array(6).fill(0);

  const offset = useSharedValue(0);

  const style = useAnimatedStyle(() => {
    return {
      transform: [{ translateX: offset.value }],
    };
  });

  const OFFSET = 20;
  const TIME = 80;

  const onNumberPress = (number: number) => {
    if (password.length === 6) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (password.length < 6) {
      setPassword([...password, number]);
    }
  };

  const numberBackspace = () => {
    if (password.length === 0) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (password.length > 0) {
      setPassword(password.slice(0, -1));
    }
  };

  useEffect(() => {
    onSubmitPasscodeLogin();
  }, [password]);

  const onSubmitPasscodeLogin = async () => {
    if (password.length === 6) {
      const logindata = {
        identifier: user?.email || user?.phone_number || "",
        password: password.join(""),
        send_otp: false,
        with_profile: true,
      };

      try {
        setSubmittingLoginData(true);
        const { data } = await loginPassword(logindata);

        // Update session and token data in Zustand store
        await setAccessToken(data.access);
        await setRefreshToken(data.refresh);
        await setSession(true);
        await setCustomerProfile(data.customerProfile);

        router.replace("/(authenticated)/(tabs)/home");
      } catch (error) {
        offset.value = withSequence(
          withTiming(-OFFSET, { duration: TIME / 2 }),
          withTiming(0, { duration: TIME / 2 })
        );

        const message = typeof error === "string" ? error : "Failed to login!";
        showNotification(message, "error", 6000);
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      } finally {
        setSubmittingLoginData(false);
        setPassword([]);
      }
    }
  };

  console.info("User data - Lock Screen: ", user);
  console.info("Customer Profile - Lock Screen: ", customerProfile);
  console.info("Session - Lock Screen: ", session);
  console.info("Submitting login data: ", submittingLoginData);
  console.info("Password entered: ", password.join(""));

  return (
    <SafeAreaView className="flex-1 bg-gray-100 dark:bg-gray-900 p-4">
      <View className="flex-1 justify-around align-center">
        {/* Header */}
        <View className="justify-center align-center mt-[10%] mb-[25%]">
          <Text className="font-semibold text-center text-3xl text-gray-800 dark:text-gray-200">
            Welcome back, {user?.first_name || "User"}!
          </Text>

          <Text className="font-extrabold mt-2 text-center text-lg text-gray-500">
            Enter your 6-digit passcode to continue.
          </Text>
        </View>

        {submittingLoginData ? (
          <View className="justify-center align-center">
            <ActivityIndicator size="large" color={defaultColors.green} />
          </View>
        ) : (
          <Animated.View
            style={[style]}
            className="flex-row justify-center align-center gap-4 mt-5"
          >
            {passwordLength.map((_, index) => (
              <View
                key={`password-${index}`}
                style={[styles.codeEmpty]}
                className={`${
                  password[index] !== undefined
                    ? "bg-teal-600"
                    : "bg-gray-200 dark:bg-gray-800"
                }`}
              />
            ))}
          </Animated.View>
        )}

        {/* Number Pad */}
        <View className="mt-10">
          <View className="flex-row justify-around mb-6">
            {[1, 2, 3].map((number) => (
              <TouchableOpacity
                activeOpacity={0.8}
                key={number}
                onPress={() => onNumberPress(number)}
                className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
              >
                <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                  {number}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <View className="flex-row justify-around mb-6">
            {[4, 5, 6].map((number) => (
              <TouchableOpacity
                activeOpacity={0.8}
                key={number}
                onPress={() => onNumberPress(number)}
                className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
              >
                <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                  {number}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <View className="flex-row justify-around mb-6">
            {[7, 8, 9].map((number) => (
              <TouchableOpacity
                activeOpacity={0.8}
                key={number}
                onPress={() => onNumberPress(number)}
                className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
              >
                <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                  {number}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <View className="flex-row justify-around mb-6">
            <View className="w-16 h-16 m-2 rounded-full justify-center items-center mb-4 bg-transparent" />

            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => onNumberPress(0)}
              className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
            >
              <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                0
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              activeOpacity={submittingLoginData ? 1 : 0.6}
              onPress={submittingLoginData ? undefined : numberBackspace}
              className={`w-16 h-16 m-2 rounded-full justify-center items-center ${
                submittingLoginData
                  ? "bg-transparent"
                  : "bg-gray-200 dark:bg-gray-800"
              }`}
            >
              {!submittingLoginData && (
                <Ionicons
                  name="backspace-outline"
                  size={20}
                  color={scheme === "dark" ? "#D1D5DB" : "#4B5563"}
                />
              )}
            </TouchableOpacity>
          </View>
        </View>

        {/* Log Out & Clear Session */}
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={() => performFullLogout()}
          disabled={submittingLoginData}
          className="justify-center items-center p-3"
        >
          <Text className="text-lg font-medium text-indigo-600 dark:text-indigo-400">
            Clear App Data & Sign Out
          </Text>
          <Text className="text-sm text-gray-500 dark:text-gray-400">
            You’ll log in with your details and an OTP next time.
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  codeEmpty: {
    width: 20,
    height: 20,
    borderRadius: 10,
  },
});
