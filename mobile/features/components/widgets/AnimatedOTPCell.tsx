import React, { useEffect, useRef } from "react";
import { Animated, TextStyle } from "react-native";
import { Cursor } from "react-native-confirmation-code-field";

interface RenderCellProps {
  index: number;
  symbol: string | undefined;
  isFocused: boolean;
  getCellOnLayoutHandler: (index: number) => (event: any) => void;
  scheme: "light" | "dark";
  CELL_COUNT: number;
}

interface AnimateCellProps {
  symbol: string | undefined;
  isFocused: boolean;
}

const CELL_SIZE = 40;
const FONT_SIZE = 24;
const MARGIN_H = 8;
const MARGIN_V = 12;

const AnimatedOTPCell: React.FC<RenderCellProps> = ({
  index,
  symbol,
  isFocused,
  getCellOnLayoutHandler,
  scheme,
  CELL_COUNT,
}) => {
  // One-time animated values per cell
  const animationColor = useRef(new Animated.Value(0)).current;
  const animationScale = useRef(new Animated.Value(1)).current;

  const animateCell = ({ symbol, isFocused }: AnimateCellProps) => {
    const hasValue = Boolean(symbol);

    Animated.parallel([
      Animated.timing(animationColor, {
        useNativeDriver: false,
        toValue: isFocused ? 1 : 0,
        duration: 250,
      }),
      Animated.spring(animationScale, {
        useNativeDriver: false,
        toValue: hasValue ? 0 : 1,
        friction: 7,
      }),
    ]).start();
  };

  useEffect(() => {
    animateCell({ symbol, isFocused });
  }, [symbol, isFocused]);

  // Derived animated interpolations
  const backgroundColor = Boolean(symbol)
    ? animationScale.interpolate({
        inputRange: [0, 1],
        outputRange: ["#FFFFFF", "#3B82F6"],
      })
    : animationColor.interpolate({
        inputRange: [0, 1],
        outputRange: [
          scheme === "dark" ? "#2D3748" : "#F9FAFB",
          scheme === "dark" ? "#F9FAFB" : "#D1D5DB",
        ],
      });

  const borderRadius = animationScale.interpolate({
    inputRange: [0, 1],
    outputRange: [70, 8],
  });

  const scaleTransform = animationScale.interpolate({
    inputRange: [0, 1],
    outputRange: [0.2, 1],
  });

  const animatedCellStyle: Animated.WithAnimatedValue<TextStyle> = {
    backgroundColor,
    borderRadius,
    transform: [{ scale: scaleTransform }],
    height: CELL_SIZE,
    width: CELL_SIZE,
    justifyContent: "center",
    alignItems: "center",
    marginHorizontal: MARGIN_H,
    marginVertical: MARGIN_V,
    textAlign: "center",
    fontSize: FONT_SIZE,
    borderWidth: 1,
    borderColor: scheme === "dark" ? "#4B5563" : "#D1D5DB",
  };

  return (
    <Animated.Text
      key={index}
      onLayout={getCellOnLayoutHandler(index)}
      style={animatedCellStyle}
    >
      {symbol || (isFocused && <Cursor />)}
    </Animated.Text>
  );
};

export default AnimatedOTPCell;
