import { useState, useEffect } from "react";
import { router } from "expo-router";
import * as LocalAuthentication from "expo-local-authentication";
import * as Haptics from "expo-haptics";

import {
  useBiometricAuthentication,
  useBiometricAvailability,
} from "@/features/hooks";
import { useNotificationToast } from "@/features/providers";
import {
  useUserStore,
  useSessionStore,
  useLogoutCleanup,
  useBiometricStore,
} from "@/features/store";
import { handleError } from "@/features/utils";

export const use2FAVerification = (launchedFromSettings: boolean) => {
  const { user, setSessionVerified } = useUserStore();
  const { setSession, refreshToken } = useSessionStore();
  const { performFullLogout } = useLogoutCleanup();
  const { showNotification } = useNotificationToast();
  const { isBiometricEnabled, setBiometricEnabled, clearBiometricState } =
    useBiometricStore();

  const [enabling2FA, setEnabling2FA] = useState(false);

  const { verifyBiometric2FAs } = useBiometricAuthentication(
    (isEnabling: boolean) => {
      if (isEnabling) {
        enable2FAVerification();
      } else {
        disable2FAVerification();
      }
    },
    () => {
      handleError("Biometric authentication failed. Please try again later.");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    }
  );

  useEffect(() => {
    const checkBiometricSupport = async () => {
      const { isBiometricSupported, isBiometricEnrolled } =
        useBiometricAvailability();
      if (!isBiometricSupported || !isBiometricEnrolled) {
        performFullLogout();
        router.replace("/(public)/auth/login");
      }
    };
    checkBiometricSupport();

    if (launchedFromSettings) {
      console.info("Triggered from settings");
    }
  }, []);

  const enable2FAVerification = async () => {
    await setBiometricEnabled(true);

    if (user && refreshToken) {
      setSession(true);
      setSessionVerified(true);
      if (!launchedFromSettings) {
        router.replace("/(authenticated)/(screens)/settings");
      }
    } else {
      performFullLogout();
      router.replace("/(public)/auth/login");
    }

    showNotification("2FA biometric enabled successfully!", "success", 6000);
    console.info("2FA biometric enabled successfully!");
  };

  const disable2FAVerification = async () => {
    await clearBiometricState();
    showNotification("2FA biometric disabled successfully!", "success", 6000);
    console.info("2FA biometric disabled successfully!");
  };

  const initiateEnable2FA = async () => {
    try {
      setEnabling2FA(true);

      const hasBiometrics = await LocalAuthentication.hasHardwareAsync();
      if (!hasBiometrics) {
        showNotification("Biometric hardware not available.", "error", 6000);
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
        return;
      }

      const verified = await verifyBiometric2FAs(
        true,
        "Authenticate to enable biometric 2FA"
      );
      if (!verified) return;
    } catch (error) {
      handleError(error, "Failed to enable biometric.");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setEnabling2FA(false);
    }
  };

  const initiateDisable2FA = async () => {
    try {
      setEnabling2FA(true);
      const verified = await verifyBiometric2FAs(
        false,
        "Authenticate to disable biometric 2FA"
      );
      if (!verified) return;
    } catch (error) {
      handleError(error, "Failed to disable biometric.");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setEnabling2FA(false);
    }
  };

  const onSkip2FAVerification = async () => {
    if (user && refreshToken) {
      await setSession(true);
      await setSessionVerified(true);
      router.replace("/(authenticated)/(tabs)/home");
    } else {
      performFullLogout();
      router.replace("/(public)/auth/login");
    }
  };

  return {
    user,
    enabling2FA,
    initiateEnable2FA,
    initiateDisable2FA,
    verifyBiometric2FAs,
    onSkip2FAVerification,
  };
};
