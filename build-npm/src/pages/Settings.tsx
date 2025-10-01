import React from 'react'
import { Card } from '@/components/ui/Card'
import { useConfig, usePipPackageInfo } from '@/hooks/useApi'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { Settings as SettingsIcon, Package } from 'lucide-react'

export const Settings: React.FC = () => {
  const { data: config, isLoading: configLoading } = useConfig()
  const { data: pipInfo, isLoading: pipLoading } = usePipPackageInfo()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-2 text-gray-600">
            System configuration and information
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Configuration */}
          <Card title="Configuration">
            {configLoading ? (
              <div className="flex items-center justify-center py-8">
                <LoadingSpinner />
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center space-x-2 mb-4">
                  <SettingsIcon className="w-5 h-5 text-gray-500" />
                  <span className="font-medium">System Configuration</span>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <span className="text-sm text-gray-500">Nexus URL:</span>
                    <div className="text-sm font-medium">{config?.nexus_url}</div>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">API Version:</span>
                    <div className="text-sm font-medium">{config?.api_version}</div>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">Supported Operations:</span>
                    <div className="mt-1">
                      {config?.supported_operations?.map((operation) => (
                        <span
                          key={operation}
                          className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded mr-2 mb-1"
                        >
                          {operation}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </Card>

          {/* Package Information */}
          <Card title="Package Information">
            {pipLoading ? (
              <div className="flex items-center justify-center py-8">
                <LoadingSpinner />
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center space-x-2 mb-4">
                  <Package className="w-5 h-5 text-gray-500" />
                  <span className="font-medium">Pip Package Info</span>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <span className="text-sm text-gray-500">Package Name:</span>
                    <div className="text-sm font-medium">{pipInfo?.package_name}</div>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">Version:</span>
                    <div className="text-sm font-medium">{pipInfo?.version}</div>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">Location:</span>
                    <div className="text-sm font-medium">{pipInfo?.location}</div>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">Install Path:</span>
                    <div className="text-sm font-medium break-all">{pipInfo?.install_path}</div>
                  </div>
                  
                  {pipInfo?.git_info && (
                    <div>
                      <span className="text-sm text-gray-500">Git Information:</span>
                      <div className="mt-1 text-sm">
                        {pipInfo.git_info.is_git_repo ? (
                          <div>
                            <div>Branch: {pipInfo.git_info.branch}</div>
                            <div>Commit: {pipInfo.git_info.commit?.substring(0, 8)}</div>
                          </div>
                        ) : (
                          <div>Not a git repository</div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Settings
