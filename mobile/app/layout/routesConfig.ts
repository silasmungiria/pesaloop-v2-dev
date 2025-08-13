// routesConfig.ts
import { router } from "expo-router";

export const routes = [
  {
    name: "(public)/auth/signup/index",
    headerShown: true,
    headerLeft: () => getHeaderLeft(() => router.replace("/")),
    headerRight: getHelpIcon,
  },
  {
    name: "(public)/auth/signup/password",
    headerShown: true,
    headerLeft: () => getHeaderLeft(() => router.back()),
    headerRight: getHelpIcon,
  },
  {
    name: "(public)/auth/verify/otp",
    headerShown: true,
    headerLeft: () => getHeaderLeft(() => router.back()),
  },
  {
    name: "(public)/auth/login/index",
    headerShown: true,
    headerLeft: () => getHeaderLeft(() => router.replace("/")),
    headerRight: getHelpIcon,
  },
  {
    name: "(public)/auth/login/password",
    headerShown: true,
    headerLeft: () => getHeaderLeft(() => router.back()),
    headerRight: getHelpIcon,
  },
  { name: "(public)/auth/forgot-password/index", presentation: "modal" },
  { name: "(public)/help/index", presentation: "modal" },
  { name: "(authenticated)" },
];
