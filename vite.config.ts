import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vercel requires base: './' or no base at all
export default defineConfig({
  plugins: [react()],

  // FIX: remove GitHub Pages base
  base: './',

  server: {
    port: 5173,
    open: true
  },

  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
