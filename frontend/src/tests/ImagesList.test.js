import {screen, waitFor} from "@testing-library/react";

import ImagesList from "../components/ImagesList";
import {renderWithProviders} from "./testUtils";

test('Images list appears after API call', async () => {
    const result = renderWithProviders(<ImagesList/>);

    expect(screen.getByText(/^No images uploaded. Start by uploading a .png image$/)).toBeInTheDocument();

    await waitFor(() => screen.getAllByText('SUCCESS'));

    expect(screen.queryByText(/^No images uploaded. Start by uploading a .png image$/)).toBeNull();
    expect(result.container.querySelector("#images-list")).toBeInTheDocument();
});