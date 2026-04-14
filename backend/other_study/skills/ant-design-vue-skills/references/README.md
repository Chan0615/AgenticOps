# Skill 目录结构

本目录包含按需加载的参考文档，主文件通过渐进式披露策略引用这些资源。

## 📁 文件说明

### templates/ - 页面模板
- **[standard-list-page.md](templates/standard-list-page.md)** - 标准列表页模板
  - 适用场景：简单 CRUD、1-2个搜索字段、无批量操作
  - 代码量：~300 行
  
- **[advanced-table.md](templates/advanced-table.md)** - 高级搜索表格模板
  - 适用场景：复杂业务、3+搜索字段、批量操作、行选择
  - 代码量：~400 行

### 核心文档
- **[design-system.md](design-system.md)** - 完整 UI/UX 设计规范
  - 色彩系统、间距系统、阴影规范、动画规范
  - 按钮设计、表格设计、表单设计规范
  - 响应式设计指南
  
- **[composables.md](composables.md)** - 组合式函数使用指南
  - useLoading - 加载状态管理
  - usePermission - 权限检查
  - useTable - 表格状态管理
  - 自定义 Composables 示例

## 🎯 使用策略

### 渐进式披露（Progressive Disclosure）

主 `SKILL.md` 文件保持精简（<500行），包含：
- ✅ 核心设计原则
- ✅ 标准开发流程（4步法）
- ✅ 必须遵守的规范
- ✅ 快速导航索引

详细内容按需读取：
1. 开发新页面时 → 读取 `templates/` 下的对应模板
2. 优化视觉细节时 → 读取 `design-system.md`
3. 简化代码逻辑时 → 读取 `composables.md`

### 读取建议

```
用户请求
   ↓
查看 SKILL.md 主文件（已加载）
   ↓
根据场景选择：
   ├─ 简单页面 → 读取 templates/standard-list-page.md
   ├─ 复杂页面 → 读取 templates/advanced-table.md
   ├─ 调整样式 → 读取 design-system.md
   └─ 使用 Hooks → 读取 composables.md
```

## 📊 优化对比

### 优化前
- ❌ 单文件 1492 行，超出推荐限制（500行）
- ❌ 重复代码多（标准模板和高级模板重复）
- ❌ 结构扁平，查找困难
- ❌ 加载效率低

### 优化后
- ✅ 主文件 220 行，符合最佳实践
- ✅ 代码零重复，模块化组织
- ✅ 三层结构，按需加载
- ✅ 加载效率提升 85%+

## 🔧 维护指南

### 何时更新？
- 添加新模板时 → 在 `templates/` 下创建新文件，更新主文件导航
- 修改设计规范时 → 更新 `design-system.md`
- 新增 Composable 时 → 更新 `composables.md`

### 命名规范
- 文件名使用 kebab-case
- 模板文件放在 `templates/` 目录
- 功能文档直接放在 `references/` 根目录

### 文件大小
- 单个文件建议 < 500 行
- 如超过，考虑进一步拆分
- 使用目录层级组织相关内容
