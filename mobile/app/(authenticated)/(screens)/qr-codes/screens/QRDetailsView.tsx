import React, { useEffect, useState } from "react";
import { View, Text, SafeAreaView, Button } from "react-native";

import ScanToPay from "./ScanToPay";
import { QRCodeProps } from "@/types";

export default function QRDetailView() {
  const [scannedData, setScannedData] = useState<QRCodeProps | null>(null);
  const [showScanner, setShowScanner] = useState(false);

  useEffect(() => {
    setShowScanner(true);
  }, []);

  const onValidScan = (result: QRCodeProps) => {
    setScannedData(result);
    setShowScanner(false);
  };

  return (
    <SafeAreaView className="flex-1 p-4 bg-gray-100 dark:bg-gray-900">
      {showScanner ? (
        <ScanToPay onValidScan={onValidScan} />
      ) : (
        <View className="flex-1 items-center justify-center">
          <Button title="Scan QR Code" onPress={() => setShowScanner(true)} />

          {scannedData && (
            <View className="mt-4 p-3 rounded-xl shadow-md gap-4 bg-white dark:bg-gray-800">
              <Text className="text-lg font-semibold text-center text-black dark:text-white">
                Scanned Data:
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Current User: {scannedData.currentUserIdentifier}
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Requested User: {scannedData.requestedUserIdentifier}
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Name: {scannedData.requestedUserName}
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Amount: {scannedData.amount} {scannedData.currency}
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Action: {scannedData.actionType}
              </Text>
              <Text className="text-center text-black dark:text-gray-300">
                Reason: {scannedData.reason || "N/A"}
              </Text>
            </View>
          )}
        </View>
      )}
    </SafeAreaView>
  );
}
