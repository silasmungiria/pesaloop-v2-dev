export interface VerifyRecipientResponse {
  email: string;
  first_name: string;
  id: string;
  last_name: string;
  phone_number: string;
}

export interface BaseModalProps {
  visible: boolean;
  onClose: () => void;
  launchedFromSettings?: boolean;
}

export interface RecipientModalProps extends BaseModalProps {
  setRequestedUser: (data: VerifyRecipientResponse) => void;
  setAmountModalVisible: (value: boolean) => void;
}

export interface AmountModalProps extends BaseModalProps {
  setAmount: (value: string) => void;
  setRecipientModalVisible: (value: boolean) => void;
  exceedUserBalance?: boolean;
  setRequestedUser?: (data: VerifyRecipientResponse) => void;
}

export interface ActionModalProps extends BaseModalProps {
  onActionSelect: (route: string) => void;
}

export interface ActionItemProps {
  label: string;
  route: string;
  icon: string;
  iconColor: string;
}
