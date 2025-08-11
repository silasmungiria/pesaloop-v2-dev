// src/features/utils/biometric-utils.ts
import * as LocalAuthentication from "expo-local-authentication";
import { handleError } from "./handleError";
import * as Haptics from "expo-haptics";

/**
 * Verifies biometric authentication
 * @param promptMessage Optional custom message to show in biometric prompt
 * @returns Promise<boolean> - true if verified, false if failed/cancelled
 */
export const verifyBiometricAuthentication = async (
  promptMessage?: string
): Promise<boolean> => {
  try {
    // First check if biometrics is available
    const hasHardware = await LocalAuthentication.hasHardwareAsync();
    const isEnrolled = await LocalAuthentication.isEnrolledAsync();

    if (!hasHardware || !isEnrolled) {
      return false;
    }

    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: promptMessage || "Verify your identity to continue",
      fallbackLabel: "Use passcode",
    });

    if (result.success) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      return true;
    }

    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    return false;
  } catch (error) {
    handleError(error, "Biometric verification failed");
    return false;
  }
};
