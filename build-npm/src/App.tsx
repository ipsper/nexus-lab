// import React from 'react' // Not needed in modern React
import { Routes, Route } from 'react-router-dom'
import { Header } from '@/components/layout/Header'
import { Dashboard } from '@/pages/Dashboard'
import { Repositories } from '@/pages/Repositories'
import { Schedules } from '@/pages/Schedules'
import { Statistics } from '@/pages/Statistics'
import { Settings } from '@/pages/Settings'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/repositories" element={<Repositories />} />
        <Route path="/schedules" element={<Schedules />} />
        <Route path="/statistics" element={<Statistics />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </div>
  )
}

export default App
