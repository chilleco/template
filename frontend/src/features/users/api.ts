import { useMutation } from "@tanstack/react-query";

import { useApiClient } from "@/lib/api";
import { useAppDispatch } from "@/lib/hooks";
import { setPreAuthToken } from "@/state/slices/sessionSlice";

export function useBootstrapSession() {
  const dispatch = useAppDispatch();
  const client = useApiClient();
  return useMutation({
    mutationFn: async () =>
      client.post<{ token: string; expires_at: string; data: Record<string, unknown> }>(
        "/api/v1/auth/session/bootstrap",
        {}
      ),
    onSuccess: (data) => {
      dispatch(setPreAuthToken(data.token));
    }
  });
}
