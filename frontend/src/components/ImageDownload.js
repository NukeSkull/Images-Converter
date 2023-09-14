import React from "react";
import {Button} from "react-bootstrap"

import globals from "./../globals"

function ImageDownload({imageId, imageName, status}) {
    return (
        <Button type="button"
                href={`${globals.SERVER}${globals.DOWNLOAD_API}${imageId}/`}
                disabled={status !== "SUCCESS"}>
            Download
        </Button>
    );
}

export default ImageDownload;