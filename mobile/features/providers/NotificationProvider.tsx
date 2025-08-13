import React, { createContext, useContext, useState } from "react";
import { ToastNotification } from "@/features/components";
import { NotificationProps, NotificationType } from "@/types";

const NotificationContext = createContext<NotificationProps | undefined>(
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
        visible={notification.visible}
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
