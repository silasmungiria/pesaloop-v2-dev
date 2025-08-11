import "dotenv/config";

export default {
  expo: {
    name: process.env.APP_NAME || "pesaloop",
    slug: "pesaloop",
    version: process.env.APP_VERSION || "0.1",
    orientation: "portrait",
    icon: "./assets/images/icon.png",
    scheme: "myapp",
    userInterfaceStyle: "automatic",
    newArchEnabled: true,
    androidStatusBar: {
      translucent: true,
      backgroundColor: "00000000",
      barStyle: "light-content",
    },
    splash: {
      resizeMode: "contain",
      backgroundColor: "#F3F4F6",
      image: "./assets/images/splash-icon.png",
      dark: {
        backgroundColor: "#111827",
        image: "./assets/images/splash-icon.png",
      },
      imageWidth: 200,
    },
    ios: {
      supportsTablet: true,
      infoPlist: {
        NSFaceIDUsageDescription:
          "This app uses Face ID to authenticate the user.",
      },
      bundleIdentifier: process.env.BUNDLE_ID || "com.pesaloop.app",
      config: {
        usesNonExemptEncryption: false,
      },
    },
    android: {
      edgeToEdgeEnabled: true,
      adaptiveIcon: {
        foregroundImage: "./assets/images/adaptive-icon.png",
        backgroundColor: "#ffffff",
      },
      package: process.env.PACKAGE_ID || "com.pesaloop.app",
      permissions: [
        "android.permission.READ_CONTACTS",
        "android.permission.WRITE_CONTACTS",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.USE_BIOMETRIC",
        "android.permission.USE_FINGERPRINT",
      ],
    },
    web: {
      bundler: "metro",
      output: "static",
      favicon: "./assets/images/favicon.png",
    },
    plugins: [
      "expo-router",
      "expo-asset",
      "expo-font",
      [
        "expo-contacts",
        {
          contactsPermission: "Allow $(PRODUCT_NAME) to access your contacts.",
        },
      ],
      [
        "expo-location",
        {
          locationAlwaysAndWhenInUsePermission:
            "Allow $(PRODUCT_NAME) to use your location. Is that okay?",
        },
      ],
      [
        "expo-local-authentication",
        {
          faceIDPermission: "Allow $(PRODUCT_NAME) to use Face ID.",
        },
      ],
      [
        "expo-notifications",
        {
          sounds: ["./assets/sounds/popup.m4a"],
        },
      ],
      [
        "expo-camera",
        {
          cameraPermission: "Allow $(PRODUCT_NAME) to access your camera",
          microphonePermission:
            "Allow $(PRODUCT_NAME) to access your microphone",
          recordAudioAndroid: true,
        },
      ],
      [
        "expo-secure-store",
        {
          configureAndroidBackup: true,
          faceIDPermission:
            "Allow $(PRODUCT_NAME) to access your Face ID biometric data.",
        },
      ],
    ],
    experiments: {
      typedRoutes: true,
    },
    assetBundlePatterns: ["**/*"],
  },
};
