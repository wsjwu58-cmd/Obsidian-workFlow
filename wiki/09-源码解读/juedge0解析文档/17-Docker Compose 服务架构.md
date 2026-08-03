# 17-Docker Compose 服务架构
本文档深入解析 Judge0 基于 Docker Compose 的微服务架构设计，涵盖生产环境与开发环境的部署拓扑、服务间通信机制以及配置管理体系。

## 服务架构概览

Judge0 采用经典的 **Web-Worker 分离架构**，通过 Docker Compose 实现服务的容器化部署。该架构将 HTTP 请求处理与计算密集型的代码执行任务解耦，确保系统在高并发场景下的稳定性和可扩展性。

```
graph TB
    subgraph Docker Network
        Client["客户端请求<br/>(:2358)"]
        
        subgraph judge0-master
            Server["server 服务<br/>Rails API Server<br/>(Puma)"]
            Worker["worker 服务<br/>Resque Workers<br/>(代码执行)"]
        end
        
        subgraph 数据层
            Redis["redis 服务<br/>Redis 7.2.4<br/>(Job Queue)"]
            DB["db 服务<br/>PostgreSQL 16.2<br/>(持久化存储)"]
        end
    end
    
    Client -->|"HTTP/REST API"| Server
    Server -->|"写入 Submission| Redis
    Redis -->|"Dequeue| Worker
    Worker -->|"查询/更新| DB
    Server -->|"查询状态| DB
```

Sources: [docker-compose.yml](#root/s3xdIB2NLhCi)

## 核心服务详解

### 1\. Server 服务（API 网关）

Server 服务是 Judge0 的核心入口，负责接收客户端请求并提供 RESTful API 接口。

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| 镜像 | `judge0/judge0:latest` | 基于自定义 Dockerfile 构建 |
| 端口映射 | `2358:2358` | 外部访问端口 |
| 启动命令 | `/api/scripts/server` | Rails 服务器启动脚本 |
| 特权模式 | `privileged: true` | 必需用于 isolate 沙箱 |
| 重启策略 | `always` | 容器异常退出后自动重启 |

启动脚本 `/api/scripts/server` 执行以下操作：

```
source ./scripts/load-config           # 加载 judge0.conf 配置
export | sudo tee /api/environment    # 将环境变量注入容器
rails db:create db:migrate db:seed    # 初始化数据库（首次启动）
rails s -b 0.0.0.0                     # 启动 Puma 服务器
```

Sources: [scripts/server](#root/dn3mAWwiSwVQ)

### 2\. Worker 服务（异步任务处理）

Worker 服务运行 Resque 后台任务处理器，负责从 Redis 队列中获取提交任务并执行代码。

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| 镜像 | `judge0/judge0:latest` | 与 server 相同镜像 |
| 启动命令 | `./scripts/workers` | Resque worker 启动脚本 |
| 并行度 | `2 × nproc` | 默认根据 CPU 核心数扩展 |
| 轮询间隔 | `0.1 秒` | 队列检查频率 |

Worker 启动脚本架构：

```
flowchart LR
    A[启动 Scheduler] --> B[启动 Workers]
    B --> C{监控进程}
    C -->|Worker 退出| D[重新启动]
    C -->|收到 SIGTERM| E[优雅关闭]
```

Sources: [scripts/workers](#root/OfMhiuQ7jh0I)

### 3\. Database 服务（PostgreSQL）

PostgreSQL 提供关系型数据存储，保存提交记录、语言配置、用户认证等核心数据。

| 配置项 | 值 |
| --- | --- |
| 镜像 | `postgres:16.2` |
| 数据卷 | `data:/var/lib/postgresql/data/` |
| 环境配置 | `env_file: judge0.conf` |
| 重启策略 | `always` |

Sources: [docker-compose.yml](#root/fZHdEz37JOCC)

### 4\. Redis 服务（消息队列）

Redis 作为 Resque 的后端存储，负责管理任务队列的元数据和待处理任务。

| 配置项 | 值 |
| --- | --- |
| 镜像 | `redis:7.2.4` |
| 持久化 | `appendonly no`（禁用 AOF） |
| 认证 | `requirepass $REDIS_PASSWORD` |
| 默认主机名 | `redis`（Docker Compose 服务名） |

Sources: [docker-compose.yml](#root/EIRnQSYmzApT)

## 服务间通信机制

### 网络拓扑

所有服务通过 Docker 默认网络进行通信。服务发现依赖 Docker Compose 的内置 DNS 机制：

```yaml
# server/worker 连接数据库
POSTGRES_HOST=db        # 指向 PostgreSQL 容器

# server/worker 连接队列
REDIS_HOST=redis       # 指向 Redis 容器
```

Sources: [judge0.conf](#root/Kr8XM7y6jQFz)

### 数据库连接配置

Rails 通过 `database.yml` 从环境变量读取数据库连接参数：

```yaml
# config/database.yml
adapter: postgresql
host: <%= ENV["POSTGRES_HOST"] %>      # 默认值: db
port: <%= ENV["POSTGRES_PORT"] %>      # 默认值: 5432
database: <%= ENV["POSTGRES_DB"] %>    # 默认值: postgres
username: <%= ENV["POSTGRES_USER"] %>  # 默认值: postgres
password: <%= ENV["POSTGRES_PASSWORD"] %>
pool: <%= [1, ENV["RAILS_SERVER_PROCESSES"].to_i * ENV["RAILS_MAX_THREADS"].to_i].max %>
```

Sources: [config/database.yml](#root/T1lfA6w6uar4)

### Resque 队列配置

Resque 在 `config/initializers/resque.rb` 中初始化 Redis 连接：

```ruby
Resque.redis = Redis.new(
  host:     ENV["REDIS_HOST"],           # 默认: localhost
  port:     ENV["REDIS_PORT"],           # 默认: 6379
  password: ENV["REDIS_PASSWORD"],
  thread_safe: true
)

Resque.redis.namespace = ENV["RESQUE_NAMESPACE"].to_sym if ENV["RESQUE_NAMESPACE"].present?
```

Sources: [config/initializers/resque.rb](#root/e1KwtsGhS5oZ)

## 配置管理体系

### 配置文件加载流程

```
sequenceDiagram
    participant Host as 宿主机
    participant Container as Docker 容器
    participant Script as load-config
    participant Judge0 as judge0.conf
    
    Host->>Container: 挂载 ./judge0.conf -> /judge0.conf
    Container->>Script: 执行 /api/scripts/server
    Script->>Judge0: source /judge0.conf
    Judge0->>Script: 导出环境变量
    Script->>Container: export | sudo tee /api/environment
```

配置加载脚本按以下优先级查找配置文件：

```
if [[ -f /api/judge0.conf ]]; then
    CONFIG_FILE=/api/judge0.conf           # 开发环境（挂载卷）
elif [[ -f /judge0.conf ]]; then
    CONFIG_FILE=/judge0.conf                # 生产环境（环境变量挂载）
fi
```

Sources: [scripts/load-config](#root/pb7I0luJZvnb)

### 关键配置参数

#### 服务器配置

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `RESTART_MAX_TRIES` | 10 | 启动失败重试次数 |
| `MAINTENANCE_MODE` | false | 维护模式开关 |
| `ENABLE_WAIT_RESULT` | true | 同步等待结果 |
| `SUBMISSION_CACHE_DURATION` | 1 | 缓存时长（秒） |

#### Worker 配置

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `INTERVAL` | 0.1 | 轮询间隔（秒） |
| `COUNT` | 2×nproc | 并行 worker 数量 |
| `MAX_QUEUE_SIZE` | 100 | 最大队列长度 |

Sources: [judge0.conf](#root/Hil5DbwGUjcl)

## 开发环境架构

开发环境使用独立的 `docker-compose.dev.yml`，采用不同的部署策略：

```yaml
# docker-compose.dev.yml
services:
  judge0:
    build:
      context: .
      target: development      # 多阶段构建：development
    volumes:
      - .:/api                 # 代码热重载
    ports:
      - "2358:2358"            # API 端口
      - "3001:3001"            # 文档服务端口
```

Sources: [docker-compose.dev.yml](#root/e1dwIqyrl1bn)

### 生产与开发环境对比

| 特性 | 生产环境 | 开发环境 |
| --- | --- | --- |
| 镜像 | `judge0/judge0:latest` | `judge0/judge0:latest-dev` |
| 架构 | Server + Worker 分离 | 单容器多进程 |
| 代码更新 | 需重新构建 | 卷挂载热重载 |
| Rails 环境 | `production` | `development` |
| 服务分离 | 4 个独立容器 | 3 个容器（合并 server/worker） |

## 日志与监控

所有服务采用统一的日志配置：

```yaml
x-logging: &default-logging
  logging:
    driver: json-file
    options:
      max-size: 100M            # 单个日志文件最大 100MB
```

Sources: [docker-compose.yml](#root/3nK60C8g1QXW)

## 下一步

完成服务架构学习后，建议继续阅读：

*   [配置文件详解](#root/04RUCISLtZxK) — 深入了解 `judge0.conf` 各配置项
*   [安全机制与沙箱隔离](#root/SmNOpSGJhyCw) — 了解 `isolate` 沙箱的工作原理
*   [性能调优与扩展](#root/iFoQwfI9w09y) — 掌握水平扩展与性能优化策略

## 相关条目
- [[2-快速启动：Docker Compose 部署指南]]
- [[16-配置文件详解]]
- [[19-性能调优与扩展]]
