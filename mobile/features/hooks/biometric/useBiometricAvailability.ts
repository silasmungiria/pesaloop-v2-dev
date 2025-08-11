// src/features/hooks/useBiometricAvailability.ts
import { useState, useEffect } from "react";
import * as LocalAuthentication from "expo-local-authentication";

/**
 * Hook to check if biometric hardware is available and configured.
 */
export function useBiometricAvailability() {
  const [isBiometricSupported, setIsBiometricSupported] = useState(false);
  const [isBiometricEnrolled, setIsBiometricEnrolled] = useState(false);
  const [biometricType, setBiometricType] = useState<string | null>(null);

  const refreshBiometricStatus = async () => {
    try {
      const hasHardware = await LocalAuthentication.hasHardwareAsync();
      const hasEnrolled = await LocalAuthentication.isEnrolledAsync();
      const supportedTypes =
        await LocalAuthentication.supportedAuthenticationTypesAsync();

      setIsBiometricSupported(hasHardware);
      setIsBiometricEnrolled(hasEnrolled);

      if (
        supportedTypes.includes(
          LocalAuthentication.AuthenticationType.FINGERPRINT
        )
      ) {
        setBiometricType("Fingerprint");
      } else if (
        supportedTypes.includes(
          LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION
        )
      ) {
        setBiometricType("Face ID");
      } else {
        setBiometricType(null);
      }
    } catch (error) {
      console.error("Error checking biometric support:", error);
    }
  };

  useEffect(() => {
    refreshBiometricStatus();
  }, []);

  return {
    isBiometricSupported,
    isBiometricEnrolled,
    biometricType,
    refreshBiometricStatus,
  };
}
