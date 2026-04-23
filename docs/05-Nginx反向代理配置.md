# AgenticOps Nginx 部署模板（前端静态 + /api 反向代理）

本文提供可直接落地的 Nginx 配置：
- 前端静态资源：`/opt/AgenticOps/frontend/dist`
- 后端 API：`http://127.0.0.1:8000`
- 路由约定：`/api/*` 转发到后端，其余走前端 SPA

## 1) 前置条件

- 前端已构建：

```bash
cd /opt/AgenticOps/frontend
npm install
npm run build
```

- 后端已运行在 `127.0.0.1:8000`（建议由 systemd 托管）。
- 服务器已安装 Nginx。

## 2) 站点配置（HTTP 版）

将以下内容保存为 `/etc/nginx/conf.d/agenticops.conf`：

```nginx
server {
    listen 80;
    server_name _;

    # 前端静态目录
    root /opt/AgenticOps/frontend/dist;
    index index.html;

    # 上传体积（按需调整）
    client_max_body_size 50m;

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 兼容流式输出/长连接（如后续 SSE 或 WebSocket）
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 3600;
        proxy_send_timeout 3600;
        proxy_buffering off;
    }

    # 前端静态缓存（按需可调整）
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff2?)$ {
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
        try_files $uri =404;
    }

    # SPA 路由回退
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 3) 启用配置

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 4) HTTPS（推荐）

若已绑定域名，建议使用 Certbot：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your.domain.com
```

## 5) 常见问题排查

- 访问前端 404：确认 `root` 指向 `frontend/dist` 且已执行 `npm run build`。
- `/api` 502：确认后端进程存在并监听 `127.0.0.1:8000`。
- 刷新页面 404：确认 `location /` 存在 `try_files ... /index.html`。
- 跨域问题：前后端同域部署一般不会触发跨域；若跨域部署，检查后端 CORS 配置。

## 6) 与本项目契约

- 前端 API 基础路径为 `/api`。
- 本地开发 Vite 代理也是 `/api -> 8000`，生产 Nginx 保持同路径可避免环境差异。
