import React, { useEffect, useMemo, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
  useColorScheme,
  Modal,
} from "react-native";
import { Picker } from "@react-native-picker/picker";
import { Ionicons } from "@expo/vector-icons";
import DateTimePicker from "@react-native-community/datetimepicker";
import dayjs from "dayjs";
import Animated, { FadeIn, FadeInDown, FadeOut } from "react-native-reanimated";

import { submitCustomerProfile } from "@/features/api";
import { useDeviceContext } from "@/features/providers";
import { appInfo, defaultColors } from "@/features/constants";
import { useNotificationToast } from "@/features/providers";
import { useUserStore } from "@/features/store";
import { handleError } from "@/features/utils/handleError";

// Environment variables
const MIN_AGE = Number(appInfo.MIN_AGE);

interface Field {
  label: string;
  key: string;
  icon: keyof typeof Ionicons.glyphMap;
  iconColor: string;
  keyboard?: "numeric" | "phone-pad" | "default";
  required?: boolean;
  section: "personal" | "address" | "next_of_kin";
}

interface VerificationProps {
  modalVisible: boolean;
  setModalVisible: (visible: boolean) => void;
}

const AnimatedView = Animated.createAnimatedComponent(View);

export default function VerificationForm({
  modalVisible,
  setModalVisible,
}: VerificationProps) {
  const scheme = useColorScheme();
  const { customerProfile, setCustomerProfile } = useUserStore();
  const { showNotification } = useNotificationToast();
  const { deviceDetails } = useDeviceContext();

  const [formValidate, setFormValidate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [activeSection, setActiveSection] = useState<
    "personal" | "address" | "next_of_kin"
  >("personal");

  const [formData, setFormData] = useState({
    id_type: customerProfile?.id_type || "",
    id_number: customerProfile?.id_number || "",
    country: deviceDetails?.country || "",
    region_state: deviceDetails?.region || "",
    city: deviceDetails?.city || "",
    postal_code: "",
    postal_address: "",
    residential_address: "",
    next_of_kin_name: "",
    next_of_kin_relationship: "",
    next_of_kin_contact: "",
    date_of_birth: "",
  });

  useEffect(() => {
    setFormValidate(
      !!formData.id_type &&
        !!formData.id_number &&
        !!formData.country &&
        !!formData.region_state &&
        !!formData.city &&
        !!formData.date_of_birth &&
        !!formData.next_of_kin_name &&
        !!formData.next_of_kin_relationship &&
        !!formData.next_of_kin_contact
    );
  }, [formData]);

  const handleChange = (field: keyof typeof formData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleClearFields = () => {
    setFormData({
      id_type: "",
      id_number: "",
      country: deviceDetails?.country || "",
      region_state: deviceDetails?.region || "",
      city: deviceDetails?.city || "",
      postal_code: "",
      postal_address: "",
      residential_address: "",
      next_of_kin_name: "",
      next_of_kin_relationship: "",
      next_of_kin_contact: "",
      date_of_birth: "",
    });
    setActiveSection("personal");
    setFormValidate(false);
  };

  const findFirstInvalidSection = ():
    | "personal"
    | "address"
    | "next_of_kin"
    | null => {
    const sections: ("personal" | "address" | "next_of_kin")[] = [
      "personal",
      "address",
      "next_of_kin",
    ];

    for (const section of sections) {
      const fieldsInSection = FormFields.filter(
        (f) => f.section === section && f.required
      );
      for (const field of fieldsInSection) {
        const value = formData[field.key as keyof typeof formData];
        if (!value) {
          return section;
        }
      }
    }
    return null;
  };

  const onFormSubmission = async () => {
    if (!formValidate) return;

    try {
      setLoading(true);
      const { data } = await submitCustomerProfile(formData);
      await setCustomerProfile(data.customerProfile);

      handleClearFields();

      setModalVisible(false);

      const message = data.message || "Customer data submitted successfully.";
      showNotification(message, "success", 6000);
    } catch (error: any) {
      handleError(
        error,
        "Failed to submit customer data. Please try again later."
      );
    } finally {
      setLoading(false);
    }
  };

  const FormFields: Field[] = useMemo(
    () => [
      {
        label: "ID Type",
        key: "id_type",
        icon: "card-outline",
        iconColor: "#4B5563",
        required: true,
        section: "personal",
      },
      {
        label: "ID Number",
        key: "id_number",
        icon: "id-card-outline",
        iconColor: "#4B5563",
        required: true,
        section: "personal",
      },
      {
        label: "Date of Birth",
        key: "date_of_birth",
        icon: "calendar-outline",
        iconColor: "#F59E0B",
        required: true,
        section: "personal",
      },
      {
        label: "Country",
        key: "country",
        icon: "earth-outline",
        iconColor: "#34D399",
        required: true,
        section: "address",
      },
      {
        label: "Region, State, or County",
        key: "region_state",
        icon: "location-outline",
        iconColor: "#3B82F6",
        required: true,
        section: "address",
      },
      {
        label: "City",
        key: "city",
        icon: "business-outline",
        iconColor: "#1D4ED8",
        required: true,
        section: "address",
      },
      {
        label: "Residential Address",
        key: "residential_address",
        icon: "home-outline",
        iconColor: "#FBBF24",
        section: "address",
      },
      {
        label: "Postal Code",
        key: "postal_code",
        icon: "mail-outline",
        iconColor: "#9b59d6",
        keyboard: "numeric",
        section: "address",
      },
      {
        label: "Postal Address",
        key: "postal_address",
        icon: "navigate-outline",
        iconColor: "#38BDF8",
        section: "address",
      },
      {
        label: "Next of Kin Name",
        key: "next_of_kin_name",
        icon: "person-outline",
        iconColor: "#F87171",
        required: true,
        section: "next_of_kin",
      },
      {
        label: "Next of Kin Relationship",
        key: "next_of_kin_relationship",
        icon: "people-outline",
        iconColor: "#F59E0B",
        required: true,
        section: "next_of_kin",
      },
      {
        label: "Next of Kin Contact",
        key: "next_of_kin_contact",
        icon: "call-outline",
        iconColor: "#10B981",
        keyboard: "phone-pad",
        required: true,
        section: "next_of_kin",
      },
    ],
    []
  );

  const defaultDate = new Date(
    new Date().setFullYear(new Date().getFullYear() - MIN_AGE)
  );

  const handleDateChange = (_: any, selectedDate?: Date) => {
    if (!selectedDate) {
      setShowDatePicker(false);
      return;
    }

    if (selectedDate > defaultDate) {
      handleChange("date_of_birth", "");

      const message = `You must be at least ${MIN_AGE} years old.`;
      showNotification(message, "info", 6000);
      return;
    } else {
      handleChange("date_of_birth", dayjs(selectedDate).format("YYYY-MM-DD"));
    }

    setShowDatePicker(false);
  };

  const renderField = (field: Field) => {
    if (field.key === "date_of_birth") {
      return (
        <AnimatedView
          key={field.key}
          entering={FadeInDown.delay(100)}
          className="mb-5"
        >
          <Text className="mb-2 text-gray-600 dark:text-gray-300 font-medium">
            {field.label}{" "}
            {field.required && <Text className="text-red-500">*</Text>}
          </Text>
          <TouchableOpacity
            onPress={() => setShowDatePicker(true)}
            className="flex-row items-center p-4 rounded-xl border-b-2 border-gray-200 dark:border-gray-800"
          >
            <Ionicons
              name={field.icon}
              size={20}
              color={field.iconColor}
              className="mr-3"
            />
            <Text className="flex-1 text-lg text-gray-900 dark:text-gray-100">
              {formData.date_of_birth
                ? dayjs(formData.date_of_birth).format("DD MMM YYYY")
                : "Select Date"}
            </Text>
          </TouchableOpacity>
        </AnimatedView>
      );
    }

    if (field.key === "id_type") {
      return (
        <AnimatedView key={field.key} entering={FadeInDown} className="mb-5">
          <Text className="mb-2 text-gray-600 dark:text-gray-300 font-medium">
            {field.label} <Text className="text-red-500">*</Text>
          </Text>
          <View className="flex-row items-center py-1 ps-4 rounded-xl border-b-2 border-gray-200 dark:border-gray-800">
            <Ionicons name={field.icon} size={20} color={field.iconColor} />
            <View className="flex-1">
              <Picker
                selectedValue={formData.id_type}
                onValueChange={(value) => handleChange("id_type", value)}
                mode="dropdown"
                dropdownIconColor={scheme === "dark" ? "#D1D5DB" : "#4B5563"}
                style={{ color: scheme === "dark" ? "#D1D5DB" : "#4B5563" }}
              >
                <Picker.Item label="Select ID Type" value="" />
                <Picker.Item label="National ID" value="national_id" />
                <Picker.Item label="Passport" value="passport" />
                <Picker.Item label="Driving License" value="driving_license" />
              </Picker>
            </View>
          </View>
        </AnimatedView>
      );
    }

    return (
      <AnimatedView
        key={field.key}
        entering={FadeInDown.delay(200)}
        className="mb-5"
      >
        <Text className="mb-2 text-gray-600 dark:text-gray-300 font-medium">
          {field.label}{" "}
          {field.required && <Text className="text-red-500">*</Text>}
        </Text>
        <View className="flex-row items-center p-4 rounded-xl border-b-2 border-gray-200 dark:border-gray-800">
          <Ionicons
            name={field.icon}
            size={20}
            color={field.iconColor}
            className="mr-3"
          />
          <TextInput
            className="flex-1 text-lg text-gray-900 dark:text-gray-100"
            placeholder={`Enter Your ${field.label}`}
            keyboardType={field.keyboard || "default"}
            value={formData[field.key as keyof typeof formData]}
            onChangeText={(text) =>
              handleChange(field.key as keyof typeof formData, text)
            }
            placeholderTextColor={scheme === "dark" ? "#888" : "#444"}
            autoCapitalize="words"
          />
        </View>
      </AnimatedView>
    );
  };

  return (
    <Modal
      animationType="fade"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => setModalVisible(false)}
    >
      <AnimatedView
        entering={FadeIn.duration(300)}
        exiting={FadeOut.duration(200)}
        className="flex-1 bg-gray-100 dark:bg-gray-900"
      >
        {/* Header Section */}
        <AnimatedView
          entering={FadeInDown.delay(50)}
          className="flex-row justify-between items-center p-6"
        >
          <Text className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Account Verification
          </Text>
          <TouchableOpacity
            onPress={() => setModalVisible(false)}
            className="p-2 rounded-full bg-gray-100 dark:bg-gray-900"
          >
            <Ionicons name="close" size={24} color={defaultColors.red} />
          </TouchableOpacity>
        </AnimatedView>

        {/* Form Section */}
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : "height"}
          className="flex-1"
        >
          {/* Tab Bar */}
          <View className="flex-row justify-around border-b border-gray-200 dark:border-gray-800 py-3">
            {["personal", "address", "next_of_kin"].map((section) => (
              <TouchableOpacity
                key={section}
                onPress={() => setActiveSection(section as any)}
              >
                <Text
                  className={`font-semibold text-lg capitalize ${
                    activeSection === section
                      ? "text-blue-500 border-b-2 border-blue-500"
                      : "text-gray-500"
                  }`}
                >
                  {section.replace(/_/g, " ")}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Form Fields */}
          <ScrollView className="p-6" showsVerticalScrollIndicator={false}>
            {FormFields.filter((f) => f.section === activeSection).map(
              renderField
            )}
            {showDatePicker && (
              <DateTimePicker
                value={
                  formData.date_of_birth
                    ? new Date(formData.date_of_birth)
                    : defaultDate
                }
                display="spinner"
                onChange={handleDateChange}
                mode="date"
                maximumDate={defaultDate}
                style={{
                  backgroundColor: scheme === "dark" ? "#1F2937" : "#fff",
                }}
              />
            )}
          </ScrollView>

          {/* Buttons */}
          <View className="flex-row justify-between items-center p-5 border-t border-gray-200 dark:border-gray-800">
            <TouchableOpacity
              onPress={() => (handleClearFields(), setModalVisible(false))}
              className="px-6 py-3 rounded-full bg-gray-300 dark:bg-gray-700"
            >
              <Text className="text-gray-900 dark:text-white font-semibold">
                Cancel
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => {
                if (formValidate) {
                  onFormSubmission();
                } else {
                  const invalidSection = findFirstInvalidSection();
                  if (invalidSection) {
                    setActiveSection(invalidSection);
                  }
                }
              }}
              disabled={loading}
              className="px-6 py-3 rounded-full bg-indigo-600"
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text className="text-white font-semibold">
                  {formValidate ? "Submit" : "Continue"}
                </Text>
              )}
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </AnimatedView>
    </Modal>
  );
}
