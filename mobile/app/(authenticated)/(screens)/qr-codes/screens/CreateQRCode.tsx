import React, { useEffect, useRef, useState } from "react";
import {
  Modal,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  useColorScheme,
  Alert,
  Platform,
} from "react-native";
import QRCode from "react-native-qrcode-svg";
import { Ionicons } from "@expo/vector-icons";
import * as MediaLibrary from "expo-media-library";
import * as Sharing from "expo-sharing";
import { captureRef } from "react-native-view-shot";

import { encryptSensitiveData } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { QRCodeProps } from "@/types";
import { useSessionAppState } from "@/features/providers";

interface Props extends QRCodeProps {
  visible: boolean;
  onClose: () => void;
}

const CreateQRCode: React.FC<Props> = ({ visible, onClose, ...props }) => {
  const scheme = useColorScheme();
  const { setBackgroundSafe } = useSessionAppState();

  const [qrData, setQrData] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [permissionResponse, requestPermission] = MediaLibrary.usePermissions();
  const qrRef = useRef<View>(null);

  useEffect(() => {
    if (!visible || qrData) return;

    const generateQR = async () => {
      setLoading(true);
      try {
        const { data } = await encryptSensitiveData(props);
        setQrData(data.encrypted_data);
      } catch (error) {
        console.error("Error generating QR Code:", error);
      } finally {
        setLoading(false);
      }
    };

    generateQR();
  }, [visible]);

  const handleDownload = async () => {
    if (!qrRef.current) return;
    setBackgroundSafe(true);

    if (!permissionResponse?.granted) {
      const { granted } = await requestPermission();
      if (!granted) {
        Alert.alert(
          "Permission Required",
          "Storage permission is needed to save the QR code."
        );
        setBackgroundSafe(false);
        return;
      }
    }

    try {
      const uri = await captureRef(qrRef, { format: "png", quality: 1 });
      const asset = await MediaLibrary.createAssetAsync(uri);
      await MediaLibrary.createAlbumAsync("QR Codes", asset, false);
      Alert.alert("Success", "QR Code saved to your gallery.");
    } catch (error) {
      console.error("Error saving QR code:", error);
      Alert.alert("Error", "Failed to save QR code.");
    } finally {
      setBackgroundSafe(false);
    }
  };

  const handleShare = async () => {
    if (!qrRef.current) return;
    setBackgroundSafe(true);

    try {
      const uri = await captureRef(qrRef, { format: "png", quality: 1 });
      await Sharing.shareAsync(uri);
    } catch (error) {
      console.error("Error sharing QR code:", error);
      Alert.alert("Error", "Failed to share QR code.");
    } finally {
      setBackgroundSafe(false);
    }
  };

  return (
    <Modal
      animationType="fade"
      transparent
      visible={visible}
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-center items-center bg-black/40">
        <View className="w-11/12 p-6 rounded-2xl bg-white dark:bg-gray-900">
          <TouchableOpacity
            onPress={onClose}
            className="absolute top-3 right-3 z-10"
          >
            <Ionicons name="close" size={20} color={defaultColors.red} />
          </TouchableOpacity>

          <Text className="text-xl font-bold text-center text-gray-800 dark:text-gray-100 mb-4">
            Scan to Pay
          </Text>

          <View
            ref={qrRef}
            className="items-center justify-center p-6 bg-gray-100 dark:bg-gray-800 rounded-xl"
            collapsable={false}
          >
            {loading ? (
              <ActivityIndicator size="large" color="#6366F1" />
            ) : qrData ? (
              <QRCode
                value={qrData}
                size={200}
                logo={require("@/assets/images/icon.png")}
                logoSize={40}
                color={scheme === "dark" ? "#FFFFFF" : "#000000"}
                backgroundColor={scheme === "dark" ? "#111827" : "#F3F4F6"}
              />
            ) : (
              <Text className="text-red-500 mt-2">
                Failed to generate QR Code
              </Text>
            )}
          </View>

          {!loading && (
            <>
              <View className="flex-row justify-between mt-6 gap-x-4">
                <TouchableOpacity
                  onPress={handleDownload}
                  className="flex-1 bg-indigo-600 p-4 rounded-full"
                >
                  <Text className="text-white font-semibold text-center">
                    Download
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  onPress={handleShare}
                  className="flex-1 bg-purple-600 p-4 rounded-full"
                >
                  <Text className="text-white font-semibold text-center">
                    Share
                  </Text>
                </TouchableOpacity>
              </View>

              <View className="mt-6 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg shadow">
                <Text className="text-center text-sm text-gray-600 dark:text-gray-300">
                  Scan this QR code to make a payment securely.
                </Text>
              </View>
            </>
          )}
        </View>
      </View>
    </Modal>
  );
};

export default CreateQRCode;
