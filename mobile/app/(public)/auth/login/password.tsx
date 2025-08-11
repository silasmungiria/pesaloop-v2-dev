import { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  useColorScheme,
} from "react-native";
import * as Haptics from "expo-haptics";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { useLocalSearchParams, router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { loginPassword } from "@/features/api";
import { defaultColors } from "@/features/constants";
import {
  formatPhoneNumberWithCountryCode,
  getUserIdentifierWithUnformattedPhone,
} from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { useUserStore, useSessionStore } from "@/features/store";

export default function LoginPassword() {
  const scheme = useColorScheme();
  const params = useLocalSearchParams();

  const email = String(params.email);
  const countryCode = String(params.countryCode);
  const phoneNumber = String(params.phoneNumber);

  const { showNotification } = useNotificationToast();

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

  const { setUserData, setCustomerProfile } = useUserStore();
  const { setAccessToken, setRefreshToken } = useSessionStore();

  useEffect(() => {
    onSubmitCredentialsLogin();
  }, [password]);

  const onSubmitCredentialsLogin = async () => {
    if (password.length === 6) {
      const logindata = {
        identifier:
          getUserIdentifierWithUnformattedPhone(
            email,
            phoneNumber,
            countryCode
          ) ?? "",
        password: password.join(""),
        send_otp: true,
        with_profile: true,
      };

      setSubmittingLoginData(true);
      try {
        const { data } = await loginPassword(logindata);

        // Save user and token data in Zustand store
        await setUserData(data.user);
        await setCustomerProfile(data.customerProfile);
        await setAccessToken(data.access);
        await setRefreshToken(data.refresh);

        router.push({
          pathname: "/(public)/auth/verify/otp",
          params: {
            phone: formatPhoneNumberWithCountryCode(countryCode, phoneNumber),
            email: email,
            previousPage: "loginPassword",
          },
        });
      } catch (error) {
        offset.value = withSequence(
          withTiming(-OFFSET, { duration: TIME / 2 }),
          withTiming(0, { duration: TIME / 2 })
        );
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);

        const message = typeof error === "string" ? error : "Failed to login!";
        showNotification(message, "error", 6000);
      } finally {
        setSubmittingLoginData(false);
        setPassword([]);
      }
    }
  };

  return (
    <View className="flex-1 justify-around align-center bg-gray-100 dark:bg-gray-900 p-4">
      <View className="gap-2">
        <Text className="font-semibold text-center text-2xl text-gray-800 dark:text-gray-200">
          Enter your passcode
        </Text>

        <Text className="mt-5s text-center text-lg text-gray-600 dark:text-gray-400">
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
          <View className="w-16 h-16 rounded-full justify-center items-center mb-4 bg-transparent" />

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
            disabled={submittingLoginData}
            className={`w-16 h-16 m-2 rounded-full justify-center items-center ${
              submittingLoginData
                ? "bg-gray-100 dark:bg-gray-900"
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
    </View>
  );
}

const styles = StyleSheet.create({
  codeEmpty: {
    width: 20,
    height: 20,
    borderRadius: 10,
  },
});
