import React from "react";
import { View, Text, TouchableOpacity } from "react-native";
export default function AirTelMoneyComponent({
  onClose,
}: {
  onClose: () => void;
}) {
  return (
    <View className="p-4">
      <Text className="text-lg font-medium text-gray-900 dark:text-gray-200">
        AirTel Money Payment
      </Text>
      <Text className="text-gray-600 dark:text-gray-400 mt-2">
        Enter your AirTel Money details to proceed.
      </Text>
      <TouchableOpacity
        onPress={onClose}
        className="mt-4 bg-red-500 p-2 rounded-lg"
      >
        <Text className="text-white text-center">Close</Text>
      </TouchableOpacity>
    </View>
  );
}
