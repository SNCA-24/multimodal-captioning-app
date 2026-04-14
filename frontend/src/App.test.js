import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import App from './App';

test('renders the real app UI and updates the selected language', async () => {
  const user = userEvent.setup();

  render(<App />);

  expect(
    screen.getByRole('heading', { name: /image & video caption generator/i })
  ).toBeInTheDocument();
  expect(screen.getByText(/upload an image/i)).toBeInTheDocument();
  expect(screen.getByText(/upload a video/i)).toBeInTheDocument();
  expect(screen.getAllByText(/no caption generated yet/i)).toHaveLength(2);

  const languageSelect = screen.getByLabelText(/select language/i);
  expect(languageSelect).toHaveValue('en');

  await user.selectOptions(languageSelect, 'fr');
  expect(languageSelect).toHaveValue('fr');
});
