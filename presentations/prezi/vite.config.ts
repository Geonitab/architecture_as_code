import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The app will be deployed under /prezi/ (served from docs/prezi/)
export default defineConfig({
  plugins: [react()],
  base: '/prezi/'
})
