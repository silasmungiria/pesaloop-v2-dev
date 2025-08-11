import React, { useState } from "react";
import {
  Modal,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import Animated from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";

import { exportTransactionStatement } from "@/features/api";
import { useModalAnimation } from "@/features/lib";
import { defaultColors } from "@/features/constants";
import { useSessionAppState, useNotificationToast } from "@/features/providers";
import { handleError } from "@/features/utils/handleError";

interface Props {
  visible: boolean;
  onClose: () => void;
}

const ExportStatementModal: React.FC<Props> = ({ visible, onClose }) => {
  const { setBackgroundSafe } = useSessionAppState();
  const { showNotification } = useNotificationToast();
  const { modalAnimatedStyle } = useModalAnimation(visible);

  const [exportFormat, setExportFormat] = useState<"pdf" | "csv">("pdf");
  const [isDownloadLoading, setIsDownloadLoading] = useState(false);
  const [isEmailLoading, setIsEmailLoading] = useState(false);

  const isActionDisabled = isDownloadLoading || isEmailLoading;

  const handleExport = async (deliveryMethod: "download" | "email") => {
    if (deliveryMethod === "download") setIsDownloadLoading(true);
    if (deliveryMethod === "email") setIsEmailLoading(true);

    try {
      const { data } = await exportTransactionStatement({
        exportFormat,
        deliveryMethod,
      });

      if (deliveryMethod === "download") {
        setBackgroundSafe(true);
        const fileUri = `${FileSystem.documentDirectory}transaction_statement.${exportFormat}`;

        if (typeof data === "string") {
          await FileSystem.writeAsStringAsync(fileUri, data);
          await Sharing.shareAsync(fileUri);
        } else {
          throw new Error("Exported data is not a string");
        }

        setBackgroundSafe(false);
      }

      if (deliveryMethod === "email") {
        const message =
          typeof data === "object" && data !== null && "message" in data
            ? (data as { message?: string }).message
            : undefined;

        showNotification(
          message ?? "Statement sent via email!",
          "success",
          6000
        );
      }
    } catch (error) {
      handleError(
        error,
        `Failed to ${deliveryMethod} statement. Try again later.`
      );
    } finally {
      if (deliveryMethod === "download") setIsDownloadLoading(false);
      if (deliveryMethod === "email") setIsEmailLoading(false);
      onClose();
    }
  };

  return (
    <Modal
      animationType="slide"
      transparent
      visible={visible}
      onRequestClose={onClose}
    >
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 w-full rounded-t-3xl bg-white dark:bg-gray-900 p-6 shadow-lg"
      >
        <View className="items-center">
          <Text className="font-bold text-xl text-gray-900 dark:text-gray-100 mb-4">
            Export Statement
          </Text>

          <View className="w-16 h-16 rounded-full items-center justify-center bg-emerald-100 dark:bg-emerald-700 mb-4">
            <Ionicons
              name="document-text-outline"
              size={32}
              color={defaultColors.green}
            />
          </View>

          <Text className="text-center text-gray-700 dark:text-gray-300 text-base mb-6">
            Select your preferred format and delivery method.
          </Text>

          {/* Format Selector */}
          <View className="flex-row w-full justify-between gap-3 mb-5">
            {["pdf", "csv"].map((format) => {
              const isActive = exportFormat === format;
              return (
                <TouchableOpacity
                  key={format}
                  onPress={() => setExportFormat(format as "pdf" | "csv")}
                  activeOpacity={0.85}
                  className={`flex-1 p-4 rounded-lg items-center justify-center shadow-sm ${
                    isActive ? "bg-blue-600" : "bg-gray-200 dark:bg-gray-700"
                  }`}
                >
                  <Ionicons
                    name={
                      format === "pdf" ? "document-outline" : "grid-outline"
                    }
                    size={26}
                    color={isActive ? "white" : defaultColors.primaryMuted}
                  />
                  <Text
                    className={`mt-1 text-base font-medium ${
                      isActive
                        ? "text-white"
                        : "text-gray-800 dark:text-gray-200"
                    }`}
                  >
                    {format.toUpperCase()}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>

          {/* Action Buttons */}
          <View className="flex-row w-full justify-between gap-3 mb-3">
            <TouchableOpacity
              activeOpacity={0.85}
              onPress={() => handleExport("email")}
              disabled={isActionDisabled}
              className={`flex-1 p-4 rounded-lg items-center justify-center ${
                isEmailLoading
                  ? "bg-gray-600 dark:bg-gray-800"
                  : "bg-indigo-600 hover:opacity-90 active:opacity-80"
              }`}
            >
              {isEmailLoading ? (
                <ActivityIndicator color={defaultColors.white} size={18} />
              ) : (
                <Text className="text-white text-lg font-medium">Email</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              activeOpacity={0.85}
              onPress={() => handleExport("download")}
              disabled={isActionDisabled}
              className={`flex-1 p-4 rounded-lg items-center justify-center ${
                isDownloadLoading
                  ? "bg-gray-600 dark:bg-gray-800"
                  : "bg-indigo-600 hover:opacity-90 active:opacity-80"
              }`}
            >
              {isDownloadLoading ? (
                <ActivityIndicator color={defaultColors.white} size={18} />
              ) : (
                <Text className="text-white text-lg font-medium">Download</Text>
              )}
            </TouchableOpacity>
          </View>

          {/* Cancel Button */}
          <TouchableOpacity
            activeOpacity={0.85}
            onPress={onClose}
            disabled={isActionDisabled}
            className="w-full p-4 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-600"
          >
            <Text className="text-center text-gray-800 dark:text-gray-200 text-lg font-medium">
              Cancel
            </Text>
          </TouchableOpacity>
        </View>
      </Animated.View>
    </Modal>
  );
};

export default ExportStatementModal;
