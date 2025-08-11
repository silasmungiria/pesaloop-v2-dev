import React from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";

export default function Help() {
  return (
    <View className="flex-1 justify-end bg-white dark:bg-black">
      <View className="h-[90%] rounded-2xl p-6 bg-gray-100 dark:bg-gray-900 shadow-lg">
        <View className="mb-6 flex-row justify-between items-center">
          <Text className="text-3xl font-bold text-gray-700 dark:text-gray-300">
            Help & Support
          </Text>
          <TouchableOpacity onPress={() => router.back()} className="p-2">
            <Ionicons name="close" size={30} color="red" />
          </TouchableOpacity>
        </View>

        <View className="h-[2px] w-[60%] bg-gray-200 dark:bg-gray-800 mx-auto mb-6" />

        <Text className="text-lg text-gray-600 dark:text-gray-300 mb-6">
          Find answers to frequently asked questions or get support here.
        </Text>

        {/* FAQ Section */}
        <View className="mb-6">
          <Text className="font-bold text-lg text-gray-800 dark:text-gray-200 mb-3">
            Frequently Asked Questions
          </Text>
          <View className="space-y-3">
            <Text className="text-base text-gray-500 dark:text-gray-400">
              How do I reset my password?
            </Text>
            <Text className="text-base text-gray-500 dark:text-gray-400">
              How do I change my email address?
            </Text>
            <Text className="text-base text-gray-500 dark:text-gray-400">
              How do I deactivate my account?
            </Text>
          </View>
        </View>

        {/* Support Section */}
        <View>
          <Text className="font-bold text-lg text-gray-800 dark:text-gray-200 mb-3">
            Get Support
          </Text>
          <Text className="text-base text-gray-500 dark:text-gray-400 mb-3">
            If you need further assistance, please contact our support team:
          </Text>
          <Text className="text-base text-gray-500 dark:text-gray-400 mb-3">
            Contact Number: 123-456-7890
          </Text>
          <Text className="text-base text-gray-500 dark:text-gray-400 mb-3">
            Email: support@sendpesa.com
          </Text>
        </View>
      </View>
    </View>
  );
}
