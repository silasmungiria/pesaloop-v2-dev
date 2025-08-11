import {
  useUserStore,
  useSessionStore,
  useBalanceStore,
  useFrequentContactsStore,
} from "@/features/store";
import { revokeAuthToken } from "@/features/api";

export const useLogoutCleanup = () => {
  const { clearFrequentContacts } = useFrequentContactsStore();
  const { resetBalanceState } = useBalanceStore();
  const { clearSessionState, refreshToken } = useSessionStore();
  const { clearUserState } = useUserStore();

  const performFullLogout = async () => {
    await clearFrequentContacts();
    await resetBalanceState();
    await clearSessionState();
    await clearUserState();
    if (refreshToken) {
      await revokeAuthToken(refreshToken);
    }

    console.info("Logout cleanup completed successfully.");
  };

  const performSessionLogout = async () => {
    await clearSessionState();
    if (refreshToken) {
      await revokeAuthToken(refreshToken);
    }

    console.info("Session logout completed.");
  };
  return { performFullLogout, performSessionLogout };
};
