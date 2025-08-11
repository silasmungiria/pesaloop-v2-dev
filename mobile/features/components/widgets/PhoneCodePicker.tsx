import React from "react";
import { CountryPicker } from "react-native-country-codes-picker";
import { useColorScheme } from "react-native";

interface CountryPickerProps {
  isVisible: boolean;
  setIsVisible: (value: boolean) => void;
  setCountryCode: (code: string) => void;
}

const PhoneCodePicker = ({
  isVisible,
  setIsVisible,
  setCountryCode,
}: CountryPickerProps) => {
  const scheme = useColorScheme();

  return (
    <CountryPicker
      show={isVisible}
      lang="en"
      pickerButtonOnPress={(item) => {
        setCountryCode(item.dial_code);
        setIsVisible(false);
      }}
      onBackdropPress={() => setIsVisible(false)}
      style={{
        backdrop: {
          backgroundColor: "rgba(0, 0, 0, 0.6)",
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          borderRadius: 12,
        },
        modal: {
          height: "85%",
          backgroundColor: scheme === "dark" ? "#1F2937" : "#FFFFFF",
          borderRadius: 12,
          position: "relative",
          zIndex: 1,
        },
        line: {
          backgroundColor: scheme === "dark" ? "#4F46E5" : "#6B78F7",
          height: 1,
          borderRadius: 50,
        },
        textInput: {
          height: 50,
          backgroundColor: scheme === "dark" ? "#2D3748" : "#F9FAFB",
          borderRadius: 8,
          paddingHorizontal: 10,
          marginBottom: 10,
        },
        searchMessageText: {
          color: scheme === "dark" ? "#A0AEC0" : "#4A5568",
          fontSize: 14,
          fontWeight: "500",
        },
        countryButtonStyles: {
          height: 60,
          backgroundColor: scheme === "dark" ? "#2D3748" : "#FFFFFF",
          borderRadius: 8,
          marginBottom: 0,
          justifyContent: "center",
          alignItems: "center",
        },
        dialCode: {
          color: scheme === "dark" ? "#D1D5DB" : "#4A5568",
          fontSize: 16,
          fontWeight: "600",
        },
        countryName: {
          color: scheme === "dark" ? "#D1D5DB" : "#4A5568",
          fontSize: 16,
          fontWeight: "500",
        },
      }}
    />
  );
};

export default PhoneCodePicker;
