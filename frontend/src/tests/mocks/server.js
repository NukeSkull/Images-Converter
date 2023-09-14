import {setupServer} from "msw/node";
import {rest} from "msw";

import globals from "../../globals";

const data = globals.TEST_DATA;

const handlers = [
    rest.get(globals.IMAGES_API, (req, res, ctx) => {
        return res(ctx.json(data));
    }),
    rest.get(`${globals.DOWNLOAD_API}:imageId/`, (req, res, ctx) => {
        return res(
            ctx.set("Content-Disposition", 'attachment: filename="test.jpg"'),
            ctx.text("This is a test image data")
        );
    })
];

export const server = setupServer(...handlers);