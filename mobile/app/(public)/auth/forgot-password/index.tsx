import { useState, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";

import { forgotPassword } from "@/features/api";
import { validateEmail } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { handleError } from "@/features/utils/handleError";

export default function ForgotPassword() {
  const { showNotification } = useNotificationToast();

  const [email, setEmail] = useState("");
  const [isSubmittingForgotPassword, setIsSubmittingForgotPassword] =
    useState(false);

  const emailRef = useRef<TextInput | null>(null);
  const isNextDisabled = !validateEmail(email);

  const onSubmitForgotPassword = async () => {
    if (isNextDisabled) return;
    setIsSubmittingForgotPassword(true);
    try {
      const result = await forgotPassword({ identifier: email });

      const message = typeof result === "string" ? result : result.message;
      showNotification(message || "Success!", "success", 6000);

      setEmail("");
      setTimeout(() => router.push("/auth/login"), 5000);
    } catch (error) {
      handleError(error, "Failed to send reset link. Please try again later.");
    } finally {
      setIsSubmittingForgotPassword(false);
    }
  };

  return (
    <View className="flex-1 justify-end bg-white dark:bg-black">
      <View className="h-[80%] rounded-2xl p-6 bg-gray-100 dark:bg-gray-900 shadow-lg">
        <View className="mb-6 flex-row justify-between items-center">
          <Text className="text-3xl font-bold text-gray-700 dark:text-gray-300">
            Forgot Password
          </Text>
          <TouchableOpacity onPress={() => router.back()} className="p-2">
            <Ionicons name="close" size={30} color="red" />
          </TouchableOpacity>
        </View>

        <View className="h-[2px] w-[60%] bg-gray-200 dark:bg-gray-800 mx-auto mb-6" />

        <Text className="text-lg text-gray-600 dark:text-gray-400 mb-6">
          Enter your registered email address to receive a password reset link.
        </Text>

        <ScrollView keyboardShouldPersistTaps="handled">
          <View className="gap-y-6">
            <TextInput
              ref={emailRef}
              placeholder="Email"
              autoCapitalize="none"
              placeholderTextColor="gray"
              keyboardType="email-address"
              value={email}
              onChangeText={setEmail}
              returnKeyType="done"
              onSubmitEditing={onSubmitForgotPassword}
              className="p-5 rounded-2xl text-lg text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
            />

            <TouchableOpacity
              activeOpacity={0.8}
              onPress={onSubmitForgotPassword}
              disabled={isNextDisabled}
              className={`p-5 rounded-full shadow-md flex-row justify-center items-center ${
                isNextDisabled
                  ? "bg-gray-300 dark:bg-gray-700"
                  : "bg-indigo-600"
              }`}
            >
              {isSubmittingForgotPassword ? (
                <ActivityIndicator size="small" color="white" />
              ) : (
                <Text className="text-xl font-semibold text-white">Submit</Text>
              )}
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </View>
  );
}
