import React, { createContext, useContext, useState } from "react";
// import Notification from '../components/Notification';
import { ToastNotification } from "@/features/components";

type NotificationType = "error" | "success" | "info" | "warning";

interface NotificationContextType {
  showNotification: (
    message: string,
    type?: NotificationType,
    duration?: number
  ) => void;
  hideNotification: () => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(
  undefined
);

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [notification, setNotification] = useState({
    message: "",
    visible: false,
    type: "success" as NotificationType,
    duration: 5000,
  });

  const showNotification = (
    message: string,
    type: NotificationType = "success",
    duration: number = 5000
  ) => {
    setNotification({
      message,
      visible: true,
      type,
      duration,
    });
  };

  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, visible: false }));
  };

  return (
    <NotificationContext.Provider
      value={{ showNotification, hideNotification }}
    >
      {children}
      <ToastNotification
        message={notification.message}
        // visible={notification.visible}
        // Use default visibility for now.
        visible={true}
        onDismiss={hideNotification}
        type={notification.type}
        duration={notification.duration}
      />
    </NotificationContext.Provider>
  );
};

export const useNotificationToast = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error(
      "useNotificationToast must be used within a NotificationProvider"
    );
  }
  return context;
};
