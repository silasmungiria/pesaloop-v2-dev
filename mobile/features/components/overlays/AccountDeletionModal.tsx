import React from "react";
import { Modal, View, Text, TouchableOpacity } from "react-native";
import Animated from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

import { useModalAnimation } from "@/features/lib";
import { BaseModalProps } from "@/types";

const AccountDeletionModal: React.FC<BaseModalProps> = ({
  visible,
  onClose,
}) => {
  const onDelete = () => {
    onClose();
    console.info("Deleted account");
  };
  const { modalAnimatedStyle } = useModalAnimation(visible);

  return (
    <Modal
      animationType="slide"
      transparent
      visible={visible}
      onRequestClose={onClose}
    >
      {/* Dark overlay */}
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      {/* Modal container */}
      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 w-full rounded-t-3xl bg-white dark:bg-gray-900 p-6 shadow-lg"
      >
        <View className="flex items-center">
          <Text className="font-bold text-xl text-gray-900 dark:text-gray-100 mb-4">
            Delete Account
          </Text>

          {/* Warning icon */}
          <View className="w-16 h-16 rounded-full flex items-center justify-center bg-red-200 dark:bg-red-500 mb-4">
            <Ionicons name="warning-outline" size={32} color="#9B2C2C" />
          </View>

          <Text className="text-center text-gray-700 dark:text-gray-300 text-base mb-6">
            Are you sure you want to delete your account? This action is
            irreversible.
          </Text>

          <View className="flex-row w-full justify-between gap-3">
            {/* Cancel Button */}
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={onClose}
              className="flex-1 p-4 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
            >
              <Text className="text-center text-gray-800 dark:text-gray-200 text-lg font-medium">
                Cancel
              </Text>
            </TouchableOpacity>

            {/* Delete Button */}
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={onDelete}
              className="flex-1 p-4 rounded-lg bg-red-600 hover:bg-red-700 active:bg-red-800 transition"
            >
              <Text className="text-center text-white text-lg font-medium">
                Delete
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </Animated.View>
    </Modal>
  );
};

export default AccountDeletionModal;
