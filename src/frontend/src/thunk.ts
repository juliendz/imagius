import { createAsyncThunk } from "@reduxjs/toolkit";
import {
  Library,
  LibraryService,
} from "../bindings/julien/imagius-go/internal";

export const getLibrary = createAsyncThunk(
  "library/getLibrary",
  async (_thunkAPI): Promise<Library> => {
    try {
      let imgs = await LibraryService.GetLibrary();
      console.log(imgs);
      if (!imgs) {
        throw new Error("Failed to fetch library");
      }
      return imgs;
    } catch (ex) {
      console.debug(ex);
    }

    return {} as Library;
  },
);
