import { useQuery, useMutation, useQueryClient } from 'react-query'
import { 
  healthApi, 
  configApi, 
  statsApi, 
  repositoryApi, 
  packageApi, 
  scheduleApi,
  handleApiError 
} from '@/services/api'
import { 
  HealthResponse, 
  ConfigResponse, 
  StatsResponse, 
  Repository, 
  Package, 
  Schedule 
} from '@/types'

// Health hooks
export const useHealth = () => {
  return useQuery<HealthResponse, Error>(
    'health',
    healthApi.getHealth,
    {
      refetchInterval: 30000, // Refetch every 30 seconds
      staleTime: 10000, // Consider data stale after 10 seconds
    }
  )
}

// Config hooks
export const useConfig = () => {
  return useQuery<ConfigResponse, Error>('config', configApi.getConfig)
}

export const usePipPackageInfo = () => {
  return useQuery('pip-package', configApi.getPipPackageInfo)
}

// Stats hooks
export const useStats = () => {
  return useQuery<StatsResponse, Error>('stats', statsApi.getStats)
}

// Repository hooks
export const useRepositories = () => {
  return useQuery<Repository[], Error>('repositories', repositoryApi.getRepositories)
}

export const useRepository = (name: string) => {
  return useQuery<Repository, Error>(
    ['repository', name],
    () => repositoryApi.getRepository(name),
    {
      enabled: !!name,
    }
  )
}

export const useRepositoryPackages = (name: string) => {
  return useQuery<Package[], Error>(
    ['repository-packages', name],
    () => repositoryApi.getRepositoryPackages(name),
    {
      enabled: !!name,
    }
  )
}

// Package hooks
export const usePackages = () => {
  return useQuery<Package[], Error>('packages', packageApi.getPackages)
}

export const usePackage = (name: string) => {
  return useQuery<Package, Error>(
    ['package', name],
    () => packageApi.getPackage(name),
    {
      enabled: !!name,
    }
  )
}

// Schedule hooks
export const useSchedules = () => {
  return useQuery<Schedule[], Error>('schedules', scheduleApi.getSchedules)
}

export const useCreateSchedule = () => {
  const queryClient = useQueryClient()
  
  return useMutation(scheduleApi.createSchedule, {
    onSuccess: () => {
      queryClient.invalidateQueries('schedules')
    },
    onError: (error) => {
      console.error('Failed to create schedule:', handleApiError(error))
    },
  })
}

export const useUpdateSchedule = () => {
  const queryClient = useQueryClient()
  
  return useMutation(
    ({ id, schedule }: { id: string; schedule: Partial<Schedule> }) =>
      scheduleApi.updateSchedule(id, schedule),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('schedules')
      },
      onError: (error) => {
        console.error('Failed to update schedule:', handleApiError(error))
      },
    }
  )
}

export const useDeleteSchedule = () => {
  const queryClient = useQueryClient()
  
  return useMutation(scheduleApi.deleteSchedule, {
    onSuccess: () => {
      queryClient.invalidateQueries('schedules')
    },
    onError: (error) => {
      console.error('Failed to delete schedule:', handleApiError(error))
    },
  })
}

export const useExecuteSchedule = () => {
  const queryClient = useQueryClient()
  
  return useMutation(scheduleApi.executeSchedule, {
    onSuccess: () => {
      queryClient.invalidateQueries('schedules')
    },
    onError: (error) => {
      console.error('Failed to execute schedule:', handleApiError(error))
    },
  })
}
