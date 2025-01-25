import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true, // Umożliwia użycie globalnych funkcji jak expect
    environment: 'jsdom', // Ustawia środowisko na jsdom
  },
});