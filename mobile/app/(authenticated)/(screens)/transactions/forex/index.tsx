import React, { useEffect, useState, useCallback, useMemo } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  useColorScheme,
  ActivityIndicator,
} from "react-native";
import Animated, {
  FadeInUp,
  FadeInDown,
  FadeIn,
  ZoomIn,
} from "react-native-reanimated";
import { Picker } from "@react-native-picker/picker";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";

import {
  previewExchange,
  executeExchange,
  fetchCurrencies,
  fetchUserWallets,
} from "@/features/api";
import { Keypad } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { validateAmount, formatCurrency } from "@/features/lib";
import { useNotificationToast } from "@/features/providers";
import { Currency, WalletResponse, PreviewExchangeResponse } from "@/types";
import { handleError } from "@/features/utils/handleError";
import { useBiometricStore } from "@/features/store";
import { useBiometricAuthentication } from "@/features/hooks";
import { CurrencyExchangePreviewModal } from "./components";

type Wallet = WalletResponse["results"][0];

export default function CurrencyBureau() {
  const scheme = useColorScheme();
  const { showNotification } = useNotificationToast();
  const { isBiometricEnabled } = useBiometricStore();
  const { verifyBiometric2FAs } = useBiometricAuthentication();

  const [amountInput, setAmountInput] = useState("");
  const [amountValid, setAmountValid] = useState(false);
  const [walletsData, setWalletsData] = useState<Wallet[]>([]);
  const [sourceCurrency, setSourceCurrency] = useState("");
  const [targetCurrency, setTargetCurrency] = useState("");
  const [supportedCurrencies, setSupportedCurrencies] = useState<Currency[]>(
    []
  );
  const [previewData, setPreviewData] =
    useState<PreviewExchangeResponse | null>(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [loadingExecute, setLoadingExecute] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [textWidth, setTextWidth] = useState(0);

  useEffect(() => {
    setAmountValid(validateAmount(amountInput));
  }, [amountInput]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [wallets, currencies] = await Promise.all([
          fetchUserWallets(),
          fetchCurrencies(),
        ]);
        setWalletsData(
          wallets.data.results.sort((a, b) =>
            a.currency.name.localeCompare(b.currency.name)
          )
        );
        setSupportedCurrencies(
          currencies.data.results.sort((a, b) => a.name.localeCompare(b.name))
        );
      } catch (error) {
        console.error("Error fetching data", error);
      }
    };
    fetchData();
  }, []);

  const handleSetAllWalletBalances = useCallback(() => {
    const sourceWallet = walletsData.find(
      (wallet) => wallet.currency.code === sourceCurrency
    );
    if (sourceWallet) {
      setAmountInput(sourceWallet.balance.toString().split(".")[0]);
    }
  }, [walletsData, sourceCurrency]);

  const onPreviewExchange = useCallback(async () => {
    if (!amountValid || !sourceCurrency || !targetCurrency) return;

    setLoadingPreview(true);
    try {
      const response = await previewExchange({
        source_currency: sourceCurrency,
        target_currency: targetCurrency,
        source_amount: amountInput,
      });
      setPreviewData(response.data);
      setModalVisible(true);
    } catch (error) {
      handleError(
        error,
        "Failed to fetch exchange rate preview. Please try again later."
      );

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setLoadingPreview(false);
    }
  }, [amountValid, sourceCurrency, targetCurrency, amountInput]);

  const onExecuteExchange = useCallback(async () => {
    if (!previewData) return;

    if (isBiometricEnabled) {
      const verified = await verifyBiometric2FAs(
        false,
        "Authenticate to confirm currency exchange"
      );
      if (!verified) return;
    }

    setLoadingExecute(true);
    try {
      await executeExchange({
        source_currency: sourceCurrency,
        target_currency: targetCurrency,
        source_amount: amountInput,
      });

      const message = `Exchange of ${formatCurrency(
        previewData.source_amount
      )} ${previewData.source_currency} to ${formatCurrency(
        previewData.converted_amount_with_fee
      )} ${previewData.target_currency} completed successfully.`;
      showNotification(message, "success", 8000);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      setSourceCurrency("");
      setTargetCurrency("");
      setAmountInput("0");
      setPreviewData(null);
      setModalVisible(false);
      router.back();
    } catch (error) {
      handleError(error, "Failed to execute currency exchange!");

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setLoadingExecute(false);
    }
  }, [previewData, sourceCurrency, targetCurrency, amountInput]);

  const isExchangeReady = useMemo(() => {
    return (
      amountValid &&
      sourceCurrency &&
      targetCurrency &&
      sourceCurrency !== targetCurrency &&
      sourceCurrency !== "placeholder" &&
      targetCurrency !== "placeholder"
    );
  }, [amountValid, sourceCurrency, targetCurrency]);

  const pickerStyle = useMemo(
    () => ({
      color: scheme === "dark" ? "#F3F4F6" : "#111827",
      backgroundColor: scheme === "dark" ? "#1F2937" : "#F9FAFB",
    }),
    [scheme]
  );

  const placeholderStyle = useMemo(
    () => ({
      color: scheme === "dark" ? "#9CA3AF" : "#6B7280",
    }),
    [scheme]
  );

  return (
    <View className="flex-1 p-4 bg-gray-100 dark:bg-gray-900">
      <Animated.View
        className="flex-1 justify-around items-center"
        entering={FadeInDown.delay(100)}
      >
        <Animated.View className="w-full mb-8" entering={FadeInUp.delay(300)}>
          <View className="gap-5">
            {[
              {
                value: sourceCurrency,
                setter: setSourceCurrency,
                data: walletsData,
                label: "Select source currency...",
              },
              {
                value: targetCurrency,
                setter: setTargetCurrency,
                data: supportedCurrencies,
                label: "Select target currency...",
              },
            ].map(({ value, setter, data, label }, idx) => (
              <View key={idx} className="overflow-hidden rounded-xl">
                <Picker
                  selectedValue={value}
                  onValueChange={setter}
                  mode="dropdown"
                  dropdownIconColor={scheme === "dark" ? "#9CA3AF" : "#6B7280"}
                  style={pickerStyle}
                >
                  <Picker.Item
                    label={label}
                    value="placeholder"
                    style={placeholderStyle}
                  />
                  {data.map((item) => {
                    if ("currency" in item) {
                      return (
                        <Picker.Item
                          key={item.currency.code}
                          label={item.currency.name}
                          value={item.currency.code}
                          style={{
                            color:
                              item.currency.code === value
                                ? "#22C55E"
                                : scheme === "dark"
                                ? "#E5E7EB"
                                : "#374151",
                          }}
                        />
                      );
                    }
                    return (
                      <Picker.Item
                        key={item.code}
                        label={item.name}
                        value={item.code}
                        style={{
                          color:
                            item.code === value
                              ? "#22C55E"
                              : scheme === "dark"
                              ? "#E5E7EB"
                              : "#374151",
                        }}
                      />
                    );
                  })}
                </Picker>
              </View>
            ))}
          </View>
        </Animated.View>

        <Animated.View
          className="w-full max-w-lg flex-row items-center gap-x-4 px-4 mb-8"
          entering={FadeIn.delay(500)}
        >
          <View className="flex-1 h-16 justify-center items-center px-4">
            <Text
              onLayout={(e) => setTextWidth(e.nativeEvent.layout.width)}
              className={`font-bold text-2xl ${
                amountInput && Number(amountInput) === 0
                  ? "text-red-500"
                  : amountInput === ""
                  ? "text-gray-400 dark:text-gray-500"
                  : "text-gray-800 dark:text-gray-200"
              }`}
            >
              {amountInput
                ? `${
                    sourceCurrency !== "placeholder" ? sourceCurrency : ""
                  } ${formatCurrency(Number(amountInput))}`
                : "Enter Amount"}
            </Text>
            <View
              style={{ width: textWidth }}
              className="h-1 rounded-full mt-2 bg-indigo-500 dark:bg-indigo-400"
            />
          </View>

          {isExchangeReady && (
            <TouchableOpacity
              onPress={handleSetAllWalletBalances}
              className="p-3 rounded-full bg-gray-200 dark:bg-gray-700 shadow-md"
            >
              <Ionicons
                name="wallet-outline"
                size={28}
                color={defaultColors.green}
              />
            </TouchableOpacity>
          )}
        </Animated.View>

        <Animated.View entering={ZoomIn.delay(600)}>
          <Keypad onInputChange={setAmountInput} />
        </Animated.View>

        <Animated.View
          className="w-full max-w-lg mt-4"
          entering={FadeInUp.delay(700)}
        >
          <TouchableOpacity
            onPress={onPreviewExchange}
            className={`p-5 rounded-full ${
              isExchangeReady
                ? "bg-indigo-600 active:bg-indigo-700"
                : "bg-gray-300 dark:bg-gray-700"
            }`}
            disabled={!isExchangeReady}
          >
            {loadingPreview ? (
              <ActivityIndicator size={20} color={defaultColors.green} />
            ) : (
              <Text className="font-semibold text-lg text-center text-white">
                Preview Exchange
              </Text>
            )}
          </TouchableOpacity>
        </Animated.View>
      </Animated.View>

      <CurrencyExchangePreviewModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        previewData={previewData}
        handleExecuteExchange={onExecuteExchange}
        loadingExecute={loadingExecute}
      />
    </View>
  );
}
