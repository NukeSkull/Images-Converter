import {configureStore} from "@reduxjs/toolkit";

import imagesReducer from "../features/images/imagesSlice"

export default configureStore({
    reducer: {
        images: imagesReducer,
    },
});