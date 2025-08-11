import React from "react";
import { Modal, View, Text, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import Animated from "react-native-reanimated";

import { defaultColors } from "@/features/constants";
import { useModalAnimation } from "@/features/lib";

interface Props {
  visible: boolean;
  onClose: () => void;
  data?: any;
}

const SuccessConfirmationModal: React.FC<Props> = ({
  visible,
  onClose,
  data,
}) => {
  const { modalAnimatedStyle } = useModalAnimation(visible);
  return (
    <Modal
      animationType="fade"
      transparent={true}
      visible={visible}
      onRequestClose={() => {
        onClose();
        router.back();
      }}
    >
      <Animated.View
        style={modalAnimatedStyle}
        className="flex-1 w-full p-5 justify-around bg-gray-100 dark:bg-gray-900 p-4 shadow-lg"
      >
        {/* Title and Success Icon */}
        <View className="items-center mt-6 mb-6s">
          <Text className="font-bold mb-4 text-3xl text-green-600 dark:text-green-400">
            Successful
          </Text>
          <View className="w-28 h-28 rounded-full flex items-center justify-center mb-4 bg-green-100 dark:bg-green-900">
            <Ionicons
              name="checkmark-circle"
              size={65}
              color={defaultColors.green}
            />
          </View>
        </View>

        {/* Transfer Details */}
        <View className="gap-y-3">
          <Text className="font-semibold text-lg text-gray-600 dark:text-gray-400">
            {data?.reference_id ? "Transfer Details:" : "Request Details:"}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Name:{" "}
            {data?.first_name && data?.last_name
              ? `${data.first_name} ${data.last_name}`
              : data?.requestee_profile?.full_name}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Amount:{" "}
            {(typeof data?.currency === "string"
              ? data.currency
              : data?.currency?.code) || "Unknown"}{" "}
            {data?.amount || "0"}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Reference: {data?.reference_id}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Email: {data?.email || data?.requestee_profile?.email || "N/A"}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Phone:{" "}
            {data?.phone_number ||
              data?.requestee_profile?.phone_number ||
              "N/A"}
          </Text>

          <Text className="text-lg text-gray-800 dark:text-gray-200">
            Status: {data?.status}
          </Text>

          {data?.reason && (
            <Text className="text-lg text-gray-800 dark:text-gray-200">
              Reason: {data.reason}
            </Text>
          )}
        </View>

        {/* OK Button */}
        <View className="mt-6 flex flex-row">
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              onClose();
              router.back();
            }}
            className="flex-1 p-4 rounded-full bg-indigo-600"
          >
            <Text className="text-lg font-semibold text-white text-center">
              OK
            </Text>
          </TouchableOpacity>
        </View>
      </Animated.View>
    </Modal>
  );
};

export default SuccessConfirmationModal;
