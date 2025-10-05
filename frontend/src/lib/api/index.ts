import { ApiClient } from "@/lib/api/client";
import { useAppSelector } from "@/lib/hooks";

export function useApiClient() {
  const accessToken = useAppSelector((state) => state.session.accessToken);
  const preAuth = useAppSelector((state) => state.session.preAuthToken);
  return new ApiClient({
    getAccessToken: () => accessToken,
    getPreAuthToken: () => preAuth
  });
}
