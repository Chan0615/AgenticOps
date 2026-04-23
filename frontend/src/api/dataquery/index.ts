/**
 * 智能问数模块 API
 */

export { datasourceApi } from './datasource'
export type { DataSource, DataSourceCreate, DataSourceUpdate, TableMetadata, ColumnInfo } from './datasource'

export { dataqueryApi } from './chat'
export type { QueryAskRequest, QueryResult, QueryHistory, QueryHistoryDetail } from './chat'
