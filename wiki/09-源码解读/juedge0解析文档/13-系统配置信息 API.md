# 13-系统配置信息 API
系统配置信息 API 是 Judge0 提供的一组只读接口，用于获取运行时环境配置、系统硬件信息和统计摘要。这些端点无需提交代码即可访问，帮助开发者了解 Judge0 实例的能力边界和当前状态。

## 架构概览

Judge0 的系统信息端点分为三个类别：**配置信息**、**系统信息**和**运行统计**。配置信息从环境变量和 `judge0.conf` 配置文件读取，系统信息通过执行系统命令实时采集，运行统计则聚合数据库中的提交记录。

```
graph TB
    subgraph "信息查询 API"
        A["/config_info<br/>配置信息"] --> B["Config Helper<br/>配置模块"]
        C["/system_info<br/>系统信息"] --> D["SystemInfo Helper<br/>系统模块"]
        E["/statistics<br/>运行统计"] --> F["Database + Cache<br/>数据库+缓存"]
        G["/workers<br/>Worker状态"] --> H["Resque<br/>队列系统"]
    end
    
    B --> I["环境变量<br/>ENV[]"]
    B --> J["judge0.conf<br/>配置文件"]
    D --> K["lscpu / free<br/>系统命令"]
    F --> L["Submissions表<br/>提交记录"]
    H --> M["Redis<br/>队列存储"]
```

Sources: [config/routes.rb](#root/Uas6ri15xK2U), [info\_controller.rb](#root/wRW1OVLotzTj)

## 配置信息端点

### GET /config\_info

获取 Judge0 的完整配置参数列表，包括默认值和允许的最大限制。这些参数决定了代码执行的各项约束条件。

**请求示例**：

```http
GET /config_info HTTP/1.1
Host: api.example.com
```

**响应格式**：

```json
{
  "maintenance_mode": false,
  "enable_wait_result": true,
  "enable_compiler_options": true,
  "allowed_languages_for_compile_options": [],
  "enable_command_line_arguments": true,
  "enable_submission_delete": false,
  "max_queue_size": 100,
  "cpu_time_limit": 5.0,
  "max_cpu_time_limit": 15.0,
  "cpu_extra_time": 1.0,
  "max_cpu_extra_time": 5.0,
  "wall_time_limit": 10.0,
  "max_wall_time_limit": 20.0,
  "memory_limit": 128000,
  "max_memory_limit": 512000,
  "stack_limit": 64000,
  "max_stack_limit": 128000,
  "max_processes_and_or_threads": 60,
  "max_max_processes_and_or_threads": 120,
  "enable_per_process_and_thread_time_limit": false,
  "allow_enable_per_process_and_thread_time_limit": true,
  "enable_per_process_and_thread_memory_limit": false,
  "allow_enable_per_process_and_thread_memory_limit": true,
  "max_file_size": 1024,
  "max_max_file_size": 4096,
  "number_of_runs": 1,
  "max_number_of_runs": 20,
  "redirect_stderr_to_stdout": false,
  "max_extract_size": 10240,
  "enable_batched_submissions": true,
  "max_submission_batch_size": 20,
  "submission_cache_duration": 1.0,
  "use_docs_as_homepage": false,
  "allow_enable_network": true,
  "enable_network": false,
  "disable_implicit_base64_encoding": false
}
```

Sources: [config.rb](#root/2stvLWSXDh7W)

### 配置参数详解

配置参数分为两大类：**功能开关**和**资源限制**。

| 类别 | 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| 功能 | `enable_wait_result` | boolean | true | 允许同步等待提交结果 |
| 功能 | `enable_compiler_options` | boolean | true | 允许自定义编译选项 |
| 功能 | `enable_command_line_arguments` | boolean | true | 允许自定义命令行参数 |
| 功能 | `enable_callbacks` | boolean | true | 允许使用回调通知 |
| 功能 | `enable_additional_files` | boolean | true | 允许上传额外文件 |
| 功能 | `enable_network` | boolean | false | 默认启用网络访问 |
| 时间 | `cpu_time_limit` | float | 5.0 | 默认 CPU 时间限制（秒） |
| 时间 | `max_cpu_time_limit` | float | 15.0 | 最大 CPU 时间限制 |
| 时间 | `wall_time_limit` | float | 10.0 | 默认墙上时间限制（秒） |
| 内存 | `memory_limit` | integer | 128000 | 默认内存限制（KB） |
| 内存 | `max_memory_limit` | integer | 512000 | 最大内存限制 |
| 并发 | `max_processes_and_or_threads` | integer | 60 | 默认最大进程/线程数 |
| 安全 | `allow_enable_per_process_and_thread_time_limit` | boolean | true | 允许启用单进程时间限制 |
| 安全 | `allow_enable_network` | boolean | true | 允许用户控制网络访问 |

Sources: [config.rb](#root/2stvLWSXDh7W), [judge0.conf](#root/Dymu2xeyDbPO)

## 系统信息端点

### GET /system\_info

获取 Judge0 Web 服务运行所在主机的硬件信息。该端点通过执行 `lscpu` 和 `free -h` 命令实时采集数据。

**注意**：Judge0 由 **Web** 和 **Worker** 两个组件组成。Web 组件提供 API 服务，Worker 组件处理代码执行。两者可能部署在不同主机上，因此此端点返回的硬件信息可能与实际代码执行环境不符。

**响应格式**：

```json
{
  "Architecture": "x86_64",
  "CPU op-mode(s)": "32-bit, 64-bit",
  "Byte Order": "Little Endian",
  "CPU(s)": "4",
  "Thread(s) per core": "2",
  "Core(s) per socket": "2",
  "Socket(s)": "1",
  "Vendor ID": "GenuineIntel",
  "Model name": "Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz",
  "CPU MHz": "2508.703",
  "L1d cache": "32K",
  "L2 cache": "256K",
  "L3 cache": "3072K",
  "Mem": "7.7G",
  "Swap": "8.0G"
}
```

Sources: [system\_info.rb](#root/kCA4HlIrizK0)

### 实现原理

`SystemInfo` 模块使用 Ruby 反引号语法执行系统命令，将命令输出解析为键值对哈希表：

```ruby
module SystemInfo
  def self.sys_info
    @@sys_info ||= self.cpu_info.merge(self.mem_info)
  end

  def self.cpu_info
    @@cpu_info ||= Hash[`lscpu`.split("\n").collect{|l| l = l.split(":"); [l[0].strip, l[1].strip]}]
  end

  def self.mem_info
    @@mem_info ||= Hash[`free -h`.split("\n")[1..-1].collect{|l| l = l.split(":"); [l[0].strip, l[1].split(" ")[0].strip]}].without("-/+ buffers/cache")
  end
end
```

返回结果合并了 CPU 信息和内存信息两个字典。由于使用了类级别缓存（`@@`），同一请求周期内不会重复执行系统命令。

Sources: [system\_info.rb](#root/kCA4HlIrizK0)

## 运行统计端点

### GET /statistics

获取提交统计摘要，包括按语言、按状态的分布以及数据库大小。统计结果默认缓存 **10 分钟**。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `invalidate_cache` | boolean | 设置为 `true` 可强制刷新缓存 |

**响应格式**：

```json
{
  "created_at": "2024-01-15T10:30:00Z",
  "cached_until": "2024-01-15T10:40:00Z",
  "submissions": {
    "total": 15000,
    "today": 42,
    "last_30_days": {
      "2024-01-15": 42,
      "2024-01-14": 38
    }
  },
  "languages": [
    {"language": {"id": 1, "name": "Python"}, "count": 5000},
    {"language": {"id": 2, "name": "JavaScript"}, "count": 3000}
  ],
  "statuses": [
    {"status": {"id": 3, "name": "Accepted"}, "count": 12000},
    {"status": {"id": 4, "name": "Wrong Answer"}, "count": 2000}
  ],
  "database": {
    "size_pretty": "256 MB",
    "size_in_bytes": 268435456
  }
}
```

Sources: [info\_controller.rb](#root/CIBqv8PR6DVg)

## 辅助信息端点

Judge0 还提供一组轻量级的信息查询端点：

| 端点 | 返回内容 | 格式 |
| :--- | :--- | :--- |
| `GET /about` | 版本、项目地址、维护者信息 | JSON |
| `GET /version` | Judge0 版本号 | 纯文本 |
| `GET /isolate` | Isolate 沙箱版本 | 纯文本 |
| `GET /license` | GPLv3 许可证全文 | 纯文本 |

Sources: [config/routes.rb](#root/Uas6ri15xK2U), [info\_controller.rb](#root/ftJoVl2WJCOD)

### About 端点详情

```json
{
  "version": "1.13.1",
  "homepage": "https://judge0.com",
  "source_code": "https://github.com/judge0/judge0",
  "maintainer": "Judge0 Team"
}
```

这些值从环境变量读取：`JUDGE0_VERSION`、`JUDGE0_HOMEPAGE`、`JUDGE0_SOURCE_CODE`、`JUDGE0_MAINTAINER`。

Sources: [info\_controller.rb](#root/9PA9oW75RePy)

## Worker 状态端点

### GET /workers

获取 Resque 队列工作进程的状态信息。该端点集成在健康检查机制中。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `prune_dead_workers` | boolean | 设置为 `true` 清理已死亡的 worker |

**响应格式**：

```json
[
  {
    "queue": "default",
    "size": 5,
    "available": 2,
    "idle": 1,
    "working": 1,
    "paused": 0
  }
]
```

| 字段 | 说明 |
| :--- | :--- |
| `queue` | 队列名称 |
| `size` | 当前排队的任务数 |
| `available` | 可用的 worker 总数 |
| `idle` | 空闲的 worker 数 |
| `working` | 正在处理的 worker 数 |
| `paused` | 暂停的 worker 数 |

Sources: [health\_controller.rb](#root/VL7aCKjBoeDY)

## 认证与授权

系统配置信息 API 默认**无需认证**，属于公开端点。管理员可在 `judge0.conf` 中配置 IP 白名单和认证令牌，但这会影响所有 API 而非特定端点。

```
sequenceDiagram
    participant C as 客户端
    participant S as SessionsController
    participant H as InfoController
    
    Note over C,S: IP 验证 (verify_ip_address)
    C->>S: GET /config_info
    S->>S: 检查 ALLOW_IP / DISALLOW_IP
    alt IP 被禁止
        S-->>C: 403 Forbidden
    else IP 允许
        Note over S: 认证验证 (authenticate_request)
        S->>S: 检查 AUTHN_TOKEN
        alt 认证失败
            S-->>C: 401 Unauthorized
        else 认证通过
            S->>H: 调用目标 Action
            H-->>C: 200 OK + JSON
        end
    end
```

Sources: [sessions\_controller.rb](#root/zYXpXF7bfH59)

## 与提交 API 的关系

配置信息 API 的核心价值在于为提交创建提供参考依据。客户端在构造提交请求前，应查询 `/config_info` 了解当前实例的能力边界：

```json
{
  "cpu_time_limit": 5.0,
  "max_cpu_time_limit": 15.0,
  "memory_limit": 128000,
  "max_memory_limit": 512000
}
```

例如，若要将 CPU 时间限制设为 10 秒，客户端应：

1.  调用 `GET /config_info` 获取 `max_cpu_time_limit`（假设为 15.0）
2.  检查 10 < 15.0，验证请求合法
3.  在提交请求中设置 `cpu_time_limit: 10`

Sources: [submission.rb](#root/ONFiklvUCoSJ)

## 后续学习路径

建议继续阅读以下页面深入理解：

*   [创建提交 API](#root/7uEJEVhhnsck) — 了解如何利用配置信息构造合法提交
*   [认证机制](#root/DhZsYaJvWcmY) — 掌握 IP 白名单和令牌的配置方式
*   [配置文件详解](#root/04RUCISLtZxK) — 深入理解 judge0.conf 的完整结构
*   [安全机制与沙箱隔离](#root/SmNOpSGJhyCw) — 理解配置参数背后的安全设计

## 相关条目
- [[12-批量提交与查询 API]]
- [[14-认证机制]]
