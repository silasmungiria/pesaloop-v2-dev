// DeviceDetailsContext.tsx
import React, { createContext, ReactNode, useContext, useMemo } from "react";
import { useDeviceDetails } from "@/features/hooks";
import { DeviceContextProps } from "@/types";

const DeviceDetailsContext = createContext<DeviceContextProps | undefined>(
  undefined
);

export const DeviceDetailsProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const deviceDetails = useDeviceDetails();

  const value = useMemo(() => ({ deviceDetails }), [deviceDetails]);

  return (
    <DeviceDetailsContext.Provider value={value}>
      {children}
    </DeviceDetailsContext.Provider>
  );
};

export const useDeviceContext = (): DeviceContextProps => {
  const context = useContext(DeviceDetailsContext);
  if (!context) {
    throw new Error(
      "useDeviceContext must be used within a DeviceDetailsProvider"
    );
  }
  return context;
};
