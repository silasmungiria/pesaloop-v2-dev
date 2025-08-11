import React, { useMemo } from "react";
import { ExternalServicesScreen, PaymentMethod } from "@/features/components";

import {
  MpesaComponent,
  TCashComponent,
  BankTransferComponent,
} from "./components";

export default function RequestsExternalServices() {
  const paymentMethods: PaymentMethod[] = useMemo(
    () => [
      {
        name: "M-Pesa",
        icon: "phone-portrait-outline",
        color: "#0F9D58",
        Component: MpesaComponent,
      },
      // {
      //   name: "AirTel Money",
      //   icon: "phone-portrait-outline",
      //   color: "#E30B5C",
      //   Component: AirTelMoneyComponent,
      // },
      {
        name: "Bank Account",
        icon: "cash-outline",
        color: "#2C3E50",
        Component: BankTransferComponent,
      },
      // {
      //   name: "Card Payment",
      //   icon: "card-outline",
      //   color: "#1A1F71",
      //   Component: CardPaymentComponent,
      // },
      {
        name: "T-Cash",
        icon: "phone-portrait-outline",
        color: "#005B96",
        Component: TCashComponent,
      },
    ],
    []
  );

  return <ExternalServicesScreen paymentMethods={paymentMethods} />;
}
