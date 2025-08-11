interface CreditItem {
  title: string;
  description: string;
  date: string;
  status: "outstanding" | "cleared";
  amount: number;
  interest?: number;
  type: "disbursement" | "repayment";
  currency: string;
}

export const creditHistory: CreditItem[] = [
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2024-05-10T08:30:00Z",
    status: "outstanding",
    amount: 20000,
    type: "disbursement",
    currency: "USD",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 25 days at 11.525% interest rate. Interest: KES 1,728.75",
    date: "2024-04-30T16:00:00Z",
    status: "cleared",
    amount: 16728.75,
    interest: 1728.75,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2024-04-05T09:00:00Z",
    status: "cleared",
    amount: 15000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 26 days at 11.986% interest rate. Interest: KES 1,198.60",
    date: "2024-03-31T16:00:00Z",
    status: "cleared",
    amount: 11198.6,
    interest: 1198.6,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2024-03-05T10:00:00Z",
    status: "cleared",
    amount: 10000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 30 days at 12.000% interest rate. Interest: KES 1,200.00",
    date: "2024-02-28T16:00:00Z",
    status: "cleared",
    amount: 11200,
    interest: 1200,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2024-02-10T08:45:00Z",
    status: "cleared",
    amount: 12000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 20 days at 10.000% interest rate. Interest: KES 800.00",
    date: "2024-01-31T16:00:00Z",
    status: "cleared",
    amount: 12800,
    interest: 800,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2024-01-05T09:00:00Z",
    status: "cleared",
    amount: 18000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 28 days at 11.500% interest rate. Interest: KES 2,070.00",
    date: "2023-12-31T16:00:00Z",
    status: "cleared",
    amount: 20070,
    interest: 2070,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2023-12-05T10:30:00Z",
    status: "cleared",
    amount: 9000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 24 days at 11.000% interest rate. Interest: KES 990.00",
    date: "2023-11-30T16:00:00Z",
    status: "cleared",
    amount: 9990,
    interest: 990,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2023-11-05T09:00:00Z",
    status: "cleared",
    amount: 11000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 27 days at 11.750% interest rate. Interest: KES 1,292.50",
    date: "2023-10-31T16:00:00Z",
    status: "cleared",
    amount: 12292.5,
    interest: 1292.5,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2023-10-05T10:00:00Z",
    status: "cleared",
    amount: 15000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 30 days at 12.000% interest rate. Interest: KES 1,800.00",
    date: "2023-09-30T16:00:00Z",
    status: "cleared",
    amount: 16800,
    interest: 1800,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2023-09-05T09:30:00Z",
    status: "cleared",
    amount: 14000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 29 days at 11.850% interest rate. Interest: KES 1,659.00",
    date: "2023-08-31T16:00:00Z",
    status: "cleared",
    amount: 15659,
    interest: 1659,
    type: "repayment",
    currency: "KES",
  },
  {
    title: "Credit Disbursed",
    description: "Funds disbursed to your wallet",
    date: "2023-08-05T09:00:00Z",
    status: "cleared",
    amount: 13000,
    type: "disbursement",
    currency: "KES",
  },
  {
    title: "Salary Deduction - Repayment",
    description:
      "Repayment for 22 days at 10.500% interest rate. Interest: KES 1,365.00",
    date: "2023-07-31T16:00:00Z",
    status: "cleared",
    amount: 14365,
    interest: 1365,
    type: "repayment",
    currency: "KES",
  },
];
