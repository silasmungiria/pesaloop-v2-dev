# 📱 PesaLoop Mobile App

## Overview

**PesaLoop Mobile** is a React Native application built with **Expo** that provides seamless access to PesaLoop’s financial services — including digital wallets, payments, forex, credit, biometric-secure authentication, and more.

It integrates directly with the **PesaLoop Django REST API backend** and is designed for speed, security, and intuitive user experience.

---

## 📦 Tech Stack

- **React Native (Expo SDK 53)**
- **Expo Router**
- **TypeScript**
- **Tailwind CSS (NativeWind)**
- **React Query**
- **Expo SecureStore**
- **Expo Notifications**
- **Custom Axios-based API Service Layer**
- **Django REST API Backend**

---

## 📁 Project Structure

```
.
├── app/                                # Main app routes and screens
│   ├── (authenticated)/               # Screens accessible after login
│   │   ├── (tabs)/                    # Bottom tab routes (home, wallets, actions)
│   │   │   ├── actions/
│   │   │   │   └── index.tsx
│   │   │   ├── home/
│   │   │   │   └── index.tsx
│   │   │   ├── wallets/
│   │   │   │   └── index.tsx
│   │   │   └── _layout.tsx            # Tabs navigation config
│   │   │
│   │   ├── (screens)/                 # Stack-based screens
│   │   │   ├── activity-center/
│   │   │   ├── credits/
│   │   │   ├── notifications/
│   │   │   ├── qr-codes/
│   │   │   ├── settings/
│   │   │   └── transactions/
│   │   │
│   │   ├── lock/
│   │   │   └── index.tsx              # App lock/biometric screen
│   │   └── _layout.tsx                # Authenticated stack layout config
│
│   ├── (public)/                      # Public, unauthenticated screens
│   │   ├── auth/                      # Authentication flows
│   │   │   ├── forgot-password/
│   │   │   │   └── index.tsx
│   │   │   ├── login/
│   │   │   │   ├── index.tsx
│   │   │   │   └── password.tsx
│   │   │   ├── signup/
│   │   │   │   ├── index.tsx
│   │   │   │   └── password.tsx
│   │   │   └── verify/
│   │   │       └── otp.tsx
│   │   └── help/
│   │       └── index.tsx
│
│   ├── layout/
│   │   └── AppNavigator.tsx           # Root navigation container and stack/tab setup
│
│   ├── index.tsx                      # Initial splash or welcome screen
│   └── _layout.tsx                    # Root navigation layout config
│
├── assets/                            # Fonts, images, icons, media
│
├── features/                          # Shared logic and app-wide resources
│   ├── api/                           # API client config and endpoints
│   ├── components/                    # Shared reusable components
│   ├── constants/                     # Centralized constants (colors, config, routes)
│   ├── hooks/                         # Custom React/React Native hooks
│   ├── lib/                           # Common utilities and libraries
│   ├── providers/                     # Global context providers
│   ├── store/                         # Zustand stores for global state
│   └── utils/                         # Utility functions/helpers
│
├── types/                             # TypeScript type definitions
│
├── android/                           # Android native project (EAS builds)
├── .expo/                             # Expo runtime and metadata
├── node_modules/                      # Project dependencies
│
├── app.json                           # Expo project configuration
├── babel.config.js                    # Babel configuration
├── expo-env.d.ts                      # Expo environment types
├── global.css                         # Global styling (if any)
├── metro.config.js                    # Metro bundler configuration
├── nativewind-env.d.ts                # NativeWind environment config
├── package.json                       # Project dependencies and scripts
├── tailwind.config.js                 # Tailwind + NativeWind config
├── tsconfig.json                      # TypeScript configuration
├── yarn.lock                          # Yarn lockfile for dependency consistency
├── todo.md                            # Project task list/notes
└── README.md                          # Project documentation (this file)
```

---

## ⚙️ Getting Started

### 1️⃣ Prerequisites

- **Node.js** (v18+ recommended)
- **Yarn** or **npm**
- **Expo Go** (install from App Store / Play Store)

Install Expo CLI tools (on-demand via `npx` — no need for global install):

```bash
npm install --global expo-cli  # (optional, legacy)
```

---

### 2️⃣ Install Dependencies

In the `mobile/` directory:

```bash
yarn install
# or
npm install
```

---

### 3️⃣ Run the App (Expo Go Development Mode)

Start the Metro bundler:

```bash
yarn start --clear
```

OR

```bash
npx expo start --clear
```

- Scan the QR code in your terminal or Expo DevTools using **Expo Go**
- The app will live reload as you make changes

---

## 🔐 Environment Configuration

Create an `.env` file (or use `expo-constants` config) for sensitive environment values:

**Example:**

```
API_BASE_URL=https://api.pesaloop.com
APP_NAME=PesaLoop
```

Access these using `expo-constants` in your app code.

---

## 🛠️ Notable Features

- **Expo Router navigation** with stack and tab layouts
- **React Query** for API state management
- **SplashScreen management** via `expo-splash-screen`
- **Axios-based API client** with interceptors and token handling
- **Expo SecureStore** for secure session and biometric key storage
- **Push Notifications** support (development builds required from SDK 53)
- **Tailwind CSS (NativeWind)** for styling

---

## 📲 Development Build (for native modules / push notifications)

As of **Expo SDK 53**, some features like **push notifications** and **native modules** require a development build (Expo Go no longer supports these).

Create a development build:

```bash
eas build --profile development --platform android
# or
eas build --profile development --platform ios
```

Then install the `.apk` / `.ipa` manually on your device.

---

## 🧪 Running Tests

If configured:

```bash
yarn test
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](../LICENSE.md) file for details.

---

## 📄 Terms & Conditions

By using this app, you agree to the terms outlined in [TERMS & CONDITIONS](../TERMS.md).

---

## 📌 Notes

- Ensure your API backend is running before testing API-related features.
- Use `expo-splash-screen` carefully: Splash screen should hide only after fonts and session verification complete.
- Update Tailwind classes after config changes:

```bash
npx nativewind --update
```

- `expo-notifications` requires a development build to function properly on SDK 53+
- Session and biometric authentication states are managed using **Zustand stores**

---

## ✅ Roadmap

- [x] Biometric authentication integration
- [x] Push notification event handling
- [x] Forex exchange screen UX
- [ ] QR Code payment scanner
- [ ] P2P transfer workflows

---

## 🔍 Helpful Commands

| Action                          | Command                                              |
| :------------------------------ | :--------------------------------------------------- |
| Install dependencies            | `yarn install` or `npm install`                      |
| Check for necessary app updates | `npx expo install --check`                           |
| Start Metro bundler (Expo Go)   | `npx expo start --clean`                             |
| Run development build (Android) | `eas build --profile development --platform android` |
| Update Tailwind classes         | `npx nativewind --update`                            |

---
