import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  root: './defense',
  base: '/defense/',
  resolve: {
    alias: {
      '@': resolve(__dirname, './shared'),
      '@defense': resolve(__dirname, './defense')
    }
  },
  server: {
    port: 3002,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 3002,
    open: false,
    host: true,
    root: './dist/defense'
  },
  build: {
    outDir: '../dist/defense',
    emptyOutDir: true
  }
})