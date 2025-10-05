import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

import type { SupportedLocale } from "@/lib/i18n";

interface SessionState {
  preAuthToken: string | null;
  accessToken: string | null;
  refreshToken: string | null;
  locale: SupportedLocale;
}

const initialState: SessionState = {
  preAuthToken: null,
  accessToken: null,
  refreshToken: null,
  locale: "en"
};

const sessionSlice = createSlice({
  name: "session",
  initialState,
  reducers: {
    setPreAuthToken(state, action: PayloadAction<string | null>) {
      state.preAuthToken = action.payload;
    },
    setTokens(state, action: PayloadAction<{ access: string; refresh: string } | null>) {
      if (!action.payload) {
        state.accessToken = null;
        state.refreshToken = null;
        return;
      }
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;
    },
    setLocale(state, action: PayloadAction<SupportedLocale>) {
      state.locale = action.payload;
    }
  }
});

export const { setPreAuthToken, setTokens, setLocale } = sessionSlice.actions;
export default sessionSlice.reducer;
