import React, { useState, useCallback } from "react";
import { View, Text, TouchableOpacity, Modal, ScrollView } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import Animated, { FadeInUp } from "react-native-reanimated";

import { useModalAnimation } from "@/features/lib";

export interface PaymentMethod {
  name: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  Component: React.FC<{ onClose: () => void }>;
}

interface ExternalServicesScreenProps {
  paymentMethods: PaymentMethod[];
}

export default function ExternalServicesScreen({
  paymentMethods,
}: ExternalServicesScreenProps) {
  const [selectedMethod, setSelectedMethod] = useState<PaymentMethod | null>(
    null
  );

  const openModal = useCallback(
    (method: PaymentMethod) => setSelectedMethod(method),
    []
  );
  const closeModal = useCallback(() => setSelectedMethod(null), []);

  const { modalAnimatedStyle } = useModalAnimation(!!selectedMethod);

  return (
    <ScrollView className="flex-1 p-4 bg-gray-100 dark:bg-gray-900">
      <View className="flex-row flex-wrap">
        {paymentMethods.map((method, index) => (
          <Animated.View
            key={method.name}
            entering={FadeInUp.delay(index * 100).springify()}
            className="w-1/2 p-2"
          >
            <PaymentMethodCard
              method={method}
              onPress={() => openModal(method)}
            />
          </Animated.View>
        ))}
      </View>

      <Modal
        visible={!!selectedMethod}
        transparent
        animationType="fade"
        onRequestClose={closeModal}
      >
        <Animated.View
          style={modalAnimatedStyle}
          className="flex-1 p-6 bg-gray-100 dark:bg-gray-900"
        >
          <View className="flex-row justify-between items-center mb-4">
            <Text className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              {selectedMethod?.name}
            </Text>

            <TouchableOpacity onPress={closeModal} className="p-2 rounded-full">
              <Ionicons name="close" size={20} color="red" />
            </TouchableOpacity>
          </View>

          {selectedMethod && <selectedMethod.Component onClose={closeModal} />}
        </Animated.View>
      </Modal>
    </ScrollView>
  );
}

const PaymentMethodCard = ({
  method,
  onPress,
}: {
  method: PaymentMethod;
  onPress: () => void;
}) => (
  <TouchableOpacity onPress={onPress} activeOpacity={0.9} className="w-full">
    <View className="flex-row items-center gap-3 rounded-2xl p-4 bg-gray-200 dark:bg-gray-800">
      <Ionicons name={method.icon} size={20} color={method.color} />
      <Text className="text-base font-medium text-gray-900 dark:text-gray-100">
        {method.name}
      </Text>
    </View>
  </TouchableOpacity>
);
