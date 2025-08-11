import React from "react";
import {
  ActivityIndicator,
  Modal,
  Text,
  TouchableOpacity,
  useColorScheme,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import Animated from "react-native-reanimated";

import { defaultColors } from "@/features/constants";
import { use2FAVerification } from "@/features/hooks";
import { useModalAnimation } from "@/features/lib";
import { useBiometricStore } from "@/features/store";

interface Props {
  visible: boolean;
  onClose: () => void;
  launchedFromSettings?: boolean;
}

const Biometric2FAModal: React.FC<Props> = ({
  visible,
  onClose,
  launchedFromSettings = false,
}) => {
  const {
    enabling2FA,
    initiateEnable2FA,
    initiateDisable2FA,
    onSkip2FAVerification,
  } = use2FAVerification(launchedFromSettings);
  const { isBiometricEnabled } = useBiometricStore();

  const scheme = useColorScheme();
  const { modalAnimatedStyle } = useModalAnimation(visible);

  const handleSkip = () => {
    if (!launchedFromSettings) onSkip2FAVerification();
    onClose();
  };

  const handleBiometricToggle = async (enable: boolean) => {
    if (enable) {
      await initiateEnable2FA();
    } else {
      await initiateDisable2FA();
    }
    onClose();
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onClose}
    >
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 w-full rounded-t-3xl bg-white dark:bg-gray-900 p-6 shadow-lg"
      >
        <View className="flex items-center pb-6">
          {enabling2FA ? (
            <View className="flex-1 items-center justify-center">
              <ActivityIndicator
                size="large"
                color={scheme === "dark" ? defaultColors.green : "#4CAF50"}
              />
            </View>
          ) : (
            <View className="w-full">
              <Text className="text-2xl font-semibold text-center text-gray-900 dark:text-gray-200 mb-4">
                Secure Your Account with Biometrics
              </Text>

              <View className="p-6 mb-4">
                <Ionicons
                  name="finger-print"
                  size={90}
                  color={scheme === "dark" ? "#4B5563" : "#D1D5DB"}
                  style={{ alignSelf: "center" }}
                />
              </View>

              <Text className="text-lg text-center text-gray-800 dark:text-gray-300 mt-6">
                Enable biometric authentication as your second factor of
                verification. This adds a quick and secure layer of protection,
                directly on your device.
              </Text>

              <View className="w-full flex-row justify-between mt-8 gap-x-4">
                {isBiometricEnabled ? (
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => handleBiometricToggle(false)}
                    className="flex-1 p-3 rounded-full bg-red-500 shadow-md"
                  >
                    <Text className="text-center text-white font-medium">
                      Disable
                    </Text>
                  </TouchableOpacity>
                ) : (
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => handleBiometricToggle(true)}
                    className="flex-1 p-3 rounded-full bg-blue-500 shadow-md"
                  >
                    <Text className="text-center text-white font-medium">
                      Enable
                    </Text>
                  </TouchableOpacity>
                )}
              </View>
            </View>
          )}
        </View>
      </Animated.View>
    </Modal>
  );
};

export default Biometric2FAModal;
