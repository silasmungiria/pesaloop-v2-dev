// src/features/hooks/useBiometricAuthentication.ts
import { useState } from "react";
import { verifyBiometricAuthentication } from "@/features/utils/biometric-utils";
import { useBiometricAvailability } from "./useBiometricAvailability";

export function useBiometricAuthentication(
  onAuthenticationSuccess?: (isEnabling: boolean) => void,
  onAuthenticationFailure?: (errorMessage?: string) => void
) {
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const { biometricType } = useBiometricAvailability();

  const verifyBiometric2FAs = async (
    isEnabling: boolean,
    promptOverride?: string
  ): Promise<boolean> => {
    setIsAuthenticating(true);
    try {
      const promptMessage =
        promptOverride ||
        (biometricType
          ? `Authenticate with ${biometricType}`
          : "Authenticate with Biometrics");

      const success = await verifyBiometricAuthentication(promptMessage);

      setIsAuthenticated(success);
      success
        ? onAuthenticationSuccess?.(isEnabling)
        : onAuthenticationFailure?.("Authentication failed. Please try again.");
      return success;
    } catch (error) {
      console.error("Biometric authentication error:", error);
      onAuthenticationFailure?.("An error occurred during authentication.");
      return false;
    } finally {
      setIsAuthenticating(false);
    }
  };

  return {
    isAuthenticating,
    isAuthenticated,
    verifyBiometric2FAs,
  };
}
