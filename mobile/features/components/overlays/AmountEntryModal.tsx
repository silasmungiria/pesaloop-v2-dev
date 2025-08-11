import React, { useEffect, useState } from "react";
import { View, Text, Modal, TouchableOpacity } from "react-native";
import Animated, { FadeIn, FadeInUp, ZoomIn } from "react-native-reanimated";
import * as Haptics from "expo-haptics";
import { Ionicons } from "@expo/vector-icons";

import { Keypad } from "@/features/components";
import { formatCurrency, validateAmount } from "@/features/lib";
import { useBalanceStore } from "@/features/store";
import { defaultColors } from "@/features/constants";

interface Props {
  isVisible: boolean;
  setIsVisible: (value: boolean) => void;
  setAmount: (value: string) => void;
  setRecipientModalVisible: (value: boolean) => void;
  exceedUserBalance?: boolean;
}

const AmountEntryModal = ({
  isVisible,
  setIsVisible,
  setAmount,
  setRecipientModalVisible,
  exceedUserBalance = false,
}: Props) => {
  const [amountInput, setAmountInput] = useState<string>("");
  const [amountValid, setAmountValid] = useState(false);
  const [textWidth, setTextWidth] = useState(0);

  const { balance, currency } = useBalanceStore.getState();

  const handleInputChange = (newInput: string) => {
    setAmountInput(newInput);
  };

  useEffect(() => {
    setAmountValid(validateAmount(amountInput));
  }, [amountInput]);

  const onContinue = async () => {
    if (!exceedUserBalance && balance < Number(amountInput)) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      return;
    }

    setAmount(amountInput);
    setIsVisible(false);
  };

  return (
    <Modal
      animationType="fade"
      transparent
      visible={isVisible}
      onRequestClose={() => {
        setIsVisible(false);
        setRecipientModalVisible(true);
      }}
    >
      <View className="flex-1 p-6 bg-gray-100 dark:bg-gray-900">
        <View className="flex-1 w-full justify-between">
          {/* Header */}
          <Animated.View
            entering={FadeIn.delay(500)}
            className="flex-row items-center justify-between mt-6 mb-10"
          >
            {/* Title */}
            <Text className="font-extrabold text-xl text-gray-700 dark:text-gray-300">
              Enter the amount to proceed
            </Text>

            {/* Close Button */}
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => {
                setIsVisible(false);
                setRecipientModalVisible(true);
              }}
            >
              <Ionicons name="close" size={28} color={defaultColors.red} />
            </TouchableOpacity>
          </Animated.View>

          <Animated.View
            entering={FadeIn.delay(500)}
            className="w-full mb-10 rounded-xl justify-center items-center p-5"
          >
            <Text
              onLayout={(event) => {
                const { width } = event.nativeEvent.layout;
                setTextWidth(width);
              }}
              className={`font-bold text-2xl ${
                amountInput && Number(amountInput) === 0
                  ? "text-red-500"
                  : amountInput === ""
                  ? "text-gray-400 dark:text-gray-600"
                  : "text-gray-700 dark:text-gray-300"
              }`}
            >
              {amountInput
                ? `${currency} ${formatCurrency(Number(amountInput))}`
                : "Enter Amount"}
            </Text>

            <View
              style={{ width: textWidth }}
              className="h-1 rounded-full mt-2 bg-blue-600 dark:bg-blue-400"
            />
          </Animated.View>

          {/* Keypad */}
          <Animated.View entering={ZoomIn.delay(300)}>
            <Keypad
              onInputChange={(value) => {
                requestAnimationFrame(() => handleInputChange(value));
              }}
              exceedUserBalance={exceedUserBalance}
            />
          </Animated.View>

          {/* Buttons */}
          <Animated.View
            className="w-full max-w-lg mt-4"
            entering={FadeInUp.delay(400).duration(300)}
          >
            <TouchableOpacity
              activeOpacity={0.9}
              onPress={onContinue}
              disabled={!amountValid}
              className={`w-full p-4 rounded-full ${
                amountValid ? "bg-indigo-600" : "bg-gray-200 dark:bg-gray-800"
              }`}
            >
              <Text className="font-semibold text-lg text-center text-gray-300">
                Validate & Continue
              </Text>
            </TouchableOpacity>
          </Animated.View>
        </View>
      </View>
    </Modal>
  );
};

export default AmountEntryModal;
