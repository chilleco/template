import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SessionState {
  accessToken: string | null;
  refreshToken: string | null;
  user: {
    id: number;
    email?: string | null;
    username?: string | null;
    locale?: string | null;
    role?: string;
  } | null;
}

const initialState: SessionState = {
  accessToken: null,
  refreshToken: null,
  user: null
};

const sessionSlice = createSlice({
  name: 'session',
  initialState,
  reducers: {
    hydrate(state, action: PayloadAction<Partial<SessionState>>) {
      return { ...state, ...action.payload };
    },
    setTokens(state, action: PayloadAction<{ accessToken: string; refreshToken: string }>) {
      state.accessToken = action.payload.accessToken;
      state.refreshToken = action.payload.refreshToken;
      if (typeof window !== 'undefined') {
        window.localStorage.setItem('accessToken', action.payload.accessToken);
        window.localStorage.setItem('refreshToken', action.payload.refreshToken);
      }
    },
    clearSession(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      if (typeof window !== 'undefined') {
        window.localStorage.removeItem('accessToken');
        window.localStorage.removeItem('refreshToken');
      }
    },
    setUser(state, action: PayloadAction<SessionState['user']>) {
      state.user = action.payload;
    }
  }
});

export const { hydrate, setTokens, clearSession, setUser } = sessionSlice.actions;
export default sessionSlice.reducer;

export const getSessionToken = () => {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('accessToken');
};
