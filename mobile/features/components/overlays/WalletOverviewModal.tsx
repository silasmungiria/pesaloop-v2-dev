import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ActivityIndicator,
} from "react-native";
import Animated from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

import { ToastNotification } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { formatCurrency, useModalAnimation } from "@/features/lib";

interface WalletDetailsProps {
  visible: boolean;
  onClose: () => void;
  wallet: any;
  handleSetDefaultWallet: () => Promise<void>;
  handleActivateWallet: () => Promise<void>;
  isSettingDefaultWallet: boolean;
  isSettingActiveWallet: boolean;
}

const WalletOverviewModal: React.FC<WalletDetailsProps> = ({
  visible,
  onClose,
  wallet,
  handleSetDefaultWallet,
  handleActivateWallet,
  isSettingDefaultWallet,
  isSettingActiveWallet,
}) => {
  if (!wallet) return null;

  const { modalAnimatedStyle } = useModalAnimation(visible);

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <Animated.View
        style={modalAnimatedStyle}
        className="absolute bottom-0 p-5 rounded-t-3xl w-full gap-y-8 bg-white/90 dark:bg-gray-900 shadow-lg"
      >
        <View className="flex-row items-center justify-between mx-2">
          {/* Title */}
          <Text className="font-bold text-xl text-gray-500">
            Wallet Details
          </Text>

          {/* Close Button */}
          <TouchableOpacity activeOpacity={0.8} onPress={onClose}>
            <Ionicons name="close" size={28} color={defaultColors.red} />
          </TouchableOpacity>
        </View>

        {/* Wallet Info */}
        <View className="gap-y-4">
          {[
            { label: "Owner", value: wallet.wallet_owner.name },
            { label: "Email", value: wallet.wallet_owner.email },
            { label: "Phone", value: wallet.wallet_owner.phone_number },
            { label: "Currency", value: wallet.currency.name },
            {
              label: "Balance",
              value: `${wallet.currency.code} ${formatCurrency(
                wallet.balance
              )}`,
            },
            {
              label: "Default Wallet",
              value: wallet.is_default ? "Yes" : "No",
            },
            {
              label: "Active Wallet",
              value: wallet.is_active ? "Yes" : "No",
            },
            {
              label: "Last Updated",
              value: new Intl.DateTimeFormat("en-US", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: true,
                year: "numeric",
                month: "long",
                day: "numeric",
              }).format(new Date(wallet.last_updated)),
            },
            {
              label: "Created At",
              value: new Intl.DateTimeFormat("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              }).format(new Date(wallet.created_at)),
            },
          ].map(({ label, value }) => (
            <View key={label} className="flex flex-row justify-between mb-4">
              <Text className="font-medium text-gray-600 dark:text-gray-600">
                {label}:
              </Text>
              <Text className="font-semibold text-gray-800 dark:text-gray-400">
                {value}
              </Text>
            </View>
          ))}
        </View>

        {/* Actions */}
        <View className="flex flex-row justify-around mt-4">
          {!wallet.is_default && (
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={handleSetDefaultWallet}
              disabled={wallet.is_default || isSettingDefaultWallet}
              className="flex-row items-center justify-center p-3 rounded-full w-[47%] bg-indigo-600"
            >
              {isSettingDefaultWallet ? (
                <ActivityIndicator size="small" color="white" />
              ) : (
                <>
                  <Ionicons
                    name="star-outline"
                    size={20}
                    color="white"
                    className="mr-2"
                  />
                  <Text className="text-white font-semibold">
                    Set as Default
                  </Text>
                </>
              )}
            </TouchableOpacity>
          )}

          {!wallet.is_active && (
            <TouchableOpacity
              className="bg-green-500 flex-row items-center justify-center p-3 rounded-full w-[47%]"
              onPress={handleActivateWallet}
              disabled={!wallet.is_active || isSettingActiveWallet}
            >
              {isSettingActiveWallet ? (
                <ActivityIndicator size="small" color="white" />
              ) : (
                <>
                  <Ionicons
                    name="checkmark-circle-outline"
                    size={20}
                    color={defaultColors.white}
                    className="mr-2"
                  />
                  <Text className="text-white font-semibold">
                    Activate Wallet
                  </Text>
                </>
              )}
            </TouchableOpacity>
          )}
        </View>
      </Animated.View>
    </Modal>
  );
};

export default WalletOverviewModal;
