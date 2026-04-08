import axios from 'axios'

const BASE_URL = '/api/server'

// ============ SaltStack 管理 ============

export async function saltExecute(
  envName: string,
  target: string,
  fun: string,
  arg?: string[]
) {
  const params = new URLSearchParams()
  if (arg) arg.forEach(a => params.append('arg', a))
  
  return axios.post(`${BASE_URL}/salt/${envName}/execute`, null, {
    params: { target, fun, ...params }
  })
}

export async function saltGetMinions(envName: string) {
  return axios.get(`${BASE_URL}/salt/${envName}/minions`)
}

export async function saltPing(envName: string, target = '*') {
  return axios.post(`${BASE_URL}/salt/${envName}/ping`, null, {
    params: { target }
  })
}

export async function saltRunCommand(
  envName: string,
  target: string,
  command: string
) {
  return axios.post(`${BASE_URL}/salt/${envName}/command`, null, {
    params: { target, command }
  })
}

// ============ SSH 管理 ============

export interface SSHExecuteParams {
  server_id: string
  hostname: string
  command: string
  port?: number
  username?: string
  password?: string
  private_key?: string
}

export async function sshExecute(params: SSHExecuteParams) {
  return axios.post(`${BASE_URL}/ssh/execute`, null, { params })
}

export async function sshDisconnect(serverId: string) {
  return axios.post(`${BASE_URL}/ssh/disconnect/${serverId}`)
}

// ============ WebSocket SSH ============

export function getWebSocketUrl(): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.hostname}:8765`
}
