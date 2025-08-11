import { useEffect, useState } from "react";
import {
  Text,
  View,
  KeyboardAvoidingView,
  ActivityIndicator,
  TouchableOpacity,
  useColorScheme,
} from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import {
  CodeField,
  useBlurOnFulfill,
  useClearByFocusCell,
} from "react-native-confirmation-code-field";
import { Ionicons } from "@expo/vector-icons";

import { resendOTP, verifyUser } from "@/features/api";
import { AnimatedOTPCell, Biometric2FAModal } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { useBiometricAvailability } from "@/features/hooks";
import { getUserIdentifierWithFormattedPhone } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import {
  useBiometricStore,
  useUserStore,
  useSessionStore,
} from "@/features/store";

const CELL_COUNT = 6;

export default function OTPVerification() {
  const { email, phone, previousPage } = useLocalSearchParams<{
    email: string;
    phone: string;
    previousPage: string;
  }>();

  const scheme = useColorScheme();
  const { isBiometricSupported, isBiometricEnrolled } =
    useBiometricAvailability();
  const { setSessionVerified } = useUserStore();
  const { setSession } = useSessionStore();
  const { showNotification } = useNotificationToast();
  const { isBiometricEnabled } = useBiometricStore();

  const [OTPCode, setOTPCode] = useState("");
  const [submittingOTP, setSubmittingOTP] = useState(false);
  const [isVerifyingEmail, setIsVerifyingEmail] = useState(true);

  const [show2FAModal, setShow2FAModal] = useState(false);
  const [enabling2FA, setEnabling2FA] = useState(false);

  const ref = useBlurOnFulfill({ value: OTPCode, cellCount: CELL_COUNT });
  const [props, getCellOnLayoutHandler] = useClearByFocusCell({
    value: OTPCode,
    setValue: setOTPCode,
  });

  // Local timer state + hook for resend control
  const [resendingOTP, setResendingOTP] = useState(false);
  const [disableResendOTP, setDisableResendOTP] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);

  const startResendTimer = () => {
    setDisableResendOTP(true);
    setTimeLeft(60);
  };

  useEffect(() => {
    if (!disableResendOTP) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [disableResendOTP]);

  useEffect(() => {
    if (timeLeft === 0 && disableResendOTP) {
      setDisableResendOTP(false);
    }
  }, [timeLeft, disableResendOTP]);

  // Automatically verify when code complete
  useEffect(() => {
    if (OTPCode.length === CELL_COUNT) {
      onSubmitOTPVerification();
    }
  }, [OTPCode]);

  const onSubmitOTPVerification = async () => {
    const identifier = getUserIdentifierWithFormattedPhone(email, phone);
    if (!identifier) {
      router.replace("/(public)/auth/login");
      return;
    }

    setSubmittingOTP(true);

    try {
      const { data } = await verifyUser({ identifier, otp: OTPCode });

      if (
        data.user_verified?.is_email_verified &&
        data.user_verified?.is_phone_verified
      ) {
        if (previousPage === "loginPassword") {
          if (isBiometricSupported && isBiometricEnrolled) {
            if (!isBiometricEnabled) {
              setEnabling2FA(true);
              setShow2FAModal(true);
            } else if (isBiometricEnabled) {
              await setSession(true);
              await setSessionVerified(true);
              router.replace("/(authenticated)/(tabs)/home");
            } else {
              router.replace("/(public)/auth/login");
            }
          } else {
            await setSession(true);
            await setSessionVerified(true);
            router.replace("/(authenticated)/(tabs)/home");
          }
        } else if (previousPage === "signupPassword") {
          if (isBiometricSupported && isBiometricEnrolled) {
            setShow2FAModal(true);
          } else {
            router.replace("/(public)/auth/login");
          }
        } else {
          router.replace("/(public)/auth/login");
        }
      } else if (data.user_verified?.is_email_verified) {
        setIsVerifyingEmail(false);
      } else if (data.user_verified?.is_phone_verified) {
        setIsVerifyingEmail(true);
      }

      showNotification(data.message || "OTP Verified Successfully!", "success");
    } catch (error) {
      showNotification("Failed to verify OTP!", "error");
    } finally {
      setSubmittingOTP(false);
      setOTPCode("");
    }
  };

  const onSubmitResendOTPRequest = async () => {
    const identifier = getUserIdentifierWithFormattedPhone(email, phone);
    if (!identifier) {
      router.replace("/(public)/auth/login");
      return;
    }

    setResendingOTP(true);

    try {
      const result = await resendOTP({ identifier });
      showNotification(result.message || "OTP Resent Successfully!", "success");
      startResendTimer();
    } catch (error) {
      showNotification("Failed to resend OTP!", "error");
    } finally {
      setResendingOTP(false);
    }
  };

  return (
    <View className="flex-1 p-4 bg-gray-100 dark:bg-gray-900">
      {enabling2FA ? (
        <Biometric2FAModal
          visible={show2FAModal}
          onClose={() => setShow2FAModal(false)}
        />
      ) : (
        <KeyboardAvoidingView className="flex-1 justify-around items-center">
          <View className="flex justify-center items-center gap-y-8">
            <Text className="font-bold text-3xl text-gray-800 dark:text-gray-200">
              OTP Verification
            </Text>

            <Ionicons
              name="lock-closed-outline"
              size={90}
              color={scheme === "dark" ? "#4B5563" : "#D1D5DB"}
            />

            <Text className="text-center text-lg text-gray-700 dark:text-gray-300 mt-4">
              {`Please enter the verification code we sent to your ${
                isVerifyingEmail ? "email" : "phone number"
              }`}
            </Text>

            <CodeField
              ref={ref}
              {...props}
              value={OTPCode}
              onChangeText={setOTPCode}
              cellCount={CELL_COUNT}
              keyboardType="number-pad"
              textContentType="oneTimeCode"
              className="flex-row justify-center mt-8"
              renderCell={({ index, symbol, isFocused }) => (
                <AnimatedOTPCell
                  key={`cell-${index}`}
                  index={index}
                  symbol={symbol}
                  isFocused={isFocused}
                  CELL_COUNT={CELL_COUNT}
                  getCellOnLayoutHandler={getCellOnLayoutHandler}
                  scheme={scheme ?? "light"}
                />
              )}
            />
          </View>

          {submittingOTP && (
            <Text className="font-bold text-center text-xl mt-4 mb-3 text-gray-400 dark:text-gray-700">
              Verifying OTP...
            </Text>
          )}

          <View className="flex justify-center items-center mt-6">
            {!resendingOTP ? (
              <TouchableOpacity
                activeOpacity={0.8}
                onPress={onSubmitResendOTPRequest}
                disabled={disableResendOTP}
              >
                <Text className="underline text-lg text-indigo-600 dark:text-indigo-400">
                  {disableResendOTP
                    ? `Resend OTP in ${timeLeft}s`
                    : "Didn't receive the OTP? Resend OTP"}
                </Text>
              </TouchableOpacity>
            ) : (
              <ActivityIndicator size="large" color={defaultColors.green} />
            )}
          </View>
        </KeyboardAvoidingView>
      )}
    </View>
  );
}
