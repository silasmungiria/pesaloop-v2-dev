import React from "react";
import { Text, TouchableOpacity, useColorScheme } from "react-native";
import Animated, {
  FadeInDown,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";

type HeaderProps = {
  showVerificationModal: () => void;
};

export default function Header({ showVerificationModal }: HeaderProps) {
  const scheme = useColorScheme();
  const iconColor = scheme === "dark" ? "#D1D5DB" : "#4B5563";
  const iconSize = 20;

  return (
    <Animated.View
      entering={FadeInDown.delay(100).springify()}
      exiting={FadeOutUp.springify()}
      layout={Layout.springify()}
      className="flex-row items-center justify-between mb-[10%]"
    >
      <TouchableOpacity onPress={router.back}>
        <Ionicons name="arrow-back-outline" size={iconSize} color={iconColor} />
      </TouchableOpacity>

      <Text className="font-extrabold text-2xl text-gray-900 dark:text-gray-100 text-center">
        Hello there 👋
      </Text>

      <TouchableOpacity onPress={showVerificationModal}>
        <Ionicons name="create-outline" size={iconSize} color={iconColor} />
      </TouchableOpacity>
    </Animated.View>
  );
}
