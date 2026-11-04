import { configureStore } from "@reduxjs/toolkit";
import { AppStore } from "./appStore";

export const store = configureStore({
  reducer: {
    appStore: AppStore.reducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
