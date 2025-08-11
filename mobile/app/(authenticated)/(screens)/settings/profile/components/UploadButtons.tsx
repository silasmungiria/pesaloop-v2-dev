import React from "react";
import { TouchableOpacity, Text } from "react-native";

interface Props {
  customerProfile: any;
  onOpenUploadModal: (type: "selfie" | "front" | "back" | "address") => void;
}

export default function UploadButtons({
  customerProfile,
  onOpenUploadModal,
}: Props) {
  const uploadItems = [
    {
      label: "Upload Face Photo",
      type: "selfie",
      uploaded: customerProfile?.is_face_uploaded,
    },
    {
      label: "Upload ID Front Side Photo",
      type: "front",
      uploaded: customerProfile?.is_id_front_uploaded,
    },
    {
      label: "Upload ID Back Side Photo",
      type: "back",
      uploaded: customerProfile?.is_id_back_uploaded,
    },
    {
      label: "Upload Proof of Address Photo",
      type: "address",
      uploaded: customerProfile?.is_address_proof_image_uploaded,
    },
  ];

  return (
    <>
      {uploadItems.map((item, index) =>
        !item.uploaded ? (
          <TouchableOpacity
            key={index}
            onPress={() => onOpenUploadModal(item.type as any)}
            className="p-4 my-2 rounded-xl bg-red-400"
          >
            <Text className="text-white text-center font-semibold">
              {item.label}
            </Text>
          </TouchableOpacity>
        ) : null
      )}
    </>
  );
}
