<template>
  <ConfigProvider :theme="themeConfig" :locale="zhCN">
    <router-view />
  </ConfigProvider>
</template>

<script setup lang="ts">
import { ConfigProvider, theme } from 'ant-design-vue'
import type { ThemeConfig } from 'ant-design-vue/es/config-provider/context'
import zhCN from 'ant-design-vue/es/locale/zh_CN'

const themeConfig: ThemeConfig = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#52C41A',
    colorInfo: '#4DABF7',
    colorSuccess: '#51CF66',
    colorWarning: '#FFD93D',
    colorError: '#FA5252',
    borderRadius: 12,
    fontFamily: "'Plus Jakarta Sans','PingFang SC','Microsoft YaHei',sans-serif",
  },
}
</script>

<style scoped>
</style>
