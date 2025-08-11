import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ActivityIndicator,
  Clipboard,
} from "react-native";
import Animated from "react-native-reanimated";
import { Feather } from "@expo/vector-icons";

import { defaultColors } from "@/features/constants";
import { formatCurrency } from "@/features/lib";
import { TransferRequest } from "@/types";
import { useNotificationToast } from "@/features/providers";

interface Props {
  visible: boolean;
  selectedRequest: TransferRequest | null;
  isApproving: boolean;
  isCanceling: boolean;
  onClose: () => void;
  onAction: (action: "APPROVE" | "CANCEL") => void;
  modalAnimatedStyle: any;
  userEmail: string | undefined;
}

export default function TransferRequestActionModal({
  visible,
  selectedRequest,
  isApproving,
  isCanceling,
  onClose,
  onAction,
  modalAnimatedStyle,
  userEmail,
}: Props) {
  const { showNotification } = useNotificationToast();

  const handleCopyReference = () => {
    if (selectedRequest) {
      Clipboard.setString(selectedRequest.reference_id);
      showNotification("Reference ID copied to clipboard!", "success", 3000);
    }
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="slide"
      onRequestClose={onClose}
    >
      {/* Dark overlay */}
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 w-full bg-white dark:bg-gray-900 rounded-t-3xl p-6 shadow-lg"
      >
        <Text className="text-lg font-bold mb-4 text-gray-900 dark:text-white text-center">
          About this Request
        </Text>

        {selectedRequest && (
          <View className="gap-y-4">
            <View className="flex-row justify-between items-center">
              {/* From / To */}
              <Text className="text-base text-gray-700 dark:text-gray-300">
                {selectedRequest.requested_user.email === userEmail
                  ? `From: ${selectedRequest.requesting_user.full_name}`
                  : `To: ${selectedRequest.requested_user.full_name}`}
              </Text>

              {/* Amount */}
              <Text className="text-xl font-semibold text-gray-900 dark:text-white">
                {formatCurrency(Number(selectedRequest.amount))}{" "}
                {selectedRequest.currency}
              </Text>
            </View>

            {/* Status */}
            <Text className="text-base text-gray-600 dark:text-gray-400">
              Status: {selectedRequest.status}
            </Text>

            {/* Payment Provider */}
            <Text className="text-base text-gray-600 dark:text-gray-400">
              Payment Channel: {selectedRequest.payment_provider}
            </Text>

            {/* Reason */}
            {selectedRequest.reason && (
              <Text className="text-base text-gray-600 dark:text-gray-400">
                Note: {selectedRequest.reason}
              </Text>
            )}

            {/* Date created */}
            <Text className="text-base text-gray-600 dark:text-gray-400">
              Requested On:{" "}
              {new Date(selectedRequest.created_at).toLocaleString("en-US", {
                day: "numeric",
                month: "short",
                year: "numeric",
                hour: "numeric",
                minute: "numeric",
                hour12: true,
              })}
            </Text>

            {/* Closed date */}
            {selectedRequest.status !== "PENDING" && (
              <Text className="text-base text-gray-600 dark:text-gray-400">
                Closed On:{" "}
                {new Date(selectedRequest.updated_at).toLocaleString("en-US", {
                  day: "numeric",
                  month: "short",
                  year: "numeric",
                  hour: "numeric",
                  minute: "numeric",
                  hour12: true,
                })}
              </Text>
            )}

            {/* Divider */}
            <View className="border-b border-gray-300 dark:border-gray-600 my-3" />

            {/* Reference ID with copy */}
            <View className="flex-row items-center justify-between">
              <Text className="text-base text-gray-600 dark:text-gray-400">
                Reference ID:
              </Text>
              <TouchableOpacity
                onPress={handleCopyReference}
                className="flex-row items-center"
              >
                <Text className="text-blue-600 dark:text-blue-400 font-medium mr-2">
                  {selectedRequest.reference_id}
                </Text>
                <Feather name="copy" size={18} color="#3B82F6" />
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* Divider */}
        <View className="border-b border-gray-300 dark:border-gray-600 my-4" />

        {/* Action buttons */}
        {selectedRequest?.status === "PENDING" && (
          <View className="flex-row gap-x-3 mt-2">
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => onAction("CANCEL")}
              disabled={isCanceling}
              className="flex-1 p-3 rounded-lg"
              style={{ backgroundColor: defaultColors.red }}
            >
              {isCanceling ? (
                <ActivityIndicator size="small" color="white" />
              ) : (
                <Text className="text-center text-white text-base font-medium">
                  {selectedRequest.requested_user.email === userEmail
                    ? "Decline"
                    : "Cancel"}
                </Text>
              )}
            </TouchableOpacity>

            {selectedRequest.requested_user.email === userEmail && (
              <TouchableOpacity
                activeOpacity={0.8}
                onPress={() => onAction("APPROVE")}
                disabled={isApproving}
                className="flex-1 p-3 rounded-lg"
                style={{ backgroundColor: defaultColors.green }}
              >
                {isApproving ? (
                  <ActivityIndicator size="small" color="white" />
                ) : (
                  <Text className="text-center text-white text-base font-medium">
                    Approve
                  </Text>
                )}
              </TouchableOpacity>
            )}
          </View>
        )}

        {/* Close button */}
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={onClose}
          className="mt-4 p-3 rounded-lg bg-gray-200 dark:bg-gray-700"
        >
          <Text className="text-center text-gray-800 dark:text-gray-200 text-base font-medium">
            Close
          </Text>
        </TouchableOpacity>
      </Animated.View>
    </Modal>
  );
}
