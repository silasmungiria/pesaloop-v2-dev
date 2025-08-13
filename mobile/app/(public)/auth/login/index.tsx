import { useState, useRef, useEffect } from "react";
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
import { Entypo } from "@expo/vector-icons";
import { Link, router } from "expo-router";

import { PhoneCodePicker } from "@/features/components";
import { useUserStore } from "@/features/store";
import {
  validateCountryCode,
  validatePhoneNumber,
  validateEmail,
} from "@/features/lib";
import { useDeviceContext } from "@/features/providers";

export default function Login() {
  const { deviceDetails } = useDeviceContext();
  const scheme = useColorScheme();
  const { loadUserData } = useUserStore();

  useEffect(() => {
    loadUserData();
  }, []);

  const [useEmailLogin, setUseEmailLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [countryCode, setCountryCode] = useState(
    deviceDetails?.countryCallingCode || "+254"
  );
  const [isCountryPickerVisible, setIsCountryPickerVisible] = useState(false);

  const keyboardVerticalOffset = Platform.OS === "ios" ? 80 : 0;

  const phoneNumberRef = useRef<TextInput | null>(null);
  const emailRef = useRef<TextInput | null>(null);

  const isNextDisabled = useEmailLogin
    ? !validateEmail(email)
    : !validateCountryCode(countryCode) || !validatePhoneNumber(phoneNumber);

  const onNext = () => {
    const params = {
      ...(useEmailLogin ? { email } : { countryCode, phoneNumber }),
    };

    router.push({
      pathname: "/(public)/auth/login/password",
      params: params,
    });
  };

  return (
    <KeyboardAvoidingView
      behavior="padding"
      keyboardVerticalOffset={keyboardVerticalOffset}
      className="flex-1 bg-gray-100 dark:bg-gray-900"
    >
      <View className="flex-1">
        <ScrollView
          contentContainerStyle={{ flexGrow: 1, paddingBottom: 10 }}
          keyboardShouldPersistTaps="handled"
          className="p-6"
        >
          <Text className="font-bold mb-6 text-4xl text-gray-800 dark:text-gray-200">
            Welcome back!
          </Text>
          <Text className="text-lg mb-4 text-gray-600 dark:text-gray-400">
            Enter your {useEmailLogin ? "email" : "phone number"} to continue.
            Confirmation code will be sent.
          </Text>

          <View className="flex-1">
            {useEmailLogin ? (
              <View className="gap-x-3 mb-8">
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
            ) : (
              <View>
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
                    className="flex-1 px-6 py-4 rounded-xl text-xl text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 shadow-sm"
                  />
                </View>
              </View>
            )}

            <View className="flex-row align-center gap-6 mb-3">
              <View className="flex-1 h-full border-b border-gray-300 dark:border-gray-700" />
              <Text className="fs-3 text-gray-600 dark:text-gray-400">OR</Text>
              <View className="flex-1 h-full border-b border-gray-300 dark:border-gray-700" />
            </View>

            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => setUseEmailLogin(!useEmailLogin)}
              className="flex-row gap-6 mt-6 px-5 h-16 rounded-full justify-center items-center bg-gray-50 dark:bg-gray-800 shadow-md"
            >
              <Entypo
                name={useEmailLogin ? "phone" : "mail"}
                size={20}
                color={useEmailLogin ? "#34C759" : "#007AFF"}
              />
              <Text className="font-semibold text-lg text-gray-600 dark:text-gray-400">
                {useEmailLogin
                  ? "Continue with Phone Number"
                  : "Continue with Email"}
              </Text>
            </TouchableOpacity>
          </View>

          <Link href={"/auth/forgot-password"} asChild>
            <TouchableOpacity
              activeOpacity={0.8}
              className="justify-center items-center p-3"
            >
              <Text className=" text-lg font-medium text-indigo-600 dark:text-indigo-400">
                Forgot password?
              </Text>
            </TouchableOpacity>
          </Link>

          <Link href={"/auth/signup"} replace asChild>
            <TouchableOpacity
              activeOpacity={0.8}
              className="justify-center items-center mb-6 p-3"
            >
              <Text className=" text-lg font-medium text-indigo-600 dark:text-indigo-400">
                Don't have an account? Sign up
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

          <PhoneCodePicker
            visible={isCountryPickerVisible}
            setVisible={setIsCountryPickerVisible}
            setCountryCode={setCountryCode}
          />
        </ScrollView>
      </View>
    </KeyboardAvoidingView>
  );
}
