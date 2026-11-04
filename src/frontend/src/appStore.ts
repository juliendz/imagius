import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface AppState {
  showThumbView: boolean;
  showImageView: boolean;
  imgId: number;
}

const initialState: AppState = {
  showThumbView: true,
  showImageView: false,
  imgId: 0,
};

export const AppStore = createSlice({
  name: "app",
  initialState,
  reducers: {
    ShowThumbsView: (state) => {
      state.showThumbView = true;
      state.showImageView = false;
      state.imgId = 0;
    },
    ShowImageView: (state, action: PayloadAction<number>) => {
      state.showThumbView = false;
      state.showImageView = true;
      state.imgId = action.payload;
    },
    SetImgId: (state, action: PayloadAction<number>) => {
      state.imgId = action.payload;
    },
  },
});

export const { ShowImageView, ShowThumbsView, SetImgId } = AppStore.actions;

export default AppStore.reducer;
