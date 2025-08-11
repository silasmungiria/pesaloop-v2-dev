import { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  useColorScheme,
} from "react-native";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import * as Haptics from "expo-haptics";
import { useLocalSearchParams, router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { signupUser } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { formatPhoneNumberWithCountryCode } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { handleError } from "@/features/utils/handleError";

export default function SignupPassword() {
  const scheme = useColorScheme();
  const params = useLocalSearchParams();

  const firstName = String(params.firstName);
  const lastName = String(params.lastName);
  const countryCode = String(params.countryCode);
  const phoneNumber = String(params.phoneNumber);
  const email = String(params.email);

  const { showNotification } = useNotificationToast();

  const [password, setPassword] = useState<number[]>([]);
  const [confirmPassword, setConfirmPassword] = useState<number[]>([]);
  const [submittingSignupData, setSubmittingSignupData] = useState(false);
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
    if (password.length === 6 && confirmPassword.length === 6) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (password.length < 6) {
      setPassword([...password, number]);
    } else if (confirmPassword.length < 6) {
      setConfirmPassword([...confirmPassword, number]);
    }
  };

  const numberBackspace = () => {
    if (password.length === 0 && confirmPassword.length === 0) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (confirmPassword.length > 0) {
      setConfirmPassword(confirmPassword.slice(0, -1));
    } else if (password.length > 0) {
      setPassword(password.slice(0, -1));
    }
  };

  useEffect(() => {
    if (password.length === 6 && confirmPassword.length === 6) {
      onSubmitUserSignupData();
    }
  }, [password, confirmPassword]);

  const onSubmitUserSignupData = async () => {
    if (password.join("") === confirmPassword.join("")) {
      const data = {
        first_name: firstName,
        last_name: lastName,
        country_code: countryCode,
        phone_number: formatPhoneNumberWithCountryCode(
          countryCode,
          phoneNumber
        ),
        email: email,
        password: password.join(""),
      };

      setSubmittingSignupData(true);
      try {
        const result = await signupUser(data);

        const message = result.message || "User signed up successfully!";
        showNotification(message, "success", 6000);

        setTimeout(() => {
          router.push({
            pathname: "/(public)/auth/verify/otp",
            params: {
              phone: formatPhoneNumberWithCountryCode(countryCode, phoneNumber),
              email: email,
              previousPage: "signupPassword",
            },
          });
        }, 3000);
      } catch (error) {
        handleError(error, "Failed to sign up user. Please try again later.");
      } finally {
        setSubmittingSignupData(false);
        setPassword([]);
        setConfirmPassword([]);
      }
    } else {
      offset.value = withSequence(
        withTiming(-OFFSET, { duration: TIME / 2 }),
        withRepeat(withTiming(OFFSET, { duration: TIME }), 4, true),
        withTiming(0, { duration: TIME / 2 })
      );
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      setPassword([]);
      setConfirmPassword([]);
    }
  };

  return (
    <View className="flex-1 justify-around align-center bg-gray-100 dark:bg-gray-900 p-4">
      <View className="gap-2">
        <Text className="font-semibold text-center text-2xl text-gray-800 dark:text-gray-200">
          Protect Your Account
        </Text>

        <Text className="mt-5 text-center text-lg text-gray-600 dark:text-gray-400">
          {password.length !== 6
            ? "Choose a 6-digit passcode to secure your account."
            : "Confirm your passcode."}
        </Text>
      </View>

      {submittingSignupData ? (
        <View className="justify-center align-center">
          <ActivityIndicator size="large" color={defaultColors.green} />
        </View>
      ) : (
        <View>
          {/* Password View */}
          {password.length !== 6 && (
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

          {/* Show Confirm Password only when 6 characters are entered in password */}
          {password.length === 6 && (
            <Animated.View
              style={[style]}
              className="flex-row justify-center align-center gap-4 mt-5"
            >
              {passwordLength.map((_, index) => (
                <View
                  key={`confirmPassword-${index}`}
                  style={[styles.codeEmpty]}
                  className={`${
                    confirmPassword[index] !== undefined
                      ? "bg-teal-600"
                      : "bg-gray-200 dark:bg-gray-800"
                  }`}
                />
              ))}
            </Animated.View>
          )}
        </View>
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
            activeOpacity={submittingSignupData ? 1 : 0.6}
            onPress={submittingSignupData ? undefined : numberBackspace}
            className={`w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center ${
              submittingSignupData
                ? "bg-gray-100 dark:bg-gray-900"
                : "bg-gray-200 dark:bg-gray-800"
            }`}
          >
            {!submittingSignupData && (
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
