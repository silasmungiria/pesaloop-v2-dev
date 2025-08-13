import React, { useState } from "react";
import {
  ActivityIndicator,
  TextInput,
  FlatList,
  View,
  Text,
  TouchableOpacity,
} from "react-native";
import Animated, { FadeInDown, FadeInUp } from "react-native-reanimated";

import { PhoneCodePicker } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { useBalanceStore } from "@/features/store";

const AnimatedView = Animated.createAnimatedComponent(View);
const AnimatedTouchable = Animated.createAnimatedComponent(TouchableOpacity);
const AnimatedText = Animated.createAnimatedComponent(Text);

export default function MpesaComponent({ onClose }: { onClose: () => void }) {
  const { currency } = useBalanceStore();

  const [selectedCountryCode, setSelectedCountryCode] = useState("+254");
  const [recipientPhoneNumber, setRecipientPhoneNumber] = useState("");
  const [transferAmount, setTransferAmount] = useState("");
  const [transferNote, setTransferNote] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [isCountryPickerVisible, setIsCountryPickerVisible] = useState(false);

  const isFormReady =
    recipientPhoneNumber.length >= 9 &&
    transferAmount.length > 0 &&
    !isNaN(Number(transferAmount));

  const handleSendMoney = async () => {
    if (!isFormReady) return;

    setIsSending(true);
    try {
      // Simulate Send Money API call
      await new Promise((resolve) => setTimeout(resolve, 2000));

      console.log(
        `Initiating Send Money to ${selectedCountryCode}${recipientPhoneNumber} for KES ${transferAmount}`
      );

      // Reset form fields
      setRecipientPhoneNumber("");
      setTransferAmount("");
      setTransferNote("");
    } catch (error) {
      console.error("Error during Send Money:", error);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <View className="px-2 flex-1 bg-gray-100 dark:bg-gray-900">
      <FlatList
        data={[]}
        renderItem={null}
        ListHeaderComponent={
          <>
            <AnimatedText
              entering={FadeInDown.duration(400)}
              className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4"
            >
              Send Money to M-Pesa
            </AnimatedText>

            <AnimatedText
              entering={FadeInDown.delay(100).duration(200)}
              className="text-gray-600 dark:text-gray-400 text-lg mb-3"
            >
              Enter the recipient's phone number and amount to send
            </AnimatedText>

            {isSending && (
              <AnimatedText
                entering={FadeInUp.duration(200)}
                className="text-gray-500 dark:text-gray-400 text-sm mt-2"
              >
                Sending {currency} {transferAmount} to{" "}
                {selectedCountryCode + recipientPhoneNumber}...
              </AnimatedText>
            )}

            <AnimatedView
              entering={FadeInDown.delay(200).duration(200)}
              className="flex-row items-center mt-4"
            >
              <TouchableOpacity
                activeOpacity={0.8}
                onPress={() => setIsCountryPickerVisible(true)}
              >
                <Text className="text-lg font-bold p-4 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700">
                  {selectedCountryCode}
                </Text>
              </TouchableOpacity>
              <TextInput
                value={recipientPhoneNumber}
                onChangeText={setRecipientPhoneNumber}
                placeholder="M-Pesa phone number"
                keyboardType="phone-pad"
                placeholderTextColor="#9CA3AF"
                className="flex-1 p-5 ml-2 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
              />
            </AnimatedView>

            <AnimatedView entering={FadeInDown.delay(200).duration(200)}>
              <TextInput
                value={transferAmount}
                onChangeText={(text) => {
                  if (/^\d*$/.test(text)) {
                    setTransferAmount(text);
                  }
                }}
                maxLength={6}
                placeholder="Amount (e.g. 100)"
                keyboardType="numeric"
                placeholderTextColor="#9CA3AF"
                className="mt-4 p-5 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
              />

              {Number(transferAmount) > 0 && (
                <Text className="mt-2 px-5 text-lg font-semibold text-green-700 dark:text-green-400">
                  {currency}{" "}
                  {transferAmount.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")}
                </Text>
              )}
            </AnimatedView>

            <AnimatedView entering={FadeInDown.delay(200).duration(200)}>
              <TextInput
                value={transferNote}
                onChangeText={setTransferNote}
                placeholder="Reason (optional)"
                placeholderTextColor="#9CA3AF"
                className="mt-4 p-5 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
              />
            </AnimatedView>

            <AnimatedTouchable
              entering={FadeInUp.duration(200)}
              activeOpacity={0.8}
              onPress={handleSendMoney}
              disabled={!isFormReady}
              className={`flex-1 mt-10 p-4 rounded-full ${
                isFormReady ? "bg-indigo-600" : "bg-gray-400"
              }`}
            >
              {isSending ? (
                <ActivityIndicator size="small" color={defaultColors.green} />
              ) : (
                <Text
                  className={`text-center font-semibold ${
                    isFormReady ? "text-white" : "text-gray-700"
                  }`}
                >
                  Send {currency} {transferAmount || ""}
                </Text>
              )}
            </AnimatedTouchable>

            <PhoneCodePicker
              visible={isCountryPickerVisible}
              setVisible={setIsCountryPickerVisible}
              setCountryCode={setSelectedCountryCode}
            />
          </>
        }
      />
    </View>
  );
}
