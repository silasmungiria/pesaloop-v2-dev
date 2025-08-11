import React from "react";
import { View, Text, FlatList } from "react-native";
import Animated, {
  FadeInDown,
  FadeInUp,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

interface CustomerProfileDetailsProps {
  customerProfile: any;
}

export default function CustomerProfileDetails({
  customerProfile,
}: CustomerProfileDetailsProps) {
  if (!customerProfile) return null;

  const details = [
    {
      label: "ID Document Type",
      value: customerProfile?.id_type?.replace(/_/g, " ").toUpperCase(),
    },
    { label: "ID Number", value: customerProfile?.id_number },
    {
      label: "Face Image Submitted",
      value: (
        <Ionicons
          name={
            customerProfile?.is_face_uploaded
              ? "checkmark-circle"
              : "close-circle"
          }
          size={18}
          color={customerProfile?.is_face_uploaded ? "green" : "red"}
        />
      ),
    },
    {
      label: "Front ID Image",
      value: (
        <Ionicons
          name={
            customerProfile?.is_id_front_uploaded
              ? "checkmark-circle"
              : "close-circle"
          }
          size={18}
          color={customerProfile?.is_id_front_uploaded ? "green" : "red"}
        />
      ),
    },
    {
      label: "Back ID Image",
      value: (
        <Ionicons
          name={
            customerProfile?.is_id_back_uploaded
              ? "checkmark-circle"
              : "close-circle"
          }
          size={18}
          color={customerProfile?.is_id_back_uploaded ? "green" : "red"}
        />
      ),
    },
    {
      label: "Proof of Address",
      value: (
        <Ionicons
          name={
            customerProfile?.is_address_proof_image_uploaded
              ? "checkmark-circle"
              : "close-circle"
          }
          size={18}
          color={
            customerProfile?.is_address_proof_image_uploaded ? "green" : "red"
          }
        />
      ),
    },
    {
      label: "Verification Status",
      value: customerProfile?.verification_status
        ?.replace(/_/g, " ")
        .toLowerCase()
        .replace(/^./, (char: string) => char.toUpperCase()),
    },
    {
      label: "Verified On",
      value: customerProfile?.verification_date
        ? new Date(customerProfile.verification_date).toLocaleDateString(
            "en-US",
            {
              year: "numeric",
              month: "short",
              day: "numeric",
            }
          )
        : null,
    },
  ].filter((item) => item.value !== null && item.value !== undefined);

  const renderItem = ({ item, index }: { item: any; index: number }) => (
    <Animated.View
      entering={FadeInDown.delay(Math.min(index * 100, 300)).springify()}
      exiting={FadeOutUp.springify()}
      layout={Layout.springify()}
      className="flex-row justify-between py-5 px-2 rounded-xl border-b border-gray-200 dark:border-gray-700"
    >
      <Text className="text-gray-700 dark:text-gray-300">{item.label}</Text>
      <View className="flex-row items-center">
        {typeof item.value === "string" ? (
          <Text className="font-semibold text-gray-900 dark:text-gray-100">
            {item.value}
          </Text>
        ) : (
          item.value
        )}
      </View>
    </Animated.View>
  );

  return (
    <View className="mt-6 w-full">
      <Text className="font-bold text-lg text-gray-800 dark:text-gray-200 mb-2">
        Customer Verification Details
      </Text>

      <FlatList
        data={details}
        renderItem={renderItem}
        keyExtractor={(item) => item.label}
        contentContainerStyle={{ paddingBottom: 20 }}
        scrollEnabled={false}
        ListFooterComponent={
          <>
            {customerProfile?.remarks && (
              <Animated.View
                entering={FadeInUp.delay(details.length * 80).duration(350)}
                className="p-5 rounded-xl border-b border-gray-200 dark:border-gray-700"
              >
                <Text className="mb-2 text-gray-700 dark:text-gray-300">
                  Remarks:
                </Text>
                <Text className="text-gray-900 dark:text-gray-100">
                  {customerProfile?.remarks}
                </Text>
              </Animated.View>
            )}
          </>
        }
      />
    </View>
  );
}
