import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const appVersion = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8')).version as string

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // About shows the version that was built.
  define: { 'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion) },
  build: {
    manifest: true,
    chunkSizeWarningLimit: 400,
    rolldownOptions: {
      output: {
        // A group also takes the modules its matches import, so groups with a higher
        // priority claim their files first: the RU split-out bundles before resources.ru.ts,
        // which imports them, and named vendors before the vendor-core catch-all.
        codeSplitting: {
          groups: [
            { name: 'app-planning-i18n', test: /\/src\/i18n\/planningInputMessages\.ts$/, priority: 100 },
            { name: 'app-teamwork-i18n', test: /\/src\/i18n\/teamwork\.en\.ts$/, priority: 100 },
            { name: 'app-teamwork-i18n-ru', test: /\/src\/i18n\/teamwork\.ru\.ts$/, priority: 100 },
            { name: 'app-agent-team-i18n-ru', test: /\/src\/i18n\/agentTeamSetup\.ru\.ts$/, priority: 100 },
            { name: 'app-plan-i18n-ru', test: /\/src\/i18n\/plan\.ru\.ts$/, priority: 100 },
            { name: 'app-landing-i18n-ru', test: /\/src\/i18n\/landing\.ru\.ts$/, priority: 100 },
            { name: 'app-surfaces-i18n-ru', test: /\/src\/i18n\/surfaces\.ru\.ts$/, priority: 100 },
            { name: 'app-literals-i18n-ru', test: /\/src\/i18n\/literals\.ru\.ts$/, priority: 100 },
            { name: 'app-i18n', test: /\/src\/i18n\/resources\.en\.ts$/, priority: 50 },
            { name: 'app-i18n-ru', test: /\/src\/i18n\/resources\.ru\.ts$/, priority: 50 },
            { name: 'vendor-query', test: /node_modules[\\/]@tanstack[\\/]/, priority: 20 },
            { name: 'vendor-motion', test: /node_modules[\\/]framer-motion[\\/]/, priority: 20 },
            { name: 'vendor-dnd', test: /node_modules[\\/]@dnd-kit[\\/]/, priority: 20 },
            { name: 'vendor-icons', test: /node_modules[\\/]lucide-react[\\/]/, priority: 20 },
            { name: 'vendor-react', test: /node_modules[\\/](react|react-dom|scheduler)[\\/]|commonjsHelpers/, priority: 20 },
            { name: 'vendor-core', test: /node_modules/, priority: 10 },
          ],
        },
      },
    },
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8001',
        changeOrigin: true,
      }
    }
  }
})
