import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    manifest: true,
    chunkSizeWarningLimit: 400,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('/src/i18n/resources.ts')) return 'app-i18n'
          if (id.includes('commonjsHelpers')) return 'vendor-react'
          if (!id.includes('node_modules')) return undefined
          if (id.includes('@tanstack')) return 'vendor-query'
          if (id.includes('framer-motion')) return 'vendor-motion'
          if (id.includes('@dnd-kit')) return 'vendor-dnd'
          if (id.includes('lucide-react')) return 'vendor-icons'
          if (
            id.includes('/node_modules/react/')
            || id.includes('/node_modules/react-dom/')
            || id.includes('/node_modules/scheduler/')
          ) return 'vendor-react'
          return 'vendor-core'
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
