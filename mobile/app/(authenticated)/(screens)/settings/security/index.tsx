import React, { useCallback, useMemo, useState } from "react";
import { View, Text, TouchableOpacity, Modal, Pressable } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import Animated, { FadeInUp } from "react-native-reanimated";

import ChangeEmail from "./ChangeEmail";
import ChangePassword from "./ChangePassword";
import ChangePhoneNumber from "./ChangePhoneNumber";
import { useModalAnimation } from "@/features/lib";

interface LinkProps {
  name: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  Component: React.FC<{ onClose: () => void }>;
}

export default function Index() {
  const [selectedLink, setSelectedLink] = useState<LinkProps | null>(null);

  const links = useMemo<LinkProps[]>(
    () => [
      {
        name: "Update Email",
        icon: "mail-outline",
        color: "#9b59d6",
        Component: ChangeEmail,
      },
      {
        name: "Update Phone Number",
        icon: "call-outline",
        color: "#34bfa3",
        Component: ChangePhoneNumber,
      },
      {
        name: "Update Password",
        icon: "lock-closed-outline",
        color: "#e94e77",
        Component: ChangePassword,
      },
    ],
    []
  );

  const openModal = useCallback(
    (method: LinkProps) => setSelectedLink(method),
    []
  );
  const closeModal = useCallback(() => setSelectedLink(null), []);

  const { modalAnimatedStyle } = useModalAnimation(!!selectedLink);

  return (
    <View className="flex-1 p-4 bg-gray-100 dark:bg-gray-900">
      <View className="flex-row flex-wrap gap-3">
        {links.map((method) => (
          <TouchableOpacity
            key={method.name}
            onPress={() => openModal(method)}
            activeOpacity={0.85}
            className="w-full"
          >
            <Animated.View
              entering={FadeInUp.delay(50)}
              className="rounded-2xl px-5 py-7 flex-row items-center justify-between bg-white dark:bg-gray-800"
            >
              <View className="flex-row items-center gap-x-4">
                <Ionicons name={method.icon} size={20} color={method.color} />
                <Text className="text-gray-900 dark:text-gray-100">
                  {method.name}
                </Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#cbd5e1" />
            </Animated.View>
          </TouchableOpacity>
        ))}
      </View>

      <Modal
        visible={!!selectedLink}
        transparent
        animationType="fade"
        onRequestClose={closeModal}
      >
        <View className="flex-1 bg-black/50 justify-center items-center px-4">
          <Animated.View
            style={modalAnimatedStyle}
            className="w-full max-w-lg bg-white dark:bg-gray-900 rounded-3xl p-6"
          >
            <View className="flex-row justify-between items-center mb-5">
              <Text className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                {selectedLink?.name}
              </Text>
              <Pressable onPress={closeModal} className="p-2 rounded-full">
                <Ionicons name="close" size={24} color="#ef4444" />
              </Pressable>
            </View>

            <View>
              {selectedLink && <selectedLink.Component onClose={closeModal} />}
            </View>
          </Animated.View>
        </View>
      </Modal>
    </View>
  );
}
