import React from 'react'
import { CardProps } from '@/types'
import { clsx } from 'clsx'

export const Card: React.FC<CardProps> = ({ 
  title, 
  children, 
  className 
}) => {
  return (
    <div className={clsx('card', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      {children}
    </div>
  )
}

export default Card
