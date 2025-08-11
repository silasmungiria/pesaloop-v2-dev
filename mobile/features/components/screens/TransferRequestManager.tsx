import { useEffect, useState } from "react";
import {
  FlatList,
  View,
  Text,
  RefreshControl,
  ActivityIndicator,
  TouchableOpacity,
  Modal,
} from "react-native";
import Animated, {
  FadeInDown,
  FadeInUp,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import * as Haptics from "expo-haptics";

import { fetchTransferRequests, actionTransferRequest } from "@/features/api";
import { defaultColors } from "@/features/constants";
import { useRefresh } from "@/features/hooks";
import { formatCurrency, useModalAnimation } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { useUserStore } from "@/features/store";
import { TransferRequestsResponse, TransferRequest } from "@/types";
import { handleError } from "@/features/utils/handleError";

import TransferRequestActionModal from "../overlays/TransferRequestActionModal";

interface Props {
  updateBalance: () => void;
}

type TabType = "OutgoingRequests" | "IncomingRequests";

export default function TransferRequestManager({ updateBalance }: Props) {
  const { user } = useUserStore();
  const { showNotification } = useNotificationToast();

  const [transferRequests, setTransferRequests] = useState<TransferRequest[]>(
    []
  );
  const [selectedRequest, setSelectedRequest] =
    useState<TransferRequest | null>(null);
  const [fetchingData, setFetchingData] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [isApproving, setIsApproving] = useState(false);
  const [isCanceling, setIsCanceling] = useState(false);

  const { refreshing, onRefresh } = useRefresh(async () => {
    try {
      setFetchingData(true);
      const { data }: { data: TransferRequestsResponse } =
        await fetchTransferRequests();
      setTransferRequests(sortTransferRequests(data.results));
      setFetchingData(false);
    } catch (error) {
      console.error("Error fetching transfer requests:", error);
    }
  });

  const [selectedTab, setSelectedTab] = useState<TabType>("IncomingRequests");

  useEffect(() => {
    onRefresh();
  }, []);

  const sortTransferRequests = (requests: TransferRequest[]) => {
    return requests.sort((a, b) => {
      if (a.status === "PENDING" && b.status !== "PENDING") return -1;
      if (a.status !== "PENDING" && b.status === "PENDING") return 1;
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    });
  };

  const handleAction = async (action: "APPROVE" | "CANCEL") => {
    if (!selectedRequest) return;
    setIsApproving(action === "APPROVE");
    setIsCanceling(action === "CANCEL");
    try {
      await actionTransferRequest({
        request_id: selectedRequest.id,
        action: action,
      });
      updateBalance();

      const message = `You have ${
        action === "APPROVE"
          ? "approved"
          : selectedRequest.requesting_user.email === user?.email
          ? "declined"
          : "canceled"
      } the transfer request referenced: ${selectedRequest.reference_id}`;

      showNotification(message, "success", 6000);

      Haptics.notificationAsync(
        action === "APPROVE"
          ? Haptics.NotificationFeedbackType.Success
          : Haptics.NotificationFeedbackType.Error
      );

      setModalVisible(false);
      onRefresh();
    } catch (error) {
      handleError(
        error,
        `Failed to ${action.toLowerCase()} transfer request. Please try again later.`
      );
    } finally {
      setIsApproving(false);
      setIsCanceling(false);
    }
  };

  const getStatusColors = (status: string) => {
    switch (status) {
      case "PENDING":
        return {
          color: "text-gray-500",
          background: "bg-gray-100 dark:bg-gray-700",
        };
      case "SUCCESS":
        return {
          color: "text-green-600 dark:text-green-400",
          background: "bg-green-100 dark:bg-gray-700",
        };
      case "CANCELLED":
        return {
          color: "text-gray-600 dark:text-gray-400",
          background: "bg-gray-300 dark:bg-gray-700",
        };
      case "DECLINED":
        return {
          color: "text-red-600 dark:text-red-400",
          background: "bg-red-100 dark:bg-gray-900",
        };
      default:
        return {
          color: "text-gray-600 dark:text-gray-400",
          background: "bg-gray-300 dark:bg-gray-700",
        };
    }
  };

  const renderTransferRequestItem = ({ item }: { item: TransferRequest }) => {
    const { color, background } = getStatusColors(item.status);

    const role = user
      ? item.requested_user.email === user.email &&
        item.requested_user.phone_number === user.phone_number
        ? "Requestee"
        : "Requester"
      : "Unknown";

    return (
      <Animated.View
        entering={FadeInDown.springify()}
        exiting={FadeOutUp.springify()}
        layout={Layout.springify()}
        className="bg-white dark:bg-gray-800 rounded-xl mb-3"
      >
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={() => {
            setSelectedRequest(item);
            setModalVisible(true);
          }}
        >
          <View className="gap-y-3 p-4 rounded-xl border-b-2 border-gray-200 dark:border-gray-700">
            {/* Top row: Name + Amount */}
            <View className="flex-row justify-between items-center">
              <Text className="font-semibold text-lg text-gray-700 dark:text-gray-300">
                {role === "Requestee" ? "From: " : "To: "}
                <Text className="text-blue-600 dark:text-blue-400">
                  {role === "Requestee"
                    ? item.requesting_user.full_name
                    : role === "Requester"
                    ? item.requested_user.full_name
                    : "Unknown User"}
                </Text>
              </Text>

              <Text
                className={`font-bold text-base px-3 py-1 rounded-full ${color} ${background}`}
              >
                {formatCurrency(Number(item.amount))} {item.currency}
              </Text>
            </View>

            {/* Reference */}
            <Text className="text-base text-gray-600 dark:text-gray-400">
              Reference:{" "}
              <Text className="font-medium">{item.reference_id}</Text>
            </Text>

            {/* Payment provider + status */}
            <View className="flex-row justify-between items-center">
              <View className="flex-row gap-x-2 items-center">
                <Text className="text-base text-gray-600 dark:text-gray-400">
                  {item.payment_provider.toUpperCase()}
                </Text>
                <Text className="text-sm text-gray-500 dark:text-gray-500">
                  •
                </Text>
                <Text
                  className={`px-3 py-1 text-xs font-semibold rounded-full text-gray-800 dark:text-gray-100 ${background}`}
                >
                  {item.status.replace(/_/g, " ")}
                </Text>
              </View>

              {/* Date */}
              <Text className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(item.created_at).toLocaleString("en-US", {
                  day: "numeric",
                  month: "short",
                  year: "numeric",
                  hour: "numeric",
                  minute: "numeric",
                  hour12: true,
                })}
              </Text>
            </View>
          </View>
        </TouchableOpacity>
      </Animated.View>
    );
  };

  const filterRequests = (role: "OutgoingRequests" | "IncomingRequests") => {
    return transferRequests.filter((request) => {
      if (role === "OutgoingRequests") {
        return user ? request.requesting_user.email === user.email : false;
      }
      return user ? request.requested_user.email === user.email : false;
    });
  };

  const { modalAnimatedStyle } = useModalAnimation(modalVisible);

  return (
    <View className="flex-1 p-3 w-full bg-gray-100 dark:bg-gray-900">
      {fetchingData && transferRequests.length === 0 ? (
        <View className="flex-1 items-center justify-center">
          <ActivityIndicator size="large" color={defaultColors.green} />
        </View>
      ) : (
        filterRequests(selectedTab).length > 0 && (
          <View>
            <Text className="font-medium mb-4 text-base text-center text-gray-400 dark:text-gray-600">
              Money Requests
            </Text>

            <View className="flex-row justify-center mb-4 border-b border-gray-300 dark:border-gray-700">
              {[
                {
                  label: "Incoming Requests",
                  value: "IncomingRequests" as TabType,
                  showApprove: true,
                },
                {
                  label: "Outgoing Requests",
                  value: "OutgoingRequests" as TabType,
                  showApprove: false,
                },
              ].map((tab) => {
                const isSelected = selectedTab === tab.value;
                return (
                  <TouchableOpacity
                    key={tab.value}
                    activeOpacity={0.8}
                    onPress={() => setSelectedTab(tab.value)}
                    className="flex-1 items-center p-2"
                  >
                    <Text
                      className={`text-base font-semibold ${
                        isSelected
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-gray-500 dark:text-gray-400"
                      }`}
                    >
                      {tab.label}
                    </Text>

                    {isSelected && (
                      <Animated.View
                        entering={FadeInUp.duration(200)}
                        className="h-1 w-10 rounded-full mt-1 bg-blue-600 dark:bg-blue-400"
                      />
                    )}
                  </TouchableOpacity>
                );
              })}
            </View>

            <FlatList
              data={filterRequests(selectedTab)}
              keyExtractor={(item) => item.id}
              // renderItem={({ item, index }) => (
              //   <Animated.View
              //     entering={FadeInUp.delay(Math.min(index * 25, 200))}
              //     key={item.id}
              //   >
              //     {renderTransferRequestItem({ item })}
              //   </Animated.View>
              // )}
              renderItem={renderTransferRequestItem}
              contentContainerStyle={{ paddingBottom: 130 }}
              initialNumToRender={10}
              maxToRenderPerBatch={10}
              windowSize={5}
              showsVerticalScrollIndicator={false}
              refreshControl={
                <RefreshControl
                  refreshing={refreshing}
                  onRefresh={onRefresh}
                  colors={[defaultColors.green]}
                />
              }
              ListEmptyComponent={
                refreshing ? (
                  <ActivityIndicator
                    size="large"
                    color={defaultColors.green}
                    className="mt-8"
                  />
                ) : (
                  <Text className="text-center mt-8 text-lg text-gray-600 dark:text-gray-300">
                    No transfer requests found.
                  </Text>
                )
              }
            />
          </View>
        )
      )}

      <TransferRequestActionModal
        visible={modalVisible}
        selectedRequest={selectedRequest}
        isApproving={isApproving}
        isCanceling={isCanceling}
        onClose={() => setModalVisible(false)}
        onAction={handleAction}
        modalAnimatedStyle={modalAnimatedStyle}
        userEmail={user?.email}
      />
    </View>
  );
}
