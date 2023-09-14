import {createAsyncThunk, createSlice, createSelector} from "@reduxjs/toolkit";

import {getImages, postImage as apiPostImage} from "../../api";
import {notifyError, notifySuccess} from "../../components/toastNotifications";

export const fetchImages = createAsyncThunk("images/fetchImages", async () => {
    const response = await getImages();
    return response;
});

export const postImage = createAsyncThunk("iamges/postImage", async (body) => {
    try {
        const response = await apiPostImage(body);

        notifySuccess("OK")

        return response;
    } catch (error) {
        notifyError("ERROR");
    }
})

export const imagesSlice = createSlice({
    name: 'images',
    initialState: {},
    reducers: {},
    extraReducers: builder => {
        builder
            .addCase(fetchImages.fulfilled, (state, action) => {
                action.payload.forEach(item => {
                    state[item.id] = item
                });
            })
            .addCase(postImage.fulfilled, (state, action) => {
                state[action.payload.id] = action.payload
            })

    }
});

const selectImages = state => state.images;

export const memoizedImagesSelector = createSelector(
    [selectImages],
    images => Object.values(images)
);

export default imagesSlice.reducer