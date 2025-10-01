import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import dts from 'vite-plugin-dts'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isLibrary = mode === 'library'
  
  return {
    plugins: [
      react(),
      isLibrary && dts({
        insertTypesEntry: true,
        include: ['src/**/*'],
        exclude: ['src/**/*.stories.*', 'src/**/*.test.*']
      })
    ].filter(Boolean),
    
    build: isLibrary ? {
      lib: {
        entry: resolve(__dirname, 'src/index.ts'),
        name: 'NexusRepositoryFrontend',
        fileName: (format) => `index.${format}.js`,
        formats: ['es', 'cjs']
      },
      rollupOptions: {
        external: ['react', 'react-dom'],
        output: {
          globals: {
            react: 'React',
            'react-dom': 'ReactDOM'
          }
        }
      }
    } : {
      outDir: 'dist',
      sourcemap: true
    },
    
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false
        }
      }
    },
    
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      }
    }
  }
})
