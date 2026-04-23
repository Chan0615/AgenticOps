# Docker 部署指南

使用 Docker Compose 一键部署 AgenticOps 全栈服务。

## 前提条件

- Docker 20.10+
- Docker Compose v2+
- 服务器内存 4GB+

## 一、快速开始

```bash
# 1. 克隆代码
git clone <your-repo-url> AgenticOps
cd AgenticOps

# 2. 准备配置文件
cp backend/config.yaml.example backend/config.yaml
```

编辑 `backend/config.yaml`，**将数据库地址改为 Docker 容器名**：

```yaml
mysql:
  default:
    host: mysql          # Docker 容器名，不是 IP
    port: 3306
    user: root
    password: "agenticops123"
    database: kefu_ai

redis:
  default:
    host: redis          # Docker 容器名
    port: 6379
    password: ""         # Docker 默认无密码
    db: 0
    cache_prefix: agenticops

pgvector:
  host: pgvector         # Docker 容器名
  port: 5432
  user: agenticops
  password: "agenticops123"
  database: agenticops_vector

# AI 配置照常填写
ai:
  qwen:
    enabled: true
    api_key: "sk-xxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model: "qwen-max"
```

```bash
# 3. 启动所有服务
docker compose up -d

# 4. 等待所有服务就绪（约 30 秒）
docker compose ps

# 5. 初始化数据库（首次部署）
docker compose exec app python init_db.py

# 6. 初始化 pgvector 向量表
docker compose exec app python init_pgvector.py
```

访问 `http://<server-ip>`，默认账号 `admin / admin123`。

## 二、服务说明

| 服务 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| app | agenticops-app | 8000 | FastAPI 后端 |
| worker | agenticops-worker | - | Celery Worker（任务执行） |
| beat | agenticops-beat | - | Celery Beat（定时调度） |
| mysql | agenticops-mysql | 3306 | MySQL 主数据库 |
| redis | agenticops-redis | 6379 | Redis 队列 |
| pgvector | agenticops-pgvector | 5432 | pgvector 向量数据库 |
| nginx | agenticops-nginx | 80 | Nginx 反向代理 |

## 三、环境变量

可通过 `.env` 文件或环境变量自定义端口和密码：

```bash
# .env 文件（放在项目根目录）
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=kefu_ai
MYSQL_PORT=3306

REDIS_PORT=6379

PG_USER=agenticops
PG_PASSWORD=your_password
PG_DATABASE=agenticops_vector
PG_PORT=5432

HTTP_PORT=80
```

## 四、常用命令

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务
docker compose down

# 查看日志
docker compose logs -f app       # API 日志
docker compose logs -f worker    # Worker 日志
docker compose logs -f beat      # Beat 日志

# 进入容器
docker compose exec app bash

# 重启单个服务
docker compose restart app
docker compose restart worker

# 重新构建（代码更新后）
docker compose build
docker compose up -d

# 查看服务状态
docker compose ps
```

## 五、数据持久化

所有数据通过 Docker Volume 持久化，删除容器不会丢失数据：

| Volume | 说明 |
|--------|------|
| `mysql_data` | MySQL 数据文件 |
| `redis_data` | Redis 持久化数据 |
| `pgvector_data` | pgvector 向量数据 |
| `app_uploads` | 上传的文档文件 |
| `app_logs` | 应用日志 |

```bash
# 查看 volume
docker volume ls | grep agenticops

# ⚠️ 完全清理（包括数据）
docker compose down -v
```

## 六、更新部署

```bash
cd AgenticOps

# 拉取最新代码
git pull

# 重新构建并启动
docker compose build
docker compose up -d

# 运行迁移脚本（如果有新模块）
docker compose exec app python add_dataquery_menu.py
docker compose exec app python init_pgvector.py
```

## 七、使用外部数据库

如果你已有 MySQL / Redis / PostgreSQL，不需要 Docker Compose 里的数据库服务。

编辑 `docker-compose.yml`，注释掉 `mysql`、`redis`、`pgvector` 服务，并删除 `app` 和 `worker` 的 `depends_on` 部分。

在 `backend/config.yaml` 中填入外部数据库的真实 IP 和端口。

## 八、HTTPS

### 方法 A：前置 Nginx + Certbot

在宿主机上安装 Nginx + Certbot，反向代理到 Docker 的 80 端口：

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 方法 B：Traefik

将 `docker-compose.yml` 中的 nginx 服务替换为 Traefik，自动管理 SSL 证书。

## 九、问题排查

### 容器启动失败

```bash
# 查看具体错误
docker compose logs app
docker compose logs mysql

# MySQL 未就绪时 app 会报连接错误，等待 healthcheck 通过后重试
docker compose restart app
```

### 数据库连接失败

确认 `config.yaml` 中的 host 使用的是 Docker 容器名（如 `mysql`）而不是 `localhost` 或外部 IP。

### 端口冲突

如果 3306/6379/5432/80 端口被占用，在 `.env` 文件中修改映射端口：

```bash
MYSQL_PORT=3307
REDIS_PORT=6380
PG_PORT=5433
HTTP_PORT=8080
```
