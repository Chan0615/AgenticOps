# PostgreSQL + pgvector 安装部署指南

本文档用于在 Linux 服务器上安装 PostgreSQL 16 + pgvector 扩展，供 AgenticOps RAG 知识库模块使用。

Windows 本地开发环境通过网络连接 Linux 上的 PostgreSQL。

---

## 方案选择

| 方案 | 适用场景 | 推荐度 |
|------|---------|--------|
| **方案 A：Docker 部署** | CentOS 7 等老系统、快速部署 | 强烈推荐 |
| **方案 B：Ubuntu/Debian 原生安装** | Ubuntu 20.04+ / Debian 11+ | 推荐 |
| **方案 C：CentOS 8+ / Rocky Linux 原生安装** | CentOS 8+ / Rocky 8+ / RHEL 8+ | 推荐 |

> **CentOS 7 用户注意**：PostgreSQL 官方已停止为 CentOS 7 提供 PG 16 软件包，
> YUM 源返回 `410 Gone` 错误。请直接使用 **方案 A（Docker 部署）**。

---

## 方案 A：Docker 部署（推荐）

适用于任何 Linux 发行版，一条命令完成安装，pgvector 扩展已内置。

### A.1 安装 Docker

如果服务器已有 Docker，跳过此步。

#### CentOS 7

```bash
# 安装依赖
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加阿里云 Docker 镜像源（官方源在 CentOS 7 上已不可用）
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo

# 安装 Docker
sudo yum makecache fast
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 如果上面报错，指定可用版本安装
# sudo yum install -y docker-ce-20.10.24 docker-ce-cli-20.10.24 containerd.io
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y docker.io
```

#### CentOS 8+ / Rocky Linux

```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io --allowerasing
```

#### 启动 Docker

```bash
sudo systemctl enable docker
sudo systemctl start docker
docker --version
```

### A.2 配置 Docker 镜像加速（可选，国内网络推荐）

```bash
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
"registry-mirrors": [
    "https://dockerpull.org",
    "https://docker.1panel.live",
    "https://docker.rainbond.cc"
  ]
}
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### A.3 启动 PostgreSQL + pgvector 容器

```bash
docker run -d \
  --name pgvector \
  --restart always \
  -e POSTGRES_USER=agenticops \
  -e POSTGRES_PASSWORD=agenticops123 \
  -e POSTGRES_DB=agenticops_vector \
  -p 5432:5432 \
  -v pgvector_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16
```

参数说明：
- `--restart always`：服务器重启后自动启动容器
- `-p 5432:5432`：映射端口，允许远程连接
- `-v pgvector_data`：数据持久化，删容器不丢数据

### A.4 启用 pgvector 扩展

```bash
# 等待容器启动完成（约 5 秒）
sleep 5

# 进入容器启用扩展
docker exec -it pgvector psql -U agenticops -d agenticops_vector -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 验证
docker exec -it pgvector psql -U agenticops -d agenticops_vector -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### A.5 防火墙放行

```bash
# CentOS/RHEL (firewalld)
sudo firewall-cmd --add-port=5432/tcp --permanent
sudo firewall-cmd --reload

# Ubuntu (ufw)
sudo ufw allow 5432/tcp

# 如果使用 iptables
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
```

### A.6 Docker 常用管理命令

```bash
# 查看容器状态
docker ps | grep pgvector

# 查看日志
docker logs pgvector

# 停止
docker stop pgvector

# 启动
docker start pgvector

# 进入 psql 交互
docker exec -it pgvector psql -U agenticops -d agenticops_vector

# 完全删除（数据保留在 volume 中）
docker rm -f pgvector

# 连 volume 一起删除（会丢数据！）
# docker rm -f pgvector && docker volume rm pgvector_data
```

**Docker 部署完成，跳到 [第六节：Windows 本地连接验证](#六windows-本地连接验证)。**

---

## 方案 B：Ubuntu / Debian 原生安装

### B.1 安装 PostgreSQL 16

```bash
# 添加 PostgreSQL 官方 APT 源
sudo apt update
sudo apt install -y gnupg2 lsb-release
echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
  | sudo tee /etc/apt/sources.list.d/pgdg.list
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo apt update

# 安装
sudo apt install -y postgresql-16 postgresql-client-16
```

### B.2 安装 pgvector 扩展

```bash
sudo apt install -y postgresql-16-pgvector
```

### B.3 启动服务

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### B.4 创建数据库和用户

```bash
sudo -u postgres psql
```

```sql
CREATE USER agenticops WITH PASSWORD 'agenticops123';
CREATE DATABASE agenticops_vector OWNER agenticops;
\c agenticops_vector
CREATE EXTENSION vector;
GRANT ALL ON SCHEMA public TO agenticops;
SELECT * FROM pg_extension WHERE extname = 'vector';
\q
```

### B.5 开启远程访问

```bash
# 修改监听地址
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" \
  /etc/postgresql/16/main/postgresql.conf

# 允许远程密码连接
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf

# 重启
sudo systemctl restart postgresql

# 防火墙放行
sudo ufw allow 5432/tcp
```

**原生安装完成，跳到 [第六节：Windows 本地连接验证](#六windows-本地连接验证)。**

---

## 方案 C：CentOS 8+ / Rocky Linux 原生安装

> CentOS 7 不适用此方案，请使用方案 A。

### C.1 安装 PostgreSQL 16

```bash
# 添加官方源
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# 禁用系统自带 PG 模块（避免冲突）
sudo dnf -qy module disable postgresql

# 安装
sudo dnf install -y postgresql16-server postgresql16
```

### C.2 安装 pgvector 扩展

```bash
sudo dnf install -y pgvector_16
```

### C.3 初始化并启动

```bash
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb
sudo systemctl enable postgresql-16
sudo systemctl start postgresql-16
sudo systemctl status postgresql-16
```

### C.4 创建数据库和用户

```bash
sudo -u postgres psql
```

```sql
CREATE USER agenticops WITH PASSWORD 'agenticops123';
CREATE DATABASE agenticops_vector OWNER agenticops;
\c agenticops_vector
CREATE EXTENSION vector;
GRANT ALL ON SCHEMA public TO agenticops;
SELECT * FROM pg_extension WHERE extname = 'vector';
\q
```

### C.5 开启远程访问

```bash
# 修改监听地址
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" \
  /var/lib/pgsql/16/data/postgresql.conf

# 允许远程密码连接
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /var/lib/pgsql/16/data/pg_hba.conf

# 重启
sudo systemctl restart postgresql-16

# 防火墙放行
sudo firewall-cmd --add-port=5432/tcp --permanent
sudo firewall-cmd --reload
```

---

## 六、Windows 本地连接验证

### 方法 1：使用 psql 命令行

```powershell
psql -h <Linux服务器IP> -p 5432 -U agenticops -d agenticops_vector
```

输入密码 `agenticops123`，能进入交互界面即成功。

验证 pgvector：

```sql
-- 创建测试表
CREATE TABLE test_vector (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(3)
);

-- 插入测试数据
INSERT INTO test_vector (content, embedding) VALUES
    ('hello', '[1,2,3]'),
    ('world', '[4,5,6]');

-- 向量相似度搜索
SELECT content, embedding <-> '[1,2,3]' AS distance
FROM test_vector
ORDER BY embedding <-> '[1,2,3]'
LIMIT 5;

-- 清理
DROP TABLE test_vector;
```

### 方法 2：使用 Python 验证

```powershell
pip install asyncpg pgvector
```

```python
import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        host="<Linux服务器IP>",
        port=5432,
        user="agenticops",
        password="agenticops123",
        database="agenticops_vector",
    )
    version = await conn.fetchval("SELECT version()")
    print(f"PostgreSQL: {version}")

    has_vector = await conn.fetchval(
        "SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'"
    )
    print(f"pgvector: {'已安装' if has_vector else '未安装'}")

    await conn.close()

asyncio.run(test())
```

### 方法 3：使用 GUI 工具

推荐使用：
- **DBeaver**（免费）：https://dbeaver.io/
- **pgAdmin 4**（官方）：https://www.pgadmin.org/
- **Navicat**（商业）

连接参数：

```
主机: <Linux服务器IP>
端口: 5432
数据库: agenticops_vector
用户名: agenticops
密码: agenticops123
```

---

## 七、AgenticOps 项目配置

安装验证通过后，在 `backend/config.yaml` 中添加 pgvector 配置：

```yaml
pgvector:
  host: "<Linux服务器IP>"
  port: 5432
  user: "agenticops"
  password: "agenticops123"
  database: "agenticops_vector"
```

---

## 八、常见问题排查

### 连接被拒绝 (Connection refused)

```bash
# 检查 PostgreSQL 是否在运行
docker ps | grep pgvector              # Docker 方案
sudo systemctl status postgresql       # Ubuntu 原生
sudo systemctl status postgresql-16    # CentOS 原生

# 检查是否监听 5432 端口
sudo ss -tlnp | grep 5432

# 检查 listen_addresses 配置（原生安装）
sudo -u postgres psql -c "SHOW listen_addresses;"
```

### 认证失败 (password authentication failed)

```bash
# Docker 方案：确认环境变量
docker inspect pgvector | grep POSTGRES

# 原生安装：重置密码
sudo -u postgres psql -c "ALTER USER agenticops WITH PASSWORD 'agenticops123';"

# 原生安装：检查 pg_hba.conf 是否有 md5 行
# Ubuntu
sudo grep -v '^#' /etc/postgresql/16/main/pg_hba.conf | grep -v '^$'
# CentOS
sudo grep -v '^#' /var/lib/pgsql/16/data/pg_hba.conf | grep -v '^$'
```

### pgvector 扩展创建失败

```bash
# Docker 方案：扩展已内置，直接创建即可
docker exec -it pgvector psql -U agenticops -d agenticops_vector \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Ubuntu 原生：确认包已安装
dpkg -l | grep pgvector
sudo apt install -y postgresql-16-pgvector

# CentOS 原生：确认包已安装
rpm -qa | grep pgvector
sudo dnf install -y pgvector_16
```

### 端口不通

```bash
# Windows 上测试连通性
Test-NetConnection -ComputerName <Linux服务器IP> -Port 5432

# Linux 上检查防火墙
sudo iptables -L -n | grep 5432
sudo firewall-cmd --list-ports     # CentOS
sudo ufw status                    # Ubuntu
```

### CentOS 7 YUM 报错 410 Gone

CentOS 7 已于 2024 年 6 月 30 日 EOL，PostgreSQL 官方不再提供 CentOS 7 的软件包。

**解决方案**：使用 Docker 部署（方案 A），不依赖系统包管理器。

### Docker 拉取镜像超时

```bash
# 配置镜像加速
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# 重新拉取
docker pull pgvector/pgvector:pg16
```
