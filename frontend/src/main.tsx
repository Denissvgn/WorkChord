import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import '@fontsource-variable/inter/index.css'
import './styles/globals.css'
import './styles/planning-masters.css'
import './i18n/i18n'
import { SystemLanguageProvider } from './i18n/SystemLanguageProvider'
import { ToastProvider } from './components/feedback/ToastProvider'
import { installPlanningNavigationInvalidation } from './features/planningMasters/planningNavigationInvalidation'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 60000, // 1 minute cache
    },
  },
})

installPlanningNavigationInvalidation(queryClient)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ToastProvider>
          <SystemLanguageProvider>
            <App />
          </SystemLanguageProvider>
        </ToastProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
