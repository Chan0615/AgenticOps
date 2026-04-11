import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    chunkSizeWarningLimit: 900,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined

          if (id.includes('ant-design-vue')) return 'vendor-antd'
          if (id.includes('@ant-design/icons-vue')) return 'vendor-ant-icons'
          if (id.includes('vue') || id.includes('pinia') || id.includes('vue-router')) {
            return 'vendor-vue-core'
          }
          if (id.includes('axios')) return 'vendor-http'
          if (id.includes('xterm')) return 'vendor-terminal'
          if (id.includes('marked') || id.includes('highlight.js')) return 'vendor-content'

          return 'vendor-misc'
        },
      },
    },
  },
})
