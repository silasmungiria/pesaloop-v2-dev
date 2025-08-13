import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { AppState, AppStateStatus } from "react-native";
import { useLogoutCleanup } from "@/features/store";
import {
  SessionAppStateContextProps,
  SessionAppStateProviderProps,
} from "@/types";

// Create the context with an initial undefined value
const SessionAppStateContext = createContext<
  SessionAppStateContextProps | undefined
>(undefined);

export const SessionAppStateProvider: React.FC<
  SessionAppStateProviderProps
> = ({ children }) => {
  const [appState, setAppState] = useState<AppStateStatus>(
    AppState.currentState
  );
  const { performSessionLogout } = useLogoutCleanup();

  // State to track if backgrounding is considered safe
  const [isBackgroundSafe, setBackgroundSafe] = useState(false);

  useEffect(() => {
    const handleAppStateChange = async (nextAppState: AppStateStatus) => {
      if (
        appState === "active" &&
        nextAppState === "background" &&
        !isBackgroundSafe
      ) {
        console.info(
          "App moving to background unsafely. Logging out session..."
        );
        await performSessionLogout();
      }
      setAppState(nextAppState);
    };

    const subscription = AppState.addEventListener(
      "change",
      handleAppStateChange
    );

    return () => {
      subscription.remove();
    };
  }, [appState, isBackgroundSafe, performSessionLogout]);

  return (
    <SessionAppStateContext.Provider
      value={{
        appState,
        isBackgroundSafe,
        setBackgroundSafe,
      }}
    >
      {children}
    </SessionAppStateContext.Provider>
  );
};

// Create a custom hook to use the SessionAppStateContext
export const useSessionAppState = (): SessionAppStateContextProps => {
  const context = useContext(SessionAppStateContext);
  if (!context) {
    throw new Error(
      "useSessionAppState must be used within an SessionAppStateProvider"
    );
  }
  return context;
};
