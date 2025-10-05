import { configureStore } from '@reduxjs/toolkit';

import sessionReducer from './sessionSlice';

export const makeStore = () =>
  configureStore({
    reducer: {
      session: sessionReducer
    }
  });

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore['getState']>;
export type AppDispatch = AppStore['dispatch'];
