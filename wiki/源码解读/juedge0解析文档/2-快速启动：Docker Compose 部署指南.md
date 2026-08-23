# 2-快速启动：Docker Compose 部署指南
本文档为初级开发者提供使用 Docker Compose 快速部署 Judge0 在线代码执行系统的完整指南。通过本指南，您将了解服务架构、配置方法，并成功运行一个可用于生产的 Judge0 实例。

Sources: [docker-compose.yml](#root/s3xdIB2NLhCi), [CHANGELOG.md](#root/DmfPs7LMLgOg)

---

## 服务架构概览

Judge0 采用微服务架构设计，通过 Docker Compose 实现各组件的容器化部署。理解服务间的交互关系是成功部署的关键前提。

### 核心服务组件

```
graph TB
    subgraph Docker Compose Services
        Client["客户端请求<br/>(Port 2358)"]
        
        subgraph Judge0 应用层
            Server["Server 服务<br/>Rails API 服务器"]
            Worker["Worker 服务<br/>代码执行工作器"]
        end
        
        subgraph 数据层
            Redis["Redis 7.2.4<br/>任务队列 & 缓存"]
            Postgres["PostgreSQL 16.2<br/>持久化存储"]
        end
    end
    
    Client --> Server
    Server --> Redis
    Server --> Postgres
    Worker --> Redis
    Worker --> Postgres
    
    style Client fill:#e1f5fe
    style Server fill:#c8e6c9
    style Worker fill:#fff9c4
    style Redis fill:#ffcdd2
    style Postgres fill:#d1c4e9
```

| 服务名称 | Docker 镜像 | 端口映射 | 核心功能 |
| --- | --- | --- | --- |
| **server** | `judge0/judge0:latest` | 2358:2358 | HTTP API 服务器，处理提交请求 |
| **worker** | `judge0/judge0:latest` | \- | 后台任务处理器，执行沙箱代码 |
| **db** | `postgres:16.2` | \- | PostgreSQL 数据库存储 |
| **redis** | `redis:7.2.4` | \- | Redis 消息队列和缓存 |

Sources: [docker-compose.yml](#root/s3xdIB2NLhCi)

### 服务职责说明

**Server 服务** 是 Rails 应用程序的入口点，运行 `/api/scripts/server` 脚本。它负责：

*   接收 HTTP JSON API 请求
*   将代码提交任务写入 Redis 队列
*   查询执行结果并返回给客户端

**Worker 服务** 运行 `/api/scripts/workers` 脚本，执行实际代码：

*   从 Redis 队列消费提交任务
*   调用 Isolate 沙箱环境执行代码
*   更新 PostgreSQL 中的执行结果状态

```
sequenceDiagram
    participant Client as 客户端
    participant Server as Server 服务
    participant Redis as Redis 队列
    participant Worker as Worker 服务
    participant DB as PostgreSQL

    Client->>Server: POST /submissions (代码提交)
    Server->>DB: 创建 Submission 记录
    Server->>Redis: 入队任务
    Server-->>Client: 返回 token
    
    Worker->>Redis: 监听任务队列
    Worker->>DB: 获取 Submission
    Worker->>Worker: 执行代码 (Isolate 沙箱)
    Worker->>DB: 更新执行结果
    Redis->>Worker: 推送新任务
    
    Client->>Server: GET /submissions/{token}
    Server->>DB: 查询结果
    Server-->>Client: 返回执行详情
```

Sources: [scripts/server](#root/dn3mAWwiSwVQ), [scripts/workers](#root/OfMhiuQ7jh0I)

---

## 部署前准备

在开始部署之前，请确保您的系统满足以下要求并完成必要的准备工作。

### 系统要求

| 要求类型 | 具体规格 |
| --- | --- |
| **操作系统** | Linux (推荐 Ubuntu 22.04) |
| **内存** | 最低 4GB RAM |
| **磁盘** | 至少 20GB 可用空间 |
| **软件** | Docker 20.10+, Docker Compose 2.0+ |

**重要提示**：Judge0 已在 Linux 环境下经过充分测试，Windows 环境可能无法正常运行沙箱功能。

Sources: [CHANGELOG.md](#root/dkawptNrX0G5)

### Ubuntu 22.04 特殊配置

Ubuntu 22.04 用户需要更新 GRUB 配置以支持 Docker 容器：

```
# 1. 编辑 GRUB 配置
sudo vim /etc/default/grub

# 2. 找到 GRUB_CMDLINE_LINUX 行，添加：
systemd.unified_cgroup_hierarchy=0

# 3. 更新 GRUB 并重启
sudo update-grub
sudo reboot
```

Sources: [CHANGELOG.md](#root/PS6BDkQTNVuo)

---

## 部署步骤

按照以下步骤完成 Judge0 的完整部署。

### 第一步：获取部署包

```
# 下载最新版本 v1.13.1
wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip

# 解压文件
unzip judge0-v1.13.1.zip
cd judge0-v1.13.1
```

Sources: [CHANGELOG.md](#root/p5EKEUbF3bqV)

### 第二步：生成安全密码

为 Redis 和 PostgreSQL 生成强密码（生产环境必须设置）：

| 服务 | 配置项 | 说明 |
| --- | --- | --- |
| Redis | `REDIS_PASSWORD` | 访问 Redis 的密码 |
| PostgreSQL | `POSTGRES_PASSWORD` | 数据库 root 密码 |

**推荐方法**：访问 [random.org](https://www.random.org/passwords/?num=1&len=32&format=plain&rnd=new) 生成 32 位随机密码。

Sources: [judge0.conf](#root/IYtktqdPlObm)

### 第三步：配置密码

编辑 `judge0.conf` 文件，填入生成的密码：

```
# 编辑配置文件
vim judge0.conf
```

找到并更新以下配置项：

```
# PostgreSQL Configuration
POSTGRES_PASSWORD=您的PostgreSQL密码

# Redis Configuration  
REDIS_PASSWORD=您的Redis密码
```

Sources: [judge0.conf](#root/IYtktqdPlObm)

### 第四步：启动服务

采用分阶段启动策略，确保数据库和缓存服务先就绪：

```
# 阶段 1：启动数据库和 Redis
docker-compose up -d db redis

# 等待初始化完成（约 10 秒）
sleep 10s

# 阶段 2：启动所有服务
docker-compose up -d

# 等待服务就绪（约 5 秒）
sleep 5s
```

Sources: [CHANGELOG.md](#root/zyOBQYz2IZfR)

### 第五步：验证部署

服务启动后，通过以下方式验证：

```
# 检查服务状态
docker-compose ps

# 访问 API 文档
# 浏览器打开: http://localhost:2358/docs
```

成功标志：

*   所有容器状态为 `Up`
*   访问 `http://localhost:2358/docs` 显示 API 文档页面

---

## 配置文件详解

`judge0.conf` 是 Judge0 的核心配置文件，采用 Shell 变量格式定义各项参数。

### 配置加载机制

```
flowchart LR
    A["judge0.conf"] --> B["load-config 脚本"]
    B --> C["环境变量导出"]
    C --> D["Rails/Rake 应用"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style D fill:#fff9c4
```

配置加载脚本会按以下优先级读取配置：

1.  `/api/judge0.conf` (容器内路径)
2.  `/judge0.conf` (Docker Compose 挂载路径)

Sources: [scripts/load-config](#root/CS2ahuBZZdhP)

### 核心配置项

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `RAILS_ENV` | production | Rails 运行环境 |
| `PORT` | 2358 | 服务监听端口 |
| `REDIS_HOST` | redis | Redis 服务主机名 |
| `POSTGRES_HOST` | db | PostgreSQL 主机名 |
| `POSTGRES_DB` | judge0 | 数据库名称 |
| `POSTGRES_USER` | judge0 | 数据库用户名 |
| `INTERVAL` | 0.1 | Worker 轮询间隔(秒) |
| `COUNT` | 2×nproc | Worker 并行数量 |
| `MAX_QUEUE_SIZE` | 100 | 最大队列长度 |

Sources: [scripts/load-config](#root/AvRhRCQrYm0p)

### 执行限制配置

这些配置控制用户代码的执行环境安全边界：

| 配置项 | 默认值 | 最大值 | 说明 |
| --- | --- | --- | --- |
| `CPU_TIME_LIMIT` | 5 秒 | 15 秒 | CPU 时间限制 |
| `WALL_TIME_LIMIT` | 10 秒 | 20 秒 | 墙上时钟限制 |
| `MEMORY_LIMIT` | 128000 KB | 512000 KB | 内存限制 |
| `MAX_PROCESSES_AND_OR_THREADS` | 60 | 120 | 进程/线程数 |
| `MAX_FILE_SIZE` | 1024 KB | 4096 KB | 文件大小限制 |

Sources: [judge0.conf](#root/wW1OdNNeDvBL)

---

## 开发环境部署

如果您需要参与 Judge0 开发，可以使用 `docker-compose.dev.yml` 配置文件。

### 开发模式与生产模式对比

| 特性 | 生产模式 | 开发模式 |
| --- | --- | --- |
| 镜像 | `judge0/judge0:latest` | `judge0/judge0:latest-dev` |
| 代码挂载 | 否 | 是 (`.:/api`) |
| 数据库迁移 | 自动 | 自动 |
| 调试端口 | 无 | 3001 (文档服务) |

Sources: [docker-compose.dev.yml](#root/e1dwIqyrl1bn)

### 启动开发环境

```
# 使用开发配置
docker-compose -f docker-compose.dev.yml up -d
```

开发模式会挂载本地源代码目录到容器，便于实时修改和调试。

---

## Docker Compose 服务配置

### 生产环境 docker-compose.yml 结构

```yaml
x-logging: &default-logging
  logging:
    driver: json-file
    options:
      max-size: 100M

services:
  server:
    image: judge0/judge0:latest
    volumes:
      - ./judge0.conf:/judge0.conf:ro
    ports:
      - "2358:2358"
    privileged: true
    <<: *default-logging
    restart: always

  worker:
    image: judge0/judge0:latest
    command: ["./scripts/workers"]
    volumes:
      - ./judge0.conf:/judge0.conf:ro
    privileged: true
    <<: *default-logging
    restart: always
```

Sources: [docker-compose.yml](#root/s3xdIB2NLhCi)

### 关键配置说明

**privileged 模式**：容器需要特权模式以运行 Isolate 沙箱，这是代码安全隔离的必要条件。

**配置卷挂载**：`./judge0.conf:/judge0.conf:ro` 将宿主机配置文件以只读方式挂载到容器。

**自动重启**：`restart: always` 确保服务在异常退出后自动恢复。

---

## 快速测试

部署完成后，使用以下命令测试 Judge0 API：

```
# 使用 curl 测试 Python 代码执行
curl \
  -H "Content-Type: application/json" \
  -d '{
      "language_id": 109,
      "source_code": "print(f\"hello, {input()}\")",
      "stdin": "World"
  }' \
  "http://localhost:2358/submissions?wait=true"
```

**参数说明**：

*   `language_id: 109` - Python 3 语言标识
*   `wait=true` - 同步等待执行结果
*   `source_code` - Base64 编码的源代码

---

## 常见问题排查

| 问题症状 | 可能原因 | 解决方案 |
| --- | --- | --- |
| 容器启动失败 | 缺少 GRUB 配置 | 参考 Ubuntu 22.04 配置步骤 |
| 连接 Redis 失败 | 密码未设置 | 检查 judge0.conf 中 REDIS\_PASSWORD |
| 连接 PostgreSQL 失败 | 密码未设置 | 检查 judge0.conf 中 POSTGRES\_PASSWORD |
| Worker 无法执行代码 | 容器未特权模式 | 确认使用 `privileged: true` |
| API 返回 500 | 数据库未初始化 | 等待 10 秒后再试 |

**健康检查**：

```
# 查看容器日志
docker-compose logs server
docker-compose logs worker

# 检查服务健康状态
docker-compose ps
```

---

## 后续学习路径

完成 Docker Compose 部署后，建议继续学习以下内容：

### 深入阅读

| 文档页面 | 内容简介 |
| --- | --- |
| [概述：开源在线代码执行系统](#root/f3nRVscLs2El) | Judge0 系统整体概念 |
| [Docker Compose 服务架构](#root/AnL4oyWjfbu7) | 服务间通信机制详解 |
| [配置文件详解](#root/04RUCISLtZxK) | judge0.conf 完整参数说明 |

### API 使用

| 文档页面 | 内容简介 |
| --- | --- |
| [创建提交 API](#root/7uEJEVhhnsck) | 提交代码执行请求 |
| [批量提交与查询 API](#root/suT9RnhiL443) | 批量处理提高效率 |
| [编程语言与状态枚举](#root/m4bhSPrC7v0y) | 支持的语言列表 |

---

## 参考资料

*   [Judge0 官方 GitHub](https://github.com/judge0/judge0)
*   [Judge0 官方网站](https://judge0.com)
*   [Isolate 沙箱文档](https://github.com/ioi/isolate)
*   [Docker Compose 官方文档](https://docs.docker.com/compose)

## 相关条目
- [[1-概述：开源在线代码执行系统]]
- [[17-Docker Compose 服务架构]]
- [[judge0 API调用]]
