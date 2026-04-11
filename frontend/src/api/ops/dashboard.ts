import request from '@/api'

export interface DashboardSummary {
  active_users: number
  total_users: number
  knowledge_bases: number
  documents: number
  indexed_documents: number
  servers: number
  online_servers: number
  today_runs: number
  failed_runs: number
  today_chats: number
  chunks: number
  enabled_tasks: number
  total_tasks: number
  success_rate: number
}

export interface DashboardNotice {
  title: string
  time: string
}

export interface DashboardHealthItem {
  name: string
  status: string
  color: string
  desc: string
}

export interface DashboardEvent {
  id: number
  log_id: number
  title: string
  time: string
  color: string
}

export interface DashboardTrendData {
  dates: string[]
  total_runs: number[]
  failed_runs: number[]
}

export interface DashboardFilterData {
  project_id?: number
  project_name?: string
  group_id?: number
  group_name?: string
}

export interface DashboardOverviewData {
  generated_at: string
  filters: DashboardFilterData
  summary: DashboardSummary
  notices: DashboardNotice[]
  health: DashboardHealthItem[]
  events: DashboardEvent[]
  trends: DashboardTrendData
}

export interface DashboardOverviewResponse {
  code: number
  message: string
  data: DashboardOverviewData
}

export const getDashboardOverview = (params?: { project_id?: number; group_id?: number }) => {
  return request.get<any, DashboardOverviewResponse>('/ops/dashboard/overview', { params })
}
