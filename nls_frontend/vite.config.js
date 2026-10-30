import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const DJANGO = 'http://127.0.0.1:8000'
const FASTAPI = 'http://127.0.0.1:8080'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': { target: DJANGO, changeOrigin: true, rewrite: path => path.replace(/^\/api/, '') },
      '/media': { target: DJANGO, changeOrigin: true },
      '/ipo_offer': { target: FASTAPI, changeOrigin: true },
      '/dse_news': { target: FASTAPI, changeOrigin: true },
      '/cse_news': { target: FASTAPI, changeOrigin: true },
      '/minutes_index_cse': { target: FASTAPI, changeOrigin: true },
    },
  },
})
