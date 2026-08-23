# 6-SubmissionsController 控制器
SubmissionsController 是 Judge0 的核心 API 控制器，负责处理代码提交（Submission）的创建、查询、删除以及批量操作。作为 Rails 应用的关键入口点，该控制器协调前端请求与后端代码执行引擎之间的交互，是整个在线代码执行系统的请求调度中枢。

## 架构概览

SubmissionsController 遵循标准的 Rails RESTful 控制器设计模式，通过 `before_action` 钩子链实现认证、授权、参数校验和缓存控制等功能。该控制器继承自 ApplicationController，而 ApplicationController 又继承自 SessionsController，形成了完整的认证授权继承链。

```
flowchart TB
    subgraph "控制器继承链"
        A["SessionsController<br/>ActionController::API"] --> B["ApplicationController<br/>分页辅助方法"]
        B --> C["SubmissionsController<br/>提交管理核心"]
    end
    
    subgraph "请求生命周期"
        D["HTTP Request"] --> E["before_action 链"]
        E --> F{"参数验证"}
        F -->|通过| G["业务逻辑处理"]
        F -->|失败| H["错误响应"]
        G --> I["IsolateRunner<br/>任务调度"]
        I --> J["IsolateJob<br/>异步执行"]
        J --> K["Rails Cache<br/>结果缓存"]
        K --> L["JSON Response"]
    end
    
    C --> E
```

Sources: [submissions\_controller.rb](#root/4rilzSMevqYa) Sources: [sessions\_controller.rb](#root/QBGh58qWCMSV) Sources: [application\_controller.rb](#root/2X1Cdn9d3qNR)

## 路由配置

SubmissionsController 暴露了 6 个主要 API 端点，分别对应不同的提交管理功能。这些路由定义在 `config/routes.rb` 中，采用 Rails 标准资源路由语法：

```ruby
resources :submissions, only: [:index, :show, :create, :destroy], param: :token do
  post 'batch', to: 'submissions#batch_create', on: :collection
  get 'batch', to: 'submissions#batch_show', on: :collection
end
```

| HTTP 方法 | 端点 | Action | 功能描述 | 认证要求 |
| :---: | --- | --- | --- | --- |
| `GET` | `/submissions` | `index` | 分页获取提交列表 | 授权令牌 |
| `GET` | `/submissions/:token` | `show` | 根据 token 获取单个提交详情 | 无 |
| `POST` | `/submissions` | `create` | 创建新的代码提交 | 维护模式检查 |
| `DELETE` | `/submissions/:token` | `destroy` | 删除指定提交 | 授权令牌 |
| `POST` | `/submissions/batch` | `batch_create` | 批量创建提交 | 批量提交开关 |
| `GET` | `/submissions/batch` | `batch_show` | 批量获取提交 | 无 |

Sources: [routes.rb](#root/cfBH6k19XC28)

## 过滤器链设计

SubmissionsController 通过 `before_action` 定义了严格的请求处理流水线，每个过滤器负责特定的验证职责：

```
sequenceDiagram
    participant Client as 客户端
    participant Controller as SubmissionsController
    participant Auth as SessionsController
    participant Config as 配置检查
    
    Note over Client,Config: create/destroy 请求
    Client->>Controller: POST /submissions
    Controller->>Auth: check_maintenance
    Auth-->>Controller: 维护模式检查结果
    Controller->>Config: check_wait (仅create)
    Config-->>Controller: wait参数检查
    Controller->>Config: check_queue_size
    Config-->>Controller: 队列容量检查
    Controller->>Controller: check_requested_fields
    Controller->>Controller: set_base64_encoded
    
    Note over Client,Controller: index/destroy 请求
    Client->>Controller: GET /submissions
    Controller->>Auth: authorize_request
    Auth-->>Controller: 授权检查结果
    
    Note over Client,Controller: batch_* 请求
    Client->>Controller: POST /submissions/batch
    Controller->>Config: check_batched_submissions
    Config-->>Controller: 批量提交开关检查
```

**过滤器执行条件对照表：**

| 过滤器方法 | 执行时机 | 权限要求 | 适用 Action |
| --- | --- | --- | --- |
| `authorize_request` | 始终 | 授权令牌 | `index`, `destroy` |
| `check_maintenance` | 始终 | 无 | `create`, `destroy` |
| `check_wait` | 始终 | 无 | `create` |
| `check_batched_submissions` | 始终 | 无 | `batch_create`, `batch_show` |
| `check_queue_size` | 始终 | 无 | `create`, `batch_create` |
| `check_requested_fields` | 始终 | 无 | 除 `batch_create` 外全部 |
| `set_base64_encoded` | 始终 | 无 | 全部 |

Sources: [submissions\_controller.rb](#root/2BsjwOnRXYCV)

## 核心 Action 实现

### 创建提交（create）

`create` action 是系统最核心的方法，处理代码提交的创建请求。该方法支持同步（`wait=true`）和异步两种执行模式：

```
flowchart TD
    A["接收 submission_params"] --> B{"submission.save 成功?"}
    B -->|是| C{"@wait == true?"}
    B -->|否| Z["返回 422 错误"]
    C -->|是 同步模式| D["IsolateRunner.perform_now"]
    C -->|否 异步模式| E["IsolateRunner.perform_later"]
    D --> F["submission.reload"]
    F --> G["返回完整结果"]
    E --> H["仅返回 token"]
    G --> I{"编码异常?"}
    I -->|是| J["render_conversion_error"]
    I -->|否| K["render json: submission"]
    
    style D fill:#e1f5fe
    style E fill:#fff3e0
    style G fill:#e8f5e9
```

**关键实现细节：**

*   **异步模式**（默认）：调用 `IsolateRunner.perform_later(submission)` 将任务入队到 Resque 队列，立即返回 `token`，响应体仅包含 `[:token]` 字段
*   **同步模式**（`wait=true`）：调用 `IsolateRunner.perform_now(submission)` 阻塞等待执行完成，返回完整提交结果
*   **编码处理**：捕获 `Encoding::UndefinedConversionError` 异常，引导用户使用 `base64_encoded=true`

Sources: [submissions\_controller.rb](#root/OK44YZfbkCHi)

### 参数白名单（submission\_params）

`submission_params` 方法定义了 20 个允许传入的参数，严格过滤用户输入：

| 参数类别 | 参数名 | 类型 | 描述 |
| --- | --- | --- | --- |
| **必需** | `source_code` | text | 程序源代码 |
| **必需** | `language_id` | integer | 编程语言 ID |
| **执行控制** | `stdin` | text | 标准输入 |
| **执行控制** | `expected_output` | text | 期望输出（用于比对） |
| **编译选项** | `compiler_options` | string | 编译器选项（最大512字符） |
| **运行时** | `command_line_arguments` | string | 命令行参数（最大512字符） |
| **资源限制** | `cpu_time_limit` | decimal | CPU 时间限制（秒） |
| **资源限制** | `cpu_extra_time` | decimal | CPU 额外时间（秒） |
| **资源限制** | `wall_time_limit` | decimal | 墙钟时间限制（秒） |
| **资源限制** | `memory_limit` | integer | 内存限制（KB） |
| **资源限制** | `stack_limit` | integer | 栈大小限制（KB） |
| **资源限制** | `max_processes_and_or_threads` | integer | 最大进程/线程数 |
| **资源限制** | `max_file_size` | integer | 最大文件大小（KB） |
| **特性开关** | `enable_per_process_and_thread_time_limit` | boolean | 每进程时间限制 |
| **特性开关** | `enable_per_process_and_thread_memory_limit` | boolean | 每进程内存限制 |
| **输出控制** | `redirect_stderr_to_stdout` | boolean | stderr 重定向到 stdout |
| **网络控制** | `enable_network` | boolean | 启用网络访问 |
| **运行配置** | `number_of_runs` | integer | 执行次数（取平均值） |
| **回调机制** | `callback_url` | string | 完成回调 URL |
| **多文件支持** | `additional_files` | binary | Base64 编码的 ZIP 压缩包 |

Sources: [submissions\_controller.rb](#root/zEWS8LBwwzXA)

### 查询提交（show）

`show` action 使用 Rails Cache 实现提交结果的缓存读取，显著提升高频查询场景的性能：

```ruby
render json: Rails.cache.fetch("#{token}", 
  expires_in: Config::SUBMISSION_CACHE_DURATION, 
  race_condition_ttl: 0.1*Config::SUBMISSION_CACHE_DURATION) {
  Submission.find_by!(token: token)
}, base64_encoded: @base64_encoded, fields: @requested_fields
```

**缓存策略要点：**

*   **缓存键**：`token` 直接作为缓存键，避免重复查询数据库
*   **默认过期时间**：1 秒（可通过 `SUBMISSION_CACHE_DURATION` 配置）
*   **竞态条件处理**：`race_condition_ttl` 设置为过期时间的 10%，防止缓存击穿
*   **批量查询不适用**：缓存仅作用于单个提交查询，`batch_show` 不使用缓存

Sources: [submissions\_controller.rb](#root/BmI1NHxEDiKL)

### 批量操作（batch\_create / batch\_show）

批量操作通过 `check_batched_submissions` 过滤器控制开关，支持同时处理多个提交：

```
flowchart LR
    subgraph "batch_create 流程"
        A1["解析 submissions 数组"] --> A2{"数量 <= MAX_SUBMISSION_BATCH_SIZE?"}
        A2 -->|否| A3["返回 400 错误"]
        A2 -->|是| A4["遍历创建每个 Submission"]
        A4 --> A5{"save 成功?"}
        A5 -->|是| A6["入队 + 记录 token"]
        A5 -->|否| A7["记录 errors"]
        A6 --> A8["返回混合结果数组"]
        A7 --> A8
    end
    
    subgraph "batch_show 流程"
        B1["解析 tokens 字符串"] --> B2{"数量 <= MAX_SUBMISSION_BATCH_SIZE?"}
        B2 -->|否| B3["返回 400 错误"]
        B2 -->|是| B4["批量查询数据库"]
        B4 --> B5["构建结果数组"]
        B5 --> B6["返回 submissions 数组"]
    end
```

**批量操作约束：**

*   单批最大提交数：由 `MAX_SUBMISSION_BATCH_SIZE` 配置（默认 20）
*   **不支持同步模式**：批量创建不响应 `wait=true` 参数
*   **返回格式**：`batch_create` 返回混合数组（成功为 token，失败为 errors 对象）；`batch_show` 返回数组（含 nil 表示不存在的 token）

Sources: [submissions\_controller.rb](#root/2JCeY0rZawub) Sources: [submissions\_controller.rb](#root/FXSOgfPCrFSd)

### 删除提交（destroy）

`destroy` action 提供受控的提交删除功能，受多重条件限制：

```ruby
if submission.status == Status.queue || submission.status == Status.process
  render json: { error: "submission cannot be deleted because its status is #{submission.status.id}..." }, 
        status: :bad_request
  return
end
```

**删除条件检查流程：**

| 检查项 | 条件 | 结果 |
| --- | --- | --- |
| 功能开关 | `ENABLE_SUBMISSION_DELETE == false` | 拒绝删除，返回 400 |
| 提交状态 | `status == queue` | 拒绝删除，返回 400 |
| 提交状态 | `status == process` | 拒绝删除，返回 400 |
| 提交状态 | 其他状态 | 允许删除 |

Sources: [submissions\_controller.rb](#root/QJdVu2ulqMMs)

## 辅助检查方法

### 队列容量检查（check\_queue\_size）

```ruby
def check_queue_size
  number_of_submissions = params[:submissions].try(:size).presence || 1
  if Resque.size(ENV["JUDGE0_VERSION"]) + number_of_submissions > Config::MAX_QUEUE_SIZE
    render json: { error: "queue is full" }, status: :service_unavailable
  end
end
```

该方法防止队列过载，通过 Redis Resque 获取当前队列深度，结合请求的提交数量进行校验。批量请求会计算数组长度，单个请求默认为 1。

Sources: [submissions\_controller.rb](#root/7HnPqtRRvgzr)

### 字段过滤（check\_requested\_fields）

```ruby
def check_requested_fields
  fields_service = Fields::Submission.new(params[:fields])
  render json: { error: "invalid fields: [#{fields_service.invalid_fields.join(", ")}]" }, 
        status: :bad_request if fields_service.has_invalid_fields?
  @requested_fields = fields_service.requested_fields
end
```

字段过滤机制使用 `Fields::Submission` 服务类验证请求的字段列表，拒绝无效字段请求。

Sources: [submissions\_controller.rb](#root/igyITtse5RsZ) Sources: [fields/submission.rb](#root/eC7s4jGFR7tp)

### Base64 编码控制（set\_base64\_encoded）

```ruby
def set_base64_encoded
  if Config::DISABLE_IMPLICIT_BASE64_ENCODING
    @base64_encoded = params[:base64_encoded] == "true"
  else
    @base64_encoded = params[:base64_encoded] != "false"
  end
end
```

该方法实现灵活的 Base64 编码策略：

*   **默认启用**（`DISABLE_IMPLICIT_BASE64_ENCODING=false`）：除显式 `base64_encoded=false` 外均启用
*   **默认禁用**（`DISABLE_IMPLICIT_BASE64_ENCODING=true`）：仅显式 `base64_encoded=true` 时启用

Sources: [submissions\_controller.rb](#root/aVV2QGXGYH3H)

## 任务调度集成

SubmissionsController 通过 `IsolateRunner` 模块与后台任务系统解耦：

```
classDiagram
    class IsolateRunner {
        +MAX_WAIT_TIME_S = 600
        +perform_now(submission)
        +perform_later(submission)
    }
    
    class IsolateJob {
        +perform(submission_id)
        -compile()
        -run()
        -verify()
        -call_callback()
    }
    
    class Resque {
        +queue_as(version)
    }
    
    IsolateRunner --> IsolateJob : perform_later → enqueue
    IsolateRunner --> IsolateJob : perform_now → enqueue + poll
    IsolateJob --|> ApplicationJob
    ApplicationJob --> Resque
```

**IsolateRunner 模块职责：**

| 方法 | 功能 | 适用场景 |
| --- | --- | --- |
| `perform_later` | 更新状态为 `queue`，设置 `queued_at`，入队 `IsolateJob` | 异步提交（默认） |
| `perform_now` | 调用 `perform_later` 后轮询等待，最长 600 秒 | 同步等待结果 |

**轮询等待策略：**

```ruby
# 初始等待 2 秒，后续等待时间递增
wait_time = i == 0 ? 2 : (i == 1 ? 1 : 0.5 * i)
```

Sources: [isolate\_runner.rb](#root/TLSxBG03OMpp) Sources: [isolate\_job.rb](#root/cSJIQbIBkhL6)

## 响应序列化

提交结果通过 `SubmissionSerializer` 序列化，支持动态字段选择和 Base64 编码：

**默认返回字段：**

```ruby
@@default_fields ||= [
  :token, :time, :memory, :stdout, :stderr,
  :compile_output, :message, :status
]
```

**序列化特性：**

*   **动态编码**：根据 `@base64_encoded` 标志决定字段编码方式
*   **关联对象**：嵌套 `language` 和 `status` 对象信息
*   **字段过滤**：支持 `fields` 参数指定返回字段子集

Sources: [submission\_serializer.rb](#root/UFBiyF7ilYSA)

## 与后续模块的关联

```
flowchart TD
    SC["SubmissionsController"] --> SR["IsolateRunner"]
    SR --> IJ["IsolateJob"]
    IJ --> IS["Isolate Sandbox"]
    IJ --> CS["编译/运行"]
    IJ --> CB["Callback 回调"]
    
    SC -.->|查询| SM["Submission Model"]
    SC -.->|缓存| RC["Rails Cache"]
    SC -.->|队列| RQ["Resque/Redis"]
    
    SM --> DB["PostgreSQL"]
    RQ -->|后台处理| IJ
    
    IJ -->|结果写入| SM
    IJ -->|结果缓存| RC
```

SubmissionsController 作为请求入口点，协调 Submission 数据模型、IsolateRunner 任务调度器、IsolateJob 异步任务执行器共同完成代码执行功能。

---

**相关文档：**

*   [IsolateJob 沙箱执行任务](#root/aeMowSDVm5Nl) — 了解提交如何被实际执行
*   [IsolateRunner 任务调度器](#root/Bc8uFkRMEOzO) — 了解任务入队和同步等待机制
*   [Submission 数据模型与字段编码](#root/X4kCRfBobv9w) — 深入了解提交数据的存储结构
*   [创建提交 API](#root/7uEJEVhhnsck) — API 使用指南

## 相关条目
- [[5-系统架构设计]]
- [[11-创建提交 API]]
- [[8-IsolateRunner 任务调度器]]
