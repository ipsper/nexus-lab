import React, { useState } from 'react'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useSchedules, useDeleteSchedule, useExecuteSchedule } from '@/hooks/useApi'
import { Schedule } from '@/types'
import { Clock, Play, Trash2, Edit, Calendar } from 'lucide-react'

const ScheduleItem: React.FC<{ 
  schedule: Schedule
  onEdit: (schedule: Schedule) => void
}> = ({ schedule, onEdit }) => {
  const deleteSchedule = useDeleteSchedule()
  const executeSchedule = useExecuteSchedule()

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this schedule?')) {
      deleteSchedule.mutate(schedule.id)
    }
  }

  const handleExecute = () => {
    executeSchedule.mutate(schedule.id)
  }

  const getFrequencyColor = (frequency: string) => {
    const colors: Record<string, string> = {
      daily: 'bg-green-100 text-green-800',
      weekly: 'bg-blue-100 text-blue-800',
      monthly: 'bg-purple-100 text-purple-800',
      hourly: 'bg-orange-100 text-orange-800',
    }
    return colors[frequency] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <Clock className="w-5 h-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">{schedule.name}</h3>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFrequencyColor(schedule.frequency)}`}>
              {schedule.frequency}
            </span>
            {schedule.enabled ? (
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Enabled
              </span>
            ) : (
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                Disabled
              </span>
            )}
          </div>
          
          <div className="text-sm text-gray-600 mb-3">
            <div className="flex items-center space-x-2">
              <span className="font-medium">{schedule.method}</span>
              <span>{schedule.endpoint}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            {schedule.last_run && (
              <div className="flex items-center space-x-1">
                <Calendar className="w-3 h-3" />
                <span>Last: {new Date(schedule.last_run).toLocaleString()}</span>
              </div>
            )}
            {schedule.next_run && (
              <div className="flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>Next: {new Date(schedule.next_run).toLocaleString()}</span>
              </div>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2 ml-4">
          <Button
            variant="secondary"
            onClick={() => onEdit(schedule)}
            className="px-3 py-1 text-sm"
          >
            <Edit className="w-4 h-4" />
          </Button>
          <Button
            variant="secondary"
            onClick={handleExecute}
            disabled={executeSchedule.isLoading}
            className="px-3 py-1 text-sm"
          >
            <Play className="w-4 h-4" />
          </Button>
          <Button
            variant="secondary"
            onClick={handleDelete}
            disabled={deleteSchedule.isLoading}
            className="px-3 py-1 text-sm text-red-600 hover:text-red-700"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

export const ScheduleList: React.FC = () => {
  const { data: schedules, isLoading, error } = useSchedules()
  const [, setEditingSchedule] = useState<Schedule | null>(null)

  if (isLoading) {
    return (
      <Card title="Schedules">
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner />
        </div>
      </Card>
    )
  }

  if (error) {
    return (
      <Card title="Schedules">
        <div className="text-red-600">Failed to load schedules</div>
      </Card>
    )
  }

  if (!schedules || schedules.length === 0) {
    return (
      <Card title="Schedules">
        <div className="text-center py-8 text-gray-500">
          No schedules found
        </div>
      </Card>
    )
  }

  return (
    <Card title="Schedules">
      <div className="space-y-4">
        {schedules.map((schedule) => (
          <ScheduleItem
            key={schedule.id}
            schedule={schedule}
            onEdit={setEditingSchedule}
          />
        ))}
      </div>
    </Card>
  )
}

export default ScheduleList
