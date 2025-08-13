import React, { useCallback, useEffect, useState } from "react";
import {
  View,
  FlatList,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import Animated, { FadeInUp } from "react-native-reanimated";
import * as Haptics from "expo-haptics";

import {
  fetchUserWallets,
  setDefaultWallet,
  activateWallet,
} from "@/features/api";
import { WalletOverviewModal } from "@/features/components";
import { appInfo, defaultColors } from "@/features/constants";
import { formatCurrency } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { useBalanceStore } from "@/features/store";
import { WalletResponse } from "@/types";
import { handleError } from "@/features/utils/handleError";

type Wallet = WalletResponse["results"][0];

export default function Wallets() {
  const { setBalance, setCurrency } = useBalanceStore();
  const { showNotification } = useNotificationToast();

  const [walletsData, setWalletsData] = useState<Wallet[]>([]);
  const [isDataFetched, setIsDataFetched] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [walletDetailsVisible, setWalletDetailsVisible] = useState(false);
  const [selectedWallet, setSelectedWallet] = useState<Wallet | null>(null);

  const [isSettingDefaultWallet, setIsSettingDefaultWallet] = useState(false);
  const [isSettingActiveWallet, setIsSettingActiveWallet] = useState(false);

  const fetchWalletsData = async () => {
    try {
      const { data } = await fetchUserWallets();

      const defaultWallet = data.results.find((wallet) => wallet.is_default);

      if (defaultWallet) {
        setBalance(defaultWallet.balance);
        setCurrency(defaultWallet.currency.code);
      } else {
        setBalance(0);
        setCurrency("USD");
      }

      const sortedWallets = data.results.sort((a, b) =>
        a.is_default === b.is_default ? 0 : a.is_default ? -1 : 1
      );
      setWalletsData(sortedWallets);
      setIsDataFetched(true);
    } catch (error) {
      console.error("Error fetching wallets:", error);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (!isDataFetched) {
      fetchWalletsData();
    }
  }, [isDataFetched]);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchWalletsData();
  }, []);

  const handleSetDefaultWallet = async () => {
    if (!selectedWallet) return;
    setIsSettingDefaultWallet(true);
    try {
      await setDefaultWallet(selectedWallet.id, {
        is_default: !selectedWallet.is_default,
      });

      fetchWalletsData();

      const message = `Your default wallet is now set to ${selectedWallet.currency.name}.`;
      showNotification(message, "success", 6000);

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      setWalletDetailsVisible(false);
    } catch (error) {
      handleError(
        error,
        "Failed to set default wallet. Please try again later."
      );
    } finally {
      setIsSettingDefaultWallet(false);
    }
  };

  const handleActivateWallet = async () => {
    if (!selectedWallet) return;
    setIsSettingActiveWallet(true);
    try {
      await activateWallet(selectedWallet.id, {
        is_active: !selectedWallet.is_active,
      });

      fetchWalletsData();

      const message = `Your wallet has been ${
        selectedWallet.is_active ? "deactivated" : "activated"
      }.`;

      showNotification(message, "success", 6000);

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      setWalletDetailsVisible(false);
    } catch (error) {
      handleError(error, "Failed to activate wallet. Please try again later.");
    } finally {
      setIsSettingActiveWallet(false);
    }
  };

  const renderItem = ({ item }: { item: Wallet }) => (
    <TouchableOpacity
      activeOpacity={0.9}
      onPress={() => {
        setSelectedWallet(item);
        setWalletDetailsVisible(true);
      }}
      className="p-4 mb-4 w-full max-w-[510px] h-[270px] rounded-2xl bg-white/90 dark:bg-gray-800"
    >
      <View className="absolute inset-0 p-4 rounded-lg">
        {/* Header */}
        <View className="absolute top-6 left-10">
          <Text className="font-medium text-sm sm:text-base text-indigo-800 dark:text-indigo-600">
            {item.is_default ? "Primary Wallet" : "Extra Wallet"}
          </Text>
        </View>
        <View className="absolute top-6 right-10">
          <Text className="font-medium italic text-sm sm:text-xl text-indigo-500 dark:text-indigo-400">
            {appInfo.APP_NAME}
          </Text>
        </View>

        {/* Card Chip */}
        <View className="absolute left-10 top-20 flex-row gap-x-2 items-center">
          <Ionicons
            name="wallet-outline"
            size={28}
            color={defaultColors.primary}
          />
          <Text className="font-normal text-base text-gray-400 dark:text-gray-600">
            {item.is_active ? "Active Wallet" : "Inactive Wallet"}
          </Text>
        </View>

        {/* Wallet ID */}
        <View className="absolute top-[120px] left-10">
          <Text className="font-medium tracking-wide text-lg sm:text-lg uppercase text-gray-800 dark:text-gray-300">
            {item.id.replace(/-/g, " ")}
          </Text>
        </View>

        {/* Balance */}
        <View className="absolute bottom-20 right-10">
          <Text className="font-medium tracking-wide text-xl sm:text-lg text-gray-800 dark:text-gray-300">
            {item.currency.code} {formatCurrency(item.balance)}
          </Text>
        </View>

        {/* Creation Date */}
        <View className="absolute bottom-20 left-10 flex-row">
          <View className="justify-center items-start">
            <Text className="text-xs sm:text-sm tracking-widest text-gray-500">
              Created
            </Text>
            <Text className="text-xs sm:text-sm tracking-widest text-gray-500">
              on
            </Text>
          </View>
          <Text className="ms-4 text-base sm:text-lg text-gray-800 dark:text-gray-400">
            {new Date(item.created_at).toLocaleString("en-US", {
              month: "short",
              year: "2-digit",
            })}
          </Text>
        </View>

        {/* Currency name */}
        <Text className="absolute bottom-10 left-10 text-gray-800 dark:text-gray-500 text-sm sm:text-lg font-medium tracking-wide">
          {item.currency.name}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View className="flex-1 bg-gray-100 dark:bg-gray-900">
      {isDataFetched ? (
        <FlatList
          className="p-3"
          data={walletsData}
          keyExtractor={(item) => item.id}
          renderItem={({ item, index }) => (
            <Animated.View
              entering={FadeInUp.delay(Math.min(index * 50, 300))}
              key={item.id}
            >
              {renderItem({ item })}
            </Animated.View>
          )}
          initialNumToRender={10}
          maxToRenderPerBatch={10}
          windowSize={5}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ paddingBottom: 80 }}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={[defaultColors.green]}
              tintColor={defaultColors.green}
            />
          }
        />
      ) : (
        <View className="flex-1 items-center bg-gray-100 dark:bg-gray-900">
          <ActivityIndicator
            size="large"
            color={defaultColors.green}
            className="mt-8"
          />
        </View>
      )}

      <WalletOverviewModal
        visible={walletDetailsVisible}
        onClose={() => setWalletDetailsVisible(false)}
        wallet={selectedWallet}
        handleSetDefaultWallet={handleSetDefaultWallet}
        handleActivateWallet={handleActivateWallet}
        isSettingDefaultWallet={isSettingDefaultWallet}
        isSettingActiveWallet={isSettingActiveWallet}
      />
    </View>
  );
}
