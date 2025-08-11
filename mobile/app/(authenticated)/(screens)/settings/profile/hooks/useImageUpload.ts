import { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import * as mime from "react-native-mime-types";
import axios from "axios";
import * as Haptics from "expo-haptics";

import { BASE_URL } from "@/features/api/apiClient";
import { useSessionAppState, useNotificationToast } from "@/features/providers";
import { useUserStore, useSessionStore } from "@/features/store";
import { handleError } from "@/features/utils/handleError";

export function useImageUpload() {
  const { setBackgroundSafe } = useSessionAppState();
  const { accessToken } = useSessionStore();
  const { showNotification } = useNotificationToast();
  const { setCustomerProfile } = useUserStore();

  const [uploadingImage, setUploadingImage] = useState(false);
  const [imageType, setImageType] = useState<
    "selfie" | "front" | "back" | "address" | null
  >(null);

  const imageFieldMapping = {
    face: "selfie_image",
    front: "id_image_front",
    back: "id_image_back",
    address: "address_proof_image",
  };

  const uploadImage = async (mode: "gallery" | "camera") => {
    if (!imageType) return;

    setBackgroundSafe(true);
    try {
      const result = await (mode === "gallery"
        ? ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: imageType === "selfie" ? [1, 1] : [4, 3],
            quality: 1,
          })
        : ImagePicker.launchCameraAsync({
            cameraType: ImagePicker.CameraType.front,
            allowsEditing: true,
            aspect: imageType === "selfie" ? [1, 1] : [4, 3],
            quality: 1,
          }));

      if (!result.canceled && result.assets?.length) {
        await sendToBackend(result.assets[0].uri);
      }
    } catch (error) {
      console.error("Image capture error", error);
    } finally {
      setBackgroundSafe(false);
    }
  };

  const sendToBackend = async (fileUri: string) => {
    const formData = new FormData();
    const fileType = mime.lookup(fileUri) || "image/jpeg";
    const fileName = fileUri.split("/").pop() || "upload.jpg";
    const fieldName = imageFieldMapping[imageType!];

    formData.append(fieldName, {
      uri: fileUri,
      type: fileType,
      name: fileName,
    } as any);
    setUploadingImage(true);

    try {
      const res = await axios.put(
        `${BASE_URL}/users/customer/upload/${imageType}/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      setCustomerProfile(res.data.customerProfile);

      const message = res.data.message || "Image uploaded successfully.";
      showNotification(message, "success", 6000);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (error: any) {
      handleError(error, "Image upload failed. Please try again later.");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setUploadingImage(false);
    }
  };

  return {
    imageType,
    setImageType,
    uploadingImage,
    uploadImage,
  };
}
