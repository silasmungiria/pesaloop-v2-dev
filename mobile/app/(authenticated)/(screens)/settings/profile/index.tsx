import React, { useState } from "react";
import { FlatList, View } from "react-native";
import {
  SafeAreaView,
  useSafeAreaInsets,
} from "react-native-safe-area-context";

import { useUserStore } from "@/features/store";
import {
  Avatar,
  Header,
  CustomerProfileDetails,
  UploadButtons,
  UploadModal,
  UserProfile,
} from "./components";
import { VerificationForm } from "./forms";
import { useImageUpload } from "./hooks";

export default function AccountProfile() {
  const { user, customerProfile } = useUserStore();
  const [verificationModalVisible, setVerificationModalVisible] = useState(
    !user?.is_verified && !customerProfile
  );

  const { imageType, setImageType, uploadingImage, uploadImage } =
    useImageUpload();
  const [uploadModalVisible, setUploadModalVisible] = useState(false);

  const insets = useSafeAreaInsets();

  const handleOpenUploadModal = (
    type: "selfie" | "front" | "back" | "address"
  ) => {
    setImageType(type);
    setUploadModalVisible(true);
  };

  const sections = [
    {
      key: "header",
      render: () => (
        <Header
          showVerificationModal={() => setVerificationModalVisible(true)}
        />
      ),
    },
    {
      key: "avatar",
      render: () => (
        <View className="mb-4">
          <Avatar
            onPress={() => console.info("Avatar pressed")}
            onButtonPress={() => handleOpenUploadModal("selfie")}
          />
        </View>
      ),
    },
    {
      key: "uploadButtons",
      render: () => (
        <UploadButtons
          customerProfile={customerProfile}
          onOpenUploadModal={handleOpenUploadModal}
        />
      ),
    },
    {
      key: "userProfile",
      render: () => <UserProfile user={user} />,
    },
    {
      key: "customerDetails",
      render: () => (
        <CustomerProfileDetails customerProfile={customerProfile} />
      ),
    },
  ];

  return (
    <SafeAreaView className="flex-1 bg-gray-100 dark:bg-gray-900">
      <FlatList
        data={sections}
        renderItem={({ item }) => item.render()}
        keyExtractor={(item) => item.key}
        contentContainerStyle={{
          paddingTop: insets.top + -5,
          paddingBottom: insets.bottom + 30,
          paddingHorizontal: 20,
        }}
        showsVerticalScrollIndicator={false}
      />

      {/* Modals rendered outside FlatList */}
      <UploadModal
        modalVisible={uploadModalVisible}
        onBackPress={() => setUploadModalVisible(false)}
        onCameraPress={() => uploadImage("camera")}
        onGalleryPress={() => uploadImage("gallery")}
        isLoading={uploadingImage}
        imageType={imageType}
      />

      <VerificationForm
        modalVisible={verificationModalVisible}
        setModalVisible={setVerificationModalVisible}
      />
    </SafeAreaView>
  );
}
