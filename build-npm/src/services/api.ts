import axios from 'axios'
import { 
  HealthResponse, 
  ConfigResponse, 
  StatsResponse, 
  Repository, 
  Package, 
  Schedule,
  ApiError 
} from '@/types'

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Health API
export const healthApi = {
  getHealth: (): Promise<HealthResponse> => 
    api.get('/health').then(res => res.data),
}

// Config API
export const configApi = {
  getConfig: (): Promise<ConfigResponse> => 
    api.get('/config').then(res => res.data),
  
  getPipPackageInfo: () => 
    api.get('/pip-package').then(res => res.data),
}

// Stats API
export const statsApi = {
  getStats: (): Promise<StatsResponse> => 
    api.get('/stats').then(res => res.data),
}

// Repository API
export const repositoryApi = {
  getRepositories: (): Promise<Repository[]> => 
    api.get('/repositories/').then(res => res.data),
  
  getRepository: (name: string): Promise<Repository> => 
    api.get(`/repositories/${name}`).then(res => res.data),
  
  getRepositoryPackages: (name: string): Promise<Package[]> => 
    api.get(`/repositories/${name}/packages`).then(res => res.data),
}

// Package API
export const packageApi = {
  getPackages: (): Promise<Package[]> => 
    api.get('/packages/').then(res => res.data),
  
  getPackage: (name: string): Promise<Package> => 
    api.get(`/packages/${name}`).then(res => res.data),
}

// Schedule API
export const scheduleApi = {
  getSchedules: (): Promise<Schedule[]> => 
    api.get('/schedule/').then(res => res.data),
  
  createSchedule: (schedule: Omit<Schedule, 'id'>): Promise<Schedule> => 
    api.post('/schedule/', schedule).then(res => res.data),
  
  updateSchedule: (id: string, schedule: Partial<Schedule>): Promise<Schedule> => 
    api.put(`/schedule/${id}`, schedule).then(res => res.data),
  
  deleteSchedule: (id: string): Promise<void> => 
    api.delete(`/schedule/${id}`).then(() => undefined),
  
  executeSchedule: (id: string): Promise<void> => 
    api.post(`/schedule/${id}/execute`).then(() => undefined),
}

// Utility functions
export const handleApiError = (error: any): ApiError => {
  if (error.response?.data) {
    return {
      detail: error.response.data.detail || 'An error occurred',
      status_code: error.response.status,
    }
  }
  
  return {
    detail: error.message || 'Network error',
    status_code: 0,
  }
}

export default api
