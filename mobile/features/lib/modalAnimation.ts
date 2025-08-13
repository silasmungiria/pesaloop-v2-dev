// modalAnimationUtils.ts

import { useEffect } from "react";
import {
  useSharedValue,
  withSpring,
  withTiming,
  useAnimatedStyle,
} from "react-native-reanimated";

export const useModalAnimation = (visible: boolean) => {
  const modalTranslateY = useSharedValue(200);
  const modalOpacity = useSharedValue(0);

  useEffect(() => {
    if (visible) {
      modalTranslateY.value = withSpring(0);
      modalOpacity.value = withTiming(1);
    } else {
      modalTranslateY.value = withTiming(25, { duration: 100 });
      modalOpacity.value = withTiming(0);
    }
  }, [visible]);

  const modalAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ translateY: modalTranslateY.value }],
      opacity: modalOpacity.value,
    };
  });

  return {
    modalAnimatedStyle,
  };
};
