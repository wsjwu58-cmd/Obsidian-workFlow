# 10-Language 语言配置模型
Language 模型是 Judge0 中用于定义和支持编程语言的核心数据实体。该模型封装了每种编程语言的编译命令、执行命令和源文件命名规则，使系统能够统一处理来自不同编程语言的代码提交请求。

## 模型架构

### 数据库结构

Language 模型对应数据库中的 `languages` 表，包含以下核心字段：

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | integer | 主键，语言唯一标识符 |
| name | string | 语言名称（含版本信息） |
| source\_file | string | 源代码文件名 |
| compile\_cmd | string | 编译命令（解释型语言可为空） |
| run\_cmd | string | 执行命令 |
| is\_archived | boolean | 是否已归档（默认 false） |

Sources: [language.rb](#root/RcgKEH0eoZvp), [schema.rb](#root/TYOeSlG8KASA)

### 模型定义

```ruby
class Language < ApplicationRecord
  validates :name, presence: true
  validates :source_file, :run_cmd, presence: true, unless: -> { is_project }
  default_scope { where(is_archived: false).order(name: :asc) }

  def is_project
    name == "Multi-file program"
  end
end
```

该模型实现了以下核心逻辑：

**默认作用域**：系统默认查询仅返回 `is_archived = false` 的活跃语言，并按名称升序排列。这一设计确保普通用户只能访问当前支持的语言环境。

**项目模式特殊处理**：名为 "Multi-file program" 的特殊语言被视为项目模式，允许跳过 source\_file 和 run\_cmd 的验证，以支持多文件上传场景。

Sources: [language.rb](#root/PpAcREiNtQ7G)

## 语言配置详解

### 命令占位符机制

Judge0 使用 `%s` 作为源文件路径的占位符，在实际执行时会被替换为 `source_file` 字段指定的具体文件名。这种设计提供了灵活的编译/执行命令配置能力。

```
graph LR
    A[提交代码] --> B[Language 配置查找]
    B --> C{是否编译型语言?}
    C -->|是| D[执行 compile_cmd]
    C -->|否| E[直接执行]
    D --> F[运行 run_cmd]
    E --> F
```

### 编译型 vs 解释型语言

**编译型语言**（如 C、C++、Java）配置示例：

| 语言 | compile\_cmd | run\_cmd |
| --- | --- | --- |
| C (GCC 9.2.0) | `/usr/local/gcc-9.2.0/bin/gcc %s main.c` | `./a.out` |
| C++ (GCC 9.2.0) | `/usr/local/gcc-9.2.0/bin/g++ %s main.cpp` | `LD_LIBRARY_PATH=/usr/local/gcc-9.2.0/lib64 ./a.out` |
| Java (OpenJDK 13.0.1) | `/usr/local/openjdk13/bin/javac %s Main.java` | `/usr/local/openjdk13/bin/java Main` |
| Rust (1.40.0) | `/usr/local/rust-1.40.0/bin/rustc %s main.rs` | `./main` |

**解释型语言**（如 Python、JavaScript）仅需配置 `run_cmd`：

| 语言 | run\_cmd |
| --- | --- |
| Python (3.8.1) | `/usr/local/python-3.8.1/bin/python3 script.py` |
| JavaScript (Node.js 12.14.0) | `/usr/local/node-12.14.0/bin/node script.js` |
| Ruby (2.7.0) | `/usr/local/ruby-2.7.0/bin/ruby script.rb` |

Sources: [active.rb](#root/lKad581C4jaE)

### 环境变量配置

部分语言需要设置特定的环境变量以确保正确运行：

```ruby
# C++ 需要配置库路径
run_cmd: "LD_LIBRARY_PATH=/usr/local/gcc-9.2.0/lib64 ./a.out"

# SBCL Lisp 需要设置 SBCL_HOME
run_cmd: "SBCL_HOME=/usr/local/sbcl-2.0.0/lib/sbcl /usr/local/sbcl-2.0.0/bin/sbcl --script script.lisp"

# Go 需要配置 GOCACHE
compile_cmd: "GOCACHE=/tmp/.cache/go-build /usr/local/go-1.13.5/bin/go build %s main.go"
```

Sources: [active.rb](#root/pAUR0J5kKRzc)

## API 接口

### 端点路由

```ruby
resources :languages, only: [:index, :show] do
  get 'all', to: 'languages#all', on: :collection
end
```

| 端点 | 方法 | 说明 |
| --- | --- | --- |
| `/languages` | GET | 获取活跃语言列表 |
| `/languages/all` | GET | 获取所有语言（含已归档） |
| `/languages/:id` | GET | 获取指定语言详情 |

Sources: [routes.rb](#root/AJmKIG06irlR)

### 序列化器配置

```ruby
class LanguageSerializer < ActiveModel::Serializer
  attributes :id, :name, :is_archived, :source_file, :compile_cmd, :run_cmd
end
```

**index 接口响应**（默认仅返回 id 和 name）：

```json
[
  { "id": 43, "name": "Plain Text" },
  { "id": 48, "name": "C (GCC 7.4.0)" },
  { "id": 71, "name": "Python (3.8.1)" }
]
```

**show 接口响应**（返回完整字段）：

```json
{
  "id": 71,
  "name": "Python (3.8.1)",
  "is_archived": false,
  "source_file": "script.py",
  "compile_cmd": null,
  "run_cmd": "/usr/local/python-3.8.1/bin/python3 script.py"
}
```

Sources: [language\_serializer.rb](#root/doMfx5TI2jQw), [languages\_controller.rb](#root/rEuodndBc26C)

## 语言数据初始化

### 种子文件结构

Judge0 使用模块化的种子文件管理语言配置：

```ruby
# db/seeds.rb
require_relative 'languages/archived'
require_relative 'languages/active'

ActiveRecord::Base.transaction do
  Language.unscoped.delete_all
  @languages.each_with_index do |language, index|
    Language.create(
      id: language[:id],
      name: language[:name],
      is_archived: language[:is_archived],
      source_file: language[:source_file],
      compile_cmd: language[:compile_cmd],
      run_cmd: language[:run_cmd],
    )
  end
end
```

Sources: [seeds.rb](#root/sd3VA728XjI1)

### 支持的语言生态

目前活跃支持的语言涵盖 47 种：

**传统编译型语言**：C、C++、Java、Go、Rust、Haskell、Pascal、Fortran、D、OCaml、Scala、Swift、Kotlin

**脚本与解释型语言**：Python、Ruby、JavaScript、PHP、Perl、Lua、Bash、Elixir、Erlang、Octave、R、SQL

**函数式语言**：Common Lisp、OCaml、F#、Clojure、Prolog

**其他语言**：Assembly (NASM)、COBOL、Visual Basic.Net、Objective-C、Plain Text、Executable

Sources: [active.rb](#root/lKad581C4jaE)

## 与 Submission 的关联

### 验证逻辑

Submission 模型通过 `language_existence` 验证方法与 Language 模型紧密耦合：

```ruby
def language_existence
  if not language
    errors.add(:language_id, "language with id #{language_id} doesn't exist")
  elsif language.is_archived
    errors.add(:language_id, "language with id #{language_id} is archived and cannot be used anymore")
  end
end
```

**关键约束**：已归档的语言（`is_archived = true`）无法再用于创建新的提交，这确保了旧语言版本的废弃管理。

Sources: [submission.rb](#root/0plmwD8tnJ8W)

### 语言查询方法

```ruby
def language
  @language ||= Language.unscoped.find_by(id: language_id)
end

def is_project
  language.try(:is_project) || false
end
```

Submission 模型使用 `Language.unscoped` 来绕过默认作用域，确保即使语言被归档，仍能正确获取其配置信息。

Sources: [submission.rb](#root/B40hgeYa7806)

## 验证规则

Language 模型的单元测试定义了基本的验证要求：

```ruby
RSpec.describe Language, type: :model do
  it { should validate_presence_of(:name) }
  it { should validate_presence_of(:run_cmd) }
  it { should validate_presence_of(:source_file) }
end
```

这些验证确保每种语言配置都必须包含名称、执行命令和源文件命名规范。

Sources: [language\_spec.rb](#root/SZyDVTQ0Ukbx)

## 扩展阅读

若需深入了解 Language 模型在实际执行流程中的应用，建议阅读以下文档：

*   [编程语言与状态枚举](#root/m4bhSPrC7v0y) — 了解语言与状态枚举的配合机制
*   [IsolateJob 沙箱执行任务](#root/aeMowSDVm5Nl) — 了解语言配置如何驱动代码执行
*   [Submission 数据模型与字段编码](#root/X4kCRfBobv9w) — 了解语言与提交的关联关系

## 相关条目
- [[4-编程语言与状态枚举]]
- [[9-Submission 数据模型与字段编码]]
- [[16-配置文件详解]]
