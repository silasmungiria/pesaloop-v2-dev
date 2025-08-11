import { useState, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  useColorScheme,
} from "react-native";
import { Link, router } from "expo-router";

import { PhoneCodePicker } from "@/features/components";
import {
  validateFirstName,
  validateLastName,
  validateCountryCode,
  validatePhoneNumber,
  validateEmail,
} from "@/features/lib";
import { useDeviceContext } from "@/features/providers";

export default function Signup() {
  const { deviceDetails } = useDeviceContext();
  const scheme = useColorScheme();
  const keyboardVerticalOffset = Platform.OS === "ios" ? 80 : 0;

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [countryCode, setCountryCode] = useState(
    deviceDetails?.countryCallingCode || "+254"
  );
  const [isCountryPickerVisible, setIsCountryPickerVisible] = useState(false);

  const lastNameRef = useRef<TextInput | null>(null);
  const phoneNumberRef = useRef<TextInput | null>(null);
  const emailRef = useRef<TextInput | null>(null);

  const isNextDisabled =
    !validateFirstName(firstName) ||
    !validateLastName(lastName) ||
    !validateCountryCode(countryCode) ||
    !validatePhoneNumber(phoneNumber) ||
    !validateEmail(email);

  const onNext = () => {
    const params = { firstName, lastName, countryCode, phoneNumber, email };
    router.push({ pathname: "/(public)/auth/signup/password", params });
  };

  return (
    <KeyboardAvoidingView
      behavior="padding"
      keyboardVerticalOffset={keyboardVerticalOffset}
      className="flex-1 bg-gray-100 dark:bg-gray-900"
    >
      <View className="flex-1 p-6">
        <ScrollView
          contentContainerStyle={{ flexGrow: 1, paddingBottom: 10 }}
          keyboardShouldPersistTaps="handled"
        >
          <Text className="font-bold mb-6 text-4xl text-gray-800 dark:text-gray-200">
            Let's get started!
          </Text>
          <Text className="text-lg mb-4 text-gray-600 dark:text-gray-400">
            Enter your details to sign up. We'll verify your contact info.
          </Text>

          <View className="flex-1">
            <View className="flex-row gap-x-3 mb-8">
              <TextInput
                placeholder="First Name"
                autoCapitalize="words"
                placeholderTextColor="gray"
                value={firstName}
                onChangeText={setFirstName}
                returnKeyType="next"
                onSubmitEditing={() => lastNameRef.current?.focus()}
                className="flex-1 px-6 py-4 rounded-xl text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
              />
              <TextInput
                ref={lastNameRef}
                placeholder="Last Name"
                autoCapitalize="words"
                placeholderTextColor="gray"
                value={lastName}
                onChangeText={setLastName}
                returnKeyType="next"
                onSubmitEditing={() => phoneNumberRef.current?.focus()}
                className="flex-1 px-6 py-4 rounded-xl text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
              />
            </View>

            <View className="flex-row gap-x-3 mb-8">
              <TouchableOpacity
                onPress={() => setIsCountryPickerVisible(true)}
                className="p-4 rounded-xl justify-center items-center text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-md flex-row"
              >
                <Text className="text-lg font-bold text-gray-700 dark:text-gray-300">
                  {countryCode}
                </Text>
              </TouchableOpacity>
              <TextInput
                ref={phoneNumberRef}
                placeholder="Mobile number"
                placeholderTextColor="gray"
                keyboardType="numeric"
                value={phoneNumber}
                onChangeText={setPhoneNumber}
                maxLength={15}
                returnKeyType="next"
                onSubmitEditing={() => emailRef.current?.focus()}
                className="flex-1 px-6 py-4 rounded-xl text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
              />
            </View>

            <View className="mb-8">
              <TextInput
                ref={emailRef}
                placeholder="Email"
                autoCapitalize="none"
                placeholderTextColor="gray"
                keyboardType="email-address"
                value={email}
                onChangeText={setEmail}
                returnKeyType="done"
                onSubmitEditing={onNext}
                className="px-6 py-4 rounded-xl text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
              />
            </View>
          </View>

          <Link href="/(public)/auth/login" replace asChild>
            <TouchableOpacity
              activeOpacity={0.8}
              className="justify-center items-center mb-6 p-3"
            >
              <Text className="text-lg font-medium text-indigo-600 dark:text-indigo-400">
                Already have an account? Log in
              </Text>
            </TouchableOpacity>
          </Link>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={onNext}
            disabled={isNextDisabled}
            className={`justify-center items-center p-5 rounded-full shadow-md ${
              isNextDisabled
                ? scheme === "dark"
                  ? "bg-gray-700"
                  : "bg-gray-300"
                : "bg-indigo-600"
            }`}
          >
            <Text
              className={`text-xl font-semibold ${
                isNextDisabled
                  ? scheme === "dark"
                    ? "text-gray-500"
                    : "text-gray-600"
                  : "text-white"
              }`}
            >
              Continue
            </Text>
          </TouchableOpacity>
        </ScrollView>

        <PhoneCodePicker
          isVisible={isCountryPickerVisible}
          setIsVisible={setIsCountryPickerVisible}
          setCountryCode={setCountryCode}
        />
      </View>
    </KeyboardAvoidingView>
  );
}
