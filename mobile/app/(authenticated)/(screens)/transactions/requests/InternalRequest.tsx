import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  TextInput,
} from "react-native";
import * as Haptics from "expo-haptics";

import { initiateTransferRequest } from "@/features/api";
import {
  AmountEntryModal,
  RecipientLookupModal,
  SuccessConfirmationModal,
} from "@/features/components";
import { defaultColors } from "@/features/constants";
import { formatCurrency } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import {
  useBalanceStore,
  useBiometricStore,
  useUserStore,
} from "@/features/store";
import { VerifyRecipientResponse, TransferRequest } from "@/types";

import { CreateQRCode } from "@/app/(authenticated)/(screens)/qr-codes";
import { handleError } from "@/features/utils";
import { useBiometricAuthentication } from "@/features/hooks";

export default function InternalRequest() {
  const { currency } = useBalanceStore();
  const { user } = useUserStore();
  const { showNotification } = useNotificationToast();
  const { isBiometricEnabled } = useBiometricStore();
  const { verifyBiometric2FAs } = useBiometricAuthentication();

  // State hooks
  const [isRecipientModalVisible, setRecipientModalVisible] = useState(true);
  const [requestedUser, setRequestedUser] =
    useState<VerifyRecipientResponse | null>(null);
  const [isAmountModalVisible, setAmountModalVisible] = useState(false);
  const [amount, setAmount] = useState("0");
  const [reason, setReason] = useState("");
  const [sendingRequest, setSendingRequest] = useState(false);
  const [transferResponse, setTransferResponse] =
    useState<TransferRequest | null>(null);
  const [isConfirmationModalVisible, setConfirmationModalVisible] =
    useState(false);
  const [isQRModalVisible, setQRModalVisible] = useState(false);

  // Handle send money logic
  const handleInitiateSendMoney = async () => {
    if (!requestedUser) return;

    if (isBiometricEnabled) {
      const verified = await verifyBiometric2FAs(
        false,
        "Authenticate to confirm transfer request"
      );
      if (!verified) return;
    }

    setSendingRequest(true);
    try {
      const { data } = await initiateTransferRequest({
        requested_user: requestedUser.id,
        request_amount: amount,
        reason: reason,
      });
      setTransferResponse(data);

      const message = `Request sent successfully to ${data.requested_user.full_name} for ${data.currency} ${data.amount}. Reference: ${data.reference_id}`;
      showNotification(message, "success", 8000);

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      setConfirmationModalVisible(true);
    } catch (error) {
      handleError(
        error,
        "Failed to initiate transfer. Please try again later."
      );

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setSendingRequest(false);
    }
  };

  return (
    <View className="flex-1 p-6 bg-gray-100 dark:bg-gray-900">
      {amount && (requestedUser?.email || requestedUser?.phone_number) && (
        <View className="flex-1 justify-center items-center gap-y-6">
          {/* Requestee Info */}
          {requestedUser && (
            <View className="w-full max-w-lg p-6 gap-2 rounded-2xl shadow-lg bg-gray-200 dark:bg-gray-800">
              <Text className="font-bold text-2xl text-gray-800 dark:text-gray-100">
                {`${requestedUser.first_name} ${requestedUser.last_name}`}
              </Text>
              <Text className="text-lg text-gray-700 dark:text-gray-300 mt-1">
                Email:{" "}
                <Text className="text-gray-600 dark:text-gray-400">
                  {requestedUser.email}
                </Text>
              </Text>
              <Text className="text-lg text-gray-700 dark:text-gray-300 mt-1">
                Phone:{" "}
                <Text className="text-gray-600 dark:text-gray-400">
                  {requestedUser.phone_number}
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
            placeholder="Reason for the request (optional)"
            placeholderTextColor="gray"
            className="w-full p-5 rounded-xl bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          />

          {/* Transfer Button */}
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={handleInitiateSendMoney}
            disabled={sendingRequest}
            className={`w-full p-5 rounded-full shadow-xl flex items-center justify-center ${
              sendingRequest ? "bg-gray-600" : "bg-indigo-600"
            }`}
          >
            <Text className="text-lg text-white text-center font-semibold">
              {sendingRequest ? (
                <>
                  <ActivityIndicator size="small" color={defaultColors.green} />
                </>
              ) : (
                `Request ${currency} ${formatCurrency(Number(amount))}`
              )}
            </Text>
          </TouchableOpacity>

          {/* Create QR Code */}
          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              Haptics.notificationAsync(
                Haptics.NotificationFeedbackType.Success
              );
              setQRModalVisible(true);
            }}
            className="w-full p-5 rounded-full flex items-center justify-center bg-gray-600 dark:bg-gray-800"
          >
            <Text className="text-lg text-center text-white font-semibold">
              Create QR Code
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Modals */}
      <RecipientLookupModal
        visible={isRecipientModalVisible}
        onClose={() => setRecipientModalVisible(false)}
        setRequestedUser={setRequestedUser}
        setAmountModalVisible={setAmountModalVisible}
      />
      <AmountEntryModal
        visible={isAmountModalVisible}
        onClose={() => setAmountModalVisible(false)}
        setAmount={setAmount}
        setRecipientModalVisible={setRecipientModalVisible}
        exceedUserBalance={true}
      />
      <SuccessConfirmationModal
        visible={isConfirmationModalVisible}
        onClose={() => setConfirmationModalVisible(false)}
        data={{ ...transferResponse, ...requestedUser }}
      />
      <CreateQRCode
        visible={isQRModalVisible}
        onClose={() => setQRModalVisible(false)}
        currentUserIdentifier={user?.email || user?.phone_number || ""}
        requestedUserIdentifier={
          requestedUser?.email || requestedUser?.phone_number || ""
        }
        requestedUserName={`${requestedUser?.first_name} ${requestedUser?.last_name}`}
        amount={typeof amount === "string" ? parseFloat(amount) : amount}
        currency={transferResponse?.currency || currency}
        reason={transferResponse?.reason || ""}
        actionType="pay"
      />
    </View>
  );
}
