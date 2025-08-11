import React, { useEffect, useState } from "react";
import { View, TouchableOpacity, Image } from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { useUserStore } from "@/features/store";
import Animated, {
  FadeInDown,
  FadeOutUp,
  Layout,
} from "react-native-reanimated";

const placeholderImage =
  "https://avatar.iran.liara.run/public/boy?username=Ash";

type AvatarProps = {
  uri?: string;
  aviOnly?: boolean;
  onPress?: () => void;
  onButtonPress?: () => void;
  props?: any;
};

export default function Avatar({
  uri,
  aviOnly = false,
  onPress,
  onButtonPress,
  ...props
}: AvatarProps) {
  const { customerProfile } = useUserStore();
  const [cachedFaceImageUrl, setCachedFaceImageUrl] =
    useState(placeholderImage);

  useEffect(() => {
    if (customerProfile && customerProfile?.selfie_image_url) {
      setCachedFaceImageUrl(customerProfile?.selfie_image_url);
    }
  }, [customerProfile]);

  return (
    <Animated.View
      entering={FadeInDown.delay(200).springify()}
      exiting={FadeOutUp.springify()}
      layout={Layout.springify()}
      className={`items-center relative ${aviOnly ? "mb-0" : "mb-4"}`}
      {...props}
    >
      <TouchableOpacity
        activeOpacity={0.8}
        onPress={onPress}
        className="relative"
      >
        <Image
          source={{
            uri: `${
              uri || cachedFaceImageUrl
            }?timestamp=${new Date().getTime()}`,
            cache: "reload",
          }}
          className={`rounded-full border-4 border-yellow-400 ${
            aviOnly ? "h-9 w-9" : "h-36 w-36"
          }`}
          onError={() =>
            console.error(
              "Failed to load face image:",
              uri || cachedFaceImageUrl
            )
          }
        />
        {!aviOnly && onButtonPress && (
          <TouchableOpacity
            activeOpacity={0.8}
            className="absolute bottom-1 right-1 p-2 rounded-full bg-gray-100 dark:bg-gray-900"
            onPress={onButtonPress}
          >
            <Ionicons name="camera-outline" size={20} color="#FACC15" />
          </TouchableOpacity>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
}
