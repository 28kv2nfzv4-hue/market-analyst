import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  // GitHub Actions sets GITHUB_ACTIONS=true; Pages serves this repo at
  // https://<owner>.github.io/market-analyst/, so assets need that base path
  // in production while local dev keeps using '/'.
  base: process.env.GITHUB_ACTIONS ? '/market-analyst/' : '/',
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
  },
})
