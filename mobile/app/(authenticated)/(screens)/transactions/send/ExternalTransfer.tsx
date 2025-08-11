import React, { useMemo } from "react";

import { ExternalServicesScreen, PaymentMethod } from "@/features/components";
import {
  MpesaComponent,
  AirtelMoneyComponent,
  TCashComponent,
  BuyAirtimeComponent,
  BankTransferComponent,
  PaymentCardsComponent,
} from "./components";

export default function SendExternalServices() {
  const paymentMethods: PaymentMethod[] = useMemo(
    () => [
      {
        name: "M-Pesa",
        icon: "phone-portrait-outline",
        color: "#0F9D58",
        Component: MpesaComponent,
      },
      {
        name: "Buy Airtime",
        icon: "cellular-outline",
        color: "#e67e22",
        Component: BuyAirtimeComponent,
      },
      {
        name: "Bank Account",
        icon: "cash-outline",
        color: "#2C3E50",
        Component: BankTransferComponent,
      },
      {
        name: "Payment Cards",
        icon: "card-outline",
        color: "#1A1F71",
        Component: PaymentCardsComponent,
      },
      {
        name: "AirTel Money",
        icon: "phone-portrait-outline",
        color: "#E30B5C",
        Component: AirtelMoneyComponent,
      },
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
