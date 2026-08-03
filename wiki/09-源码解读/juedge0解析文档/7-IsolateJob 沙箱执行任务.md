# 7-IsolateJob 沙箱执行任务
IsolateJob 是 Judge0 系统中负责在隔离沙箱环境中执行代码提交的核心任务类。它基于 Rails ActiveJob 框架构建，通过 Linux `isolate` 工具实现进程级别的资源隔离与执行控制。本文深入分析其架构设计、执行流程、错误处理机制以及与外部组件的协作关系。

## 核心架构设计

### 类继承结构

IsolateJob 继承自 `ApplicationJob`，后者是 Rails ActiveJob 框架的简单封装：

```ruby
class ApplicationJob < ActiveJob::Base
end
```

Sources: [application\_job.rb](#root/nGW5BCQKsyez)

IsolateJob 本身声明了三个关键配置：

```ruby
class IsolateJob < ApplicationJob
  retry_on RuntimeError, wait: 0.1.seconds, attempts: 100
  queue_as ENV["JUDGE0_VERSION"].to_sym
```

Sources: [isolate\_job.rb](#root/7znGIBJ7WV97)

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| `retry_on` | RuntimeError, 100次, 间隔0.1秒 | 运行时错误自动重试机制 |
| `queue_as` | JUDGE0\_VERSION 环境变量 | 任务队列命名基于版本号 |
| `retry_jitter` | 未配置 | 重试间隔不添加随机抖动 |

### 文件路径常量定义

```ruby
STDIN_FILE_NAME = "stdin.txt"
STDOUT_FILE_NAME = "stdout.txt"
STDERR_FILE_NAME = "stderr.txt"
METADATA_FILE_NAME = "metadata.txt"
ADDITIONAL_FILES_ARCHIVE_FILE_NAME = "additional_files.zip"
```

Sources: [isolate\_job.rb](#root/DT1RTPePpW1r)

这些常量定义了沙箱环境中标准输入/输出文件及元数据文件的命名规范，确保代码执行过程中产生的所有数据都有明确的存储位置。

## 任务调度入口：IsolateRunner

IsolateRunner 是连接控制器与 IsolateJob 的中间模块，位于 `app/helpers/isolate_runner.rb`：

```ruby
module IsolateRunner
  MAX_WAIT_TIME_S = 600

  def self.perform_later(submission)
    submission.update(status: Status.queue, queued_at: DateTime.now, queue_host: ENV["HOSTNAME"])
    IsolateJob.perform_later(submission.id)
  end

  def self.perform_now(submission)
    IsolateRunner.perform_later(submission)
    # ... 轮询等待直到任务完成
  end
end
```

Sources: [isolate\_runner.rb](#root/TLSxBG03OMpp)

### 同步与异步执行模式

| 模式 | 方法 | 行为 |
| --- | --- | --- |
| 异步 | `perform_later` | 立即入队，返回 token |
| 同步 | `perform_now` | 入队后轮询等待最多 600 秒 |

同步模式采用指数退避等待策略：

*   首次等待 2 秒
*   次次等待 1 秒
*   后续等待时间 = 0.5 × 迭代次数

Sources: [isolate\_runner.rb](#root/p4IXSmQE19GF)

### 控制器集成

在 SubmissionsController 中，任务的执行模式由 `wait` 参数决定：

```ruby
def create
  submission = Submission.new(submission_params(params))
  if submission.save
    if @wait
      IsolateRunner.perform_now(submission)
      submission.reload
      render json: submission, status: :created, base64_encoded: @base64_encoded, fields: @requested_fields
    else
      IsolateRunner.perform_later(submission)
      render json: submission, status: :created, fields: [:token]
    end
  end
end
```

Sources: [submissions\_controller.rb](#root/OK44YZfbkCHi)

## 主执行流程：`perform` 方法详解

`perform(submission_id)` 是任务的入口点，执行流程分为六个阶段：

```
flowchart TD
    A[接收 submission_id] --> B[加载 Submission 并设置状态为 Processing]
    B --> C{循环执行 number_of_runs 次}
    C --> D[initialize_workdir 初始化工作目录]
    D --> E{compile 编译阶段}
    E -->|失败| F[cleanup 清理并返回]
    E -->|成功| G[run 执行程序]
    G --> H[verify 验证结果]
    H --> I[记录 time 和 memory]
    I --> J{是否 AC 状态?}
    J -->|是| C
    J -->|否| K[break 跳出循环]
    C -->|循环完成| L[计算平均值]
    L --> M[保存结果]
    M --> N{callback_url 存在?}
    N -->|是| O[call_callback 回调通知]
    N -->|否| P[结束]
    F --> P
    O --> P
```

Sources: [isolate\_job.rb](#root/peGbUvuRhtSS)

### 状态转换与元数据更新

```ruby
def perform(submission_id)
  @submission = Submission.find(submission_id)
  submission.update(status: Status.process, started_at: DateTime.now, execution_host: ENV["HOSTNAME"])

  time = []
  memory = []

  submission.number_of_runs.times do
    # ... 执行逻辑
  end

  submission.time = time.inject(&:+).to_f / time.size
  submission.memory = memory.inject(&:+).to_f / memory.size
  submission.save
rescue Exception => e
  submission.update(message: e.message, status: Status.boxerr, finished_at: DateTime.now)
  cleanup(raise_exception: false)
ensure
  call_callback
end
```

Sources: [isolate\_job.rb](#root/peGbUvuRhtSS)

## 工作目录初始化

`initialize_workdir` 方法负责设置隔离执行环境：

```
sequenceDiagram
    participant IJ as IsolateJob
    participant OS as isolate 命令
    participant FS as 文件系统

    IJ->>OS: isolate --cg -b box_id --init
    OS->>FS: 创建 /var/local/lib/isolate/{box_id}/box
    OS-->>IJ: 返回 workdir 路径
    IJ->>FS: 创建 stdin.txt, stdout.txt, stderr.txt, metadata.txt
    IJ->>FS: 写入 source_code 到 boxdir/source_file
    IJ->>FS: 写入 stdin 到 workdir/stdin.txt
    IJ->>FS: extract_archive 解压附加文件
```

### 沙箱 ID 生成算法

```ruby
def initialize_workdir
  @box_id = submission.id % 2147483647  # 2^31 - 1, 最大有符号整数
  @cgroups = (!submission.enable_per_process_and_thread_time_limit || 
              !submission.enable_per_process_and_thread_memory_limit) ? "--cg" : ""
  @workdir = `isolate #{cgroups} -b #{box_id} --init`.chomp
  # ...
end
```

Sources: [isolate\_job.rb](#root/3XELw5lbnU9u)

| 字段 | 计算方式 | 用途 |
| --- | --- | --- |
| `box_id` | `submission.id % 2147483647` | 沙箱容器唯一标识 |
| `cgroups` | 条件表达式 | 控制组隔离开关 |
| `workdir` | `isolate --init` 命令返回 | 沙箱工作目录 |
| `boxdir` | `workdir + "/box"` | 代码文件存储位置 |

### Cgroups 隔离策略

```ruby
@cgroups = (!submission.enable_per_process_and_thread_time_limit || 
            !submission.enable_per_process_and_thread_memory_limit) ? "--cg" : ""
```

Sources: [isolate\_job.rb](#root/1FDzNj0eKj3C)

| 用户配置 | Cgroups 标志 | 效果 |
| --- | --- | --- |
| 启用进程级时间限制 | 不使用 `--cg` | 使用 `/proc` 计时 |
| 启用进程级内存限制 | 不使用 `--cg` | 使用 `/proc` 内存统计 |
| 禁用上述任一选项 | 使用 `--cg` | 启用 cgroups v1 隔离 |

## 编译阶段

编译阶段仅对需要编译的语言执行：

```
flowchart LR
    A[检查语言配置] --> B{compile_cmd 存在?}
    B -->|Python/JS| C[跳过编译]
    B -->|C/Java/Python| D[生成 compile.sh]
    D --> E[执行 isolate run]
    E --> F{exit code = 0?}
    F -->|成功| G[继续执行]
    F -->|失败| H[设置状态为 CE]
    H --> I[保存结果并返回]
```

### 编译命令执行

```ruby
def compile
  unless submission.is_project
    return :success unless submission.language.compile_cmd
  end
  # ...
  command = "isolate #{cgroups} \
    -s \
    -b #{box_id} \
    -M #{metadata_file} \
    -i /dev/null \
    -t #{Config::MAX_CPU_TIME_LIMIT} \
    -w #{Config::MAX_WALL_TIME_LIMIT} \
    -k #{Config::MAX_STACK_LIMIT} \
    -p#{Config::MAX_MAX_PROCESSES_AND_OR_THREADS} \
    -f #{Config::MAX_MAX_FILE_SIZE} \
    -E HOME=/tmp \
    -E PATH=\"...\" \
    -d /etc:noexec \
    --run \
    -- /bin/bash compile.sh"
  `#{command}`
  # ...
end
```

Sources: [isolate\_job.rb](#root/u9S6xnOjaR6t)

### Isolate 命令参数对照表

| 参数 | 值来源 | 说明 |
| --- | --- | --- |
| `-s` | 固定 | 共享网络命名空间 |
| `-b` | box\_id | 沙箱标识符 |
| `-M` | metadata\_file | 元数据输出文件 |
| `-i` | /dev/null | 标准输入重定向 |
| `-t` | MAX\_CPU\_TIME\_LIMIT | CPU 时间限制（秒） |
| `-w` | MAX\_WALL\_TIME\_LIMIT | 墙钟时间限制（秒） |
| `-k` | MAX\_STACK\_LIMIT | 栈大小限制（KB） |
| `-p` | MAX\_MAX\_PROCESSES | 最大进程/线程数 |
| `-m` / `--cg-mem` | MAX\_MEMORY\_LIMIT | 内存限制（KB） |
| `-f` | MAX\_MAX\_FILE\_SIZE | 最大文件大小（KB） |
| `-E` | 环境变量 | 设置沙箱内环境变量 |
| `-d` | /etc:noexec | 禁止执行目录 |
| `--run` | 固定 | 执行模式标志 |

Sources: [isolate\_job.rb](#root/YX8WY5gvhpdI)

### 编译失败处理

```ruby
return :success if process_status.success?

if metadata[:status] == "TO"
  submission.compile_output = "Compilation time limit exceeded."
end

submission.finished_at = DateTime.now
submission.time = nil
submission.wall_time = nil
submission.memory = nil
submission.stdout = nil
submission.stderr = nil
submission.exit_code = nil
submission.exit_signal = nil
submission.message = nil
submission.status = Status.ce  # Compilation Error
submission.save

return :failure
```

Sources: [isolate\_job.rb](#root/SmK0vyxs68yP)

## 执行阶段

`run` 方法在隔离环境中执行编译后的程序：

```
sequenceDiagram
    participant IJ as IsolateJob
    participant ISO as isolate
    participant Box as 沙箱环境
    participant UserProg as 用户程序

    IJ->>ISO: isolate -M metadata.txt [参数] --run -- bash run.sh
    ISO->>Box: 创建隔离环境
    Box->>UserProg: 执行用户代码
    UserProg->>Box: 读取 stdin.txt
    Box->>UserProg: 写入 stdout.txt, stderr.txt
    UserProg->>Box: 退出
    Box-->>ISO: 返回元数据
    ISO-->>IJ: 返回 metadata.txt 内容
```

### 执行命令构建

```ruby
def run
  run_script = boxdir + "/" + "run.sh"
  unless submission.is_project
    command_line_arguments = submission.command_line_arguments.to_s.strip
      .encode("UTF-8", invalid: :replace)
      .gsub(/[$&;<>|`]/, "")  # 安全过滤
    File.open(run_script, "w") { |f| f.write("#{submission.language.run_cmd} #{command_line_arguments}")}
  end

  command = "isolate #{cgroups} \
    -s \
    -b #{box_id} \
    -M #{metadata_file} \
    #{submission.redirect_stderr_to_stdout ? '--stderr-to-stdout' : ''} \
    #{submission.enable_network ? '--share-net' : ''} \
    -t #{submission.cpu_time_limit} \
    -x #{submission.cpu_extra_time} \
    -w #{submission.wall_time_limit} \
    -k #{submission.stack_limit} \
    -p#{submission.max_processes_and_or_threads} \
    #{submission.enable_per_process_and_thread_time_limit ? ... : '--cg-timing'} \
    #{submission.enable_per_process_and_thread_memory_limit ? '-m' : '--cg-mem='}#{submission.memory_limit} \
    -f #{submission.max_file_size} \
    --run \
    -- /bin/bash run.sh \
    < #{stdin_file} > #{stdout_file} 2> #{stderr_file}"
  `#{command}`
end
```

Sources: [isolate\_job.rb](#root/rQ2KoyJGOMnu)

### 关键安全措施

| 安全机制 | 实现位置 | 目的 |
| --- | --- | --- |
| 命令注入过滤 | \`gsub(/\[$&;\<\> | `]/)` |
| 路径隔离 | `boxdir` 目录 | 限制文件访问范围 |
| 网络控制 | `--share-net` | 可选启用网络 |
| `/etc:noexec` | 禁止执行 | 防止执行危险二进制 |

## 结果验证阶段

`verify` 方法解析元数据并确定最终状态：

```ruby
def verify
  submission.finished_at = DateTime.now
  metadata = get_metadata

  program_stdout = File.read(stdout_file)
  submission.stdout = program_stdout.empty? ? nil : program_stdout

  submission.time = metadata[:time]
  submission.wall_time = metadata[:"time-wall"]
  submission.memory = (cgroups.present? ? metadata[:"cg-mem"] : metadata[:"max-rss"])
  submission.exit_code = metadata[:exitcode].try(:to_i) || 0
  submission.exit_signal = metadata[:exitsig].try(:to_i)
  submission.message = metadata[:message]
  submission.status = determine_status(metadata[:status], submission.exit_signal)
end
```

Sources: [isolate\_job.rb](#root/lJvPqyBBiH5x)

### 元数据解析

```ruby
def get_metadata
  metadata = File.read(metadata_file).split("\n").collect do |e|
    { e.split(":").first.to_sym => e.split(":")[1..-1].join(":") }
  end.reduce({}, :merge)
  return metadata
end
```

Sources: [isolate\_job.rb](#root/vIIbj6ADye4h)

Isolate 工具输出的元数据格式为每行 `key:value`，例如：

```
time:0.012
time-wall:0.034
max-rss:4096
exitcode:0
status:OK
```

### 状态判定逻辑

```
flowchart TD
    A[metadata :status] --> B{状态值}
    B -->|TO| C[TLE - 时间超限]
    B -->|SG| D[根据 exit_signal 判定]
    B -->|RE| E[NZEC - 非零退出码]
    B -->|XX| F[Internal Error]
    B -->|OK| G{stdout == expected_output?}
    G -->|相等| H[AC - Accepted]
    G -->|不等| I[WA - 答案错误]
```

```ruby
def determine_status(status, exit_signal)
  if status == "TO"
    return Status.tle
  elsif status == "SG"
    return Status.find_runtime_error_by_status_code(exit_signal)
  elsif status == "RE"
    return Status.nzec
  elsif status == "XX"
    return Status.boxerr
  elsif submission.expected_output.nil? || strip(submission.expected_output) == strip(submission.stdout)
    return Status.ac
  else
    return Status.wa
  end
end
```

Sources: [isolate\_job.rb](#root/0m31vf4ZSAWF)

### Status 枚举完整定义

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
         other:     { id: 12, 'Runtime Error (Other)' },
         boxerr:    { id: 13, name: 'Internal Error' },
         exeerr:    { id: 14, name: 'Exec Format Error' }

  def self.find_runtime_error_by_status_code(status_code)
    case status_code.to_i
      when 11 then Status.sigsegv    # SIGSEGV
      when 25 then Status.sigxfsz    # SIGXFSZ
      when 8  then Status.sigfpe     # SIGFPE
      when 6  then Status.sigabrt    # SIGABRT
      else Status.other
    end
  end
end
```

Sources: [status.rb](#root/gwiyKvrDVvoB)

## 清理与回调

### 沙箱清理

```
flowchart TD
    A[cleanup] --> B[fix_permissions 修复权限]
    B --> C[删除 boxdir 和 tmpdir 内容]
    C --> D[删除 stdin/stdout/stderr/metadata 文件]
    D --> E[isolate --cleanup 清理沙箱]
    E --> F{workdir 仍存在?}
    F -->|是| G[抛出异常]
    F -->|否| H[成功返回]
```

```ruby
def cleanup(raise_exception = true)
  fix_permissions
  `sudo rm -rf #{boxdir}/* #{tmpdir}/*`
  [stdin_file, stdout_file, stderr_file, metadata_file].each do |f|
    `sudo rm -rf #{f}`
  end
  `isolate #{cgroups} -b #{box_id} --cleanup`
  raise "Cleanup of sandbox #{box_id} failed." if raise_exception && Dir.exists?(workdir)
end
```

Sources: [isolate\_job.rb](#root/oZjz0gTCDvOU)

### 回调通知机制

```ruby
def call_callback
  return unless submission.callback_url.present?

  serialized_submission = ActiveModelSerializers::SerializableResource.new(
    submission,
    serializer: SubmissionSerializer,
    base64_encoded: true,
    fields: SubmissionSerializer.default_fields
  ).to_json

  Config::CALLBACKS_MAX_TRIES.times do
    begin
      response = HTTParty.put(
        submission.callback_url,
        body: serialized_submission,
        headers: { "Content-Type" => "application/json" },
        timeout: Config::CALLBACKS_TIMEOUT
      )
      break
    rescue Exception => e
      # 重试直到达到最大次数
    end
  end
rescue Exception => e
  # 静默处理回调错误，避免影响主流程
end
```

Sources: [isolate\_job.rb](#root/hRf2HqhNCoUO)

## 配置参数体系

IsolateJob 依赖 Config 模块读取环境变量配置：

```ruby
module Config
  CPU_TIME_LIMIT = (ENV["CPU_TIME_LIMIT"].presence || 5).to_f
  MAX_CPU_TIME_LIMIT = (ENV["MAX_CPU_TIME_LIMIT"].presence || 15).to_f
  MEMORY_LIMIT = (ENV["MEMORY_LIMIT"].presence || 128000).to_i  # KB
  MAX_MEMORY_LIMIT = (ENV["MAX_MEMORY_LIMIT"].presence || 512000).to_i
  STACK_LIMIT = (ENV["STACK_LIMIT"].presence || 64000).to_i
  MAX_STACK_LIMIT = (ENV["MAX_STACK_LIMIT"].presence || 128000).to_i
  MAX_PROCESSES_AND_OR_THREADS = (ENV["MAX_PROCESSES_AND_OR_THREADS"].presence || 60).to_i
  # ... 更多配置
end
```

Sources: [config.rb](#root/qtDp4vlRqNtT)

| 参数分类 | 变量名 | 默认值 | 单位 |
| --- | --- | --- | --- |
| **时间限制** | `CPU_TIME_LIMIT` | 5 | 秒 |
| **时间限制** | `MAX_CPU_TIME_LIMIT` | 15 | 秒 |
| **时间限制** | `WALL_TIME_LIMIT` | 10 | 秒 |
| **内存限制** | `MEMORY_LIMIT` | 128000 | KB |
| **内存限制** | `MAX_MEMORY_LIMIT` | 512000 | KB |
| **栈限制** | `STACK_LIMIT` | 64000 | KB |
| **进程限制** | `MAX_MAX_PROCESSES_AND_OR_THREADS` | 120 | 数量 |
| **文件限制** | `MAX_FILE_SIZE` | 1024 | KB |
| **运行次数** | `NUMBER_OF_RUNS` | 1 | 次 |

Sources: [judge0.conf](#root/nwe9aoMN89Ot)

## 错误处理与容错

### 重试策略

```ruby
retry_on RuntimeError, wait: 0.1.seconds, attempts: 100
```

*   **触发条件**: RuntimeError 异常
*   **重试间隔**: 0.1 秒（固定值，无抖动）
*   **最大次数**: 100 次

### 异常捕获层级

```ruby
def perform(submission_id)
  # 主逻辑
rescue Exception => e
  raise e.message unless submission
  submission.update(message: e.message, status: Status.boxerr, finished_at: DateTime.now)
  cleanup(raise_exception: false)
ensure
  call_callback  # 即使出错也会执行回调
end
```

Sources: [isolate\_job.rb](#root/ABXG5aPISSga)

| 异常场景 | 处理方式 | 状态码 |
| --- | --- | --- |
| Isolate 命令失败 | 重试 | RuntimeError |
| 资源超限 | 记录后继续 | Status.tle/Status.oom |
| 沙箱内部错误 | 设置 boxerr | Status.boxerr |
| 回调失败 | 静默忽略 | 无状态变化 |

## 与外部组件的交互

### 消息队列：Resque

```ruby
# config/application.rb
config.active_job.queue_adapter = :resque
```

Sources: [application.rb](#root/OTrX9La6aIsh)

```ruby
# config/initializers/resque.rb
Resque.redis = Redis.new(
  host: ENV["REDIS_HOST"],
  port: ENV["REDIS_PORT"],
  password: ENV["REDIS_PASSWORD"],
  thread_safe: true
)
```

Sources: [resque.rb](#root/e1KwtsGhS5oZ)

### 任务队列命名

```ruby
queue_as ENV["JUDGE0_VERSION"].to_sym
```

Sources: [isolate\_job.rb](#root/QDtn1e0SQjuM)

队列名称动态生成，例如 `v1` 或 `v13`。

### Worker 启动脚本

```
# scripts/workers
while [[ $run_resque -eq 1 ]]; do
    rake resque:scheduler &
    rails resque:workers &
done
```

Sources: [workers](#root/OfMhiuQ7jh0I)

## 性能考量

### 多轮执行平均值

```ruby
submission.number_of_runs.times do
  # ... 执行 ...
  time << submission.time
  memory << submission.memory
  cleanup
  break if submission.status != Status.ac  # 提前终止优化
end

submission.time = time.inject(&:+).to_f / time.size
submission.memory = memory.inject(&:+).to_f / memory.size
```

Sources: [isolate\_job.rb](#root/INactdrUHV2A)

### 提前终止优化

当某次运行结果不是 Accepted 状态时，循环立即终止，不再执行后续轮次。

## 扩展阅读

*   [IsolateRunner 任务调度器](#root/Bc8uFkRMEOzO) — 深入了解 IsolateJob 的调度机制
*   [Submission 数据模型与字段编码](#root/X4kCRfBobv9w) — 理解提交数据的完整结构
*   [安全机制与沙箱隔离](#root/SmNOpSGJhyCw) — 探索 isolate 的底层隔离原理
*   [系统架构设计](#root/QzHV2LofURMt) — 从宏观角度理解 Judge0 的整体架构

## 相关条目
- [[5-系统架构设计]]
- [[8-IsolateRunner 任务调度器]]
- [[18-安全机制与沙箱隔离]]
