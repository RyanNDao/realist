import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: path.resolve(__dirname, 'realist-app'),
  base: '/',
  build: {
    outDir: './dist',
    emptyOutDir: true
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    },
    fs: {
      allow: [
        '.',
        path.resolve(__dirname, '../../node_modules/leaflet/dist')
      ]
    }
  },
  
})
