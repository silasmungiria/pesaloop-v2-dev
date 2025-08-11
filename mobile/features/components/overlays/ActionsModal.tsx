import React from "react";
import { Modal, View, Text, TouchableOpacity, FlatList } from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { defaultColors } from "@/features/constants";
import { useLogoutCleanup, useUserStore } from "@/features/store";

type ActionItem = {
  label: string;
  route: string;
  icon: string;
  iconColor: string;
};

type Props = {
  visible: boolean;
  onClose: () => void;
  onActionSelect: (route: string) => void;
};

const ActionsModal = ({ visible, onClose, onActionSelect }: Props) => {
  const { performFullLogout } = useLogoutCleanup();
  const { user } = useUserStore();

  const actions: ActionItem[] = [
    {
      label: "Send to a Friend",
      route: "/(authenticated)/(screens)/transactions/send/InternalTransfer",
      icon: "paper-plane-outline",
      iconColor: "#4a90e2",
    },
    {
      label: "Ask for Money",
      route: "/(authenticated)/(screens)/transactions/requests/InternalRequest",
      icon: "arrow-down-circle-outline",
      iconColor: "#e94e77",
    },
    {
      label: "Add Money to Wallet",
      route: "/(authenticated)/(screens)/transactions/requests/ExternalRequest",
      icon: "wallet-outline",
      iconColor: "#3498db",
    },
    {
      label: "Send Elsewhere",
      route: "/(authenticated)/(screens)/transactions/send/ExternalTransfer",
      icon: "swap-horizontal-outline",
      iconColor: "#2ecc71",
    },
    {
      label: "Swap Currency",
      route: "/(authenticated)/(screens)/transactions/forex",
      icon: "swap-vertical-outline",
      iconColor: "#9b59d6",
    },
    {
      label: "Money Moves",
      route: "/(authenticated)/(screens)/activity-center",
      icon: "pulse-outline",
      iconColor: "#3498db",
    },
    {
      label: "My Credit Hub",
      route: "/(authenticated)/(screens)/credits",
      icon: "trending-up-outline",
      iconColor: "#e67e22",
    },
    {
      label: "Account Settings",
      route: "/(authenticated)/(screens)/settings",
      icon: "settings-outline",
      iconColor: "#f5a623",
    },
    {
      label: "About This Device",
      route: "/(authenticated)/(screens)/dev-samples/useDeviceDetails",
      icon: "hardware-chip-outline",
      iconColor: "#2ecc71",
    },
  ];

  const filteredActions = actions.filter(
    (item) => item.label !== "My Credit Hub" || user?.is_loan_qualified
  );

  const renderItem = ({ item }: { item: ActionItem }) => (
    <TouchableOpacity
      activeOpacity={0.8}
      className="py-3 border-b border-gray-200 dark:border-gray-800"
      onPress={() => onActionSelect(item.route)}
    >
      <View className="flex-row items-center px-6 py-4 gap-x-4">
        <Ionicons name={item.icon as any} size={20} color={item.iconColor} />
        <Text className="text-lg text-gray-800 dark:text-gray-200 font-medium">
          {item.label}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent
      onRequestClose={onClose}
    >
      <TouchableOpacity className="flex-1 bg-black/60" onPress={onClose} />

      <View className="absolute bottom-0 w-full max-h-[95vh] bg-gray-100 dark:bg-gray-900 rounded-t-3xl shadow-lg">
        {/* Header */}
        <View className="flex-row justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-800">
          <View>
            <Text className="text-lg font-semibold text-gray-800 dark:text-gray-200">
              Quick Actions
            </Text>
            <Text className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Choose an action to perform
            </Text>
          </View>
          <TouchableOpacity onPress={onClose} className="p-2 rounded-full">
            <Ionicons name="close" size={24} color={defaultColors.red} />
          </TouchableOpacity>
        </View>

        {/* Action List */}
        <FlatList
          data={filteredActions}
          keyExtractor={(item) => item.label}
          renderItem={renderItem}
          ListFooterComponent={
            <TouchableOpacity
              activeOpacity={0.8}
              className="border-b border-gray-200 dark:border-gray-800"
              onPress={performFullLogout}
            >
              <View className="flex-row items-center px-6 py-4 gap-x-4">
                <Ionicons name="log-out-outline" size={20} color="#e74c3c" />
                <Text className="text-lg text-red-500 font-medium">
                  Sign Out
                </Text>
              </View>
            </TouchableOpacity>
          }
          contentContainerStyle={{ paddingBottom: 20 }}
        />
      </View>
    </Modal>
  );
};

export default ActionsModal;
