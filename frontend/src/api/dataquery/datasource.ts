/**
 * 数据源管理 API 客户端
 */

import api from '../index'

// ============ 类型定义 ============

export interface DataSource {
  id: number
  name: string
  description?: string
  db_type: string
  host: string
  port: number
  database: string
  username: string
  is_system_db: boolean
  status: string
  extra_config?: Record<string, any>
  created_by?: string
  created_at: string
  updated_at: string
}

export interface DataSourceCreate {
  name: string
  description?: string
  db_type: string
  host: string
  port: number
  database: string
  username: string
  password: string
  is_system_db?: boolean
  extra_config?: Record<string, any>
}

export interface DataSourceUpdate {
  name?: string
  description?: string
  db_type?: string
  host?: string
  port?: number
  database?: string
  username?: string
  password?: string
  status?: string
  extra_config?: Record<string, any>
}

export interface TableMetadata {
  id: number
  datasource_id: number
  table_name: string
  table_comment?: string
  columns?: ColumnInfo[]
  sample_data?: Record<string, any>[]
  custom_description?: string
  synced_at?: string
}

export interface ColumnInfo {
  name: string
  type: string
  comment?: string
  is_pk: boolean
  nullable: boolean
}

export interface DataSourceListResponse {
  code: number
  message: string
  data: DataSource[]
  total: number
}

// ============ API 方法 ============

export const datasourceApi = {
  /** 数据源列表 */
  list: (params?: { page?: number; page_size?: number; name?: string; db_type?: string; status?: string }) =>
    api.get<any, DataSourceListResponse>('/dataquery/datasources', { params }),

  /** 数据源详情 */
  get: (id: number) => api.get<any, DataSource>(`/dataquery/datasources/${id}`),

  /** 创建数据源 */
  create: (data: DataSourceCreate) => api.post<any, DataSource>('/dataquery/datasources', data),

  /** 更新数据源 */
  update: (id: number, data: DataSourceUpdate) => api.put<any, DataSource>(`/dataquery/datasources/${id}`, data),

  /** 删除数据源 */
  delete: (id: number) => api.delete(`/dataquery/datasources/${id}`),

  /** 测试已保存的数据源连接 */
  test: (id: number) => api.post<any, { code: number; message: string }>(`/dataquery/datasources/${id}/test`),

  /** 直接测试连接 */
  testDirect: (data: { db_type: string; host: string; port: number; database: string; username: string; password: string }) =>
    api.post<any, { code: number; message: string }>('/dataquery/datasources/test-connection', data),

  /** 同步元数据 */
  syncMetadata: (id: number) =>
    api.post<any, { code: number; message: string; data: { table_count: number } }>(`/dataquery/datasources/${id}/sync-metadata`),

  /** 获取表列表 */
  getTables: (id: number) =>
    api.get<any, { code: number; data: TableMetadata[] }>(`/dataquery/datasources/${id}/tables`),

  /** 更新表描述 */
  updateTableDescription: (datasourceId: number, tableName: string, description: string) =>
    api.put(`/dataquery/datasources/${datasourceId}/tables/${tableName}/description`, { custom_description: description }),
}
