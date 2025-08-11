import { useCallback, useState } from "react";
import {
  FlatList,
  View,
  Text,
  RefreshControl,
  ActivityIndicator,
  TouchableOpacity,
} from "react-native";
import { useFocusEffect } from "expo-router";
import Animated, {
  FadeIn,
  FadeInDown,
  FadeInUp,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";

import DetailsModal from "./DetailsModal";
import {
  fetchAccountActivitiesReport,
  ActivitiesResponse,
} from "@/features/api";
import { defaultColors } from "@/features/constants";
import { useRefresh } from "@/features/hooks";
import { formatCurrency } from "@/features/lib";

export default function ActivityCenter() {
  const [isFetching, setIsFetching] = useState(false);
  const [sortedData, setSortedData] = useState<any[]>([]);
  const [selectedRecord, setSelectedRecord] = useState<any | null>(null);

  useFocusEffect(
    useCallback(() => {
      onRefresh();
    }, [])
  );

  const { refreshing, onRefresh } = useRefresh(async () => {
    setIsFetching(true);
    try {
      const { data } = await fetchAccountActivitiesReport();
      transformAndSortActivities(data);
    } catch (error) {
      console.error("Error fetching account activities:", error);
    } finally {
      setIsFetching(false);
    }
  });

  const transformAndSortActivities = (activityData: ActivitiesResponse) => {
    const allActivities = [
      ...activityData.results.exchange_records.map((record) => ({
        id: record.id,
        createdAt: record.created_at,
        amount: Number(record.source_amount),
        currency: record.source_currency,
        referenceId: record.reference_id,
        targetCurrency: record.target_currency,
        exchangeRate: Number(record.platform_exchange_rate),
        convertedAmount: Number(record.converted_amount_with_fee),
        fees: Number(record.charged_amount),
        chargedCurrency: record.charged_amount_currency,
        isDebit: record.is_debit,
        status: record.status,
        payment_provider: record.payment_provider,
        exchangeUser: record.user,
        type: record.transaction_type,
        category: "Exchange",
      })),
      ...activityData.results.transfer_requests.map((record) => ({
        id: record.id,
        createdAt: record.created_at,
        amount: record.amount,
        currency: record.currency,
        referenceId: record.reference_id,
        isDebit: record.is_debit,
        status: record.status,
        action: record.action,
        payment_provider: record.payment_provider,
        requesting_user: record.requesting_user,
        requested_user: record.requested_user,
        reason: record.reason,
        type: record.transaction_type,
        category: "Request",
      })),
      ...activityData.results.transaction_records.map((record) => ({
        id: record.id,
        createdAt: record.created_at,
        amount: record.amount,
        currency: record.currency,
        referenceId: record.reference_id,
        fees: record.transaction_charge
          ? Number(record.transaction_charge)
          : null,
        isDebit: record.is_debit,
        status: record.status,
        payment_provider: record.payment_provider,
        senderWallet: record.sender_wallet,
        receiverWallet: record.receiver_wallet,
        reason: record.reason,
        type: record.transaction_type,
        category: "Transaction",
      })),
    ];

    const sortedActivities = allActivities.sort(
      (a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );

    setSortedData(sortedActivities);
  };

  const getActivityDisplayInfo = (item: any) => {
    if (item.category === "Exchange" && item.exchangeUser) {
      return {
        label: "Exchange by:",
        name: `${item.exchangeUser.first_name} ${item.exchangeUser.last_name}`,
      };
    } else if (item.category === "Transaction") {
      if (item.isDebit && item.receiverWallet) {
        return {
          label: "Transaction to:",
          name: `${item.receiverWallet.wallet_owner.first_name} ${item.receiverWallet.wallet_owner.last_name}`,
        };
      } else if (!item.isDebit && item.senderWallet) {
        return {
          label: "Transaction from:",
          name: `${item.senderWallet.wallet_owner.first_name} ${item.senderWallet.wallet_owner.last_name}`,
        };
      }
    } else if (item.category === "Request") {
      if (!item.isDebit && item.requested_user) {
        return {
          label: "Request to:",
          name: `${item.requested_user.first_name} ${item.requested_user.last_name}`,
        };
      } else if (item.isDebit && item.requesting_user) {
        return {
          label: "Request from:",
          name: `${item.requesting_user.first_name} ${item.requesting_user.last_name}`,
        };
      }
    }
    return { label: "", name: "" };
  };

  const renderActivityItem = ({
    item,
    index,
  }: {
    item: any;
    index: number;
  }) => {
    const { label, name } = getActivityDisplayInfo(item);

    return (
      <Animated.View
        entering={FadeInDown.delay(Math.min(index * 100, 300)).springify()}
        exiting={FadeOutUp.springify()}
        layout={Layout.springify()}
        className="bg-white dark:bg-gray-800 rounded-xl mb-3"
      >
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={() => {
            requestAnimationFrame(() => setSelectedRecord(item));
          }}
        >
          <View className="gap-y-3 p-4 rounded-xl border-b-2 border-gray-200 dark:border-gray-700">
            <View className="flex-row justify-between items-center">
              <View>
                {label && name && (
                  <Text className="font-semibold text-lg text-gray-700 dark:text-gray-300">
                    {label}{" "}
                    <Text className="text-blue-600 dark:text-blue-400">
                      {name}
                    </Text>
                  </Text>
                )}
              </View>

              <View className="flex-row items-center">
                {/* Show Exchange From & To */}
                {item.category === "Exchange" ? (
                  <View className="items-end gap-y-1">
                    <Text className="font-bold text-base text-green-500">
                      + {formatCurrency(item.convertedAmount)}{" "}
                      {item.targetCurrency}
                    </Text>
                    <Text className="font-bold text-base text-red-600 dark:text-red-400">
                      - {formatCurrency(item.amount)} {item.currency}
                    </Text>
                  </View>
                ) : (
                  <Text
                    className={`font-bold text-base ${
                      item.isDebit
                        ? "text-red-600 dark:text-red-400"
                        : "text-green-500"
                    }`}
                  >
                    {item.isDebit ? "-" : "+"} {formatCurrency(item.amount)}{" "}
                    {item.currency}
                  </Text>
                )}
              </View>
            </View>

            {item.type && (
              <Text className="text-base text-gray-600 dark:text-gray-400">
                Type:{" "}
                <Text className="font-medium text-sm">
                  {item.type.replace(/_/g, " ")}
                </Text>
              </Text>
            )}

            {item.referenceId && (
              <Text className="text-base text-gray-600 dark:text-gray-400">
                Reference:{" "}
                <Text className="font-medium">{item.referenceId}</Text>
              </Text>
            )}

            <View className="flex-row justify-between items-center">
              <View className="flex-row gap-x-2">
                <Text
                  className={`px-3 py-1 text-xs font-semibold rounded-full text-gray-800 dark:text-gray-100 ${
                    item.isDebit
                      ? "bg-red-300 dark:bg-red-700"
                      : "bg-green-200 dark:bg-green-900"
                  }`}
                >
                  {item.isDebit ? "OUTGOING" : "INCOMING"}
                </Text>
                <Text className="text-sm text-gray-500 dark:text-gray-800">
                  •
                </Text>
                <Text
                  className={`px-3 py-1 text-xs font-semibold rounded-full text-gray-800 dark:text-gray-100 ${
                    item.status === "SUCCESS"
                      ? "bg-green-200 dark:bg-green-900"
                      : item.status === "DECLINED"
                      ? "bg-red-300 dark:bg-red-700"
                      : item.status === "CANCELLED"
                      ? "bg-yellow-200 dark:bg-yellow-900"
                      : "bg-gray-200 dark:bg-gray-700"
                  }`}
                >
                  {item.status.replace(/_/g, " ")}
                </Text>
              </View>

              <Text className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(item.createdAt).toLocaleString("en-US", {
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

  return (
    <View className="flex-1 bg-gray-100 dark:bg-gray-900">
      {isFetching && sortedData.length === 0 ? (
        <View className="mt-4 items-center justify-center">
          <ActivityIndicator size="large" color={defaultColors.green} />
        </View>
      ) : (
        <View>
          <Animated.View
            entering={FadeInUp.duration(200)}
            className="h-1 w-1/3 rounded-full mt-1 bg-blue-600 dark:bg-blue-400 mx-auto mb-4"
          />

          <View className="px-3">
            <FlatList
              data={sortedData}
              renderItem={renderActivityItem}
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
                <Text className="text-center mt-8 text-lg text-gray-600">
                  No activities found
                </Text>
              }
            />
          </View>
        </View>
      )}

      <DetailsModal
        record={selectedRecord}
        visible={!!selectedRecord}
        onClose={() => setSelectedRecord(null)}
      />
    </View>
  );
}
