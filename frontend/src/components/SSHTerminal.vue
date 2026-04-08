<template>
  <div class="ssh-terminal-container">
    <div ref="terminalRef" class="terminal-wrapper"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'
import 'xterm/css/xterm.css'
import { Message } from '@arco-design/web-vue'
import { getWebSocketUrl } from '@/api/server'

interface Props {
  hostname: string
  port?: number
  username: string
  password?: string
  privateKey?: string
  connectionId: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'connected'): void
  (e: 'disconnected'): void
  (e: 'error', error: Error): void
}>()

const terminalRef = ref<HTMLElement>()
let terminal: Terminal | null = null
let fitAddon: FitAddon | null = null
let ws: WebSocket | null = null

onMounted(() => {
  initTerminal()
  connectSSH()
})

onUnmounted(() => {
  disconnect()
})

function initTerminal() {
  if (!terminalRef.value) return

  terminal = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    theme: {
      background: '#1e1e1e',
      foreground: '#ffffff',
      cursor: '#ffffff',
      selectionBackground: '#5a5a5a',
      black: '#000000',
      red: '#ff5c57',
      green: '#5af78e',
      yellow: '#f3f99d',
      blue: '#57c7ff',
      magenta: '#ff6ac1',
      cyan: '#9aedfe',
      white: '#f1f1f0',
      brightBlack: '#686868',
      brightRed: '#ff5c57',
      brightGreen: '#5af78e',
      brightYellow: '#f3f99d',
      brightBlue: '#57c7ff',
      brightMagenta: '#ff6ac1',
      brightCyan: '#9aedfe',
      brightWhite: '#ffffff',
    },
  })

  fitAddon = new FitAddon()
  terminal.loadAddon(fitAddon)
  terminal.open(terminalRef.value)
  fitAddon.fit()

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  if (fitAddon && terminal) {
    fitAddon.fit()
    if (ws && ws.readyState === WebSocket.OPEN) {
      const dimensions = fitAddon.proposeDimensions()
      ws.send(
        JSON.stringify({
          action: 'resize',
          cols: dimensions?.cols || 80,
          rows: dimensions?.rows || 24,
        })
      )
    }
  }
}

async function connectSSH() {
  try {
    const wsUrl = getWebSocketUrl()
    ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      // 发送连接信息
      ws!.send(
        JSON.stringify({
          action: 'connect',
          connection_id: props.connectionId,
          hostname: props.hostname,
          port: props.port || 22,
          username: props.username,
          password: props.password,
          private_key: props.privateKey,
        })
      )
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'connected') {
        Message.success('SSH 连接成功')
        emit('connected')
        
        // 附加终端到 WebSocket
        const attachAddon = new AttachAddon(ws!)
        terminal!.loadAddon(attachAddon)
      } else if (data.type === 'output') {
        terminal!.write(data.data)
      } else if (data.type === 'disconnected') {
        Message.info('SSH 连接已关闭')
        emit('disconnected')
      }
    }

    ws.onerror = (error) => {
      Message.error('WebSocket 连接错误')
      emit('error', new Error('WebSocket 连接错误'))
    }

    ws.onclose = () => {
      emit('disconnected')
    }
  } catch (error) {
    Message.error('SSH 连接失败')
    emit('error', error as Error)
  }
}

function disconnect() {
  if (ws) {
    ws.send(
      JSON.stringify({
        action: 'disconnect',
        connection_id: props.connectionId,
      })
    )
    ws.close()
    ws = null
  }
  
  if (terminal) {
    terminal.dispose()
    terminal = null
  }
  
  window.removeEventListener('resize', handleResize)
}

// 暴露方法供父组件调用
defineExpose({
  disconnect,
})
</script>

<style scoped>
.ssh-terminal-container {
  width: 100%;
  height: 100%;
  background: #1e1e1e;
  border-radius: 4px;
  overflow: hidden;
}

.terminal-wrapper {
  width: 100%;
  height: 100%;
  padding: 8px;
}
</style>
