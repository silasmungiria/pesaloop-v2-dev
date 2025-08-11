// DeviceDetailsContext.tsx
import React, { createContext, useContext, ReactNode, useMemo } from "react";
import { DeviceDetails, useDeviceDetails } from "@/features/hooks";

interface DeviceDetailsContextProps {
  deviceDetails: DeviceDetails;
}

const DeviceDetailsContext = createContext<
  DeviceDetailsContextProps | undefined
>(undefined);

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

export const useDeviceContext = (): DeviceDetailsContextProps => {
  const context = useContext(DeviceDetailsContext);
  if (!context) {
    throw new Error(
      "useDeviceContext must be used within a DeviceDetailsProvider"
    );
  }
  return context;
};
