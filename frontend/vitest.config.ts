import { configDefaults, defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    // Pending: these navigation check files run under Node's built-in test runner and
    // stay out of vitest until their helpers exist. Remove this entry when they do.
    exclude: [...configDefaults.exclude, 'src/navigation/*.check.test.ts'],
    clearMocks: true,
    restoreMocks: true,
    unstubEnvs: true,
    unstubGlobals: true,
  },
})
