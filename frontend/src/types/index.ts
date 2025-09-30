// API Response Types
export interface HealthResponse {
  status: string
  timestamp: string
  version: string
  environment: string
}

export interface ConfigResponse {
  nexus_url: string
  api_version: string
  supported_operations: string[]
}

export interface StatsResponse {
  total_repositories: number
  total_packages: number
  active_repositories: number
  packages_by_repository: Record<string, number>
}

export interface Repository {
  name: string
  type: string
  format: string
  url: string
  status: string
}

export interface Package {
  name: string
  version: string
  repository: string
  size: number
  upload_date: string
}

export interface Schedule {
  id: string
  name: string
  endpoint: string
  method: string
  frequency: string
  enabled: boolean
  last_run?: string
  next_run?: string
}

// UI Component Props
export interface CardProps {
  title: string
  children: React.ReactNode
  className?: string
}

export interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  className?: string
}

export interface InputProps {
  label: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  type?: string
  required?: boolean
  className?: string
}

// API Error Types
export interface ApiError {
  detail: string
  status_code: number
}

// Navigation Types
export interface NavItem {
  label: string
  href: string
  icon: React.ComponentType<{ className?: string }>
}
