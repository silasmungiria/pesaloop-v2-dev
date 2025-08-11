import React from "react";
import { View, Text, TouchableOpacity, FlatList } from "react-native";
import Animated, {
  FadeInDown,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

interface UserProfileProps {
  user: any;
}

export default function UserProfile({ user }: UserProfileProps) {
  const infoItems = [
    { label: "Full Name", value: `${user?.first_name} ${user?.last_name}` },
    { label: "Account Number", value: user?.account_number },
    {
      label: "Email Address",
      value: user?.email,
      verified: user?.is_email_verified,
    },
    {
      label: "Phone Number",
      value: user?.phone_number,
      verified: user?.is_phone_verified,
    },
    {
      label: "Account Status",
      value: user?.is_active ? "Active" : "Inactive",
    },
    {
      label: "Qualified for Loan",
      value: user?.is_loan_qualified ? "Yes" : "No",
      verified: user?.is_loan_qualified,
    },
  ];

  const renderItem = ({ item, index }: { item: any; index: number }) => (
    <Animated.View
      entering={FadeInDown.delay(Math.min(index * 100, 300)).springify()}
      exiting={FadeOutUp.springify()}
      layout={Layout.springify()}
      className="flex-row justify-between py-5 px-2 rounded-xl border-b border-gray-200 dark:border-gray-700"
    >
      <Text className="text-gray-700 dark:text-gray-300">{item.label}</Text>
      <View className="flex-row items-center gap-x-2">
        <Text className="font-semibold text-gray-900 dark:text-gray-100">
          {item.value}
        </Text>
        {item.verified !== undefined && (
          <Ionicons
            name={item.verified ? "checkmark-circle" : "close-circle"}
            size={18}
            color={item.verified ? "green" : "red"}
          />
        )}
      </View>
    </Animated.View>
  );

  return (
    <View className="flex-1 mb-12">
      {/* User Name + Verification Status */}
      <Animated.View entering={FadeInDown.duration(300)}>
        <View className="flex-row justify-center items-center gap-x-2 mb-6 p-3 rounded-xl">
          <Text className="font-semibold text-xl text-center text-gray-900 dark:text-gray-100">
            {user?.first_name} {user?.last_name}
          </Text>
          <Ionicons
            name={user?.is_verified ? "checkmark-circle" : "close-circle"}
            size={18}
            color={user?.is_verified ? "green" : "red"}
          />
        </View>
      </Animated.View>

      {/* Personal Info List */}
      <Animated.View entering={FadeInDown.delay(200).duration(300)}>
        <Text className="font-bold text-lg text-gray-800 dark:text-gray-200 mb-2">
          Personal Information
        </Text>

        <FlatList
          data={infoItems}
          renderItem={renderItem}
          keyExtractor={(item) => item.label}
          contentContainerStyle={{ paddingBottom: 20 }}
          scrollEnabled={false}
        />
      </Animated.View>
    </View>
  );
}
