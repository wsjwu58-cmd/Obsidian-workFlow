# 3-提交（Submission）核心概念
**提交（Submission）** 是 Judge0 中最核心的概念，它代表一次完整的代码执行请求。当你向 Judge0 发送代码并指定编程语言和运行时约束时，系统会创建一个 Submission 对象来跟踪和管理这个代码执行的全生命周期。

本文档面向初级开发者，帮助你理解 Submission 的数据结构、状态流转、关键字段含义，以及它在 Judge0 系统中的角色定位。

## Submission 是什么？

从数据模型角度来看，Submission 是 `submissions` 数据库表中的一条记录，映射到 `app/models/submission.rb` 中定义的 `Submission` 类。它封装了代码执行所需的所有信息：从源代码本身，到输入数据，再到执行结果和性能指标。

从业务逻辑角度来看，Submission 代表了 Judge0 系统处理代码执行请求的完整生命周期——从创建、排队、执行、验证，到最终返回结果。这个生命周期由 `SubmissionsController` 控制器、`IsolateRunner` 异步任务调度器和 `IsolateJob` 沙箱执行任务共同完成。

```
flowchart LR
    subgraph Client["客户端"]
        Create[创建提交]
        Query[查询结果]
    end
    
    subgraph Judge0API["Judge0 API 层"]
        Controller[SubmissionsController]
        Serializer[SubmissionSerializer]
    end
    
    subgraph Processing["处理层"]
        Queue[Resque 队列]
        Runner[IsolateRunner]
        Job[IsolateJob]
    end
    
    subgraph Sandbox["沙箱环境"]
        Isolate[Isolate 沙箱]
        Metadata[元数据文件]
    end
    
    Create --> Controller
    Query --> Controller
    Controller --> Serializer
    Controller -->|入队| Queue
    Queue --> Runner
    Runner --> Job
    Job -->|执行| Isolate
    Isolate --> Metadata
    
    Serializer -.->|缓存| Query
```

Sources: [submission.rb](#root/xyZP6XEe0p90), [submissions\_controller.rb](#root/kOTDrdYjt8ea), [isolate\_job.rb](#root/peGbUvuRhtSS)

## Submission 数据结构

一个 Submission 包含 33 个属性，这些属性可分为三大类：**创建时必需的属性**、**可选的配置变量**，以及**执行后填充的结果属性**。

### 必需属性

这两个属性是创建 Submission 时必须提供的，它们定义了要执行的代码和目标语言。

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `source_code` | 文本 | 程序的源代码（单文件程序必需） |
| `language_id` | 整数 | 编程语言的 ID，可在[语言配置模型](#root/m4bhSPrC7v0y)中查看支持的完整语言列表 |

```ruby
# submission.rb 中定义的验证逻辑
validates :source_code, presence: true, unless: -> { is_project }
validates :language_id, presence: true
```

Sources: [submission.rb](#root/9xZV9Z0SbhbZ)

### 配置变量（17个）

配置变量允许你自定义代码执行的运行时约束。系统为每个配置项都设置了默认值，同时也定义了允许的最大值以防止资源滥用。

| 属性名 | 类型 | 单位 | 默认值 | 最大值 | 说明 |
| --- | --- | :---: | :---: | :---: | --- |
| `cpu_time_limit` | 小数 | 秒 | 5 | 15 | CPU 时间限制，OS 调度任务的时间不计入 |
| `cpu_extra_time` | 小数 | 秒 | 1 | 5 | 超时后等待的额外时间，用于报告真实执行时间 |
| `wall_time_limit` | 小数 | 秒 | 10 | 20 | 墙上时钟限制，程序等待外部事件时也会计时 |
| `memory_limit` | 整数 | KB | 128000 | 512000 | 程序地址空间限制 |
| `stack_limit` | 整数 | KB | 64000 | 128000 | 进程栈大小限制 |
| `max_processes_and_or_threads` | 整数 | \- | 60 | 120 | 程序可创建的最大进程/线程数 |
| `max_file_size` | 整数 | KB | 1024 | 4096 | 程序可创建/修改的文件大小限制 |
| `number_of_runs` | 整数 | \- | 1 | 20 | 重复执行次数，用于取平均值 |
| `enable_per_process_and_thread_time_limit` | 布尔 | \- | false | \- | 是否对每个进程/线程单独计时 |
| `enable_per_process_and_thread_memory_limit` | 布尔 | \- | false | \- | 是否对每个进程/线程单独限制内存 |
| `redirect_stderr_to_stdout` | 布尔 | \- | false | \- | 是否将标准错误重定向到标准输出 |
| `enable_network` | 布尔 | \- | false | \- | 是否允许程序访问网络 |

```ruby
# 默认值设置逻辑
def set_defaults
  self.status ||= Status.queue
  self.number_of_runs ||= Config::NUMBER_OF_RUNS
  self.cpu_time_limit ||= Config::CPU_TIME_LIMIT
  self.memory_limit ||= Config::MEMORY_LIMIT
  # ... 其他默认值
end
```

Sources: [submission.rb](#root/6e6pTTn9RkOy), [judge0.conf](#root/PpWJVgAr4Mlr)

### 结果属性（12个）

这些属性在代码执行完成后由系统填充，包含了程序的实际运行结果。

| 属性名 | 类型 | 单位 | 说明 |
| --- | --- | :---: | --- |
| `stdout` | 文本 | \- | 程序的标准输出 |
| `stderr` | 文本 | \- | 程序的标准错误输出 |
| `compile_output` | 文本 | \- | 编译器输出（仅编译型语言） |
| `exit_code` | 整数 | \- | 程序退出码 |
| `exit_signal` | 整数 | \- | 程序接收的信号码 |
| `message` | 文本 | \- | 状态消息或错误信息 |
| `time` | 小数 | 秒 | 程序实际运行时间 |
| `wall_time` | 小数 | 秒 | 墙上时钟时间 |
| `memory` | 整数 | KB | 程序使用的内存 |
| `status` | 对象 | \- | 提交状态（见下节） |
| `created_at` | 日期时间 | \- | 提交创建时间 |
| `finished_at` | 日期时间 | \- | 提交完成时间 |

```ruby
# 验证方法中填充结果的示例
submission.time = metadata[:time]
submission.memory = (cgroups.present? ? metadata[:"cg-mem"] : metadata[:"max-rss"])
submission.status = determine_status(metadata[:status], submission.exit_signal)
```

Sources: [isolate\_job.rb](#root/aOoIeb1x2MHY), [submission\_serializer.rb](#root/UFBiyF7ilYSA)

## Submission 状态枚举

状态（Status）是 Submission 执行过程中反映程序运行结果的关键指标。Judge0 定义了 14 种不同的状态，通过 `app/enumerations/status.rb` 中的枚举类进行管理。

```
stateDiagram-v2
    [*] --> InQueue: 创建提交
    InQueue --> Processing: 取出执行
    Processing --> Accepted: 正常退出且输出匹配
    Processing --> WrongAnswer: 正常退出但输出不匹配
    Processing --> TimeLimitExceeded: 超时
    Processing --> CompilationError: 编译失败
    Processing --> RuntimeError: 程序异常退出
    Processing --> InternalError: 沙箱内部错误
    
    note right of RuntimeError
        包括 SIGSEGV、SIGXFSZ
        SIGFPE、SIGABRT、NZEC
    end note
```

| 状态 ID | 状态名称 | 含义 | 触发条件 |
| :---: | --- | --- | --- |
| 1 | In Queue | 排队中 | 提交刚创建，等待被执行 |
| 2 | Processing | 处理中 | 正在编译或执行代码 |
| 3 | Accepted | 通过 | 程序正常结束且输出与预期匹配 |
| 4 | Wrong Answer | 答案错误 | 程序正常结束但输出与预期不匹配 |
| 5 | Time Limit Exceeded | 超时 | CPU 时间超过限制 |
| 6 | Compilation Error | 编译错误 | 编译阶段失败 |
| 7 | Runtime Error (SIGSEGV) | 运行时错误 | 段错误（非法内存访问） |
| 8 | Runtime Error (SIGXFSZ) | 运行时错误 | 文件大小超出限制 |
| 9 | Runtime Error (SIGFPE) | 运行时错误 | 浮点异常（除零等） |
| 10 | Runtime Error (SIGABRT) | 运行时错误 | 程序主动调用 abort() |
| 11 | Runtime Error (NZEC) | 运行时错误 | 非零退出码 |
| 12 | Runtime Error (Other) | 运行时错误 | 其他运行时错误 |
| 13 | Internal Error | 内部错误 | Judge0 系统内部错误 |
| 14 | Exec Format Error | 格式错误 | 可执行文件格式错误 |

```ruby
class Status < Enumerations::Base
  values queue:     { id:  1, name: 'In Queue' },
         process:   { id:  2, name: 'Processing' },
         ac:        { id:  3, name: 'Accepted' },
         wa:        { id:  4, name: 'Wrong Answer' },
         tle:       { id:  5, name: 'Time Limit Exceeded' },
         ce:        { id:  6, name: 'Compilation Error' },
         # ... 更多状态定义
end
```

Sources: [status.rb](#root/N5p1lYRhbgyz), [isolate\_job.rb](#root/0m31vf4ZSAWF)

## Submission 生命周期

理解 Submission 的生命周期对于正确使用 Judge0 API 至关重要。从创建到获取结果，整个流程涉及多个组件的协作。

```
sequenceDiagram
    participant Client as 客户端
    participant API as SubmissionsController
    participant Queue as Resque 队列
    participant Job as IsolateJob
    participant Sandbox as Isolate 沙箱
    
    Client->>+API: POST /submissions<br/>{source_code, language_id}
    API->>API: 验证参数<br/>生成 UUID token
    API->>API: 保存到数据库
    API->>+Queue: IsolateRunner.perform_later
    API-->>-Client: 201 Created<br/>{token: "xxx"}
    
    Queue->>+Job: 执行任务
    Job->>Job: 更新状态为 Processing
    Job->>Sandbox: 初始化沙箱目录
    Sandbox-->>Job: 工作目录路径
    
    alt 编译型语言
        Job->>Sandbox: 编译源代码
        Sandbox-->>Job: compile_output
        alt 编译失败
            Job->>Job: 设置状态为 CE
            Job->>Job: 清理沙箱
            Job-->>-Queue: 完成
        end
    end
    
    Job->>Sandbox: 执行程序
    Sandbox-->>Job: stdout, stderr, metadata
    
    Job->>Job: 验证输出
    Job->>Job: 更新 status, time, memory
    Job->>Job: 清理沙箱
    
    alt 有回调 URL
        Job->>Client: PUT callback_url
    end
    
    Job-->>-Queue: 完成
    
    Note over Client,Queue: 轮询获取结果
    Client->>API: GET /submissions/{token}
    API-->>Client: 完整结果
```

### 各阶段详解

**1\. 创建阶段（Create）** 当你调用 `POST /submissions` 接口时，系统首先验证请求参数的合法性，然后为提交生成一个唯一的 UUID token，并将其保存到数据库中。

```ruby
# 创建成功后返回 token
def create
  submission = Submission.new(submission_params(params))
  if submission.save
    IsolateRunner.perform_later(submission)
    render json: submission, status: :created, fields: [:token]
  else
    render json: submission.errors, status: :unprocessable_entity
  end
end
```

**2\. 排队阶段（Queue）** 提交被放入 Resque 队列等待执行。队列大小可以通过 `MAX_QUEUE_SIZE` 配置项限制。

**3\. 执行阶段（Processing）** `IsolateJob` 从队列中取出提交，依次执行以下步骤：初始化沙箱目录、解压附加文件、编译（如需要）、运行程序、收集元数据、验证输出。

**4\. 完成阶段（Finished）** 执行完成后，系统更新提交的所有结果字段，并通过缓存返回给后续的查询请求。

Sources: [submissions\_controller.rb](#root/OK44YZfbkCHi), [isolate\_job.rb](#root/peGbUvuRhtSS), [submissions.md](#root/qmtANSWmlcS8)

## Token 机制

每个 Submission 都有一个唯一的 `token`（UUID 格式），用于后续查询结果。这个 token 在提交创建时自动生成，保证了在高并发场景下的唯一性。

```ruby
def generate_token
  begin
    self.token = SecureRandom.uuid
  end while self.class.exists?(token: token)
end
```

查询结果时，系统会优先从 Rails 缓存中读取，以减少数据库压力：

```ruby
def show
  token = params[:token]
  render json: Rails.cache.fetch("#{token}", 
    expires_in: Config::SUBMISSION_CACHE_DURATION, 
    race_condition_ttl: 0.1*Config::SUBMISSION_CACHE_DURATION) {
    Submission.find_by!(token: token)
  }, base64_encoded: @base64_encoded, fields: @requested_fields
end
```

Sources: [submission.rb](#root/JgDkTSAMDKtn), [submissions\_controller.rb](#root/BmI1NHxEDiKL)

## Base64 编码处理

由于代码内容可能包含二进制数据或无法直接 JSON 序列化的字符，Judge0 使用 Base64 编码来处理这类情况。模型会自动在 getter 和 setter 中进行编解码。

```ruby
def source_code
  @decoded_source_code ||= Base64Service.decode(self[:source_code])
end

def source_code=(value)
  super(value)
  self[:source_code] = Base64Service.encode(self[:source_code])
end
```

| 字段 | 是否支持 Base64 |
| --- | --- |
| `source_code` | ✅ 支持 |
| `stdin` | ✅ 支持 |
| `expected_output` | ✅ 支持 |
| `stdout` | ✅ 支持 |
| `stderr` | ✅ 支持 |
| `compile_output` | ✅ 支持 |

Sources: [submission.rb](#root/5o0R6xGcEV5p), [base64\_service.rb](#root/e4k3IpEqkiGz)

## 单文件与多文件程序

Judge0 支持两种类型的程序执行方式，这通过 `additional_files` 属性来区分。

| 类型 | source\_code | additional\_files | 说明 |
| --- | :---: | :---: | --- |
| 单文件程序 | ✅ 必需 | ❌ 可选 | 只有一个源文件，使用预定义的编译/运行脚本 |
| 多文件程序 | ❌ 禁用 | ✅ 必需 | 所有文件通过 ZIP 包上传，可自定义编译/运行脚本 |

多文件程序的语言 ID 为 89（称为 "Multi-file program"），需要在 ZIP 包中包含 `compile` 和 `run` 两个可执行脚本。

Sources: [submission.rb](#root/KqHXyaQH8nf3), [submissions.md](#root/3g2cGfr174GO)

## 后续学习路径

完成本篇核心概念学习后，建议按以下顺序继续深入：

1.  [**编程语言与状态枚举**](#root/m4bhSPrC7v0y) - 了解 Language 模型和完整的 Status 枚举定义
2.  [**SubmissionsController 控制器**](#root/OaIZJ9wPL6PX) - 深入学习提交相关的 API 端点实现
3.  [**IsolateJob 沙箱执行任务**](#root/aeMowSDVm5Nl) - 理解代码如何在沙箱中安全执行
4.  [**创建提交 API**](#root/7uEJEVhhnsck) - 实际动手调用 API 创建你的第一个提交

## 快速参考表

| API 端点 | 方法 | 说明 |
| --- | :---: | --- |
| `/submissions` | POST | 创建单个提交 |
| `/submissions/batch` | POST | 批量创建提交 |
| `/submissions/{token}` | GET | 查询单个提交结果 |
| `/submissions/batch` | GET | 批量查询提交结果 |
| `/submissions` | GET | 分页列出所有提交 |
| `/submissions/{token}` | DELETE | 删除已完成的提交 |

## 相关条目
- [[1-概述：开源在线代码执行系统]]
- [[4-编程语言与状态枚举]]
- [[9-Submission 数据模型与字段编码]]
