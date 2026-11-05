import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface AppState {
  currentView: "thumbs" | "image" | "slideshow";
  imgId: number;
  slideShowDirId: number;
}

const initialState: AppState = {
  currentView: "thumbs",
  imgId: 0,
  slideShowDirId: 0,
};

export const AppStore = createSlice({
  name: "app",
  initialState,
  reducers: {
    ShowThumbsView: (state) => {
      state.currentView = "thumbs";
      state.imgId = 0;
    },
    ShowImageView: (state, action: PayloadAction<number>) => {
      state.currentView = "image";
      state.imgId = action.payload;
    },
    ShowSlideshowView: (state, action: PayloadAction<number>) => {
      state.currentView = "slideshow";
      state.slideShowDirId = action.payload;
    },
    SetImgId: (state, action: PayloadAction<number>) => {
      state.imgId = action.payload;
    },
  },
});

export const { ShowImageView, ShowThumbsView, ShowSlideshowView, SetImgId } =
  AppStore.actions;

export default AppStore.reducer;
