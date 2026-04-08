# AgenticOps 完整启动指南

## 📋 环境要求

- **Python**: 3.10+ (推荐 3.12)
- **Node.js**: 18+ 
- **MySQL**: 8.0+
- **Redis**: 6.0+
- **操作系统**: Windows 10/11

---

## 🚀 快速启动（5分钟）

### 第一步：创建 Python 虚拟环境

```powershell
# 进入后端目录
cd D:\00_ChAn_Workspace\AgenticOps\backend

# 创建虚拟环境
python312 -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\Activate.ps1
```

> ⚠️ 如果提示执行策略错误，以管理员身份运行 PowerShell 并执行：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 第二步：安装后端依赖

```powershell
# 确保虚拟环境已激活（命令行前应有 (.venv) 标识）

# 升级 pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

### 第三步：配置后端环境

```powershell
# 复制配置文件
copy config.yaml.example config.yaml

# 编辑 config.yaml，确保数据库配置正确
# 默认配置已填好，如需修改请使用编辑器打开
notepad config.yaml
```

**config.yaml 关键配置**：
```yaml
mysql:
  default:
    host: 10.225.138.121
    port: 3306
    user: root
    password: "CAr8RvRA"
    database: kefu_ai

redis:
  default:
    host: 10.225.138.125
    port: 6579
    password: "leadton@qwe"
    db: 20
```

### 第四步：初始化数据库

```powershell
# 确保虚拟环境已激活
python init_db.py
```

**预期输出**：
```
[1/4] 创建数据库 'kefu_ai' ...
      数据库 'kefu_ai' 就绪
[2/4] 创建数据表 ...
      数据表创建完成
[3/4] 初始化基础数据 ...
      创建菜单 20 条
      创建角色 2 个
      角色菜单关联完成
      创建管理员用户 admin / admin123
[4/4] 初始化完成！

✅ 数据库初始化成功！
   管理员账号: admin  密码: admin123
```

### 第五步：启动后端服务

```powershell
# 方式1：使用 app/main.py（推荐）
uvicorn app.main:app --reload --port 8000

# 方式2：使用 backend/main.py
python main.py
```

**预期输出**：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**验证后端**：
- 打开浏览器访问：http://localhost:8000
- 看到 `{"message": "AgenticOps API", "version": "1.0.0"}` 表示成功
- API 文档：http://localhost:8000/docs

---

### 第六步：安装前端依赖

**打开新的 PowerShell 窗口**（保持后端运行）

```powershell
# 进入前端目录
cd D:\00_ChAn_Workspace\AgenticOps\frontend

# 安装依赖（首次运行需要）
npm install

# 如果 npm 下载慢，可以使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

### 第七步：启动前端服务

```powershell
# 启动开发服务器
npm run dev
```

**预期输出**：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 第八步：访问系统

打开浏览器访问：**http://localhost:5173**

**默认管理员账号**：
- 用户名：`admin`
- 密码：`admin123`

---

## 📝 详细步骤说明

### 1. 虚拟环境管理

#### 创建虚拟环境
```powershell
cd D:\00_ChAn_Workspace\AgenticOps\backend
python -m venv .venv
```

#### 激活虚拟环境
```powershell
.\.venv\Scripts\Activate.ps1
```

#### 退出虚拟环境
```powershell
deactivate
```

#### 验证虚拟环境
```powershell
# 查看 Python 路径（应包含 .venv）
where python

# 查看已安装的包
pip list
```

### 2. 依赖安装问题排查

#### 问题1：pip 安装慢
```powershell
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题2：bcrypt 安装失败
```powershell
# 安装 Visual C++ Build Tools
# 下载地址：https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 或安装预编译版本
pip install --only-binary :all: bcrypt
```

#### 问题3：依赖冲突
```powershell
# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### 3. 数据库连接验证

```powershell
# 测试 MySQL 连接
python -c "import pymysql; conn = pymysql.connect(host='10.225.138.121', port=3306, user='root', password='CAr8RvRA'); print('MySQL 连接成功'); conn.close()"

# 测试 Redis 连接
python -c "import redis; r = redis.Redis(host='10.225.138.125', port=6579, password='leadton@qwe', db=20); print('Redis 连接成功' if r.ping() else '连接失败')"
```

### 4. 后端启动选项

#### 开发模式（推荐）
```powershell
uvicorn app.main:app --reload --port 8000
```
- `--reload`: 代码修改自动重启
- `--port 8000`: 指定端口

#### 生产模式
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 指定配置文件
```powershell
$env:CONFIG_FILE="D:\path\to\config.yaml"
uvicorn app.main:app --reload
```

### 5. 前端启动选项

#### 默认启动
```powershell
npm run dev
```

#### 指定端口
```powershell
npm run dev -- --port 3000
```

#### 允许网络访问
```powershell
npm run dev -- --host
```

#### 构建生产版本
```powershell
npm run build
# 产物在 dist/ 目录
```

---

## 🔧 常用命令速查

### 后端命令

```powershell
# 进入后端目录
cd D:\00_ChAn_Workspace\AgenticOps\backend

# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 启动服务
uvicorn app.main:app --reload --port 8000

# 初始化数据库
python init_db.py

# 安装新依赖
pip install package_name

# 导出依赖
pip freeze > requirements.txt

# 退出虚拟环境
deactivate
```

### 前端命令

```powershell
# 进入前端目录
cd D:\00_ChAn_Workspace\AgenticOps\frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 代码检查
npm run lint
```

---

## 🐛 常见问题解决

### Q1: PowerShell 无法运行脚本

**错误信息**：
```
无法加载文件 .venv\Scripts\Activate.ps1，因为在此系统上禁止运行脚本
```

**解决方法**：
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2: 端口被占用

**错误信息**：
```
[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**解决方法**：
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000

# 结束进程（替换 PID）
taskkill /PID <进程ID> /F

# 或使用其他端口
uvicorn app.main:app --reload --port 8001
```

### Q3: MySQL 连接失败

**检查清单**：
1. MySQL 服务是否启动
2. 数据库 `kefu_ai` 是否创建
3. 用户名密码是否正确
4. 防火墙是否允许 3306 端口

**测试连接**：
```powershell
python -c "import pymysql; pymysql.connect(host='10.225.138.121', user='root', password='CAr8RvRA')"
```

### Q4: Redis 连接失败

**检查清单**：
1. Redis 服务是否启动
2. 密码是否正确
3. 端口是否正确（6579）

**测试连接**：
```powershell
python -c "import redis; r = redis.Redis(host='10.225.138.125', port=6579, password='leadton@qwe'); print(r.ping())"
```

### Q5: npm install 失败

**解决方法**：
```powershell
# 清理缓存
npm cache clean --force

# 删除 node_modules 和 package-lock.json
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json

# 重新安装
npm install

# 或使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

### Q6: 前端启动后白屏

**检查步骤**：
1. 打开浏览器开发者工具（F12）查看错误
2. 确认后端是否正常运行
3. 检查 `vite.config.ts` 中的代理配置
4. 清除浏览器缓存

---

## 📊 服务状态检查

### 后端健康检查
```powershell
# 命令行测试
curl http://localhost:8000/health

# 或访问
Invoke-WebRequest -Uri http://localhost:8000/health
```

**预期响应**：
```json
{"status": "healthy"}
```

### 前端访问检查
```powershell
# 检查服务是否启动
netstat -ano | findstr :5173
```

---

## 🎯 完整启动流程（一键脚本）

创建启动脚本 `start.ps1`：

```powershell
# start.ps1 - AgenticOps 启动脚本

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  AgenticOps 启动脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 启动后端
Write-Host "`n[1/2] 启动后端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\00_ChAn_Workspace\AgenticOps\backend; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"
Start-Sleep -Seconds 3

# 启动前端
Write-Host "[2/2] 启动前端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\00_ChAn_Workspace\AgenticOps\frontend; npm run dev"

Write-Host "`n✅ 服务启动完成！" -ForegroundColor Green
Write-Host "后端: http://localhost:8000" -ForegroundColor Green
Write-Host "前端: http://localhost:5173" -ForegroundColor Green
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "`n按任意键退出此窗口..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
```

**使用方法**：
```powershell
cd D:\00_ChAn_Workspace\AgenticOps
.\start.ps1
```

---

## 📚 后续学习

- **API 文档**: http://localhost:8000/docs
- **项目结构**: 查看 README.md
- **配置说明**: 查看 config.yaml.example
- **问题排查**: 查看 FIX_BCRYPT_ISSUE.md

---

**更新日期**: 2026-04-07  
**适用版本**: AgenticOps v1.0.0  
**维护者**: AgenticOps Team
