import React, { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";

import CreditIssuance from "./CreditIssuance";
import CreditHistory from "./CreditHistory";

type TabKey = "issuance" | "history";

export default function Index() {
  const [activeTab, setActiveTab] = useState<TabKey>("issuance");

  return (
    <View className="flex-1 bg-gray-100 dark:bg-gray-900">
      {/* Tab Bar */}
      <View className="flex-row justify-center bg-gray-100 dark:bg-gray-900 p-2 rounded-b-2xl shadow-md">
        <TouchableOpacity
          onPress={() => setActiveTab("issuance")}
          className={`flex-1 items-center p-3 border-b-2 ${
            activeTab === "issuance"
              ? "border-indigo-600"
              : "border-transparent"
          }`}
        >
          <Text
            className={`text-lg ${
              activeTab === "issuance"
                ? "text-indigo-500 font-bold"
                : "text-gray-700 dark:text-gray-300"
            }`}
          >
            Issue Credit
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => setActiveTab("history")}
          className={`flex-1 items-center p-3 border-b-2 ${
            activeTab === "history" ? "border-indigo-600" : "border-transparent"
          }`}
        >
          <Text
            className={`text-lg ${
              activeTab === "history"
                ? "text-indigo-500 font-bold"
                : "text-gray-700 dark:text-gray-300"
            }`}
          >
            Issuance History
          </Text>
        </TouchableOpacity>
      </View>

      {/* Tab Content */}
      <View className="flex-1">
        {activeTab === "issuance" ? <CreditIssuance /> : <CreditHistory />}
      </View>
    </View>
  );
}
