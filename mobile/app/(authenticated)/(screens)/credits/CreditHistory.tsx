import { useState, useMemo } from "react";
import {
  View,
  Text,
  FlatList,
  Pressable,
  KeyboardAvoidingView,
  RefreshControl,
  ActivityIndicator,
} from "react-native";
import Animated, {
  FadeIn,
  FadeOut,
  FadeInDown,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import { Ionicons, MaterialIcons } from "@expo/vector-icons";

import { useRefresh } from "@/features/hooks";
import { defaultColors } from "@/features/constants";
import { creditHistory as data } from "@/assets/data";

const tabs = [
  { label: "All", value: "all" },
  { label: "Active", value: "outstanding" },
  { label: "Closed", value: "cleared" },
];

export default function CreditHistory() {
  const [selectedTab, setSelectedTab] = useState("all");
  const [isFetching, setIsFetching] = useState(false);
  const [creditHistoryData, setCreditHistoryData] = useState(data);

  const { refreshing, onRefresh } = useRefresh(async () => {
    setIsFetching(true);
    try {
      // Simulated API fetch
      setCreditHistoryData(data);
    } catch (error) {
      console.error("Error fetching account activities:", error);
    } finally {
      setIsFetching(false);
    }
  });

  const filteredHistory = useMemo(() => {
    const sortedData = [...creditHistoryData].sort(
      (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
    );
    return selectedTab === "all"
      ? sortedData
      : sortedData.filter((item) => item.status === selectedTab);
  }, [selectedTab, creditHistoryData]);

  const formatDate = (dateString: string) =>
    new Date(dateString).toLocaleDateString(undefined, {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const renderItem = ({
    item,
    index,
  }: {
    item: (typeof data)[0];
    index: number;
  }) => {
    const isDisbursement = item.type === "disbursement";
    const amountColor = isDisbursement ? "#4F46E5" : "#16A34A";
    const statusColor = item.status === "outstanding" ? "#CA8A04" : "#15803D";

    return (
      <Animated.View
        entering={FadeInDown.delay(Math.min(index * 100, 300)).springify()}
        exiting={FadeOutUp.springify()}
        layout={Layout.springify()}
        className="bg-white dark:bg-gray-800 rounded-xl px-4 py-5 mb-2"
      >
        <View className="flex-row justify-between items-center">
          <View className="flex-row items-center gap-x-3 w-3/5">
            {isDisbursement ? (
              <Ionicons
                name="cash-outline"
                size={24}
                color={
                  item.status === "outstanding" ? statusColor : amountColor
                }
              />
            ) : (
              <MaterialIcons name="paid" size={24} color={amountColor} />
            )}
            <View>
              <Text className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                {item.title}
              </Text>
              <Text className="text-sm text-gray-500 dark:text-gray-400 mt-0.5 max-w-2/3">
                {item.description}
              </Text>
            </View>
          </View>
          <Text
            className="font-bold text-lg w-2/5 text-right"
            style={{
              color: item.status === "outstanding" ? statusColor : amountColor,
            }}
          >
            {item.currency}{" "}
            {item.amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,")}
          </Text>
        </View>

        <View className="flex-row justify-between mt-4 items-center">
          <Text className="text-sm italic text-gray-400 dark:text-gray-500">
            {formatDate(item.date)}
          </Text>
          <View
            style={{ backgroundColor: statusColor }}
            className="px-3 py-1 rounded-full"
          >
            <Text className="text-white text-xs font-semibold uppercase tracking-wide">
              {item.status === "outstanding" ? "Active" : "Closed"}
            </Text>
          </View>
        </View>
      </Animated.View>
    );
  };

  return (
    <KeyboardAvoidingView className="flex-1 bg-gray-100 dark:bg-gray-900">
      {/* Tabs */}
      <Animated.View
        layout={Layout.springify()}
        className="flex-row justify-around items-center px-6 mb-4 border-b border-gray-300 dark:border-gray-700"
      >
        {tabs.map(({ label, value }) => (
          <Pressable
            key={value}
            onPress={() => setSelectedTab(value)}
            className="flex-1 items-center p-3 mx-2"
            style={({ pressed }) => ({
              borderBottomWidth: selectedTab === value ? 3 : 0,
              borderBottomColor:
                selectedTab === value ? "#4F46E5" : "transparent",
              opacity: pressed ? 0.6 : 1,
            })}
          >
            <Animated.Text
              entering={FadeIn.springify()}
              className={`text-base font-semibold ${
                selectedTab === value
                  ? "text-indigo-500"
                  : "text-gray-600 dark:text-gray-400"
              }`}
            >
              {label}
            </Animated.Text>
          </Pressable>
        ))}
      </Animated.View>

      {/* History List */}
      <View className="px-4">
        <FlatList
          data={filteredHistory}
          keyExtractor={(_, idx) => idx.toString()}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 80 }}
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
              <Animated.View
                entering={FadeIn.springify()}
                className="flex-1 items-center justify-center py-20"
                style={{ flexGrow: 1 }}
              >
                <ActivityIndicator size="large" color={defaultColors.green} />
              </Animated.View>
            ) : (
              <Animated.View
                entering={FadeIn.springify()}
                exiting={FadeOut.springify()}
                layout={Layout}
                className="flex-1 items-center justify-center py-20"
                style={{ flexGrow: 1 }}
              >
                <Ionicons name="file-tray-outline" size={64} color="#9CA3AF" />
                <Text className="text-base text-center text-gray-500 dark:text-gray-400 mt-4 px-6">
                  No credit history available.
                </Text>
              </Animated.View>
            )
          }
        />
      </View>
    </KeyboardAvoidingView>
  );
}
