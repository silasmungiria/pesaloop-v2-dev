import React, { useState, useEffect } from "react";
import {
  ActivityIndicator,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  FlatList,
} from "react-native";
import Animated, {
  useSharedValue,
  withTiming,
  FadeInUp,
  FadeInDown,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";

import { initiateMpesaSTKPush } from "@/features/api";
import { PhoneCodePicker } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { validatePhoneNumber } from "@/features/lib";
import { useDeviceContext, useNotificationToast } from "@/features/providers";
import { useBalanceStore } from "@/features/store";

const AnimatedView = Animated.createAnimatedComponent(View);
const AnimatedTouchable = Animated.createAnimatedComponent(TouchableOpacity);
const AnimatedText = Animated.createAnimatedComponent(Text);

export default function MpesaComponent({ onClose }: { onClose: () => void }) {
  const { deviceDetails } = useDeviceContext();
  const { showNotification } = useNotificationToast();
  const { currency } = useBalanceStore();

  const [countryCode, setCountryCode] = useState(
    deviceDetails?.countryCallingCode || "+254"
  );
  const [countryPicker, setCountryPicker] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [reason, setReason] = useState("");
  const [useSTKPush, setUseSTKPush] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const isFormValid =
    phoneNumber.trim() !== "" && !isNaN(Number(amount)) && Number(amount) > 0;

  // Animation values
  const buttonScale = useSharedValue(1);
  const buttonOpacity = useSharedValue(0.5);

  useEffect(() => {
    buttonScale.value = withTiming(isFormValid ? 1 : 0.95, { duration: 200 });
    buttonOpacity.value = withTiming(isFormValid ? 1 : 0.5, { duration: 200 });
  }, [isFormValid]);

  const handleStkPush = async () => {
    const fullPhoneNumber = phoneNumber.startsWith("+")
      ? phoneNumber
      : `${countryCode}${phoneNumber}`;

    if (!validatePhoneNumber(fullPhoneNumber)) {
      Alert.alert("Invalid", "Please enter a valid phone number.");
      return;
    }

    if (!fullPhoneNumber || !amount) {
      Alert.alert("Error", "Please enter both phone number and amount.");
      return;
    }

    setIsLoading(true);
    try {
      const { data } = await initiateMpesaSTKPush({
        phone_number: fullPhoneNumber,
        amount: parseFloat(amount),
        reason,
      });

      console.info("STK Push response:", data);

      // Alert.alert("Success", `${data?.message}`);
      showNotification(`${data?.message}`, "success", 6000);

      setTimeout(() => {
        onClose();
      }, 3000);
    } catch (error) {
      // Alert.alert("Error", "Failed to send STK Push request.");
      showNotification(
        "Failed to send STK Push request. Please try again.",
        "error",
        6000
      );
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      console.error("STK Push error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView className="flex-1 p-2 bg-gray-100 dark:bg-gray-900">
      {useSTKPush ? (
        <FlatList
          data={[]}
          renderItem={null}
          ListHeaderComponent={
            <>
              <AnimatedText
                entering={FadeInDown.duration(400)}
                className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4"
              >
                Top Up Your Wallet
              </AnimatedText>

              <AnimatedText
                entering={FadeInDown.delay(100).duration(200)}
                className="text-gray-600 dark:text-gray-400 text-lg mb-3"
              >
                Enter your phone number and amount:
              </AnimatedText>

              {isLoading && (
                <AnimatedText
                  entering={FadeInUp.duration(200)}
                  className="text-gray-500 dark:text-gray-400 text-sm mt-2"
                >
                  Processing STK Push to {countryCode + phoneNumber} for KES{" "}
                  {amount}...
                </AnimatedText>
              )}

              <AnimatedView
                entering={FadeInDown.delay(200).duration(200)}
                className="flex-row items-center mt-4"
              >
                <TouchableOpacity
                  activeOpacity={0.8}
                  onPress={() => setCountryPicker(true)}
                >
                  <Text className="text-lg font-bold p-4 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700">
                    {countryCode}
                  </Text>
                </TouchableOpacity>
                <TextInput
                  value={phoneNumber}
                  onChangeText={setPhoneNumber}
                  placeholder="M-Pesa Phone number"
                  keyboardType="phone-pad"
                  placeholderTextColor="#9CA3AF"
                  className="flex-1 p-5 ml-2 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
                />
              </AnimatedView>

              <AnimatedView entering={FadeInDown.delay(200).duration(200)}>
                <TextInput
                  value={amount}
                  onChangeText={(text) => {
                    if (/^\d*$/.test(text)) {
                      setAmount(text);
                    }
                  }}
                  maxLength={6}
                  placeholder="Amount (e.g. 100)"
                  keyboardType="numeric"
                  placeholderTextColor="#9CA3AF"
                  className="mt-4 p-5 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
                />

                {/* Show formatted amount */}
                {Number(amount) > 0 && (
                  <Text className="mt-2 px-5 text-lg font-semibold text-green-700 dark:text-green-400">
                    {currency}{" "}
                    {amount.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")}
                  </Text>
                )}
              </AnimatedView>

              <AnimatedView entering={FadeInDown.delay(200).duration(200)}>
                <TextInput
                  value={reason}
                  onChangeText={setReason}
                  placeholder="Reason (optional)"
                  placeholderTextColor="#9CA3AF"
                  className="mt-4 p-5 rounded-lg text-gray-900 dark:text-gray-100 border-b border-gray-300 dark:border-gray-700"
                />
              </AnimatedView>

              <View className="flex-row items-center justify-between mt-6 gap-x-4">
                <AnimatedTouchable
                  entering={FadeInUp.duration(200)}
                  activeOpacity={0.8}
                  onPress={() => setUseSTKPush(false)}
                  className="flex-1 mt-4 p-4 rounded-full shadow-md bg-green-700"
                >
                  <Text className="text-white text-center font-semibold">
                    Use Paybill
                  </Text>
                </AnimatedTouchable>

                <AnimatedTouchable
                  entering={FadeInUp.duration(200)}
                  activeOpacity={0.8}
                  onPress={handleStkPush}
                  disabled={!isFormValid}
                  className={`flex-1 mt-4 p-4 rounded-full ${
                    isFormValid ? "bg-indigo-600" : "bg-gray-400"
                  }`}
                >
                  {isLoading ? (
                    <ActivityIndicator
                      size="small"
                      color={defaultColors.green}
                    />
                  ) : (
                    <Text
                      className={`text-center font-semibold ${
                        isFormValid ? "text-white" : "text-gray-700"
                      }`}
                    >
                      Proceed with STK Push
                    </Text>
                  )}
                </AnimatedTouchable>
              </View>

              <PhoneCodePicker
                isVisible={countryPicker}
                setIsVisible={setCountryPicker}
                setCountryCode={setCountryCode}
              />
            </>
          }
        />
      ) : (
        <FlatList
          data={[
            "Open M-Pesa on your phone.",
            "Go to Lipa na M-Pesa.",
            "Select Paybill.",
            "Enter the Paybill Number: ABC123456.",
            "Enter your account number: (e.g., email or phone number)",
            "Enter the amount: KES 1000.",
            "Confirm the payment and enter your M-Pesa PIN.",
            "You'll receive an SMS confirmation.",
          ]}
          keyExtractor={(_, index) => index.toString()}
          contentContainerStyle={{ paddingBottom: 20 }}
          ListHeaderComponent={
            <>
              <AnimatedText
                entering={FadeInDown.duration(200)}
                className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4"
              >
                Top Up Your Wallet
              </AnimatedText>
              <AnimatedText
                entering={FadeInDown.delay(100).duration(400)}
                className="text-gray-700 dark:text-gray-300 font-semibold mb-3"
              >
                Paybill Payment Guidelines:
              </AnimatedText>
            </>
          }
          renderItem={({ item, index }) => (
            <AnimatedView
              entering={FadeInUp.delay(index * 50).duration(300)}
              className="mb-4 flex-row items-center gap-x-2"
            >
              <Ionicons
                name="checkmark-circle-outline"
                size={20}
                color="#4B5563"
              />
              <Text className="text-lg text-gray-600 dark:text-gray-400">
                {item}
              </Text>
            </AnimatedView>
          )}
          ListFooterComponent={
            <AnimatedTouchable
              entering={FadeInUp.delay(200).duration(200)}
              activeOpacity={0.8}
              onPress={() => setUseSTKPush(true)}
              className="mt-5 p-4 rounded-full shadow-md bg-indigo-600"
            >
              <Text className="text-white text-center font-semibold">
                Use STK Push
              </Text>
            </AnimatedTouchable>
          }
        />
      )}
    </KeyboardAvoidingView>
  );
}
