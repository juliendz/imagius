import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface AppState {
  currentView: "thumbs" | "image" | "slideshow";
  imgId: number;
  slideShowDirId: number;
  slideshowStartIdx: number;
  currDirIndex: number;
  triggerScroll: number;
}

const initialState: AppState = {
  currentView: "thumbs",
  imgId: 0,
  slideShowDirId: 0,
  slideshowStartIdx: 0,
  currDirIndex: 0,
  triggerScroll: 0,
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
    ShowSlideshowView: (
      state,
      action: PayloadAction<{ dirId: number; startIdx: number }>,
    ) => {
      state.currentView = "slideshow";
      state.slideShowDirId = action.payload.dirId;
      state.slideshowStartIdx = action.payload.startIdx;
    },
    ScrollToDir: (state, action: PayloadAction<number>) => {
      state.currDirIndex = action.payload;
      state.triggerScroll += 1;
    },
    SetImgId: (state, action: PayloadAction<number>) => {
      state.imgId = action.payload;
    },
  },
});

export const {
  ShowImageView,
  ShowThumbsView,
  ShowSlideshowView,
  SetImgId,
  ScrollToDir,
} = AppStore.actions;

export default AppStore.reducer;
