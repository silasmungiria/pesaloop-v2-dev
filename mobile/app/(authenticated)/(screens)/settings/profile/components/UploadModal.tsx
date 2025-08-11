import React from "react";
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  Pressable,
  ActivityIndicator,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { defaultColors } from "@/features/constants";
import { useModalAnimation } from "@/features/lib";
import Animated from "react-native-reanimated";

interface UploadModalProps {
  modalVisible?: boolean;
  onBackPress?: () => void;
  onCameraPress?: () => void;
  onGalleryPress?: () => void;
  onRemovePress?: () => void;
  isLoading?: boolean;
  imageType?: string | null;
}

export default function UploadModal({
  modalVisible = false,
  onBackPress,
  onCameraPress,
  onGalleryPress,
  isLoading = false,
  imageType,
}: UploadModalProps) {
  const { modalAnimatedStyle } = useModalAnimation(modalVisible);

  return (
    <Modal animationType="fade" transparent={true} visible={modalVisible}>
      <Pressable
        className="flex-1 justify-center items-center bg-black/50"
        onPress={onBackPress}
      >
        {isLoading && (
          <ActivityIndicator size={70} color={defaultColors.green} />
        )}

        {!isLoading && (
          <Animated.View
            style={modalAnimatedStyle}
            className="w-4/5 p-5 rounded-lg items-center bg-gray-100 dark:bg-gray-800"
          >
            <Text className="text-lg font-bold text-gray-900 dark:text-white mb-6">
              Upload a photo for your {imageType}
            </Text>

            <View className="flex-row justify-between w-full">
              <TouchableOpacity
                activeOpacity={0.8}
                onPress={onCameraPress}
                className="items-center gap-y-1"
              >
                <Ionicons name="camera-outline" size={28} color="#FACC15" />
                <Text className="text-base text-gray-900 dark:text-gray-100">
                  Camera
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                activeOpacity={0.8}
                onPress={onGalleryPress}
                className="items-center gap-y-1"
              >
                <Ionicons name="image-outline" size={20} color="#FACC15" />
                <Text className="text-base text-gray-700 dark:text-gray-300">
                  Gallery
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                activeOpacity={0.8}
                onPress={onBackPress}
                className="items-center gap-y-1"
              >
                <Ionicons
                  name="return-up-back-outline"
                  size={20}
                  color="gray"
                />
                <Text className="text-base text-gray-700 dark:text-gray-300">
                  Return
                </Text>
              </TouchableOpacity>
            </View>
          </Animated.View>
        )}
      </Pressable>
    </Modal>
  );
}
