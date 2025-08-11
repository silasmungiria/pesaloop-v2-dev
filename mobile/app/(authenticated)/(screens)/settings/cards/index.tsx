import { View, Text } from "react-native";
import React from "react";

export default function PaymentCard() {
  return (
    <View className="flex-1 p-6 bg-gray-100 dark:bg-gray-900">
      <Text className="text-lg text-gray-700 dark:text-gray-300">
        Payment Card
      </Text>
    </View>
  );
}
