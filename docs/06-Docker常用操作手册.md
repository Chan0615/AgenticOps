# Docker 常用操作手册

AgenticOps Docker 部署的日常运维命令参考。

---

## 一、容器管理

### 查看状态

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（含已停止）
docker ps -a

# 查看 compose 管理的服务状态
docker compose ps
```

### 启停操作

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务（保留数据）
docker compose down

# 重启所有服务
docker compose restart

# 重启单个服务
docker compose restart app
docker compose restart worker
docker compose restart nginx

# 停止单个容器
docker stop agenticops-app

# 启动单个容器
docker start agenticops-app
```

### 强制删除

```bash
# 强制删除单个容器
docker rm -f agenticops-app

# 停止并删除所有 compose 容器
docker compose down

# 停止并删除所有 compose 容器 + 数据卷（⚠️ 会丢数据）
docker compose down -v
```

---

## 二、日志查看

```bash
# 实时查看日志
docker compose logs -f app         # API 日志
docker compose logs -f worker      # Worker 日志
docker compose logs -f beat        # Beat 日志
docker compose logs -f nginx       # Nginx 日志

# 查看最近 100 行
docker compose logs --tail=100 app

# 查看所有服务日志
docker compose logs -f

# 直接用 docker 查看
docker logs -f agenticops-app
docker logs --tail=50 agenticops-worker
```

---

## 三、进入容器

```bash
# 进入 app 容器（bash）
docker compose exec app bash

# 进入后可执行：
python init_db.py                    # 初始化数据库
python init_pgvector.py              # 初始化向量表
python add_dataquery_menu.py         # 添加智能问数菜单
python test_pgvector.py              # 测试 pgvector 连接

# 退出容器
exit

# 不进入容器，直接执行命令
docker compose exec app python init_pgvector.py
```

---

## 四、构建与更新

```bash
# 重新构建镜像（代码更新后）
docker compose build

# 构建并启动
docker compose up -d --build

# 强制不使用缓存构建（依赖变更时）
docker compose build --no-cache

# 只构建不启动
docker compose build app
```

---

## 五、镜像管理

```bash
# 查看本地镜像
docker images

# 查看 agenticops 相关镜像
docker images | grep agenticops

# 删除无用镜像（悬空镜像）
docker image prune -f

# 删除所有未使用的镜像（⚠️ 慎用）
docker image prune -a -f
```

---

## 六、数据卷管理

```bash
# 查看所有数据卷
docker volume ls

# 查看 agenticops 相关卷
docker volume ls | grep agenticops

# 查看卷详情（如挂载路径）
docker volume inspect agenticops_app_static

# ⚠️ 删除单个卷（会丢数据）
docker volume rm agenticops_app_static

# ⚠️ 删除所有未使用的卷
docker volume prune -f
```

---

## 七、网络管理

```bash
# 查看 compose 创建的网络
docker network ls | grep agenticops

# 查看网络内的容器
docker network inspect agenticops_default

# 容器间通信用容器名，如 app 容器访问 pgvector：
#   host: pgvector（全量模式）
#   host: 10.225.138.183（应用模式，用外部 IP）
```

---

## 八、端口排查

```bash
# 查看端口占用
ss -tlnp | grep -E '80|8000|9080|3306|5432|6379'

# 查看容器端口映射
docker port agenticops-nginx

# 端口冲突解决：改 .env 或启动时指定
HTTP_PORT=9090 docker compose up -d
```

---

## 九、资源监控

```bash
# 查看容器资源使用（CPU/内存）
docker stats

# 只看 agenticops 容器
docker stats agenticops-app agenticops-worker agenticops-beat agenticops-nginx

# 查看磁盘使用
docker system df
```

---

## 十、常见问题处理

### 容器反复重启

```bash
# 查看重启原因
docker compose logs --tail=50 app
docker inspect agenticops-app | grep -A 5 "State"
```

### 清理所有 agenticops 容器重新开始

```bash
# 1. 停止并删除所有容器
docker compose down

# 2. 如果还有残留
docker rm -f $(docker ps -a -q --filter "name=agenticops")

# 3. 清理旧镜像
docker image prune -f

# 4. 清理旧数据卷（⚠️ 会丢上传的文件）
docker volume rm $(docker volume ls -q --filter "name=agenticops")

# 5. 重新构建启动
docker compose up -d --build
```

### config.yaml 修改后生效

```bash
# config.yaml 是 readonly 挂载的，修改宿主机文件后重启即可
docker compose restart app worker beat
```

### 前端更新不生效

```bash
# 前端编译在 docker build 阶段，需要重新构建
docker compose build --no-cache
docker compose up -d

# 如果还不生效，清理静态文件卷
docker volume rm agenticops_app_static
docker compose up -d --build
```
