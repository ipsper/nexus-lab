import React from 'react'
import { Card } from '@/components/ui/Card'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useRepositories } from '@/hooks/useApi'
import { Repository } from '@/types'
import { Database, ExternalLink, CheckCircle, XCircle } from 'lucide-react'

const RepositoryItem: React.FC<{ repository: Repository }> = ({ repository }) => {
  const getStatusIcon = (status: string) => {
    return status === 'active' ? (
      <CheckCircle className="w-4 h-4 text-green-600" />
    ) : (
      <XCircle className="w-4 h-4 text-red-600" />
    )
  }

  const getFormatColor = (format: string) => {
    const colors: Record<string, string> = {
      pypi: 'bg-blue-100 text-blue-800',
      apt: 'bg-red-100 text-red-800',
      rpm: 'bg-orange-100 text-orange-800',
      docker: 'bg-cyan-100 text-cyan-800',
      maven: 'bg-purple-100 text-purple-800',
      npm: 'bg-green-100 text-green-800',
    }
    return colors[format] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <Database className="w-5 h-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">{repository.name}</h3>
            {getStatusIcon(repository.status)}
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFormatColor(repository.format)}`}>
              {repository.format.toUpperCase()}
            </span>
            <span className="capitalize">{repository.type}</span>
            <span className="capitalize">{repository.status}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <ExternalLink className="w-4 h-4 text-gray-400" />
            <a
              href={repository.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-nexus-600 hover:text-nexus-700 truncate"
            >
              {repository.url}
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export const RepositoryList: React.FC = () => {
  const { data: repositories, isLoading, error } = useRepositories()

  if (isLoading) {
    return (
      <Card title="Repositories">
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner />
        </div>
      </Card>
    )
  }

  if (error) {
    return (
      <Card title="Repositories">
        <div className="text-red-600">Failed to load repositories</div>
      </Card>
    )
  }

  if (!repositories || repositories.length === 0) {
    return (
      <Card title="Repositories">
        <div className="text-center py-8 text-gray-500">
          No repositories found
        </div>
      </Card>
    )
  }

  return (
    <Card title="Repositories">
      <div className="space-y-4">
        {repositories.map((repository) => (
          <RepositoryItem key={repository.name} repository={repository} />
        ))}
      </div>
    </Card>
  )
}

export default RepositoryList
