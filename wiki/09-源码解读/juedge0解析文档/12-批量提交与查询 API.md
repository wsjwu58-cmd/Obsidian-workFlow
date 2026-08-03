# 12-批量提交与查询 API
Judge0 提供了一套完整的批量操作接口，允许开发者一次性提交多个代码执行任务或批量查询执行结果。这对于竞赛系统、在线评测平台和自动化测试场景尤为关键，能够显著减少网络往返次数并提升整体吞吐量。

## 核心架构

批量 API 的实现基于标准的 RESTful 设计模式，遵循以下请求-响应范式：

```
sequenceDiagram
    participant Client as 客户端
    participant API as SubmissionsController
    participant Queue as Resque Queue
    participant DB as Database

    Note over Client,API: 批量创建提交
    Client->>API: POST /submissions/batch
    API->>API: 验证批次大小 (≤20)
    API->>DB: 创建多个 Submission 记录
    DB-->>API: 返回 token 列表
    API->>Queue: 入队多个 IsolateRunner 任务
    API-->>Client: 201 Created + token 数组

    Note over Client,API: 批量查询提交
    Client->>API: GET /submissions/batch?tokens=a,b,c
    API->>DB: WHERE token IN (a,b,c)
    DB-->>API: 提交对象数组
    API-->>Client: 200 OK + 提交结果数组
```

### 路由配置

批量 API 的路由定义位于 `config/routes.rb`，采用 Rails 标准的资源路由集合方法：

```ruby
resources :submissions, only: [:index, :show, :create, :destroy], param: :token do
  post 'batch', to: 'submissions#batch_create', on: :collection
  get 'batch', to: 'submissions#batch_show', on: :collection
end
```

Sources: [routes.rb](#root/jKKLCHFOmlBO)

这生成了两个关键端点：

| 端点 | 方法 | 控制器动作 | 说明 |
| --- | --- | --- | --- |
| `/submissions/batch` | POST | `batch_create` | 批量创建提交 |
| `/submissions/batch` | GET | `batch_show` | 批量查询提交 |

## 批量创建提交 API

### 基本用法

批量创建接口允许在单次请求中提交多个代码执行任务。所有提交将以异步方式入队处理，不支持同步等待模式。

**请求格式**：

```http
POST /submissions/batch
Content-Type: application/json
X-Auth-Token: your_auth_token (可选)

{
  "submissions": [
    {
      "language_id": 46,
      "source_code": "echo hello from Bash"
    },
    {
      "language_id": 71,
      "source_code": "print(\"hello from Python\")"
    },
    {
      "language_id": 72,
      "source_code": "puts(\"hello from Ruby\")"
    }
  ]
}
```

Sources: [create\_a\_submission\_batch.md](#root/BRnDTl0vHJYd)

**成功响应 (201 Created)**：

```json
[
  {
    "token": "db54881d-bcf5-4c7b-a2e3-d33fe7e25de7"
  },
  {
    "token": "ecc52a9b-ea80-4a00-ad50-4ab6cc3bb2a1"
  },
  {
    "token": "1b35ec3b-5776-48ef-b646-d5522bdeb2cc"
  }
]
```

每个成功的提交返回一个包含 `token` 的对象，该 token 用于后续的结果查询。

### 部分成功场景

批量创建采用**尽力而为**策略：有效提交将被处理，无效提交返回错误信息。

**请求格式**（包含无效数据）：

```json
{
  "submissions": [
    {
      "language_id": 46,
      "source_code": "echo hello from Bash"
    },
    {
      "language_id": 123456789,
      "source_code": "print(\"hello from Python\")"
    },
    {
      "language_id": 72,
      "source_code": ""
    }
  ]
}
```

**混合响应**：

```json
[
  {
    "token": "c2dd8881-644b-462d-b1f9-73dd3bb0118a"
  },
  {
    "language_id": [
      "language with id 123456789 doesn't exist"
    ]
  },
  {
    "source_code": [
      "can't be blank"
    ]
  }
]
```

Sources: [create\_a\_submission\_batch.md](#root/ihni8aLf2jqo)

### 支持的参数

每个提交对象支持以下参数，参数结构与单条提交 API 完全一致：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source_code` | string | 是\* | 源代码（\*项目类型除外） |
| `language_id` | integer | 是 | 编程语言 ID |
| `stdin` | string | 否 | 标准输入数据 |
| `expected_output` | string | 否 | 期望输出（用于比对） |
| `compiler_options` | string | 否 | 编译器选项 |
| `command_line_arguments` | string | 否 | 命令行参数 |
| `cpu_time_limit` | decimal | 否 | CPU 时间限制（秒） |
| `memory_limit` | integer | 否 | 内存限制（字节） |

Sources: [submissions\_controller.rb](#root/9NBRbXxMKxd2)

### 实现细节

控制器动作 `batch_create` 的核心逻辑如下：

```ruby
def batch_create
  number_of_submissions = params[:submissions].try(:size).to_i

  # 验证批次大小
  if number_of_submissions > Config::MAX_SUBMISSION_BATCH_SIZE
    render json: { error: "..." }, status: :bad_request
    return
  end

  # 构建提交对象
  submissions = params[:submissions].each.collect{ |p| Submission.new(submission_params(p)) }

  response = []
  has_valid_submission = false

  submissions.each do |submission|
    if submission.save
      IsolateRunner.perform_later(submission)  # 异步入队
      response << { token: submission.token }
      has_valid_submission = true
    else
      response << submission.errors  # 记录错误
    end
  end

  # 响应状态根据是否存在有效提交决定
  render json: response, status: has_valid_submission ? :created : :unprocessable_entity
end
```

Sources: [submissions\_controller.rb](#root/41syWiUISEc6)

关键实现要点：

*   **异步处理**：使用 `perform_later` 将任务入队，不支持 `wait=true` 同步模式
*   **部分成功**：即使部分提交失败，仍会处理有效的提交
*   **响应状态码**：至少有一个成功提交时返回 201，全部失败时返回 422

## 批量查询提交 API

### 基本用法

批量查询接口允许通过 token 列表一次性获取多个提交的执行结果。

**请求格式**：

```http
GET /submissions/batch?tokens=db54881d...,ecc52a9b...,1b35ec3b...
Content-Type: application/json
X-Auth-Token: your_auth_token (可选)
```

或者通过 HTTP Header 传递 tokens：

```http
GET /submissions/batch
Tokens: db54881d-bcf5-4c7b-a2e3-d33fe7e25de7,ecc52a9b-ea80-4a00-ad50-4ab6cc3bb2a1
X-Auth-Token: your_auth_token
```

Sources: [get\_a\_submission\_batch.md](#root/vM3qKDdNFFGd)

**成功响应 (200 OK)**：

```json
{
  "submissions": [
    {
      "language_id": 46,
      "stdout": "hello from Bash\n",
      "status_id": 3,
      "stderr": null,
      "token": "db54881d-bcf5-4c7b-a2e3-d33fe7e25de7"
    },
    {
      "language_id": 71,
      "stdout": "hello from Python\n",
      "status_id": 3,
      "stderr": null,
      "token": "ecc52a9b-ea80-4a00-ad50-4ab6cc3bb2a1"
    },
    {
      "language_id": 72,
      "stdout": "hello from Ruby\n",
      "status_id": 3,
      "stderr": null,
      "token": "1b35ec3b-5776-48ef-b646-d5522bdeb2cc"
    }
  ]
}
```

### 不存在的 Token 处理

对于不存在的 token，响应数组中对应位置返回 `null`：

```
graph TD
    A["请求 tokens: [A, B, C, D]"] --> B["数据库查询"]
    B --> C["找到 A, C"]
    B --> D["未找到 B, D"]
    C --> E["响应 submissions: [提交A, null, 提交C, null]"]
    D --> E
```

Sources: [submissions\_controller.rb](#root/7iJzkpxAxD55)

### 实现细节

控制器动作 `batch_show` 的核心逻辑：

```ruby
def batch_show
  # 解析 tokens（支持 Header 或 Query Parameter）
  tokens = (request.headers[:tokens] || params[:tokens]).to_s.strip.split(",")

  # 验证 tokens 数量
  if tokens.length > Config::MAX_SUBMISSION_BATCH_SIZE
    render json: { error: "..." }, status: :bad_request
    return
  end

  # 批量查询并构建结果数组
  existing_submissions = Hash[Submission.where(token: tokens).collect{ |s| [s.token, s] }]

  submissions = []
  tokens.each do |token|
    if existing_submissions.has_key?(token)
      serialized_submission = ActiveModelSerializers::SerializableResource.new(
        existing_submissions[token],
        { serializer: SubmissionSerializer, base64_encoded: @base64_encoded, fields: @requested_fields }
      )
      submissions << serialized_submission.as_json
    else
      submissions << nil  # 不存在的 token 返回 null
    end
  end

  render json: { submissions: submissions }
end
```

Sources: [submissions\_controller.rb](#root/bzLYTcTZk39P)

## 配置参数

批量 API 的行为可通过以下环境变量控制：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `ENABLE_BATCHED_SUBMISSIONS` | true | 启用/禁用批量提交功能 |
| `MAX_SUBMISSION_BATCH_SIZE` | 20 | 单次批量操作的最大提交数量 |

Sources: [judge0.conf](#root/BrSSyE3vJIUX)

### 禁用批量功能

如需禁用批量 API，可设置环境变量：

```
ENABLE_BATCHED_SUBMISSIONS=false
```

此时访问批量端点将返回错误：

```json
{
  "error": "batched submissions are not allowed"
}
```

Sources: [submissions\_controller.rb](#root/jyA5uw4AIjsG)

## 错误处理

### 批次大小超限

```json
{
  "error": "number of submissions in a batch should be less than or equal to 20"
}
```

### 空批次

```json
{
  "error": "there should be at least one submission in a batch"
}
```

### 队列满载

```json
{
  "error": "queue is full"
}
```

Sources: [submissions\_controller.rb](#root/BGSQgsHLARct)

## 最佳实践

### 1\. 合理分批

虽然最大批次大小为 20，但建议根据实际场景进行更细粒度的分批：

```
graph LR
    A["批量创建"] --> B{"任务数量"}
    B -->|< 5| C["同步等待"]
    B -->|5-20| D["异步轮询"]
    B -->|> 20| E["分批处理"]
```

### 2\. 结果轮询策略

对于异步批量提交，推荐使用指数退避策略轮询结果：

```python
import time
import requests

def batch_wait_for_results(tokens, base_url, max_retries=30):
    for attempt in range(max_retries):
        response = requests.get(f"{base_url}/submissions/batch", 
                                params={"tokens": ",".join(tokens)})
        results = response.json()["submissions"]
        
        # 检查是否全部完成
        pending = sum(1 for r in results if r and r["status_id"] in [1, 2])
        if pending == 0:
            return results
        
        # 指数退避
        time.sleep(min(2 ** attempt, 10))
    
    return results
```

### 3\. Base64 编码建议

对于包含特殊字符或二进制数据的提交，建议启用 base64 编码：

```http
POST /submissions/batch?base64_encoded=true

{
  "submissions": [
    {
      "language_id": 46,
      "source_code": "ZWNobyBoZWxsbyBmcm9tIEJhc2g="
    }
  ]
}
```

Sources: [submissions\_controller.rb](#root/Td1UuGxJ7ba7)

## 相关资源

*   [创建提交 API](#root/7uEJEVhhnsck) — 单条提交接口详解
*   [SubmissionsController 控制器](#root/OaIZJ9wPL6PX) — 控制器实现分析
*   [认证机制](#root/DhZsYaJvWcmY) — API 认证配置
*   [系统配置信息 API](#root/eW2TvXSbykHS) — 配置参数查询

## 相关条目
- [[11-创建提交 API]]
- [[13-系统配置信息 API]]
