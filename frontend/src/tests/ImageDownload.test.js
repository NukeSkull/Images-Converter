import {render, screen} from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import ImageDownload from "../components/ImageDownload";

import globals from "../globals"

test('Click download button triggers download request', async () => {
    render(<ImageDownload imageId={1} imageName="test.png" status="SUCCESS"/>);
    const user = userEvent.setup();

    const downloadButton = screen.getByRole("button", {name: "Download"});
    expect(downloadButton).toBeInTheDocument();
    expect(downloadButton).toBeEnabled();
    expect(downloadButton.href).toStrictEqual(`http://localhost:8000${globals.DOWNLOAD_API}1/`);
});
