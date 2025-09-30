import React from 'react'
import { Link } from 'react-router-dom'
import { HealthCard } from '@/components/dashboard/HealthCard'
import { StatsCard } from '@/components/dashboard/StatsCard'
import { RepositoryList } from '@/components/repositories/RepositoryList'
import { ScheduleList } from '@/components/schedules/ScheduleList'
import { 
  ExternalLink
} from 'lucide-react'

export const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-white">

      {/* Welcome Section */}
      <section className="bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Välkommen till Dashboard
            </h2>
            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
              Hantera dina paketarkiv och artefakter med kraftfullt och flexibelt system.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/repositories" className="btn btn-primary">
                Kom igång
              </Link>
              <a 
                href="/api/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn btn-outline flex items-center"
              >
                API Dokumentation
                <ExternalLink className="w-4 h-4 ml-2" />
              </a>
            </div>
          </div>
        </div>
      </section>


      {/* System Overview Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="section-header">Systemöversikt</h2>
            <p className="section-subtitle">
              Övervaka och hantera ditt Nexus Repository Manager system
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left column */}
            <div className="space-y-8">
              <HealthCard />
              <StatsCard />
            </div>

            {/* Right column */}
            <div className="space-y-8">
              <RepositoryList />
              <ScheduleList />
            </div>
          </div>
        </div>
      </section>

    </div>
  )
}

export default Dashboard
