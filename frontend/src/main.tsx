import '@mantine/core/styles.css'

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MantineProvider } from '@mantine/core'
import {
  emotionTransform,
  MantineEmotionProvider,
} from '@mantine/emotion'
import './index.css'
import App from './App.tsx'


const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider stylesTransform={emotionTransform}>
      <MantineEmotionProvider>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </MantineEmotionProvider>
    </MantineProvider>
  </StrictMode>,
)
