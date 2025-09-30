import React from 'react'
import { Card } from '@/components/ui/Card'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useStats } from '@/hooks/useApi'
import { Database, Package, Activity, BarChart3 } from 'lucide-react'

export const StatsCard: React.FC = () => {
  const { data: stats, isLoading, error } = useStats()

  if (isLoading) {
    return (
      <Card title="Statistics">
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner />
        </div>
      </Card>
    )
  }

  if (error) {
    return (
      <Card title="Statistics">
        <div className="text-red-600">Failed to load statistics</div>
      </Card>
    )
  }

  const statItems = [
    {
      label: 'Total Repositories',
      value: stats?.total_repositories || 0,
      icon: Database,
      color: 'text-blue-600',
    },
    {
      label: 'Total Packages',
      value: stats?.total_packages || 0,
      icon: Package,
      color: 'text-green-600',
    },
    {
      label: 'Active Repositories',
      value: stats?.active_repositories || 0,
      icon: Activity,
      color: 'text-nexus-600',
    },
  ]

  return (
    <Card title="Statistics">
      <div className="grid grid-cols-1 gap-4">
        {statItems.map((item) => (
          <div key={item.label} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <item.icon className={`w-5 h-5 ${item.color}`} />
              <span className="text-sm font-medium text-gray-700">{item.label}</span>
            </div>
            <span className="text-lg font-bold text-gray-900">{item.value}</span>
          </div>
        ))}
        
        {stats?.packages_by_repository && Object.keys(stats.packages_by_repository).length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 mb-3">
              <BarChart3 className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">Packages by Repository</span>
            </div>
            <div className="space-y-2">
              {Object.entries(stats.packages_by_repository).map(([repo, count]) => (
                <div key={repo} className="flex justify-between text-sm">
                  <span className="text-gray-600">{repo}</span>
                  <span className="font-medium">{count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}

export default StatsCard
