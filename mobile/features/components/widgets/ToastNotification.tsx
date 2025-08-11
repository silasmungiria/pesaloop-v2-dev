import React, { useEffect } from "react";
import {
  View,
  Text,
  Animated,
  TouchableOpacity,
  Easing,
  Platform,
} from "react-native";

interface NotificationProps {
  message: string;
  visible: boolean;
  onDismiss: () => void;
  duration?: number;
  type?: "error" | "success" | "info" | "warning";
}

// Adjust this value to change the top margin
const TOP_MARGIN = Platform.select({
  ios: 30, // More space for iOS notch
  android: 25, // Less space needed for Android
  default: 30, // Default for other platforms
});

const ToastNotification: React.FC<NotificationProps> = ({
  message,
  visible,
  onDismiss,
  duration = 10000,
  type = "success",
}) => {
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const slideAnim = React.useRef(new Animated.Value(-100 - TOP_MARGIN)).current;

  useEffect(() => {
    if (!visible || !message) return;

    // Animation in
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: TOP_MARGIN, // Animate to the margin position
        duration: 300,
        easing: Easing.out(Easing.quad),
        useNativeDriver: true,
      }),
    ]).start();

    const timer = setTimeout(() => {
      handleDismiss();
    }, duration);

    return () => clearTimeout(timer);
  }, [visible, message]);

  const handleDismiss = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: -100 - TOP_MARGIN,
        duration: 200,
        easing: Easing.in(Easing.quad),
        useNativeDriver: true,
      }),
    ]).start(() => {
      onDismiss();
    });
  };

  if (!visible || !message) return null;

  const getStyles = () => {
    const base = "mx-4 p-4 rounded-lg flex-row items-start justify-between";
    switch (type) {
      case "error":
        return `${base} bg-red-50 border-l-4 border-red-500`;
      case "success":
        return `${base} bg-green-50 border-l-4 border-green-500`;
      case "warning":
        return `${base} bg-amber-50 border-l-4 border-amber-500`;
      case "info":
        return `${base} bg-blue-50 border-l-4 border-blue-500`;
      default:
        return `${base} bg-gray-50 border-l-4 border-gray-500`;
    }
  };

  const getTextColor = () => {
    switch (type) {
      case "error":
        return "text-red-800";
      case "success":
        return "text-green-800";
      case "warning":
        return "text-amber-800";
      case "info":
        return "text-blue-800";
      default:
        return "text-gray-800";
    }
  };

  const getIcon = () => {
    switch (type) {
      case "error":
        return "❌";
      case "success":
        return "✅";
      case "warning":
        return "⚠️";
      case "info":
        return "ℹ️";
      default:
        return "";
    }
  };

  return (
    <Animated.View
      style={{
        opacity: fadeAnim,
        transform: [{ translateY: slideAnim }],
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 999,
        marginTop: TOP_MARGIN,
      }}
    >
      <View className={getStyles()}>
        <View className="flex-1 flex-row items-start">
          <Text className={`text-xl mr-2 ${getTextColor()}`}>{getIcon()}</Text>
          <View className="flex-1">
            <Text className={`text-lg font-bold mb-1 ${getTextColor()}`}>
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </Text>
            <Text className={`text-base ${getTextColor()}`}>{message}</Text>
          </View>
        </View>
        <TouchableOpacity
          onPress={handleDismiss}
          className="ml-2 p-1"
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
        >
          <Text className={`text-lg ${getTextColor()}`}>✕</Text>
        </TouchableOpacity>
      </View>
    </Animated.View>
  );
};

export default ToastNotification;
