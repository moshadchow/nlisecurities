import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const DJANGO = 'http://127.0.0.1:8000'
const FASTAPI = 'http://127.0.0.1:8080'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/about':            { target: DJANGO,  changeOrigin: true },
      '/slider':           { target: DJANGO,  changeOrigin: true },
      '/service':          { target: DJANGO,  changeOrigin: true },
      '/product':          { target: DJANGO,  changeOrigin: true },
      '/feature':          { target: DJANGO,  changeOrigin: true },
      '/offer':            { target: DJANGO,  changeOrigin: true },
      '/board_member':     { target: DJANGO,  changeOrigin: true },
      '/mancom':           { target: DJANGO,  changeOrigin: true },
      '/tech':             { target: DJANGO,  changeOrigin: true },
      '/event':            { target: DJANGO,  changeOrigin: true },
      '/market_news':      { target: DJANGO,  changeOrigin: true },
      '/client':           { target: DJANGO,  changeOrigin: true },
      '/faq':              { target: DJANGO,  changeOrigin: true },
      '/contact':          { target: DJANGO,  changeOrigin: true },
      '/ipo':              { target: DJANGO,  changeOrigin: true },
      '/privacy-policy':   { target: DJANGO,  changeOrigin: true },
      '/branch':           { target: DJANGO,  changeOrigin: true },
      '/categories':       { target: DJANGO,  changeOrigin: true },
      '/research':         { target: DJANGO,  changeOrigin: true },
      '/top_share_price_by': { target: DJANGO, changeOrigin: true },
      '/minutes_index':    { target: DJANGO,  changeOrigin: true },
      '/market_info':      { target: DJANGO,  changeOrigin: true },
      '/market_index':     { target: DJANGO,  changeOrigin: true },
      '/ticker_price':     { target: DJANGO,  changeOrigin: true },
      '/sector_wise_inst': { target: DJANGO,  changeOrigin: true },
      '/media':            { target: DJANGO,  changeOrigin: true },
      '/ipo_offer':        { target: FASTAPI, changeOrigin: true },
      '/dse_news':         { target: FASTAPI, changeOrigin: true },
      '/cse_news':         { target: FASTAPI, changeOrigin: true },
      '/minutes_index_cse':{ target: FASTAPI, changeOrigin: true },
    },
  },
})
