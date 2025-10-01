import React from 'react'
import { Card } from '@/components/ui/Card'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useHealth } from '@/hooks/useApi'
import { CheckCircle, XCircle, Clock } from 'lucide-react'

export const HealthCard: React.FC = () => {
  const { data: health, isLoading, error } = useHealth()

  if (isLoading) {
    return (
      <Card title="System Health" className="card-hover">
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner />
        </div>
      </Card>
    )
  }

  if (error) {
    return (
      <Card title="System Health" className="card-hover">
        <div className="flex items-center space-x-2 text-red-600">
          <XCircle className="w-5 h-5" />
          <span>System unavailable</span>
        </div>
      </Card>
    )
  }

  const isHealthy = health?.status === 'healthy'

  return (
    <Card title="System Health" className="card-hover">
      <div className="space-y-6">
        <div className="flex items-center space-x-3">
          {isHealthy ? (
            <CheckCircle className="w-6 h-6 text-green-600" />
          ) : (
            <XCircle className="w-6 h-6 text-red-600" />
          )}
          <span className={`text-lg font-semibold ${isHealthy ? 'text-green-600' : 'text-red-600'}`}>
            {health?.status || 'Unknown'}
          </span>
        </div>
        
        <div className="grid grid-cols-1 gap-4">
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-gray-600 font-medium">Version:</span>
            <span className="font-semibold text-gray-900">{health?.version}</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-gray-600 font-medium">Environment:</span>
            <span className="font-semibold text-gray-900 capitalize">{health?.environment}</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-2 text-sm text-gray-500 bg-gray-50 p-3 rounded">
          <Clock className="w-4 h-4" />
          <span>Last updated: {new Date(health?.timestamp || '').toLocaleString()}</span>
        </div>
      </div>
    </Card>
  )
}

export default HealthCard
