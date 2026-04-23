# Docker 部署指南

使用 Docker Compose 部署 AgenticOps 应用服务。

## 前提条件

- Docker 20.10+
- Docker Compose v2+
- 服务器内存 2GB+（仅应用服务） / 4GB+（全量部署）

## 部署模式选择

| 模式 | 文件 | 说明 | 适用场景 |
|------|------|------|---------|
| **应用模式（默认）** | `docker-compose.yml` | 只部署 app/worker/beat/nginx，使用外部已有数据库 | 已有 MySQL/Redis/pgvector |
| **全量模式** | `docker-compose.full.yml` | 全部服务在 Docker 内运行，包括数据库 | 全新服务器 |

---

## 一、获取代码

```bash
# 方式 A：Git 克隆
git clone <your-repo-url> AgenticOps
cd AgenticOps

# 方式 B：本地打包上传（国内服务器推荐）
# ---- 本地 Windows/Mac 执行 ----
tar -czf AgenticOps.tar.gz \
  --exclude=node_modules --exclude=.venv \
  --exclude=__pycache__ --exclude=dist --exclude=.git \
  AgenticOps
scp AgenticOps.tar.gz root@<服务器IP>:/opt/

# ---- 服务器上执行 ----
cd /opt
tar -xzf AgenticOps.tar.gz
rm -f AgenticOps.tar.gz
cd AgenticOps
```

## 二、应用模式部署（使用外部数据库）

适用于已有 MySQL、Redis、pgvector 的情况。Docker 只跑应用服务。

### 2.1 准备配置文件

```bash
cp backend/config.yaml.example backend/config.yaml
vi backend/config.yaml
```

填入外部数据库的**真实 IP 地址**（不能用 `localhost`，容器内的 localhost 指向容器自己）：

```yaml
mysql:
  default:
    host: 10.225.138.121        # 外部 MySQL 真实 IP
    port: 3306
    user: root
    password: "your_password"
    database: kefu_ai

redis:
  default:
    host: 10.225.138.125        # 外部 Redis 真实 IP
    port: 6579
    password: "your_password"
    db: 20
    cache_prefix: agenticops_

pgvector:
  host: 10.225.138.183          # 外部 pgvector 真实 IP
  port: 5432
  user: agenticops
  password: "agenticops123"
  database: agenticops_vector

ai:
  qwen:
    enabled: true
    api_key: "sk-xxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model: "qwen-max"
```

### 2.2 启动

```bash
# 构建并启动（app + worker + beat + nginx）
docker compose up -d --build

# 查看状态（4 个服务都应该是 Up）
docker compose ps

# 首次部署：初始化数据库
docker compose exec app python init_db.py
docker compose exec app python init_pgvector.py
```

访问 `http://<服务器IP>:8080`，默认账号 `admin / admin123`。

### 2.3 服务列表

| 服务 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| app | agenticops-app | 8000 | FastAPI 后端 |
| worker | agenticops-worker | - | Celery Worker |
| beat | agenticops-beat | - | Celery Beat |
| nginx | agenticops-nginx | 8080 | Nginx 反向代理 |

---

## 三、全量模式部署（Docker 内自建数据库）

适用于全新服务器，所有服务全部在 Docker 内运行。

### 3.1 准备配置文件

```bash
cp backend/config.yaml.example backend/config.yaml
vi backend/config.yaml
```

数据库地址使用 **Docker 容器名**（Compose 内部网络自动解析）：

```yaml
mysql:
  default:
    host: mysql               # 容器名，不是 IP
    port: 3306
    user: root
    password: "agenticops123"
    database: kefu_ai

redis:
  default:
    host: redis               # 容器名
    port: 6379
    password: ""
    db: 0
    cache_prefix: agenticops

pgvector:
  host: pgvector              # 容器名
  port: 5432
  user: agenticops
  password: "agenticops123"
  database: agenticops_vector
```

### 3.2 启动

```bash
# 指定全量模式的 compose 文件
docker compose -f docker-compose.full.yml up -d --build

# 等待数据库健康检查通过（约 30 秒）
docker compose -f docker-compose.full.yml ps

# 首次部署：初始化
docker compose -f docker-compose.full.yml exec app python init_db.py
docker compose -f docker-compose.full.yml exec app python init_pgvector.py
```

### 3.3 全量模式服务列表

| 服务 | 容器名 | 端口 | 说明 |
|------|--------|------|------|
| app | agenticops-app | 8000 | FastAPI 后端 |
| worker | agenticops-worker | - | Celery Worker |
| beat | agenticops-beat | - | Celery Beat |
| nginx | agenticops-nginx | 8080 | Nginx 反向代理 |
| mysql | agenticops-mysql | 3306 | MySQL 主数据库 |
| redis | agenticops-redis | 6379 | Redis 队列 |
| pgvector | agenticops-pgvector | 5432 | pgvector 向量数据库 |

---

## 四、环境变量

通过 `.env` 文件自定义端口和密码（仅全量模式需要）：

```bash
cat <<'EOF' > .env
# MySQL（全量模式）
MYSQL_ROOT_PASSWORD=agenticops123
MYSQL_DATABASE=kefu_ai
MYSQL_PORT=3306

# Redis（全量模式）
REDIS_PORT=6379

# pgvector（全量模式）
PG_USER=agenticops
PG_PASSWORD=agenticops123
PG_DATABASE=agenticops_vector
PG_PORT=5432

# Nginx 对外端口
HTTP_PORT=8080
EOF
```

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MYSQL_ROOT_PASSWORD` | `agenticops123` | MySQL root 密码 |
| `MYSQL_DATABASE` | `kefu_ai` | MySQL 数据库名 |
| `MYSQL_PORT` | `3306` | MySQL 对外端口 |
| `REDIS_PORT` | `6379` | Redis 对外端口 |
| `PG_USER` | `agenticops` | pgvector 用户名 |
| `PG_PASSWORD` | `agenticops123` | pgvector 密码 |
| `PG_DATABASE` | `agenticops_vector` | pgvector 数据库名 |
| `PG_PORT` | `5432` | pgvector 对外端口 |
| `HTTP_PORT` | `8080` | Nginx 对外 HTTP 端口 |

> `.env` 中的变量只影响 `docker-compose.yml` 的占位符，后端应用读的是 `config.yaml`，两者需要对应。

---

## 五、常用命令

```bash
# 启动
docker compose up -d

# 停止
docker compose down

# 重启单个服务
docker compose restart app

# 查看日志
docker compose logs -f app
docker compose logs -f worker
docker compose logs -f beat

# 进入容器
docker compose exec app bash

# 查看状态
docker compose ps
```

## 六、更新部署

```bash
# 方式 A：Git 更新
git pull

# 方式 B：本地打包上传
# 本地: tar + scp
# 服务器:
cp backend/config.yaml /tmp/config.yaml.bak    # 备份配置
tar -xzf AgenticOps.tar.gz                      # 解压覆盖
cp /tmp/config.yaml.bak backend/config.yaml     # 恢复配置

# 重新构建并启动
docker compose build
docker compose up -d

# 运行增量迁移（如果有新模块）
docker compose exec app python add_dataquery_menu.py
docker compose exec app python init_pgvector.py
```

## 七、数据持久化

| Volume | 说明 |
|--------|------|
| `app_uploads` | 上传的文档文件 |
| `app_logs` | 应用日志 |
| `mysql_data` | MySQL 数据（全量模式） |
| `redis_data` | Redis 数据（全量模式） |
| `pgvector_data` | pgvector 向量数据（全量模式） |

```bash
# 查看 volume
docker volume ls | grep agenticops

# ⚠️ 完全清理（包括数据，慎用）
docker compose down -v
```

## 八、HTTPS

在宿主机上安装 Nginx + Certbot，反向代理到 Docker 的 8080 端口：

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

# Nginx 配置
cat <<'EOF' | sudo tee /etc/nginx/sites-available/agenticops
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # SSE 支持
        proxy_buffering off;
        proxy_read_timeout 3600s;
    }

    client_max_body_size 50m;
}
EOF

sudo ln -sf /etc/nginx/sites-available/agenticops /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 自动配置 SSL
sudo certbot --nginx -d your-domain.com
```

## 九、问题排查

### 容器状态为 Created 但没有 Up

```bash
# 查看失败原因
docker compose logs <服务名>

# 常见原因：端口被占用
# 解决：修改 .env 中的端口，或停掉占用端口的服务
docker compose down
# 修改端口后重新启动
docker compose up -d
```

### 数据库连接失败

- **应用模式**：确认 `config.yaml` 中的 host 是外部数据库的**真实 IP**，不是 `localhost`
- **全量模式**：确认 `config.yaml` 中的 host 是**容器名**（`mysql` / `redis` / `pgvector`）
- 容器内 `127.0.0.1` 指向容器自己，不是宿主机

### 端口冲突

```bash
# 查看端口占用
ss -tlnp | grep -E '3306|6379|5432|8080'

# 修改 .env 避开冲突端口
HTTP_PORT=9090
```

### 构建失败

```bash
# 查看构建日志
docker compose build --no-cache

# 清理旧镜像
docker image prune -f
```
