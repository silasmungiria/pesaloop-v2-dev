import { useEffect, useState, useCallback, useRef } from "react";
import { View, Text, TouchableOpacity, Modal } from "react-native";
import { router, useFocusEffect } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import Animated from "react-native-reanimated";

import { fetchUserWallets } from "@/features/api";
import { TransferRequestManager } from "@/features/components";
import { appInfo, defaultColors } from "@/features/constants";
import { formatCurrency, useModalAnimation } from "@/features/lib";
import { useBalanceStore } from "@/features/store";

export default function Home() {
  const { balance, currency, setBalance, setCurrency } = useBalanceStore();
  const [showBalance, setShowBalance] = useState(false);
  const [isSendModalVisible, setSendModalVisible] = useState(false);
  const [isRequestModalVisible, setRequestModalVisible] = useState(false);

  const hideBalanceTimeoutRef = useRef<number | null>(null);

  const handleBalanceVisibility = () => {
    // Clear any existing timeout first
    if (hideBalanceTimeoutRef.current) {
      clearTimeout(hideBalanceTimeoutRef.current);
      hideBalanceTimeoutRef.current = null;
    }

    // Toggle balance visibility
    setShowBalance((prev) => {
      const newValue = !prev;

      // If new value is true, set a new timeout to hide it after 5 seconds
      if (newValue) {
        hideBalanceTimeoutRef.current = setTimeout(() => {
          setShowBalance(false);
          hideBalanceTimeoutRef.current = null;
        }, 5000);
      }

      return newValue;
    });

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  useEffect(() => {
    if (!balance || !currency) {
      fetchWalletsData();
    }
  }, []);

  const fetchWalletsData = async () => {
    try {
      const { data } = await fetchUserWallets();
      const defaultWallet = data.results.find((wallet) => wallet.is_default);

      if (defaultWallet) {
        setBalance(defaultWallet.balance);
        setCurrency(defaultWallet.currency.code);
      } else {
        console.warn("No default wallet found.");
        setBalance(0);
        setCurrency("USD");
      }
    } catch (error) {
      console.error("Error fetching wallets:", error);
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchWalletsData();
    }, [])
  );

  const { modalAnimatedStyle } = useModalAnimation(
    isSendModalVisible || isRequestModalVisible
  );

  return (
    <View className="flex-1 bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <View className="w-full p-3">
        <View className="w-full rounded-t-3xl rounded-b-xl p-2 bg-white/90 dark:bg-gray-800">
          {/* Balance */}
          <View className="justify-center items-center p-6 rounded-3xl bg-zinc-100 dark:bg-gray-700">
            <Text className="mb-3 text-sm font-medium text-neutral-700 dark:text-gray-400">
              Balance
            </Text>
            <View className="flex-row justify-center items-center">
              {showBalance && (
                <Text className="font-medium font-mono text-3xl tracking-wide text-neutral-900 dark:text-gray-100">
                  {`${currency} ${formatCurrency(balance)}`}
                </Text>
              )}
              <TouchableOpacity
                onPress={handleBalanceVisibility}
                className="ml-2"
              >
                <Ionicons
                  name={showBalance ? "eye-off" : "eye"}
                  size={20}
                  color="gray"
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* Actions */}
          <View className="flex-row justify-between items-center w-full gap-2 p-3 mt-4 z-10">
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => {
                console.info("Opening Send Modal");
                setSendModalVisible(true);
                setRequestModalVisible(false);
              }}
              className="justify-center items-center p-3 rounded-lg flex-grow max-w-full bg-gray-800s"
              style={{ backgroundColor: defaultColors.primary }}
            >
              <Text className="text-lg font-medium text-white">Send</Text>
            </TouchableOpacity>

            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => {
                console.info("Opening Request Modal");
                setSendModalVisible(false);
                setRequestModalVisible(true);
              }}
              className="justify-center items-center p-3 rounded-lg flex-grow max-w-full bg-gray-800s"
              style={{ backgroundColor: defaultColors.primary }}
            >
              <Text className="text-lg font-medium text-white">Request</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* Transfer Request Manager */}
      <TransferRequestManager updateBalance={fetchWalletsData} />

      {/* Send Modal */}
      <Modal
        animationType="slide"
        transparent
        visible={isSendModalVisible}
        onRequestClose={() => setSendModalVisible(false)}
      >
        <TouchableOpacity
          className="flex-1 bg-black/60"
          onPress={() => setSendModalVisible(false)}
        />

        <Animated.View
          style={modalAnimatedStyle}
          className="absolute bottom-0 p-5 pb-12 rounded-t-3xl w-full gap-y-8 bg-white/90 dark:bg-gray-900 shadow-lg"
        >
          <View className="flex-row items-center justify-between mx-2">
            <Text className="font-bold text-xl text-gray-500">Send Money</Text>

            {/* Close Button */}
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => setSendModalVisible(false)}
            >
              <Ionicons name="close" size={20} color={defaultColors.red} />
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              setSendModalVisible(false);
              router.push(
                "/(authenticated)/(screens)/transactions/send/InternalTransfer"
              );
            }}
            className="flex-row items-center"
          >
            <Ionicons
              name="wallet-outline"
              size={20}
              color={defaultColors.primary}
            />
            <Text className="ml-3 text-lg text-gray-800 dark:text-gray-300">
              Send within {appInfo.APP_NAME}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              setSendModalVisible(false);
              router.push(
                "/(authenticated)/(screens)/transactions/send/ExternalTransfer"
              );
            }}
            className="flex-row items-center"
          >
            <Ionicons
              name="swap-horizontal"
              size={20}
              color={defaultColors.primary}
            />
            <Text className="ml-3 text-lg text-gray-800 dark:text-gray-300">
              Send Outside {appInfo.APP_NAME}
            </Text>
          </TouchableOpacity>
        </Animated.View>
      </Modal>

      {/* Request Modal */}
      <Modal
        animationType="slide"
        transparent
        visible={isRequestModalVisible}
        onRequestClose={() => setRequestModalVisible(false)}
      >
        <TouchableOpacity
          className="flex-1 bg-black/60"
          onPress={() => setRequestModalVisible(false)}
        />

        <Animated.View
          style={modalAnimatedStyle}
          className="absolute bottom-0 p-5 pb-12 rounded-t-3xl w-full gap-y-8 bg-white/90 dark:bg-gray-900 shadow-lg"
        >
          <View className="flex-row items-center justify-between mx-2">
            <Text className="font-bold text-xl text-gray-500">
              Request Money
            </Text>

            {/* Close Button */}
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => setRequestModalVisible(false)}
            >
              <Ionicons name="close" size={20} color={defaultColors.red} />
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              setRequestModalVisible(false),
                router.push(
                  "/(authenticated)/(screens)/transactions/requests/InternalRequest"
                );
            }}
            className="flex-row items-center"
          >
            <Ionicons
              name="wallet-outline"
              size={20}
              color={defaultColors.primary}
            />
            <Text className="ml-3 text-lg text-gray-800 dark:text-gray-300">
              Ask a {appInfo.APP_NAME} Friend
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            activeOpacity={0.8}
            onPress={() => {
              setRequestModalVisible(false);
              router.push(
                "/(authenticated)/(screens)/transactions/requests/ExternalRequest"
              );
            }}
            className="flex-row items-center"
          >
            <Ionicons
              name="swap-horizontal"
              size={20}
              color={defaultColors.primary}
            />
            <Text className="ml-3 text-lg text-gray-800 dark:text-gray-300">
              Request Outside {appInfo.APP_NAME}
            </Text>
          </TouchableOpacity>
        </Animated.View>
      </Modal>
    </View>
  );
}
