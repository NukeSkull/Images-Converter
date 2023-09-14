import {act, fireEvent, render, screen} from "@testing-library/react";

import DropBox from '../components/DropBox'

test('dropbox renders correctly', () => {
    const result = render(<DropBox onDrop={() => null}
                                   resetSelectedFile={() => null}/>);

    const dropbox = result.container.querySelector("#dropbox")
    const text = screen.getByText(/Drag and drop .png images here, or click to select/i);

    expect(dropbox).toBeInTheDocument();
    expect(text).toBeInTheDocument();
});

test('dropbox accepts .png images', async () => {
    const result = render(<DropBox onDrop={() => null}
                                   resetSelectedFile={() => null}/>);
    global.URL.createObjectURL = jest.fn();

    const file = new File(['(⌐□_□)'], 'test.png', {type: 'image/png'});
    const input = result.container.querySelector('#input-image')
    await act(async () => {
        fireEvent.change(input, {target: {files: [file]}});
    });
    expect(input.files[0]).toStrictEqual(file);
});

test('dropbox does not accept other file types', async () => {
    const result = render(<DropBox onDrop={() => null}
                                   resetSelectedFile={() => null}/>);
    global.URL.createObjectURL = jest.fn();

    const file = new File(['(⌐□_□)'], 'test2.txt', {type: 'text/plain'});
    const input = result.container.querySelector('#input-image');

    await act(async () => {
        fireEvent.change(input, {target: {files: [file]}});
    });

    const fileNameDisplay = screen.queryByText(/test2.txt/i);
    const errorMsg = screen.queryByText(/Only .png files are allowed. Please drag and drop .png images here, or click to select/i);

    expect(errorMsg).toBeInTheDocument();
    expect(fileNameDisplay).toBeNull();
});
