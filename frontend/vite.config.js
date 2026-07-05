import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  // GitHub Actions sets GITHUB_ACTIONS=true; Pages serves this repo at
  // https://<owner>.github.io/market-analyst/, so assets need that base path
  // in production while local dev keeps using '/'.
  base: process.env.GITHUB_ACTIONS ? '/market-analyst/' : '/',
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Atlas | Trading Dashboard',
        short_name: 'Atlas',
        description: 'Trading Intelligence Platform dashboard',
        theme_color: '#020617',
        background_color: '#020617',
        display: 'standalone',
        start_url: '.',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
    }),
  ],
  server: {
    port: 5173,
  },
})
