import { View, Text, Modal, TouchableOpacity, Clipboard } from "react-native";
import Animated from "react-native-reanimated";
import { Feather } from "@expo/vector-icons";

import { formatCurrency, useModalAnimation } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";

export default function DetailsModal({
  record,
  visible,
  onClose,
}: {
  record: any;
  visible: boolean;
  onClose: () => void;
}) {
  const { showNotification } = useNotificationToast();
  const { modalAnimatedStyle } = useModalAnimation(visible);

  const handleCopyReference = () => {
    Clipboard.setString(record?.referenceId);
    showNotification("Reference ID copied to clipboard!", "success", 3000);
  };

  const infoText = "text-sm text-gray-500 dark:text-gray-400";
  const category = record?.category;

  return (
    <Modal
      transparent
      animationType="slide"
      visible={visible}
      onRequestClose={onClose}
    >
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 w-full rounded-t-3xl bg-white dark:bg-gray-900 p-6 shadow-lg"
      >
        <Text className="text-lg font-bold mb-4 text-gray-900 dark:text-white">
          {category} Details
        </Text>

        <Text className="text-xl font-semibold text-gray-900 dark:text-white">
          {formatCurrency(record?.amount || 0)} {record?.currency}
        </Text>

        {record?.fees > 0 && (
          <Text className="text-base text-gray-600 dark:text-gray-400">
            Transaction Fee: {record?.currency}{" "}
            {formatCurrency(record?.fees || 0)}
          </Text>
        )}

        <Text className="mt-4 text-gray-600 dark:text-gray-400">
          Type: {record?.type.replace(/_/g, " ")}
        </Text>
        <Text className="text-gray-600 dark:text-gray-400">
          Status: {record?.status}
        </Text>

        <View className="border-b border-gray-300 dark:border-gray-600 my-4" />

        {category === "Exchange" && (
          <View className="gap-y-1">
            <Text className={infoText}>
              Exchange Rate: 1 {record?.currency} = {record?.targetCurrency}{" "}
              {formatCurrency(record?.exchangeRate || 0)}
            </Text>
            <Text className={infoText}>
              Converted Amount: {record?.targetCurrency}{" "}
              {formatCurrency(record?.convertedAmount || 0)}
            </Text>
            <Text className={infoText}>
              Charged Currency: {record?.chargedCurrency}
            </Text>
            <Text className={infoText}>
              Payment Provider: {record?.payment_provider}
            </Text>
            <Text className={infoText}>
              Exchange User: {record?.exchangeUser.first_name}{" "}
              {record?.exchangeUser.last_name}
            </Text>
          </View>
        )}

        {category === "Request" && (
          <View className="gap-y-1">
            <Text className={infoText}>Action: {record?.action}</Text>
            <Text className={infoText}>
              Payment Provider: {record?.payment_provider}
            </Text>
            <Text className={infoText}>
              Requesting User: {record?.requesting_user.first_name}{" "}
              {record?.requesting_user.last_name}
            </Text>
            <Text className={infoText}>
              Requested User: {record?.requested_user.first_name}{" "}
              {record?.requested_user.last_name}
            </Text>
            {record?.reason && (
              <Text className={infoText}>Reason: {record?.reason}</Text>
            )}
          </View>
        )}

        {category === "Transaction" && (
          <View className="gap-y-1">
            <Text className={infoText}>
              Sender Wallet: {record?.senderWallet.wallet_owner.first_name}{" "}
              {record?.senderWallet.wallet_owner.last_name}
            </Text>
            <Text className={infoText}>
              Receiver Wallet: {record?.receiverWallet.wallet_owner.first_name}{" "}
              {record?.receiverWallet.wallet_owner.last_name}
            </Text>
            {record?.payment_provider && (
              <Text className={infoText}>
                Payment Provider: {record?.payment_provider}
              </Text>
            )}
          </View>
        )}

        <View className="border-b border-gray-300 dark:border-gray-600 my-4" />

        <View className="flex-row items-center justify-between">
          <Text className="text-gray-600 dark:text-gray-400">
            Reference ID:
          </Text>
          <TouchableOpacity
            onPress={handleCopyReference}
            className="flex-row items-center"
          >
            <Text className="text-blue-600 dark:text-blue-400 font-medium mr-2">
              {record?.referenceId}
            </Text>
            <Feather name="copy" size={18} color="#3B82F6" />
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          className="mt-6 p-3 bg-red-500 rounded-lg shadow-lg"
          onPress={onClose}
        >
          <Text className="text-white text-center font-medium">Close</Text>
        </TouchableOpacity>
      </Animated.View>
    </Modal>
  );
}
