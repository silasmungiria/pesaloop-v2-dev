import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  Pressable,
  KeyboardAvoidingView,
  Alert,
} from "react-native";
import Animated, { FadeInUp, FadeInDown } from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

import { useUserStore } from "@/features/store";

export default function CreditIssuance() {
  const { user } = useUserStore();

  // Date calculations
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const today = currentDate.getDate();
  const hoursNow = currentDate.getHours();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const remainingHoursToday = 23 - hoursNow;
  const isLastDayOfMonth = today === daysInMonth;
  const includeToday = remainingHoursToday > 18;
  const remainingDays = isLastDayOfMonth
    ? 1
    : daysInMonth - today + (includeToday ? 1 : 0);
  const remainingDaysPercent = (remainingDays / daysInMonth) * 100;

  // Credit config
  const dailyInterestRate = 0.00461;
  const minAmount = 50;
  const maxAmount = 100000;
  const currencySymbol = "KES";
  const displayMin = `${currencySymbol} ${minAmount.toLocaleString("en-US")}`;
  const displayMax = `${currencySymbol} ${maxAmount.toLocaleString("en-US")}`;
  const recommendedAmount = Math.floor(
    minAmount + (remainingDays / daysInMonth) * (maxAmount - minAmount)
  );

  const [amount, setAmount] = useState(
    recommendedAmount.toLocaleString("en-US")
  );
  const [submitting, setSubmitting] = useState(false);

  const parsedAmount = parseInt(amount.replace(/,/g, ""), 10) || 0;
  const progressPercent = Math.round((parsedAmount / maxAmount) * 100);

  const totalInterest = (
    parsedAmount *
    dailyInterestRate *
    remainingDays
  ).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const totalRepayment = (
    parsedAmount +
    parsedAmount * dailyInterestRate * remainingDays
  ).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const handleAmountChange = (value: string) => {
    const numericValue = parseInt(value.replace(/[^0-9]/g, ""), 10);
    if (!isNaN(numericValue)) {
      const clamped = Math.max(minAmount, Math.min(numericValue, maxAmount));
      setAmount(clamped.toLocaleString("en-US"));
    } else {
      setAmount(minAmount.toLocaleString("en-US"));
    }
  };

  const adjustAmount = (direction: "increment" | "decrement") => {
    const step = Math.floor(maxAmount / 10);
    const newAmount =
      direction === "increment"
        ? Math.min(parsedAmount + step, maxAmount)
        : Math.max(parsedAmount - step, minAmount);
    setAmount(newAmount.toLocaleString("en-US"));
  };

  const submitCreditApplication = () => {
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      Alert.alert(
        "Application Submitted",
        "Your credit application has been sent successfully."
      );
      setAmount(recommendedAmount.toLocaleString("en-US"));
    }, 2000);
  };

  const animatedEnter = (delay: number) =>
    FadeInUp.delay(delay)
      .duration(500)
      .springify()
      .damping(18)
      .mass(0.7)
      .stiffness(110);

  return (
    <KeyboardAvoidingView behavior="padding" className="flex-1 w-full">
      <View className="border-b border-gray-300 dark:border-gray-700" />
      <View className="bg-gray-100 dark:bg-gray-900 h-full w-full">
        <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="pb-20">
          <Pressable className="p-3 gap-y-3">
            {/* Header */}
            <Animated.View
              entering={animatedEnter(50)}
              className="bg-gray-200 dark:bg-gray-800 p-5 rounded-3xl items-center"
            >
              <Text className="text-lg font-extrabold text-gray-800 dark:text-white text-center mb-2">
                Need a Little Extra? We’ve Got You.
              </Text>
              <Text className="text-base text-gray-600 dark:text-gray-300 text-center leading-relaxed">
                Simple, flexible credit built around you.
              </Text>
            </Animated.View>

            {/* Loan Amount */}
            <Animated.View
              entering={animatedEnter(100)}
              className="bg-gray-200 dark:bg-gray-800 p-5 rounded-3xl"
            >
              <View className="flex-row justify-between mb-2">
                <Text className="text-sm font-bold text-gray-800 dark:text-gray-100">
                  Loan Amount
                </Text>
                <View className="flex-row items-center p-2 w-1/2 rounded-lg border-b border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700">
                  <Text className="text-base text-gray-800 dark:text-gray-100 mr-2">
                    {currencySymbol}
                  </Text>
                  <TextInput
                    className="flex-1 text-right text-base font-bold text-gray-800 dark:text-gray-100"
                    keyboardType="numeric"
                    value={amount}
                    onChangeText={handleAmountChange}
                    editable={!submitting}
                    placeholder={recommendedAmount.toLocaleString("en-US")}
                    placeholderTextColor="gray"
                    style={{ minWidth: 100 }}
                    autoFocus
                  />
                </View>
              </View>

              <View className="flex-row items-center mb-3">
                <TouchableOpacity
                  onPress={() => adjustAmount("decrement")}
                  disabled={submitting}
                  className="bg-slate-300 p-1 rounded-full"
                >
                  <Ionicons name="remove-outline" size={24} color="white" />
                </TouchableOpacity>
                <View className="flex-1 h-3 bg-emerald-100 dark:bg-emerald-900 mx-2 rounded-full overflow-hidden">
                  <Animated.View
                    entering={FadeInDown.delay(120).springify()}
                    className="h-full bg-emerald-500 rounded-full"
                    style={{ width: `${progressPercent}%` }}
                  />
                </View>
                <TouchableOpacity
                  onPress={() => adjustAmount("increment")}
                  disabled={submitting}
                  className="bg-blue-400 p-1 rounded-full"
                >
                  <Ionicons name="add-outline" size={24} color="white" />
                </TouchableOpacity>
              </View>

              <View className="flex-row justify-between">
                <Text className="text-xs text-gray-500">{displayMin}</Text>
                <Text className="text-xs text-gray-500">{displayMax}</Text>
              </View>
            </Animated.View>

            {/* Credit Term */}
            <Animated.View
              entering={animatedEnter(150)}
              className="bg-gray-200 dark:bg-gray-800 p-5 rounded-3xl"
            >
              <View className="flex-row justify-between mb-2">
                <Text className="text-sm font-bold text-gray-800 dark:text-gray-100">
                  Credit Term
                </Text>
                <View className="border-b border-gray-300 dark:border-gray-600 p-3 w-1/2 rounded-lg">
                  <Text className="text-right text-base font-bold text-gray-800 dark:text-gray-100">
                    {remainingDays} Days
                  </Text>
                </View>
              </View>

              <View className="flex-row items-center mb-3">
                <View className="bg-slate-300 p-1 rounded-full">
                  <Ionicons name="remove-outline" size={24} color="white" />
                </View>
                <View className="flex-1 h-3 bg-blue-100 dark:bg-blue-900 mx-2 rounded-full overflow-hidden">
                  <Animated.View
                    entering={FadeInDown.delay(160).springify()}
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${remainingDaysPercent}%` }}
                  />
                </View>
                <View className="bg-blue-300 p-1 rounded-full">
                  <Ionicons name="add-outline" size={24} color="white" />
                </View>
              </View>

              <View className="flex-row justify-between">
                <Text className="text-xs text-gray-500">1 Day</Text>
                <Text className="text-xs text-gray-500">
                  {daysInMonth} Days
                </Text>
              </View>
            </Animated.View>

            {/* Summary */}
            <Animated.View
              entering={animatedEnter(200)}
              className="bg-gray-50 dark:bg-gray-900 p-5 rounded-3xl shadow-lg"
            >
              <Text className="text-sm font-bold text-blue-800 dark:text-blue-300 mb-4">
                Loan Summary
              </Text>

              {[
                {
                  label: "Account Number",
                  value: user?.account_number || "Not provided",
                },
                {
                  label: "Email Address",
                  value: user?.email || "Not provided",
                },
                {
                  label: "Phone Number",
                  value: user?.phone_number || "Not provided",
                },
                {
                  label: "Loan Amount",
                  value: `${currencySymbol} ${amount}`,
                },
                {
                  label: "Repayment Term",
                  value: `${remainingDays} Days`,
                },
                {
                  label: "Daily Interest Rate",
                  value: `${(dailyInterestRate * 100).toFixed(2)}%`,
                },
                {
                  label: "Total Interest Payable",
                  value: `${currencySymbol} ${totalInterest}`,
                },
                {
                  label: "Total Amount Due",
                  value: `${currencySymbol} ${totalRepayment}`,
                },
              ].map(({ label, value }, i) => (
                <Animated.View
                  key={i}
                  entering={animatedEnter(210 + i * 40)}
                  className="flex-row justify-between mb-3"
                >
                  <Text className="text-base text-gray-600 dark:text-gray-200">
                    {label}
                  </Text>
                  <Text className="text-base font-bold text-gray-800 dark:text-gray-100">
                    {value}
                  </Text>
                </Animated.View>
              ))}

              <Text className="text-sm text-gray-500 dark:text-gray-400 mt-4">
                By applying, you agree to the terms and conditions of our credit
                policy.
              </Text>

              <Animated.View entering={animatedEnter(400)} className="mt-6">
                <TouchableOpacity
                  onPress={submitCreditApplication}
                  disabled={submitting}
                  className="bg-indigo-600 py-4 rounded-full shadow-lg active:opacity-90 disabled:opacity-50"
                  style={{ opacity: submitting ? 0.7 : 1 }}
                >
                  <Text className="text-center text-white text-base font-bold">
                    {submitting ? "Submitting..." : "Apply Now"}
                  </Text>
                </TouchableOpacity>
              </Animated.View>
            </Animated.View>
          </Pressable>
        </ScrollView>
      </View>
    </KeyboardAvoidingView>
  );
}
