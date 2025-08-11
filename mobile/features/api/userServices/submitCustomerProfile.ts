import { apiRequest, setAuthorizationHeader } from "@/features/api/apiClient";
import { useSessionStore } from "@/features/store";
import { CustomerProfile } from "@/types";

interface CustomerData {
  id_type: string;
  id_number: string;
  country: string;
  region_state: string;
  city: string;
  postal_code: string;
  postal_address: string;
  residential_address: string;
  next_of_kin_name: string;
  next_of_kin_relationship: string;
  next_of_kin_contact: string;
}

interface CustomerProfileResponse {
  message: string;
  customerProfile: CustomerProfile;
}

export const submitCustomerProfile = async (data: CustomerData) => {
  const { accessToken } = useSessionStore.getState();
  setAuthorizationHeader(accessToken);
  return apiRequest<CustomerProfileResponse>(
    "post",
    "/users/customer/submit/",
    data
  );
};
