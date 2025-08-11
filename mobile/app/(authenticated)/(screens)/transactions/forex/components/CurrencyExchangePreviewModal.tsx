import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ActivityIndicator,
} from "react-native";
import Animated from "react-native-reanimated";

import { defaultColors } from "@/features/constants";
import { formatCurrency, useModalAnimation } from "@/features/lib";

interface Props {
  modalVisible: boolean;
  setModalVisible: (visible: boolean) => void;
  previewData: any;
  handleExecuteExchange: () => void;
  loadingExecute: boolean;
}

export const CurrencyExchangePreviewModal: React.FC<Props> = ({
  modalVisible,
  setModalVisible,
  previewData,
  handleExecuteExchange,
  loadingExecute,
}) => {
  if (!previewData) {
    return null;
  }

  const { modalAnimatedStyle } = useModalAnimation(modalVisible);

  return (
    <Modal visible={modalVisible} transparent animationType="slide">
      <Animated.View
        style={modalAnimatedStyle}
        className="flex-1 justify-center items-center bg-black/60 p-4"
      >
        <View className="w-full bg-gray-100 dark:bg-gray-900 p-6 rounded-lg shadow-lg">
          {previewData && (
            <>
              <Text className="text-2xl font-bold text-gray-600 dark:text-gray-400 mb-6 text-center">
                Exchange Preview
              </Text>

              {/* Preview Data */}
              <View className="mb-6">
                <Text className="text-lg text-gray-500 dark:text-gray-400 mb-2">
                  Exchange Rate:{" "}
                  <Text className="font-semibold text-gray-700 dark:text-gray-200">
                    1 {previewData.source_currency} ={" "}
                    {previewData.platform_exchange_rate.toFixed(4)}{" "}
                    {previewData.target_currency}
                  </Text>
                </Text>

                <Text className="text-lg text-gray-500 dark:text-gray-400 mb-2">
                  Conversion Amount:{" "}
                  <Text className="font-semibold text-gray-700 dark:text-gray-200">
                    {previewData.source_currency}{" "}
                    {formatCurrency(previewData.source_amount)}
                  </Text>
                </Text>

                <Text className="text-lg text-gray-500 dark:text-gray-400 mb-2">
                  Forex Fee:{" "}
                  <Text className="font-semibold text-red-500">
                    {previewData.source_currency}{" "}
                    {formatCurrency(previewData.charged_amount)}
                  </Text>
                </Text>

                <Text className="text-lg text-gray-500 dark:text-gray-400">
                  Converted Amount:{" "}
                  <Text className="font-semibold text-green-600">
                    {previewData.target_currency}{" "}
                    {formatCurrency(previewData.converted_amount_with_fee)}
                  </Text>
                </Text>
              </View>

              {/* Execute Exchange Button */}
              <TouchableOpacity
                onPress={handleExecuteExchange}
                className="p-4 mt-6 rounded-full bg-indigo-600"
              >
                {loadingExecute ? (
                  <ActivityIndicator size={20} color={defaultColors.green} />
                ) : (
                  <Text className="font-semibold text-lg text-center text-gray-300">
                    Execute Exchange
                  </Text>
                )}
              </TouchableOpacity>

              {/* Close Modal Button */}
              <TouchableOpacity
                onPress={() => setModalVisible(false)}
                className="p-4 mt-4 rounded-full bg-gray-200 dark:bg-gray-800"
              >
                <Text className="font-semibold text-lg text-center text-gray-500">
                  Close
                </Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </Animated.View>
    </Modal>
  );
};

// export default CurrencyExchangePreviewModal;
