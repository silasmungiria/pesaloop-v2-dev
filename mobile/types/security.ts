export interface QRCodeProps {
  currentUserIdentifier: string;
  requestedUserIdentifier: string;
  requestedUserName: string;
  amount: number;
  currency: string;
  actionType: string;
  reason?: string;
}
