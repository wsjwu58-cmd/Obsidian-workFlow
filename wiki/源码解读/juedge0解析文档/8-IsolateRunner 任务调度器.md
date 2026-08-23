# 8-IsolateRunner 任务调度器
IsolateRunner 是 Judge0 中负责协调代码执行任务的**任务调度门面模块**，封装了异步任务的入队、状态管理和同步等待机制。作为 Rails 应用与 Resque 队列系统之间的桥梁，IsolateRunner 统一处理 `IsolateJob` 的调度逻辑，屏蔽了底层队列操作的复杂性。

## 核心架构

IsolateRunner 采用\*\*门面模式（Facade Pattern）\*\*设计，提供 `perform_now`（同步等待）和 `perform_later`（异步入队）两种任务调度接口。系统基于 Resque + Redis 构建分布式任务队列，支持多 worker 并行处理提交任务。

```
flowchart TB
    subgraph Client["客户端请求"]
        A[创建提交]
    end
    
    subgraph Controller["SubmissionsController"]
        B{wait 参数?}
    end
    
    subgraph IsolateRunner["IsolateRunner 模块"]
        C[perform_now<br/>同步等待]
        D[perform_later<br/>异步入队]
    end
    
    subgraph QueueSystem["任务队列系统"]
        E[(Redis<br/>队列)]
        F[Resque Scheduler]
        G[Resque Worker × N]
    end
    
    subgraph IsolateJob["IsolateJob"]
        H[沙箱初始化]
        I[编译阶段]
        J[运行阶段]
        K[结果验证]
    end
    
    subgraph Database["PostgreSQL"]
        L[Submission 记录]
    end
    
    A --> B
    B -->|wait=true| C
    B -->|wait=false| D
    C --> D
    D -->|update status: queue| L
    D -->|enqueue| E
    E --> G
    F -.->|调度| E
    G -->|perform| H
    H --> I --> J --> K
    K -->|update status| L
```

**关键源文件**: [app/helpers/isolate\_runner.rb](#root/CtRMH8Xpyx01), [app/jobs/isolate\_job.rb](#root/cSJIQbIBkhL6)

## 源码解析

### IsolateRunner 模块定义

IsolateRunner 定义在 `app/helpers/isolate_runner.rb` 中，是一个包含两个核心方法的 Ruby Module：

```ruby
module IsolateRunner
  MAX_WAIT_TIME_S = 600                    # 最大等待时间 10 分钟

  INITIAL_WAIT_TIME_S = 2                   # 首次等待 2 秒
  NEXT_WAIT_TIME_S = 1                      # 第二次等待 1 秒
  WAIT_TIME_FACTOR_S = 0.5                  # 后续等待因子

  WAITING_STATUSES = [Status.queue.id, Status.process.id, nil]  # 等待状态列表
```

Sources: [app/helpers/isolate\_runner.rb](#root/nd2lvvM4JRAA)

### perform\_later 异步入队

`perform_later` 方法将任务投入队列并更新数据库状态：

```ruby
def self.perform_later(submission)
  submission.update(status: Status.queue, queued_at: DateTime.now, queue_host: ENV["HOSTNAME"])
  IsolateJob.perform_later(submission.id)
end
```

该方法完成两个关键操作：

1.  **状态更新**：将提交状态设为 `queue`，记录入队时间和队列主机
2.  **任务入队**：调用 ActiveJob 将 IsolateJob 投入 Resque 队列

Sources: [app/helpers/isolate\_runner.rb](#root/ndLI5mVNr28C)

### perform\_now 同步等待

`perform_now` 方法实现同步等待模式，适用于需要立即获取结果的场景：

```ruby
def self.perform_now(submission)
  IsolateRunner.perform_later(submission)   # 先入队

  submission_id = submission.id
  total_wait_time = 0

  (0..).each do |i|
    break if total_wait_time >= MAX_WAIT_TIME_S    # 超时保护

    # 递增等待时间策略
    wait_time = if i == 0 then INITIAL_WAIT_TIME_S
                elsif i == 1 then NEXT_WAIT_TIME_S
                else WAIT_TIME_FACTOR_S * i
                end

    sleep(wait_time)
    total_wait_time += wait_time

    # 检查状态是否仍在等待列表
    break if !WAITING_STATUSES.include?(Submission.where(id: submission_id).pluck(:status_id).first)
  end
end
```

**等待时间策略**采用递增退避算法：

*   第 1 次轮询等待 2 秒
*   第 2 次轮询等待 1 秒
*   后续轮询等待时间 = `0.5 × 轮询次数` 秒

Sources: [app/helpers/isolate\_runner.rb](#root/p4IXSmQE19GF)

## 任务调度流程

### 控制器层调用

在 SubmissionsController 中，根据 `wait` 参数决定调度方式：

```ruby
def create
  submission = Submission.new(submission_params(params))
  
  if submission.save
    if @wait
      IsolateRunner.perform_now(submission)    # 同步模式
      submission.reload
      render json: submission, status: :created
    else
      IsolateRunner.perform_later(submission) # 异步模式
      render json: submission, status: :created, fields: [:token]
    end
  end
end
```

Sources: [app/controllers/submissions\_controller.rb](#root/OK44YZfbkCHi)

### IsolateJob 执行流程

IsolateJob 继承自 `ApplicationJob`（ActiveJob 基类），实现完整的代码执行流程：

```ruby
class IsolateJob < ApplicationJob
  retry_on RuntimeError, wait: 0.1.seconds, attempts: 100   # 自动重试配置

  queue_as ENV["JUDGE0_VERSION"].to_sym                    # 按版本号分队列

  def perform(submission_id)
    @submission = Submission.find(submission_id)
    submission.update(status: Status.process, started_at: DateTime.now, execution_host: ENV["HOSTNAME"])

    time = []
    memory = []

    submission.number_of_runs.times do
      initialize_workdir      # 初始化沙箱工作目录
      if compile == :failure   # 编译阶段
        cleanup
        return
      end
      run                      # 运行阶段
      verify                   # 结果验证

      time << submission.time
      memory << submission.memory

      cleanup
      break if submission.status != Status.ac  # 错误即停止
    end

    # 计算多次运行的平均值
    submission.time = time.inject(&:+).to_f / time.size
    submission.memory = memory.inject(&:+).to_f / memory.size
    submission.save
  end
end
```

Sources: [app/jobs/isolate\_job.rb](#root/X8seiCvhBJQO)

### 执行阶段详解

| 阶段 | 方法 | 功能 |
| --- | --- | --- |
| **初始化** | `initialize_workdir` | 创建沙箱目录结构、准备源代码和输入文件 |
| **编译** | `compile` | 调用编译器处理源代码，处理编译错误 |
| **运行** | `run` | 在 isolate 沙箱中执行程序，捕获输出和性能数据 |
| **验证** | `verify` | 解析执行元数据，确定最终状态 |
| **清理** | `cleanup` | 销毁沙箱环境，释放资源 |

Sources: [app/jobs/isolate\_job.rb](#root/HnrTEW7Vihpe)

## 状态机设计

### 状态流转

```
stateDiagram-v2
    [*] --> queue: perform_later
    queue --> process: Worker 取出任务
    process --> ac: Accepted
    process --> wa: Wrong Answer
    process --> tle: Time Limit
    process --> ce: Compilation Error
    process --> sigsegv: SIGSEGV
    process --> nzec: Non-Zero Exit
    process --> boxerr: Internal Error
    ac --> [*]
    wa --> [*]
    tle --> [*]
    ce --> [*]
    sigsegv --> [*]
    nzec --> [*]
    boxerr --> [*]
```

### 状态枚举定义

```ruby
class Status < Enumerations::Base
  values queue:     { id:  1, name: 'In Queue' },
         process:   { id:  2, name: 'Processing' },
         ac:        { id:  3, name: 'Accepted' },
         wa:        { id:  4, name: 'Wrong Answer' },
         tle:       { id:  5, name: 'Time Limit Exceeded' },
         ce:        { id:  6, name: 'Compilation Error' },
         sigsegv:   { id:  7, name: 'Runtime Error (SIGSEGV)' },
         sigxfsz:   { id:  8, name: 'Runtime Error (SIGXFSZ)' },
         sigfpe:    { id:  9, name: 'Runtime Error (SIGFPE)' },
         sigabrt:   { id: 10, name: 'Runtime Error (SIGABRT)' },
         nzec:      { id: 11, name: 'Runtime Error (NZEC)' },
         other:     { id: 12, name: 'Runtime Error (Other)' },
         boxerr:    { id: 13, name: 'Internal Error' },
         exeerr:    { id: 14, name: 'Exec Format Error' }
end
```

Sources: [app/enumerations/status.rb](#root/N5p1lYRhbgyz)

## Worker 进程管理

### Workers 启动脚本

```
#!/bin/bash
# scripts/workers

source ./scripts/load-config
export | sudo tee /api/environment

while [[ $run_resque -eq 1 ]]; do
    echo "[$(date_now)] Starting scheduler."
    rake resque:scheduler &                    # 启动定时调度器
    scheduler_pid=$!

    rm -rf tmp/pids/resque.pid &> /dev/null
    echo "[$(date_now)] Starting workers."
    rails resque:workers &                     # 启动 worker 进程池
    resque_pid=$!
    
    while ps -p $resque_pid > /dev/null; do sleep 1s; done
    echo "[$(date_now)] Workers are stopped."
done
```

Sources: [scripts/workers](#root/OfMhiuQ7jh0I)

### Worker 配置参数

| 参数 | 来源 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `COUNT` | `load-config` | `2 × CPU核数` | 并行 worker 数量 |
| `QUEUE` | `JUDGE0_VERSION` | 版本号 | 队列名称 |
| `INTERVAL` | `judge0.conf` | `0.1` 秒 | 轮询间隔 |
| `MAX_QUEUE_SIZE` | `judge0.conf` | `100` | 队列最大容量 |

Sources: [scripts/load-config](#root/xIm01Wi6vs8t)

### Docker Compose 服务架构

```yaml
services:
  server:
    image: judge0/judge0:latest
    command: ["./scripts/server"]
    ports:
      - "2358:2358"
    privileged: true

  worker:
    image: judge0/judge0:latest
    command: ["./scripts/workers"]
    privileged: true

  db:
    image: postgres:16.2

  redis:
    image: redis:7.2.4
```

Sources: [docker-compose.yml](#root/s3xdIB2NLhCi)

## 依赖技术栈

| 组件 | Gem | 版本 | 职责 |
| --- | --- | --- | --- |
| **Rails 框架** | rails | 6.1 | Web 应用框架 |
| **ActiveJob** | \- | 内置 | 异步任务抽象层 |
| **Resque** | resque | 2.6 | Redis 队列适配器 |
| **Resque Scheduler** | resque-scheduler | 4.10 | 定时任务调度 |
| **Redis** | redis | < 4.6 | 队列后端存储 |
| **PostgreSQL** | pg | 1.2 | 关系数据库 |

Sources: [Gemfile](#root/s74IKX3bCxyL)

## 关键设计决策

### 1\. 门面模式应用

IsolateRunner 作为门面，封装了直接操作 IsolateJob 和队列系统的复杂性。控制器无需了解：

*   队列选择逻辑
*   重试策略配置
*   等待轮询算法

### 2\. 指数退避等待

`perform_now` 采用渐进式等待策略：

*   初始等待 2 秒（应对快速任务）
*   后续等待递增（减少数据库查询压力）
*   最大等待时间 10 分钟保护

### 3\. 任务重试机制

```ruby
retry_on RuntimeError, wait: 0.1.seconds, attempts: 100
```

IsolateJob 配置了快速重试策略：失败后等待 100ms 重试，最多尝试 100 次，适用于瞬时故障恢复。

### 4\. 沙箱隔离执行

所有代码执行都通过 `isolate` 命令在独立沙箱中进行，支持：

*   cgroups 资源限制（CPU 时间、内存）
*   文件系统隔离
*   网络访问控制

## 相关文档

*   [IsolateJob 沙箱执行任务](#root/aeMowSDVm5Nl) - 详细了解沙箱操作底层实现
*   [SubmissionsController 控制器](#root/OaIZJ9wPL6PX) - 任务提交入口
*   [Submission 数据模型](#root/X4kCRfBobv9w) - 提交记录数据结构

## 相关条目
- [[7-IsolateJob 沙箱执行任务]]
- [[6-SubmissionsController 控制器]]
