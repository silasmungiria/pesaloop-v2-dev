import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import React, { useEffect, useState } from "react";
import { Ionicons } from "@expo/vector-icons";

import { changePhoneNumber } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { useNotification } from "@/features/hooks";
import { validatePhoneNumber } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { handleError } from "@/features/utils/handleError";

export default function ChangePhoneNumber({
  onClose,
}: {
  onClose: () => void;
}) {
  const { showNotification } = useNotificationToast();

  const [phoneNumber, setPhoneNumber] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [validated, setValidated] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setValidated(
      validatePhoneNumber(phoneNumber) && currentPassword.length === 6
    );
  }, [phoneNumber, currentPassword]);

  const onPhoneNumberUpdate = async () => {
    if (!validated) return;

    setLoading(true);

    const resetForm = () => {
      setPhoneNumber("");
      setCurrentPassword("");
    };

    try {
      const { data } = await changePhoneNumber({
        phoneNumber,
        currentPassword,
      });

      const message = data?.message || "Phone number updated successfully.";
      showNotification(message, "success", 6000);

      resetForm();
      onClose();
    } catch (error: any) {
      handleError(
        error,
        "Failed to update phone number. Please try again later."
      );

      resetForm();
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <Text className="text-gray-500 dark:text-gray-400 mb-8">
        Verify your account to update your phone number.
      </Text>

      <View className="mb-6">
        <Text className="text-gray-700 dark:text-gray-300 mb-4 font-medium">
          New Phone Number
        </Text>

        <View className="flex-row items-center p-2 rounded-xl border-b border-gray-200 dark:border-gray-700 mb-4">
          <Ionicons
            name="call-outline"
            size={20}
            color={defaultColors.green}
            className="mr-2"
          />
          <TextInput
            className="flex-1 text-lg text-gray-900 dark:text-gray-100"
            placeholder="Enter new phone number"
            placeholderTextColor="#888"
            keyboardType="phone-pad"
            value={phoneNumber}
            onChangeText={setPhoneNumber}
          />
        </View>
      </View>

      <View className="mb-8">
        <Text className="text-gray-700 dark:text-gray-300 mb-4 font-medium">
          Current Password
        </Text>
        <View className="flex-row items-center p-2 rounded-xl border-b border-gray-200 dark:border-gray-700">
          <Ionicons
            name="lock-closed-outline"
            size={20}
            color={defaultColors.red}
            className="mr-2"
          />
          <TextInput
            className="flex-1 text-lg text-gray-900 dark:text-gray-100"
            placeholder="Enter current password"
            placeholderTextColor="#888"
            secureTextEntry
            keyboardType="number-pad"
            value={currentPassword}
            onChangeText={setCurrentPassword}
          />
        </View>
      </View>

      <TouchableOpacity
        onPress={onPhoneNumberUpdate}
        disabled={!validated || loading}
        className="w-full"
      >
        <View
          className={`rounded-full py-4 flex-row items-center justify-center transition-all ${
            validated ? "bg-indigo-600" : "bg-gray-400 dark:bg-gray-800"
          }`}
        >
          {loading ? (
            <ActivityIndicator size="small" color={defaultColors.green} />
          ) : (
            <Text className="font-semibold text-center text-white text-lg">
              Update Phone Number
            </Text>
          )}
        </View>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}
