import React from 'react'
import { HealthCard } from '@/components/dashboard/HealthCard'
import { StatsCard } from '@/components/dashboard/StatsCard'
import { RepositoryList } from '@/components/repositories/RepositoryList'
import { ScheduleList } from '@/components/schedules/ScheduleList'
import { 
  Database, 
  Clock, 
  Shield, 
  Cloud, 
  Monitor, 
  Users,
  ArrowRight
} from 'lucide-react'

const services = [
  {
    title: 'Nätverk & automatisering',
    description: 'Inom nätverksområdet gör vi allt från analyser, förstudier och designarbete till implementation, felsökning samt utbildning.',
    icon: Database,
    color: 'text-blue-600'
  },
  {
    title: 'Systemutveckling',
    description: 'Vi tar ett helhetsansvar genom hela utvecklingskedjan och våra konsulter har bred och djup erfarenhet inom systemutveckling.',
    icon: Monitor,
    color: 'text-green-600'
  },
  {
    title: 'Tekniskt ledarskap',
    description: 'Vi leder projekt och genomför utredningar och ger upphandlingsstöd, utför strategiutredningar och agerar expertrådgivare.',
    icon: Users,
    color: 'text-purple-600'
  },
  {
    title: 'Säkerhet',
    description: 'Vi hjälper till med allt från säkerhetsutredningar, riskanalyser, förstudier, via designarbete, implementation, felsökning, säkerhetstestning till idrifttagande och utbildning.',
    icon: Shield,
    color: 'text-red-600'
  },
  {
    title: 'Molntjänster',
    description: 'Vi kan erbjuda dig hjälp med dina molntjänster på många olika områden, oberoende om det är public, private eller hybrid cloud.',
    icon: Cloud,
    color: 'text-cyan-600'
  },
  {
    title: 'Monitorering',
    description: 'Vi hjälper till med övervakning och monitorering av dina system för att säkerställa optimal prestanda och tillgänglighet.',
    icon: Clock,
    color: 'text-orange-600'
  }
]

export const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="hero-gradient text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">
              Ett konsultbolag i teknikens framkant
            </h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Vi tillhandahåller expertkonsulter inom tele- och datakommunikation och Cloud.
              <br />
              <span className="font-semibold">– Vår samlade kunskap gör skillnad för er.</span>
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="btn btn-primary">
                Läs mer om hur vi kan bidra
              </button>
              <button className="btn btn-outline border-white text-white hover:bg-white hover:text-blue-600">
                Kontakta oss
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="section-header">Våra tjänster</h2>
            <p className="section-subtitle">
              Vi erbjuder expertkonsulter inom olika tekniska områden
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <div key={index} className="service-card">
                <div className="flex items-center mb-4">
                  <service.icon className={`w-8 h-8 ${service.color} mr-3`} />
                  <h3 className="text-xl font-bold text-gray-900">{service.title}</h3>
                </div>
                <p className="text-gray-600 mb-4">{service.description}</p>
                <button className="flex items-center text-blue-600 font-semibold hover:text-blue-700 transition-colors">
                  Läs mer om hur vi kan bidra
                  <ArrowRight className="w-4 h-4 ml-2" />
                </button>
              </div>
            ))}
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

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-4">Hur kan vi hjälpa dig?</h2>
          <p className="text-xl mb-8">
            Fyll i dina uppgifter så kontaktar vi dig så snart vi kan!
          </p>
          <div className="max-w-md mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                placeholder="Din e-postadress"
                className="flex-1 px-4 py-3 rounded-none text-gray-900"
              />
              <button className="btn bg-white text-blue-600 hover:bg-gray-100">
                Skicka
              </button>
            </div>
            <p className="text-sm mt-4 opacity-90">
              Jag godkänner att IP-Solutions registrerar ovanstående information för att komma i kontakt med mig, ej ur marknadsföringssyfte.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Dashboard
