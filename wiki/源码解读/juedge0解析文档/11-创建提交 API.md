# 11-创建提交 API
创建提交 API 是 Judge0 的核心接口，用于将源代码提交到沙箱环境中执行。该 API 采用 RESTful 设计风格，通过 HTTP POST 方法将代码提交到队列中等待处理，成功创建后返回唯一标识符（token）用于后续查询执行结果。

## 端点规范

创建提交 API 的路由定义在 `config/routes.rb` 中，采用 Rails 标准的资源路由：

```ruby
resources :submissions, only: [:index, :show, :create, :destroy], param: :token do
  post 'batch', to: 'submissions#batch_create', on: :collection
  get 'batch', to: 'submissions#batch_show', on: :collection
end
```

**基本信息**：

| 属性 | 值 |
| :--- | :--- |
| HTTP 方法 | POST |
| 端点路径 | `/submissions` |
| 认证要求 | 可选（详见 [认证机制](#root/DhZsYaJvWcmY)） |
| 授权要求 | 无（创建提交无需授权） |
| 内容类型 | application/json |

Sources: [routes.rb](#root/gWnGvOa3IuGl)

## 请求参数详解

创建提交 API 支持 20 个请求参数，其中 `source_code` 和 `language_id` 为必填项，其余均为可选配置变量。

### 必填参数

**source\_code** — 程序的源代码内容，类型为文本。如果代码中包含无法直接通过 JSON 传输的二进制字符或非打印字符，应使用 Base64 编码并设置 `base64_encoded=true` 查询参数。

```json
{
    "source_code": "#include <stdio.h>\n\nint main(void) {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
    "language_id": 4
}
```

**language\_id** — 指定编程语言的唯一标识符。可通过 [获取语言列表 API](#root/suT9RnhiL443) 查询所有可用语言 ID。

Sources: [submissions\_controller.rb](#root/FX5iF6sKgn8T) Sources: [submission.rb](#root/H257SNQxTEgj)

### 可选配置变量

**compiler\_options** — 编译器选项（如编译器标志），最大长度为 512 字符。仅对编译型语言有效，且需要系统配置允许此功能。

**command\_line\_arguments** — 程序运行时接收的命令行参数，最大长度为 512 字符。

**stdin** — 程序的标准输入数据。当需要向程序传递输入时使用。

**expected\_output** — 程序的期望输出。当设置此值时，Judge0 会将程序的 stdout 与期望输出进行比对，适用于答案验证场景。

**cpu\_time\_limit** — CPU 时间限制，单位为秒，默认值为 5 秒，最大值不超过 15 秒（可通过 `MAX_CPU_TIME_LIMIT` 配置）。

**cpu\_extra\_time** — CPU 额外时间，单位为秒。当时间超限时，系统会等待额外时间再终止程序，默认值为 1 秒。

**wall\_time\_limit** — 墙钟时间限制，单位为秒。该时间包括程序等待 CPU 的时间，默认值为 10 秒。

**memory\_limit** — 内存限制，单位为 KB，默认值为 128000 KB（约 125 MB）。

**stack\_limit** — 栈空间限制，单位为 KB，默认值为 64000 KB。

**max\_processes\_and\_or\_threads** — 程序可创建的最大进程和/或线程数，默认值为 60。

**enable\_per\_process\_and\_thread\_time\_limit** — 布尔值，如果为 true，则 cpu\_time\_limit 应用于每个进程和线程。

**enable\_per\_process\_and\_thread\_memory\_limit** — 布尔值，如果为 true，则 memory\_limit 应用于每个进程和线程。

**max\_file\_size** — 程序可创建或修改的最大文件大小，单位为 KB，默认值为 1024 KB。

**redirect\_stderr\_to\_stdout** — 布尔值，如果为 true，则标准错误将重定向到标准输出。

**enable\_network** — 布尔值，如果为 true，程序将获得网络访问权限。

**number\_of\_runs** — 程序运行次数，用于计算平均时间和内存使用量，默认值为 1。

**additional\_files** — Base64 编码的 ZIP 文件，包含程序运行时需要的额外文件。

**callback\_url** — 回调 URL，提交处理完成后系统会向此 URL 发送 PUT 请求。

Sources: [submissions\_controller.rb](#root/FX5iF6sKgn8T) Sources: [submission.rb](#root/6e6pTTn9RkOy) Sources: [config.rb](#root/2stvLWSXDh7W)

## 查询参数

**base64\_encoded** — 布尔值，默认为 false。当设置为 true 时，`source_code`、`stdin` 和 `expected_output` 应使用 Base64 编码传输。

```http
POST /submissions?base64_encoded=true
```

**wait** — 布尔值，默认为 false。当设置为 true 时，系统将同步等待执行结果而非仅返回 token。此功能可能未在所有 Judge0 实例上启用，请先查询 [系统配置信息 API](#root/eW2TvXSbykHS) 确认。

::: warning 不推荐使用 `wait=true` 功能，因为它无法良好扩展，在高并发场景下可能导致请求超时或服务器过载。 :::

**fields** — 逗号分隔的字段列表，用于指定返回结果中包含哪些字段。例如：`?fields=token,status,stdout`。

Sources: [submissions\_controller.rb](#root/pHK6daWcALEX) Sources: [submission\_serializer.rb](#root/HAZQzsPnElr7)

## 请求流程架构

```
sequenceDiagram
    participant Client as 客户端
    participant Controller as SubmissionsController
    participant Model as Submission
    participant Serializer as SubmissionSerializer
    participant Queue as Resque Queue

    Client->>Controller: POST /submissions<br/>{source_code, language_id, ...}
    
    Note over Controller: 执行前置过滤器链
    
    rect rgb(240, 248, 255)
        Note over Controller: 1. check_maintenance<br/>验证系统是否处于维护模式
    end
    
    rect rgb(255, 250, 240)
        Note over Controller: 2. check_wait<br/>验证wait参数是否允许
    end
    
    rect rgb(240, 255, 240)
        Note over Controller: 3. check_queue_size<br/>验证队列是否已满
    end
    
    rect rgb(255, 240, 255)
        Note over Controller: 4. check_requested_fields<br/>验证fields参数有效性
    end
    
    rect rgb(255, 255, 240)
        Note over Controller: 5. set_base64_encoded<br/>设置Base64解码模式
    end
    
    Controller->>Model: submission_params(params)
    Note over Model: 提取参数并进行Base64解码
    
    Controller->>Model: Submission.new(params)
    Note over Model: 创建模型实例并验证
    
    alt 验证通过
        alt wait = true
            Controller->>Queue: IsolateRunner.perform_now(submission)
            Note over Queue: 同步执行（阻塞）
            Queue-->>Controller: 执行完成
            Controller->>Serializer: 序列化完整结果
            Controller-->>Client: HTTP 201<br/>{token, status, stdout, ...}
        else wait = false
            Controller->>Queue: IsolateRunner.perform_later(submission)
            Note over Queue: 异步执行
            Controller->>Serializer: 仅序列化token
            Controller-->>Client: HTTP 201<br/>{token}
        end
    else 验证失败
        Controller-->>Client: HTTP 422<br/>{errors}
    end
```

Sources: [submissions\_controller.rb](#root/98OfBncrBbrM)

## 响应格式

### 成功响应（异步模式 - 默认）

返回 201 Created 状态码，仅包含 token 字段：

```json
{
    "token": "d85cd024-1548-4165-96c7-7bc88673f194"
}
```

### 成功响应（同步模式 - wait=true）

返回 201 Created 状态码，包含完整的执行结果：

```json
{
    "token": "eb0dd001-66db-47f4-8a69-b736c9bc23f6",
    "status": {
        "id": 3,
        "description": "Accepted"
    },
    "stdout": "hello, Judge0\n",
    "stderr": null,
    "compile_output": null,
    "message": null,
    "time": "0.001",
    "memory": 380
}
```

### 验证错误响应

返回 422 Unprocessable Entity 状态码：

```json
{
    "language_id": ["can't be blank"]
}
```

或：

```json
{
    "language_id": ["language with id 150000 doesn't exist"]
}
```

### 队列满响应

返回 503 Service Unavailable 状态码：

```json
{
    "error": "queue is full"
}
```

### 等待功能未启用响应

返回 400 Bad Request 状态码：

```json
{
    "error": "wait not allowed"
}
```

Sources: [submissions\_controller.rb](#root/OK44YZfbkCHi) Sources: [submission\_serializer.rb](#root/90YxGpHDwGSQ)

## Base64 编码使用场景

当源代码、输入数据或期望输出包含以下内容时，必须使用 Base64 编码：

*   非打印字符（如 `\xFE`、`\x00`）
*   二进制数据
*   无法正确编码为 UTF-8 的字符

**示例请求（使用 Base64 编码）**：

```http
POST /submissions?base64_encoded=true
Content-Type: application/json

{
    "source_code": "I2luY2x1ZGUgPHN0ZGlvLmg+CgppbnQgbWFpbih2b2lkKSB7CiAgY2hhciBuYW1lWzEwXTsKICBzY2FuZigiJXMiLCBuYW1lKTsKICBwcmludGYoImhlbGxvLCAlc1xuIiwgbmFtZSk7CiAgcmV0dXJuIDA7Cn0=",
    "language_id": 4,
    "stdin": "SnVkZ2Uw"
}
```

对应的原始数据为：

```csrc
#include <stdio.h>

int main(void) {
  char name[10];
  scanf("%s", name);
  printf("hello, %s\n", name);
  return 0;
}
```

输入：`Judge0`

Sources: [submission.rb](#root/5o0R6xGcEV5p) Sources: [create\_a\_submission.md](#root/BGfrYSuJC09b)

## 字段筛选机制

使用 `fields` 查询参数可以指定返回结果中包含哪些字段，这有助于减少网络传输量并提高响应速度：

```http
POST /submissions?fields=token,status,stdout,stderr
```

返回结果中将仅包含指定的四个字段：

```json
{
    "token": "xxx",
    "status": {"id": 3, "description": "Accepted"},
    "stdout": "result\n",
    "stderr": null
}
```

可用的字段包括：token、time、memory、stdout、stderr、compile\_output、message、status、language、exit\_code、exit\_signal 等全部 33 个属性。

Sources: [submission.rb](#root/wbj7xYMgeXgl) Sources: [fields/submission.rb](#root/eC7s4jGFR7tp)

## 配置限制参考

系统通过环境变量定义各参数的有效范围：

| 参数 | 环境变量 | 默认值 | 最大值 |
| :--- | :--- | ---: | ---: |
| cpu\_time\_limit | CPU\_TIME\_LIMIT | 5 秒 | MAX\_CPU\_TIME\_LIMIT: 15 秒 |
| cpu\_extra\_time | CPU\_EXTRA\_TIME | 1 秒 | MAX\_CPU\_EXTRA\_TIME: 5 秒 |
| wall\_time\_limit | WALL\_TIME\_LIMIT | 10 秒 | MAX\_WALL\_TIME\_LIMIT: 20 秒 |
| memory\_limit | MEMORY\_LIMIT | 128000 KB | MAX\_MEMORY\_LIMIT: 512000 KB |
| stack\_limit | STACK\_LIMIT | 64000 KB | MAX\_STACK\_LIMIT: 128000 KB |
| max\_file\_size | MAX\_FILE\_SIZE | 1024 KB | MAX\_MAX\_FILE\_SIZE: 4096 KB |
| number\_of\_runs | NUMBER\_OF\_RUNS | 1 | MAX\_NUMBER\_OF\_RUNS: 20 |
| max\_processes | MAX\_PROCESSES\_AND\_OR\_THREADS | 60 | MAX\_MAX\_PROCESSES\_AND\_OR\_THREADS: 120 |

Sources: [config.rb](#root/2stvLWSXDh7W) Sources: [submission.rb](#root/pUdyBSYASxGO)

## 完整请求示例

### C 语言程序

```http
POST /submissions HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
    "source_code": "#include <stdio.h>\n\nint main(void) {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n    printf(\"%d\\n\", a + b);\n    return 0;\n}",
    "language_id": 4,
    "stdin": "10 20",
    "cpu_time_limit": 2,
    "memory_limit": 128000
}
```

### Python 程序（带 Base64 编码）

```http
POST /submissions?base64_encoded=true HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
    "source_code": "cHJpbnQoIkhFTExPIiApCg==",
    "language_id": 71,
    "stdin": ""
}
```

### 同步等待模式

```http
POST /submissions?wait=true HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
    "source_code": "print('Hello, World!')",
    "language_id": 71
}
```

Sources: [create\_a\_submission.md](#root/ZgAs79Tr5fWJ)

## 后续步骤

创建提交后，可以使用返回的 token 通过以下方式获取执行结果：

*   **[获取单个提交 API](#root/suT9RnhiL443)** — 使用 token 查询提交状态和结果
*   **[批量提交与查询 API](#root/suT9RnhiL443)** — 一次性创建或查询多个提交
*   **[编程语言与状态枚举](#root/m4bhSPrC7v0y)** — 了解所有支持的编程语言和状态码含义

如需了解提交在后台如何执行，请参阅 [IsolateJob 沙箱执行任务](#root/aeMowSDVm5Nl) 和 [IsolateRunner 任务调度器](#root/Bc8uFkRMEOzO)。

## 相关条目
- [[12-批量提交与查询 API]]
- [[6-SubmissionsController 控制器]]
- [[9-Submission 数据模型与字段编码]]
