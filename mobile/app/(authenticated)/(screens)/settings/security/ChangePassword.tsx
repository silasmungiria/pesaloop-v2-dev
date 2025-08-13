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

import { changePassword } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { useNotificationToast } from "@/features/providers";
import { handleError } from "@/features/utils/handleError";

export default function ChangePassword({ onClose }: { onClose: () => void }) {
  const { showNotification } = useNotificationToast();

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [validated, setValidated] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setValidated(
      newPassword.length === 6 &&
        confirmPassword.length === 6 &&
        currentPassword.length > 1 &&
        newPassword === confirmPassword
    );
  }, [currentPassword, newPassword, confirmPassword]);

  const onPasswordUpdate = async () => {
    if (!validated) return;

    setLoading(true);

    const resetForm = () => {
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    };

    try {
      const { data } = await changePassword({
        currentPassword,
        newPassword,
        confirmPassword,
      });

      const message = data?.message || "Password updated successfully.";
      showNotification(message, "success", 6000);

      resetForm();
      onClose();
    } catch (error: any) {
      handleError(error, "Failed to update password. Please try again later.");

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
        Verify your account to update your password.
      </Text>

      <View className="mb-6">
        <Text className="text-gray-700 dark:text-gray-300 mb-4 font-medium">
          Current Password
        </Text>
        <View className="flex-row items-center p-2 rounded-xl border-b border-gray-200 dark:border-gray-700 mb-4">
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

      <View className="mb-6">
        <Text className="text-gray-700 dark:text-gray-300 mb-4 font-medium">
          New Password
        </Text>
        <View className="flex-row items-center p-2 rounded-xl border-b border-gray-200 dark:border-gray-700 mb-4">
          <Ionicons
            name="lock-closed-outline"
            size={20}
            color={defaultColors.primary}
            className="mr-2"
          />
          <TextInput
            className="flex-1 text-lg text-gray-900 dark:text-gray-100"
            placeholder="Enter new password"
            placeholderTextColor="#888"
            keyboardType="number-pad"
            secureTextEntry
            value={newPassword}
            onChangeText={setNewPassword}
          />
        </View>
      </View>

      <View className="mb-8">
        <Text className="text-gray-700 dark:text-gray-300 mb-4 font-medium">
          Confirm New Password
        </Text>
        <View className="flex-row items-center p-2 rounded-xl border-b border-gray-200 dark:border-gray-700 mb-4">
          <Ionicons
            name="lock-closed-outline"
            size={20}
            color={defaultColors.green}
            className="mr-2"
          />
          <TextInput
            className="flex-1 text-lg text-gray-900 dark:text-gray-100"
            placeholder="Confirm new password"
            placeholderTextColor="#888"
            secureTextEntry
            keyboardType="number-pad"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
          />
        </View>
      </View>

      <TouchableOpacity
        onPress={onPasswordUpdate}
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
              Update Password
            </Text>
          )}
        </View>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}
