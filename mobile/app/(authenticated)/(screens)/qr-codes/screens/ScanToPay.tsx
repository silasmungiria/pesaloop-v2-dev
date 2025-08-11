import React, { useEffect, useRef } from "react";
import {
  View,
  Text,
  Button,
  SafeAreaView,
  AppState,
  Platform,
  StyleSheet,
  Alert,
} from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import { StatusBar } from "expo-status-bar";

import Overlay from "../components/Overlay";
import { decryptSensitiveData } from "@/features/api";
import { useSessionAppState } from "@/features/providers";
import { QRCodeProps } from "@/types";

interface ScanQRProps {
  onValidScan: (result: QRCodeProps) => void;
}

export default function ScanToPay({ onValidScan }: ScanQRProps) {
  const [permission, requestPermission] = useCameraPermissions();
  const qrLock = useRef(false);
  const appState = useRef(AppState.currentState);
  const { setBackgroundSafe } = useSessionAppState();

  useEffect(() => {
    const subscription = AppState.addEventListener("change", (nextState) => {
      if (
        appState.current.match(/inactive|background/) &&
        nextState === "active"
      ) {
        qrLock.current = false;
      }
      appState.current = nextState;
    });

    return () => subscription.remove();
  }, []);

  const handleBarcodeScanned = async ({ data }: { data: string }) => {
    if (data && !qrLock.current) {
      qrLock.current = true;

      try {
        const { data: decryptedData } = await decryptSensitiveData(data);
        onValidScan(decryptedData.decrypted_data);

        console.info("QR Code scanned successfully:", decryptedData);
      } catch {
        Alert.alert("Error", "Invalid or tampered QR Code.");
      } finally {
        setTimeout(() => (qrLock.current = false), 1000);
      }
    }
  };

  useEffect(() => {
    if (!permission) return;
    setBackgroundSafe(!permission.granted);
  }, [permission]);

  if (!permission) return <View />;
  if (!permission.granted) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-100 dark:bg-gray-900">
        <Text className="text-lg font-semibold mb-4 text-black dark:text-white">
          We need your permission to access the camera
        </Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  return (
    <SafeAreaView style={StyleSheet.absoluteFillObject}>
      {Platform.OS === "android" ? <StatusBar hidden /> : null}
      <CameraView
        style={StyleSheet.absoluteFillObject}
        facing="back"
        onBarcodeScanned={qrLock.current ? undefined : handleBarcodeScanned}
      />
      <Overlay />
    </SafeAreaView>
  );
}
