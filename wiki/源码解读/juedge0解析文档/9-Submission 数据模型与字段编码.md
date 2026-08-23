# 9-Submission 数据模型与字段编码
本文档详细阐述 Judge0 系统中 **Submission（提交）** 数据模型的核心架构、字段设计及其 Base64 编码机制。作为代码执行系统的核心实体，Submission 承载着从源码提交到结果返回的完整生命周期管理。

## 数据模型概览

Submission 是 Judge0 系统中处理代码执行请求的核心模型。它通过 `active_record` 与 PostgreSQL 数据库交互，并在 `IsolateJob` 的配合下完成沙箱环境中的代码编译与执行。

```
classDiagram
    class Submission {
        +integer id
        +text source_code
        +integer language_id
        +text stdin
        +text expected_output
        +text stdout
        +integer status_id
        +decimal time
        +integer memory
        +string token
        +datetime created_at
        +datetime finished_at
        +string compiler_options
        +string command_line_arguments
        +boolean enable_network
        +binary additional_files
    }
    
    class Language {
        +integer id
        +string name
        +string compile_cmd
        +string run_cmd
        +boolean is_archived
    }
    
    class Status {
        +integer id
        +string name
        <<enumeration>>
    }
    
    class IsolateJob {
        +perform(submission_id)
        +compile()
        +run()
        +verify()
    }
    
    class Base64Service {
        +encode(text)
        +decode(text)
    }
    
    Submission --> Language : belongs_to
    Submission --> Status : belongs_to
    IsolateJob --> Submission : processes
    Submission --> Base64Service : uses encoding
```

Sources: [submission.rb](#root/AAjrqXr6Cgij), [schema.rb](#root/1lY0ZQnYIraM)

## 核心字段分类

Submission 表包含 38 个字段，按功能可划分为以下五大类别：

| 类别 | 字段 | 说明 |
| --- | --- | --- |
| **标识与关联** | `id`, `token`, `language_id`, `status_id` | 唯一标识与关联关系 |
| **代码与输入输出** | `source_code`, `stdin`, `expected_output`, `stdout`, `stderr`, `compile_output` | 代码执行的核心数据 |
| **执行资源限制** | `cpu_time_limit`, `cpu_extra_time`, `wall_time_limit`, `memory_limit`, `stack_limit` | 资源配额控制 |
| **执行结果** | `time`, `memory`, `exit_code`, `exit_signal`, `message`, `wall_time` | 执行后的度量数据 |
| **生命周期管理** | `created_at`, `queued_at`, `started_at`, `finished_at`, `updated_at`, `queue_host`, `execution_host` | 状态追踪 |

Sources: [schema.rb](#root/1lY0ZQnYIraM)

## Base64 编码机制

### 设计原理

Judge0 采用 Base64 编码处理所有文本数据字段，以支持二进制安全传输和特殊字符处理。这一机制确保了代码源码、标准输入输出等数据在 HTTP 传输过程中的完整性和可靠性。

```
flowchart LR
    subgraph ClientSide
        A[原始源码] -->|UTF-8 编码| B[Base64 编码字符串]
        C[原始输入] -->|UTF-8 编码| D[Base64 编码字符串]
    end
    
    subgraph Transport
        B -->|HTTP POST| E[API Gateway]
        D -->|HTTP POST| E
    end
    
    subgraph ServerSide
        E -->|存储前| F[Base64Service.decode]
        F --> G[(数据库)]
        G -->|读取后| H[Base64Service.decode]
        H --> I[解码后数据]
    end
    
    style ClientSide fill:#e1f5fe
    style ServerSide fill:#f3e5f5
    style Transport fill:#fff3e0
```

### 编码服务实现

`Base64Service` 模块提供了简洁的编解码接口，应用于所有文本类型的存取操作：

```ruby
module Base64Service
  def self.encode(text)
    return nil unless text
    Base64.encode64(text)
  end

  def self.decode(text)
    return nil unless text
    Base64.decode64(text)
  end
end
```

Sources: [base64\_service.rb](#root/vJ6mfmqlYK4r)

### 模型层自动编解码

Submission 模型通过自定义 getter/setter 方法，在数据存取层面透明地处理编码转换：

```ruby
# 源码字段示例 - 其他字段模式相同
def source_code
  @decoded_source_code ||= Base64Service.decode(self[:source_code])
end

def source_code=(value)
  super(value)
  self[:source_code] = Base64Service.encode(self[:source_code])
end
```

此模式应用于以下字段：

*   `source_code` - 源代码内容
*   `stdin` - 标准输入数据
*   `stdout` - 标准输出结果
*   `expected_output` - 期望输出（用于比对）
*   `stderr` - 标准错误输出
*   `compile_output` - 编译输出信息

Sources: [submission.rb](#root/zJ5r3Oz1FMYj)

### API 响应编码控制

序列化器支持通过 `base64_encoded` 参数控制响应格式：

```ruby
def object_decoder(method)
  instance_options[:base64_encoded] ? object[method] : object.send(method)
end
```

当 `base64_encoded=true` 时，返回原始 Base64 编码数据；否则返回解码后的可读文本。

Sources: [submission\_serializer.rb](#root/lzx87QVwh869)

## 状态枚举与执行状态机

### 状态定义

Status 枚举定义了代码执行的完整状态集合：

| ID | 状态码 | 名称 | 含义 |
| --- | --- | --- | --- |
| 1 | queue | In Queue | 等待处理 |
| 2 | process | Processing | 正在执行 |
| 3 | ac | Accepted | 执行成功且结果正确 |
| 4 | wa | Wrong Answer | 结果不正确 |
| 5 | tle | Time Limit Exceeded | 超出时间限制 |
| 6 | ce | Compilation Error | 编译错误 |
| 7 | sigsegv | Runtime Error (SIGSEGV) | 内存段错误 |
| 8 | sigxfsz | Runtime Error (SIGXFSZ) | 文件大小超出限制 |
| 9 | sigfpe | Runtime Error (SIGFPE) | 浮点运算错误 |
| 10 | sigabrt | Runtime Error (SIGABRT) | 异常中止 |
| 11 | nzec | Runtime Error (NZEC) | 非零退出码 |
| 12 | other | Runtime Error (Other) | 其他运行时错误 |
| 13 | boxerr | Internal Error | 沙箱内部错误 |
| 14 | exeerr | Exec Format Error | 可执行文件格式错误 |

Sources: [status.rb](#root/oVg2OAh41oKn)

### 状态转换逻辑

IsolateJob 中的 `determine_status` 方法根据 Isolate 沙箱返回的元数据确定最终状态：

```ruby
def determine_status(status, exit_signal)
  case status
  when "TO" then Status.tle           # Time Limit Exceeded
  when "SG" then Status.find_runtime_error_by_status_code(exit_signal)
  when "RE" then Status.nzec          # Non Zero Exit Code
  when "XX" then Status.boxerr         # Internal Error
  else
    # 比较输出与期望输出
    if submission.expected_output.nil? || strip(expected_output) == strip(stdout)
      Status.ac
    else
      Status.wa
    end
  end
end
```

Sources: [isolate\_job.rb](#root/f2Qa2Bd7kx1A)

## 执行配置参数

### 时间限制配置

| 参数 | 类型 | 默认值 | 最大值 | 说明 |
| --- | --- | --- | --- | --- |
| `cpu_time_limit` | decimal | 5.0 秒 | 15.0 秒 | CPU 时间限制 |
| `cpu_extra_time` | decimal | 1.0 秒 | 5.0 秒 | 额外缓冲时间 |
| `wall_time_limit` | decimal | 10.0 秒 | 20.0 秒 | 墙上时间限制 |

Sources: [config.rb](#root/6OtOD21rE8Z8)

### 内存与存储限制

| 参数 | 类型 | 默认值 | 最大值 | 说明 |
| --- | --- | --- | --- | --- |
| `memory_limit` | integer | 128000 KB | 512000 KB | 内存限制 |
| `stack_limit` | integer | 64000 KB | 128000 KB | 栈空间限制 |
| `max_file_size` | integer | 1024 KB | 4096 KB | 最大文件大小 |
| `max_processes_and_or_threads` | integer | 60 | 120 | 最大进程/线程数 |

Sources: [config.rb](#root/Flg689luQrXa)

### 安全控制参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable_per_process_and_thread_time_limit` | boolean | false | 启用进程级时间限制 |
| `enable_per_process_and_thread_memory_limit` | boolean | false | 启用进程级内存限制 |
| `redirect_stderr_to_stdout` | boolean | false | 将 stderr 重定向到 stdout |
| `enable_network` | boolean | false | 启用网络访问 |
| `number_of_runs` | integer | 1 | 执行次数 |

Sources: [submission.rb](#root/SCsDgdafmJFP), [config.rb](#root/QtJD39NV0qHl)

## Token 生成与唯一性保证

每个 Submission 通过 `before_create` 回调自动生成唯一 token：

```ruby
before_create :generate_token

def generate_token
  self.token = SecureRandom.hex
end
```

Token 作为 API 访问的唯一标识符，存储在数据库中并建立了索引以确保查询性能：

```ruby
t.index ["token"], name: "index_submissions_on_token"
```

Sources: [submission.rb](#root/73N0T1nj1zEb), [schema.rb](#root/1wsKM2UPzDl6)

## 生命周期时间戳

Submission 记录了完整的处理生命周期：

| 字段 | 说明 |
| --- | --- |
| `created_at` | 提交创建时间 |
| `queued_at` | 进入任务队列时间 |
| `started_at` | 开始执行时间 |
| `finished_at` | 执行完成时间 |
| `updated_at` | 最后更新时间 |
| `queue_host` | 接收提交的服务器 |
| `execution_host` | 执行提交的服务器 |

这些时间戳对于性能监控、队列分析和问题排查至关重要。

Sources: [schema.rb](#root/9dprz1dyE3nu)

## 回调机制

当提交执行完成后，系统支持向指定的回调 URL 发送结果通知：

```ruby
def call_callback
  return unless submission.callback_url.present?
  
  serialized_submission = ActiveModelSerializers::SerializableResource.new(
    submission,
    { serializer: SubmissionSerializer, base64_encoded: true }
  ).to_json
  
  Config::CALLBACKS_MAX_TRIES.times do
    begin
      HTTParty.put(submission.callback_url, body: serialized_submission)
      break
    rescue Exception
      # 重试逻辑
    end
  end
end
```

回调功能可通过环境变量 `ENABLE_CALLBACKS=false` 禁用，默认为启用状态。

Sources: [isolate\_job.rb](#root/MBMz7Zblgiep), [config.rb](#root/wXGWLNgaFfzV)

## 完整执行流程

```
sequenceDiagram
    participant Client as 客户端
    participant API as SubmissionsController
    participant DB as 数据库
    participant Queue as IsolateRunner
    participant Sandbox as Isolate (沙箱)
    
    Client->>API: POST /submissions (Base64 编码)
    Note over API: Base64Service.decode() 解码
    API->>DB: Submission.create()
    DB-->>API: 返回 token
    API-->>Client: 返回 token
    
    alt 同步模式 (wait=true)
        API->>Queue: perform_now()
    else 异步模式
        API->>Queue: perform_later()
    end
    
    Queue->>Sandbox: 初始化沙箱环境
    Sandbox-->>Queue: box_id, workdir
    
    alt 需要编译
        Queue->>Sandbox: 执行 compile_cmd
        alt 编译成功
            Queue->>Sandbox: 执行 run_cmd
        else 编译失败
            Note over Queue: status = CE (Compilation Error)
        end
    else 解释型语言
        Queue->>Sandbox: 直接执行 run_cmd
    end
    
    Sandbox-->>Queue: metadata, stdout, stderr
    Queue->>Queue: determine_status() 判定状态
    
    alt 有回调 URL
        Queue->>Client: HTTP PUT callback_url
    end
    
    Queue->>DB: submission.save()
    Client->>API: GET /submissions/{token}
    API->>DB: 查询结果
    DB-->>API: Submission 数据
    API-->>Client: 返回结果 (Base64 可选)
```

Sources: [submissions\_controller.rb](#root/cnKYJxpnOjSD), [isolate\_job.rb](#root/e6HfOElu3Sbl)

## 字段验证规则

Submission 模型实现了多层次的验证机制：

| 验证项 | 规则 |
| --- | --- |
| `source_code` | 存在性验证（非项目模式必须，项目模式禁止） |
| `additional_files` | 项目模式必须存在 |
| `language_id` | 必须存在且未被归档 |
| `number_of_runs` | 1 ~ MAX\_NUMBER\_OF\_RUNS (默认 20) |
| `cpu_time_limit` | 0 ~ MAX\_CPU\_TIME\_LIMIT (默认 15 秒) |
| `memory_limit` | 2048 KB ~ MAX\_MEMORY\_LIMIT (默认 512000 KB) |
| `compiler_options` | 长度 ≤ 512 字符 |
| `command_line_arguments` | 长度 ≤ 512 字符 |

Sources: [submission.rb](#root/N9H17FZiwLLD)

## 序列化输出

SubmissionSerializer 定义了 API 响应的字段结构：

```ruby
def self.default_fields
  @@default_fields ||= [
    :token, :time, :memory, :stdout, :stderr,
    :compile_output, :message, :status
  ]
end
```

默认响应包含执行结果的核心字段，完整字段列表可通过 `fields` 参数指定：

Sources: [submission\_serializer.rb](#root/N5Cf22ZCq8cS)

---

**相关文档**：

*   继续深入 → [SubmissionsController 控制器](#root/OaIZJ9wPL6PX)
*   理解执行 → [IsolateJob 沙箱执行任务](#root/aeMowSDVm5Nl)
*   语言配置 → [Language 语言配置模型](#root/xxwEdJCxOuVp)

## 相关条目
- [[3-提交（Submission）核心概念]]
- [[11-创建提交 API]]
- [[10-Language 语言配置模型]]
