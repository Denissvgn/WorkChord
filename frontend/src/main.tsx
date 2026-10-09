import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App'
import '@fontsource-variable/inter/index.css'
import './styles/globals.css'
import './styles/planning-masters.css'
import './i18n/i18n'
import { SystemLanguageProvider } from './i18n/SystemLanguageProvider'
import { ToastProvider } from './components/feedback/ToastProvider'
import { IdentityProvider } from './features/identity/IdentityProvider'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: true,
      staleTime: 15000,
    },
  },
})

const router = createBrowserRouter([{ path: '*', element: (
  <ToastProvider>
    <IdentityProvider>
      <SystemLanguageProvider><App /></SystemLanguageProvider>
    </IdentityProvider>
  </ToastProvider>
) }])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
