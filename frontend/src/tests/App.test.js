import {screen} from '@testing-library/react';

import App from '../App';
import {renderWithProviders} from "./testUtils";

test('app contains dropbox component', () => {
    renderWithProviders(<App/>);

    const dropbox = screen.getByRole('form', {id: 'upload_form'})
    expect(dropbox).toBeInTheDocument();
});

test('renders form upload button', () => {
    renderWithProviders(<App/>);

    const button = screen.getByText(/^Upload$/);
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
});