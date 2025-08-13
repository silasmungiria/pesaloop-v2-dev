import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  TextInput,
} from "react-native";
import * as Haptics from "expo-haptics";

import { initiateTransfer } from "@/features/api";
import {
  AmountEntryModal,
  RecipientLookupModal,
  SuccessConfirmationModal,
} from "@/features/components";
import { defaultColors } from "@/features/constants";
import { useBalanceStore, useBiometricStore } from "@/features/store";
import { formatCurrency } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { VerifyRecipientResponse, InitiateTransferResponse } from "@/types";
import { handleError } from "@/features/utils/handleError";
import { useBiometricAuthentication } from "@/features/hooks";

export default function InternalTransfer() {
  const { currency } = useBalanceStore();
  const { showNotification } = useNotificationToast();
  const { isBiometricEnabled } = useBiometricStore();
  const { verifyBiometric2FAs } = useBiometricAuthentication();

  // State hooks
  const [showRecipientModal, setShowRecipientModal] = useState(true);
  const [recipient, setRecipient] = useState<VerifyRecipientResponse | null>(
    null
  );
  const [showAmountModal, setShowAmountModal] = useState(false);
  const [amount, setAmount] = useState("0");
  const [reason, setReason] = useState("");
  const [sendingMoney, setSendingMoney] = useState(false);
  const [transferRes, setTransferRes] =
    useState<InitiateTransferResponse | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [paymentDone, setPaymentDone] = useState(false);

  // Handle send money logic
  const handleInitiateSendMoney = async () => {
    if (!recipient) return;

    if (isBiometricEnabled) {
      const verified = await verifyBiometric2FAs(
        false,
        "Authenticate to confirm transfer"
      );
      if (!verified) return;
    }

    setSendingMoney(true);
    try {
      const { data } = await initiateTransfer({
        recipient_user: String(recipient.id),
        transfer_amount: amount,
        reason: reason,
      });
      setTransferRes(data);

      const message = `Reference: ${data.reference_id}. Transfer of ${data.currency} ${data.amount} to ${data.receiver_wallet.wallet_owner} was successful.`;
      showNotification(message, "success", 8000);

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      setShowConfirmModal(true);
    } catch (error) {
      handleError(
        error,
        "Failed to initiate transfer. Please try again later."
      );
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setSendingMoney(false);
    }
  };

  return (
    <View className="flex-1 p-6 bg-gray-100 dark:bg-gray-900">
      {amount && (recipient?.email || recipient?.phone_number) && (
        <View className="flex-1 justify-center gap-y-6">
          {/* Success Alert */}
          {paymentDone && (
            <View
              className="p-4 mb-4 rounded-lg bg-green-50 dark:bg-gray-900"
              role="alert"
            >
              <Text className="font-bold text-sm text-green-800 dark:text-green-400">
                Payment Successful
              </Text>
              <Text className="text-sm text-green-800 dark:text-green-400 mt-1">
                {`Your payment to ${recipient.first_name} has been successfully processed. Would you like to make another similar payment?`}
              </Text>
            </View>
          )}

          {/* Recipient Info */}
          {recipient && (
            <View className="w-full max-w-lg p-6 gap-2 rounded-2xl shadow-lg bg-gray-200 dark:bg-gray-800">
              <Text className="font-bold text-2xl text-gray-800 dark:text-gray-100">
                {`${recipient.first_name} ${recipient.last_name}`}
              </Text>
              <Text className="text-lg text-gray-700 dark:text-gray-300 mt-1">
                Email:{" "}
                <Text className="text-gray-600 dark:text-gray-400">
                  {recipient.email}
                </Text>
              </Text>
              <Text className="text-lg text-gray-700 dark:text-gray-300 mt-1">
                Phone:{" "}
                <Text className="text-gray-600 dark:text-gray-400">
                  {recipient.phone_number}
                </Text>
              </Text>
              <Text className="text-lg text-gray-700 dark:text-gray-300 mt-1">
                Amount:{" "}
                <Text className="font-semibold text-gray-900 dark:text-gray-200">
                  {currency} {formatCurrency(Number(amount))}
                </Text>
              </Text>
            </View>
          )}

          {/* Reason input field */}
          <TextInput
            value={reason}
            onChangeText={setReason}
            placeholder="Reason for transfer (Optional)"
            placeholderTextColor="gray"
            className="w-full p-5 rounded-xl bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          />

          {/* Transaction Button */}
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={handleInitiateSendMoney}
            disabled={sendingMoney}
            className={`w-full p-5 rounded-full shadow-xl flex items-center justify-center ${
              sendingMoney ? "bg-gray-600" : "bg-indigo-600"
            }`}
          >
            <Text className="text-lg text-white text-center font-semibold">
              {sendingMoney ? (
                <>
                  <ActivityIndicator size="small" color={defaultColors.green} />
                </>
              ) : (
                `Transfer ${currency} ${formatCurrency(Number(amount))}`
              )}
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Modals */}
      <RecipientLookupModal
        visible={showRecipientModal}
        setVisible={setShowRecipientModal}
        setDetails={setRecipient}
        setAmountModalVisible={setShowAmountModal}
      />
      <AmountEntryModal
        visible={showAmountModal}
        setVisible={setShowAmountModal}
        setAmount={setAmount}
        setRecipientModalVisible={setShowRecipientModal}
        exceedUserBalance={false}
      />
      <SuccessConfirmationModal
        visible={showConfirmModal}
        onClose={() => setShowConfirmModal(false)}
        data={{ ...transferRes, ...recipient }}
      />
    </View>
  );
}
