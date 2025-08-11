import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  Modal,
  TouchableOpacity,
  ActivityIndicator,
  FlatList,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import * as Haptics from "expo-haptics";
import * as Contacts from "expo-contacts";
import Animated, { FadeInRight, FadeInUp } from "react-native-reanimated";

import { verifyRecipient } from "@/features/api";
import { PhoneCodePicker } from "@/features/components";
import { defaultColors } from "@/features/constants";
import { validateEmail, validatePhoneNumber } from "@/features/lib";
import {
  useDeviceContext,
  useNotificationToast,
  useSessionAppState,
} from "@/features/providers";
import { ContactProp, useFrequentContactsStore } from "@/features/store";
import { VerifyRecipientResponse } from "@/types";
import { handleError } from "@/features/utils/handleError";

interface Props {
  isVisible: boolean;
  setIsVisible: (value: boolean) => void;
  setDetails: (data: VerifyRecipientResponse) => void;
  setAmountModalVisible: (value: boolean) => void;
}

const RecipientLookupModal = ({
  isVisible,
  setIsVisible,
  setDetails,
  setAmountModalVisible,
}: Props) => {
  const { deviceDetails } = useDeviceContext();
  const { showNotification } = useNotificationToast();
  const { setBackgroundSafe } = useSessionAppState();

  const [queryParams, setQueryParams] = useState("");
  const [queryParamsValid, setQueryParamsValid] = useState(false);
  const [validatingRecipient, setValidatingRecipient] = useState(false);

  const [contacts, setContacts] = useState<ContactProp[]>([]);
  const [filteredContacts, setFilteredContacts] = useState<ContactProp[]>([]);
  const { frequentContacts, addToFrequentContacts } =
    useFrequentContactsStore();
  const [showNumberInput, setShowNumberInput] = useState(false);

  const [countryCode, setCountryCode] = useState(
    deviceDetails?.countryCallingCode || "+254"
  );
  const [isCountryPickerVisible, setIsCountryPickerVisible] = useState(false);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    setBackgroundSafe(true);
    const { status } = await Contacts.requestPermissionsAsync();
    setBackgroundSafe(false);

    if (status === "granted") {
      const { data } = await Contacts.getContactsAsync({
        fields: [Contacts.Fields.PhoneNumbers],
      });

      if (data.length > 0) {
        const uniquePhoneNumbers = new Set<string>();

        const formattedContacts: ContactProp[] = data
          .filter((c) => c.phoneNumbers?.length)
          .flatMap((c) =>
            (c.phoneNumbers ?? [])
              .filter((p) => p.number)
              .map((p) => {
                const cleanedNumber = p.number?.replace(/[\s-]/g, "") ?? "";

                if (uniquePhoneNumbers.has(cleanedNumber)) {
                  return null;
                }

                uniquePhoneNumbers.add(cleanedNumber);
                return {
                  id: c.id ?? "",
                  name: c.name,
                  phoneNumbers: [cleanedNumber],
                };
              })
          )
          .filter((contact) => contact !== null);

        setContacts(formattedContacts);
        setFilteredContacts(formattedContacts);
      }
    }
  };

  const handleInputChange = (newInput: string) => {
    setQueryParams(newInput);
  };

  useEffect(() => {
    const isEmail = queryParams.includes("@");
    if (isEmail) {
      setQueryParamsValid(validateEmail(queryParams));
    } else if (queryParams.length > 0) {
      setQueryParamsValid(validatePhoneNumber(queryParams));
    } else {
      setQueryParamsValid(false);
    }
  }, [queryParams]);

  const handleSearch = (query: string) => {
    setQueryParams(query);
    if (query.length > 0) {
      const filtered = contacts.filter(
        (contact) =>
          contact.name.toLowerCase().includes(query.toLowerCase()) ||
          contact.phoneNumbers.some((num) => num.includes(query))
      );
      setFilteredContacts(filtered);
    } else {
      setFilteredContacts(contacts);
    }
  };

  const handleRecipientVerification = async () => {
    setValidatingRecipient(true);
    try {
      let responseData = null;

      if (queryParams.includes("@")) {
        if (!validateEmail(queryParams)) {
          throw new Error("Invalid email format");
        }
        ({ data: responseData } = await verifyRecipient({
          email: queryParams,
        }));
      } else {
        const fullPhoneNumber = queryParams.startsWith("+")
          ? queryParams
          : `${countryCode}${queryParams}`;
        if (!validatePhoneNumber(fullPhoneNumber)) {
          throw new Error("Invalid phone number format");
        }
        ({ data: responseData } = await verifyRecipient({
          phone: fullPhoneNumber,
        }));
      }

      setDetails(responseData);
      setAmountModalVisible(true);
      setIsVisible(false);
    } catch (error) {
      handleError(
        error,
        "Failed to validate recipient. Please try again later."
      );

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setValidatingRecipient(false);
    }
  };

  const handleNumberInputToggle = () => {
    setShowNumberInput(!showNumberInput);
    setQueryParams("");
  };

  return (
    <Modal
      animationType="fade"
      transparent
      visible={isVisible}
      onRequestClose={router.back}
    >
      <View className="flex-1 w-full p-4 bg-gray-100 dark:bg-gray-900">
        {/* Header */}
        <View className="flex-row items-center justify-between mb-8">
          {/* Title */}
          <Text className="font-extrabold text-xl text-gray-700 dark:text-gray-300">
            Fill details to proceed
          </Text>
          {/* Close Button */}
          <TouchableOpacity activeOpacity={0.8} onPress={router.back}>
            <Ionicons name="close" size={28} color={defaultColors.red} />
          </TouchableOpacity>
        </View>

        {/* Frequent Contacts Section */}
        {frequentContacts.length > 0 && (
          <View className="mb-2">
            <Text className="font-semibold mb-2 text-base text-gray-600">
              Frequent Contacts
            </Text>
            <FlatList
              horizontal
              data={frequentContacts}
              keyExtractor={(item) => item.id}
              contentContainerStyle={{ paddingBottom: 10 }}
              scrollEnabled
              showsHorizontalScrollIndicator={false}
              renderItem={({ item, index }) => (
                <Animated.View
                  entering={FadeInRight.delay(Math.min(index * 25, 200))}
                  key={item.id}
                >
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => setQueryParams(item.phoneNumbers[0])}
                    className="p-4 rounded-xl mr-2 items-center bg-white dark:bg-gray-800"
                  >
                    <Text className="text-base text-gray-600">
                      {item.name.split(" ").slice(0, 2).join(" ")}
                    </Text>
                    <Text className="text-gray-500">
                      {item.phoneNumbers[0]}
                    </Text>
                  </TouchableOpacity>
                </Animated.View>
              )}
            />
          </View>
        )}

        {/* Search Input */}
        {!showNumberInput && (
          <TextInput
            placeholder="Search contacts, enter phone or email"
            placeholderTextColor={defaultColors.gray}
            value={queryParams}
            onChangeText={handleSearch}
            autoCapitalize="none"
            className="w-full p-4 rounded-xl mb-4 text-gray-500 bg-white/90 dark:bg-gray-800"
          />
        )}

        {/* Country Code & Number Input */}
        {showNumberInput && (
          <View className="flex-row items-center mb-4">
            <TouchableOpacity
              activeOpacity={0.8}
              onPress={() => setIsCountryPickerVisible(true)}
            >
              <Text className="text-lg font-bold px-4 py-3 rounded-lg text-gray-900 dark:text-gray-300 bg-white/90 dark:bg-gray-700">
                {countryCode}
              </Text>
            </TouchableOpacity>

            <TextInput
              placeholder="Enter number"
              keyboardType="phone-pad"
              value={queryParams}
              onChangeText={handleInputChange}
              placeholderTextColor={defaultColors.gray}
              className="flex-1 p-4 rounded-xl ml-2 text-gray-500 bg-white/90 dark:bg-gray-800"
            />
          </View>
        )}

        {/* Toggle Search / Number Input */}
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={handleNumberInputToggle}
          className="mb-4 p-3 rounded-xl"
        >
          <Text className="font-semibold text-center text-blue-500">
            {showNumberInput ? "Switch to Search" : "Enter Number"}
          </Text>
        </TouchableOpacity>

        {/* Contacts List */}
        <View className="flex-1">
          <Text className="font-semibold text-base text-gray-500 mb-2">
            Contacts
          </Text>

          {filteredContacts.length > 0 ? (
            <FlatList
              data={filteredContacts}
              keyExtractor={(item, index) => `${item.id}-${index}`}
              showsVerticalScrollIndicator={false}
              renderItem={({ item, index }) => (
                <Animated.View
                  entering={FadeInUp.delay(Math.min(index * 20, 200))}
                  key={item.id}
                >
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => {
                      setQueryParams(item.phoneNumbers[0]);
                      addToFrequentContacts(item);
                    }}
                    className="p-5 mb-2 gap-y-3 rounded-xl border-b-2 border-gray-200 dark:border-gray-800"
                  >
                    <Text className="font-semibold text-gray-700 dark:text-gray-400">
                      {item.name}
                    </Text>
                    {item.phoneNumbers.map((number, index) => (
                      <Text key={index} className="text-gray-500">
                        {number}
                      </Text>
                    ))}
                  </TouchableOpacity>
                </Animated.View>
              )}
            />
          ) : (
            <View className="flex-1">
              <ActivityIndicator size={28} color={defaultColors.green} />
            </View>
          )}
        </View>

        {/* Submit Button */}
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={handleRecipientVerification}
          disabled={!queryParamsValid}
          className={`w-full p-4 rounded-full mt-4 ${
            queryParamsValid ? "bg-indigo-600" : "bg-gray-200 dark:bg-gray-800"
          }`}
        >
          {validatingRecipient ? (
            <ActivityIndicator size="small" color={defaultColors.green} />
          ) : (
            <Text className="font-semibold text-lg text-center text-gray-300">
              Validate & Continue
            </Text>
          )}
        </TouchableOpacity>

        {/* Use the reusable CountryPicker component */}
        <PhoneCodePicker
          isVisible={isCountryPickerVisible}
          setIsVisible={setIsCountryPickerVisible}
          setCountryCode={setCountryCode}
        />
      </View>
    </Modal>
  );
};

export default RecipientLookupModal;
