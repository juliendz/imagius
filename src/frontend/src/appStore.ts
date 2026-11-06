import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { getLibrary, addRecentDir } from "./thunk";
import {
  Library,
  RecentDirListItem,
} from "../bindings/julien/imagius-go/internal";

export interface AppState {
  currentView: "thumbs" | "image" | "slideshow";
  imgId: number;
  slideShowDirId: number;
  slideshowStartIdx: number;
  currDirIndex: number;
  triggerScroll: number;
  library: Library;
}

const initialState: AppState = {
  currentView: "thumbs",
  imgId: 0,
  slideShowDirId: 0,
  slideshowStartIdx: 0,
  currDirIndex: 0,
  triggerScroll: 0,
  library: {} as Library,
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
  extraReducers: (builder) => {
    builder
      .addCase(
        getLibrary.fulfilled,
        (state, action: PayloadAction<Library>) => {
          console.log("getLibrary.fulfilled", action);
          state.library = action.payload;
        },
      )
      .addCase(addRecentDir.fulfilled, (state, action) => {
        console.log("addRecentDir.fulfilled", action);
        if (state.library.Dirs) {
          const dir = state.library.Dirs[action.payload.dirIndex];

          //Remove if its already exists in the recent list
          const existingIndex =
            state.library.Recent?.findIndex((r) => r?.DirID === dir?.ID) ?? -1;
          console.log("Existing recent index:", existingIndex);
          if (existingIndex !== -1) {
            state.library.Recent?.splice(existingIndex, 1);
          }

          if (state.library.Recent) {
            console.log(
              "Max recent dir ID:",
              ...state.library.Recent.map((r) => r!.ID),
            );
            const newRecentDir: RecentDirListItem = {
              ID:
                (state.library.Recent.length > 0
                  ? Math.max(...state.library.Recent.map((r) => r!.ID))
                  : 0) + 1,
              DirID: dir?.ID!,
              Name: dir?.Name!,
              ThumbViewIndex: dir?.ThumbViewIndex!,
            };
            console.log("Adding new recent dir:", newRecentDir);
            state.library.Recent?.unshift(newRecentDir);
          }
        }
      });
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
