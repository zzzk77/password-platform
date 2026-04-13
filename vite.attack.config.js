import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  root: './attack',
  base: '/attack/',
  resolve: {
    alias: {
      '@': resolve(__dirname, './shared'),
      '@attack': resolve(__dirname, './attack')
    }
  },
  server: {
    port: 3001,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 3001,
    open: false,
    host: true,
    root: './dist/attack'
  },
  build: {
    outDir: '../dist/attack',
    emptyOutDir: true
  }
})



