import React, { useState } from "react";
import { View, Text, TouchableOpacity, useColorScheme } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";

import Notification from "./ToastNotification";
import { useBalanceStore } from "@/features/store";
import { formatCurrency } from "@/features/lib";

interface Props {
  onInputChange: (newInput: string) => void;
  exceedUserBalance?: boolean;
}

export default function Keypad({
  onInputChange,
  exceedUserBalance = false,
}: Props) {
  const scheme = useColorScheme();

  const { balance, currency } = useBalanceStore.getState();

  const [input, setInput] = useState<string>("");

  const [notificationMessage, setNotificationMessage] = useState("");
  const [isNotificationVisible, setIsNotificationVisible] = useState(false);
  const [hasApiCallSucceeded, setHasApiCallSucceeded] = useState(false);

  const handlePress = (value: string) => {
    const newAmount = Number(input + value);

    if (!exceedUserBalance && balance < newAmount) {
      const message = `Insufficient funds. Oops! Your balance is ${currency} ${formatCurrency(
        balance
      )}. Please top up.`;

      setNotificationMessage(message);
      setIsNotificationVisible(true);
      setHasApiCallSucceeded(false);

      Haptics?.notificationAsync(Haptics.NotificationFeedbackType.Error);
      return;
    }

    Haptics?.impactAsync(Haptics.ImpactFeedbackStyle.Soft);

    setInput((prevInput) => {
      const updatedInput = prevInput + value;
      onInputChange(updatedInput);
      return updatedInput;
    });
  };

  const handleDelete = () => {
    if (input.length === 0) return;

    if (Haptics) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft);
    }
    setInput((prevInput) => {
      const newInput = prevInput.slice(0, -1);
      onInputChange(newInput);
      return newInput;
    });
  };

  return (
    <View className="flex w-full justify-center items-center">
      {/* Show Notification */}
      <View className="absolute w-full items-center top-[-50%]">
        {isNotificationVisible && (
          <Notification
            message={notificationMessage}
            setMessage={setNotificationMessage}
            setVisible={setIsNotificationVisible}
            duration={6000}
            type={hasApiCallSucceeded ? "success" : "error"}
          />
        )}
      </View>

      {/* Keypad */}
      <View className="flex w-full items-center">
        {/* First row */}
        <View className="flex-row w-full justify-around items-center mb-4">
          {[1, 2, 3].map((number) => (
            <TouchableOpacity
              activeOpacity={0.8}
              key={number}
              onPress={() => handlePress(number.toString())}
              className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
            >
              <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                {number}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Second row */}
        <View className="flex-row w-full justify-around items-center mb-4">
          {[4, 5, 6].map((number) => (
            <TouchableOpacity
              activeOpacity={0.8}
              key={number}
              onPress={() => handlePress(number.toString())}
              className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
            >
              <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                {number}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Third row */}
        <View className="flex-row w-full justify-around items-center mb-4">
          {[7, 8, 9].map((number) => (
            <TouchableOpacity
              activeOpacity={0.8}
              key={number}
              onPress={() => handlePress(number.toString())}
              className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
            >
              <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                {number}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Fourth row */}
        <View className="flex-row w-full justify-around items-center">
          <View className="w-16 h-16 m-2 rounded-full justify-center items-center mb-4 bg-transparent" />
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => handlePress("0")}
            className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
          >
            <Text className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
              0
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={handleDelete}
            className="w-16 h-16 m-2 rounded-full bg-gray-200 dark:bg-gray-800 justify-center items-center"
          >
            <Ionicons
              name="backspace-outline"
              size={20}
              color={scheme === "dark" ? "#D1D5DB" : "#4B5563"}
            />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
