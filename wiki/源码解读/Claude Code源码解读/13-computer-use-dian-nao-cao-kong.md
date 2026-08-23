# 13-computer-use-dian-nao-cao-kong
Computer Use 是 Claude Code 的核心功能之一，赋予 AI 直接操控用户计算机的能力——通过截屏观察屏幕、移动鼠标、点击按钮、输入文字，就像一个远程助手坐在屏幕前操作一样。该功能基于 Model Context Protocol (MCP) 构建，通过标准化的工具接口实现跨平台计算机控制。

Sources: [executor.ts](#root/Y0RqpavUd3EK)

## 架构设计

### 三层模块架构

Computer Use 系统采用分层架构，核心由三个原生模块组成：

| 模块 | 技术栈 | 职责 |
| --- | --- | --- |
| `@ant/computer-use-mcp` | TypeScript | MCP 服务器、工具定义、安全门控 |
| `@ant/computer-use-input` | Rust/enigo | 鼠标键盘输入控制 |
| `@ant/computer-use-swift` | Swift | macOS 截图、TCC 权限、窗口管理 |

```
graph TB
    subgraph "MCP 工具层"
        A["Claude AI"] --> B["MCP Tools<br/>screenshot/click/type..."]
    end
    
    subgraph "编排层 src/utils/computerUse/"
        B --> C["executor.ts<br/>跨平台执行器"]
        C --> D["gates.ts<br/>特性开关"]
        C --> E["toolCalls.ts<br/>安全门控"]
        C --> F["wrapper.tsx<br/>会话绑定"]
    end
    
    subgraph "原生模块层 packages/@ant/"
        C --> G["computer-use-input<br/>Rust/enigo"]
        C --> H["computer-use-swift<br/>Swift"]
    end
    
    subgraph "平台适配 src/utils/computerUse/win32/"
        C --> I["uiAutomation.ts<br/>UI Automation"]
        C --> J["windowCapture.ts<br/>PrintWindow"]
        C --> K["ocr.ts<br/>WinRT OCR"]
        C --> L["windowEnum.ts<br/>EnumWindows"]
    end
    
    G --> M["macOS: CGEvent"]
    G --> N["Windows: SendInput"]
    H --> O["macOS: SCContentFilter"]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style I fill:#f3e5f5
    style J fill:#f3e5f5
    style K fill:#f3e5f5
    style L fill:#f3e5f5
```

Sources: [executor.ts](#root/Y0RqpavUd3EK), [mcpServer.ts](#root/mKSttxkOZJIY)

### CLI 执行器工厂

`createCliExecutor()` 是 CLI 模式下的核心工厂函数，返回跨平台的 `ComputerExecutor` 接口。该接口在进程生命周期内保持单例，所有平台特定逻辑封装于此：

```typescript
export function createCliExecutor(opts: {
  getMouseAnimationEnabled: () => boolean
  getHideBeforeActionEnabled: () => boolean
}): ComputerExecutor
```

执行器内部按需加载原生模块：Swift 模块在工厂创建时加载（每个执行器方法都需要），Input 模块延迟到首次鼠标/键盘调用时加载（截图流程不会触发）。

Sources: [executor.ts](#root/TTOQrAxZJtn3)

## 平台支持矩阵

| 平台 | 截图方式 | 键鼠控制 | UI 结构感知 | OCR | 状态 |
| --- | --- | --- | --- | --- | --- |
| macOS | SCContentFilter (per-app) | CGEvent + enigo | Accessibility API | 无内置 | ✅ 可用 |
| Windows | CopyFromScreen / PrintWindow | SendInput + PowerShell | UI Automation | Windows.Media.Ocr | ⚠️ 增强中 |
| Linux | scrot | xdotool | 无 | 无 | ❌ 待开发 |

Sources: [common.ts](#root/pUYvuQJqrw7H), [computer-use-windows-enhancement.md](#root/KBJIkxllw0cL)

## MCP 工具集

### 工具分类总览

Computer Use MCP 提供 17 个核心工具（含复合操作），分为五大类：

| 类别 | 工具 | 数量 |
| --- | --- | --- |
| 截图/显示 | `screenshot`, `switch_display`, `zoom` | 3 |
| 鼠标操作 | `left_click`, `right_click`, `double_click`, `triple_click`, `middle_click`, `left_click_drag`, `mouse_move`, `left_mouse_down`, `left_mouse_up` | 9 |
| 键盘操作 | `key`, `type`, `hold_key` | 3 |
| 状态查询 | `cursor_position`, `request_access`, `list_granted_applications` | 3 |
| 复合/辅助 | `computer_batch`, `wait`, `open_application`, `read_clipboard`, `write_clipboard` | 5 |

Sources: [tools.ts](#root/ggFJh97JhB8f)

### 坐标系统

工具参数中的坐标描述在工具列表构建时从 `chicago_coordinate_mode` 特性开关读取，支持两种模式：

```typescript
const COORD_DESC: Record<CoordinateMode, { x: string; y: string }> = {
  pixels: {
    x: "Horizontal pixel position read directly from the most recent screenshot...",
    y: "Vertical pixel position read directly from the most recent screenshot...",
  },
  normalized_0_100: {
    x: "Horizontal position as a percentage of screen width, 0.0–100.0...",
    y: "Vertical position as a percentage of screen height, 0.0–100.0...",
  },
}
```

模型在一次会话中只能看到一种坐标约定，防止混淆。

Sources: [tools.ts](#root/SxOqVu4nURt6), [gates.ts](#root/26kitgzDtAvY)

### 批量操作

`computer_batch` 工具允许单次 API 调用执行多个操作序列，显著减少往返延迟：

```json
{
  "actions": [
    { "action": "left_click", "coordinate": [100, 200] },
    { "action": "type", "text": "hello" },
    { "action": "key", "text": "Return" }
  ]
}
```

批量执行时，每个操作前都会运行前台应用检查——如果某操作打开了非授权应用，后续操作的检查会捕获并停止。

Sources: [tools.ts](#root/REJeIH4mRz44), [toolCalls.ts](#root/iNlkOpr0AO9Q)

## 权限模型

### 三级权限体系

Computer Use 采用分层权限模型，基于应用类型分配不同权限级别：

```
graph TB
    A["request_access"] --> B{应用分类}
    B -->|浏览器| C["Tier: read"]
    B -->|IDE/终端| D["Tier: click"]
    B -->|系统应用| E["Tier: full"]
    
    C --> C1["✓ 可见"]
    C --> C2["✗ 不可交互"]
    
    D --> D1["✓ 可见"]
    D --> D2["✓ 左键点击"]
    D --> D3["✓ 滚轮滚动"]
    D --> D4["✗ 键盘输入"]
    D --> D5["✗ 右键/中键"]
    
    E --> E1["✓ 全部能力"]
    
    style E fill:#c8e6c9
    style D fill:#fff9c4
    style C fill:#ffcdd2
```

| 权限级别 | 能力 | 适用场景 |
| --- | --- | --- |
| **read** | 仅可见，截图时包含内容 | 浏览器（需使用 Claude-in-Chrome MCP 导航） |
| **click** | 可见 + 左键点击 + 滚轮 | IDE（VS Code、Cursor）、终端 |
| **full** | 全部能力 | Finder、系统设置等系统应用 |

Sources: [types.ts](#root/Uipi3gizdNV2)

### 权限标志位

与按应用授权正交，权限标志位控制全局能力：

```typescript
interface CuGrantFlags {
  clipboardRead: boolean    // 读取剪贴板
  clipboardWrite: boolean  // 写入剪贴板
  systemKeyCombos: boolean // 系统级快捷键（cmd+q、cmd+tab 等）
}
```

这些标志在 `request_access` 时作为独立选项请求，用户可单独开关。

Sources: [types.ts](#root/bTGzSL8yjHmQ)

## 安全门控机制

### 执行顺序

每次工具调用都经过严格的安全检查序列：

```
sequenceDiagram
    participant TC as toolCalls.ts
    participant Gate as 安全门控
    participant Exec as executor.ts
    
    TC->>Gate: 1. 杀死开关检查
    Note over Gate: adapter.isDisabled()
    TC->>Gate: 2. TCC 权限检查
    Note over Gate: macOS 辅助功能/屏幕录制
    TC->>Gate: 3. 工具特定门控
    Note over Gate: prepareForAction<br/>前台应用检查<br/>像素验证
    Gate->>Exec: 4. 调用执行器方法
    Exec-->>TC: 返回结果
```

工具特定门控在 `toolCalls.ts` 中实现，任何门控异常都直接返回工具错误，执行器永不调用。

Sources: [toolCalls.ts](#root/8gaBmKxQ0PZ6)

### 操作前准备序列

输入操作（点击/输入/按键/滚动/拖拽/移动）前执行准备序列：

1.  **隐藏非授权应用**：`prepareForAction` 隐藏所有不在白名单的应用，然后取消前台焦点
2.  **前台应用检查**：验证目标应用在授权列表中且权限级别足够
3.  **像素验证**（可选）：9×9 区域精确字节比对，确保截图未过时

```typescript
async prepareForAction(
  allowlistBundleIds: string[],
  displayId?: number,
): Promise<string[]>
```

该序列通过 `drainRunLoop()` 泵送 CFRunLoop，确保 macOS 上窗口管理器事件队列被及时处理。

Sources: [executor.ts](#root/yeMqSN5UXVFt), [drainRunLoop.ts](#root/CbBd0pQIcsQg)

## Windows 增强实现

### 窗口级截图

Windows 基础实现使用 `CopyFromScreen` 仅能截取全屏。增强方案利用 `PrintWindow` API 实现窗口级截图：

```powershell
# 核心 Win32 API
[DllImport("user32.dll")]
public static extern IntPtr FindWindow(string c, string t);
[DllImport("user32.dll")]
public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint f);
```

`PrintWindow` 即使窗口被遮挡或最小化也能捕获，这是 macOS SCContentFilter 无法实现的场景。

Sources: [windowCapture.ts](#root/nXs5hJOlY4iY)

### UI Automation 元素树

Windows 专属能力：通过 `System.Windows.Automation` 读取 UI 元素树结构：

```typescript
interface UIElement {
  name: string
  controlType: string      // Button, Edit, Text, List, Window...
  automationId: string
  boundingRect: { x: number; y: number; w: number; h: number }
  isEnabled: boolean
  value?: string
  children?: UIElement[]
}
```

支持操作：元素查找、点击（InvokePattern）、值设置（ValuePattern）、坐标点元素识别。这使得 AI 不仅能通过坐标点击，还能理解 UI 语义结构。

Sources: [uiAutomation.ts](#root/RQTFcBA4Q88f)

### OCR 文字识别

利用 Windows.Media.Ocr.OcrEngine 对截图进行文字识别：

```typescript
interface OcrResult {
  text: string
  lines: { text: string, bounds: {x, y, w, h} }[]
  language: string
}
```

已验证支持英语（en-US）和简体中文（zh-Hans-CN）。OCR 结果包含每行文字的边界框坐标，便于 AI 定位屏幕元素。

Sources: [ocr.ts](#root/qKnpUachlcKO)

### 窗口枚举

通过 `EnumWindows` API 枚举所有可见窗口，返回 HWND、进程 ID 和标题：

```typescript
interface WindowInfo {
  hwnd: number   // 窗口句柄
  pid: number   // 进程 ID
  title: string // 窗口标题
}
```

Sources: [windowEnum.ts](#root/hncGoTcB1LC6)

## 会话管理

### 文件锁机制

Computer Use 使用基于文件的锁实现多会话协调，防止并发操控冲突：

```typescript
interface ComputerUseLock {
  sessionId: string  // 会话 ID
  pid: number        // 进程 ID
  acquiredAt: number // 获取时间戳
}
```

锁文件位于配置目录（`~/.claude/computer-use.lock`），通过 `O_EXCL` 标志保证原子创建。实现包括 PID 存活检测和过期锁自动恢复。

Sources: [computerUseLock.ts](#root/KxppPiKFlLqO)

### Escape 热键拦截

macOS 平台通过 CGEventTap 注册全局 Escape 热键用于中止操作：

```typescript
export function registerEscHotkey(onEscape: () => void): boolean
export function unregisterEscHotkey(): void
export function notifyExpectedEscape(): void
```

热键注册时保留 CFRunLoop 泵引用，释放时递减引用计数。`notifyExpectedEscape()` 为模型合成的 Escape 打孔，防止被误捕获。

Sources: [escHotkey.ts](#root/bg0fRxBX23O7)

### 轮次结束清理

每个会话轮次结束时自动执行清理：

```typescript
export async function cleanupComputerUseAfterTurn(
  ctx: Pick<ToolUseContext, 'getAppState' | 'setAppState' | 'sendOSNotification'>
): Promise<void>
```

清理流程：

1.  自动取消隐藏 `prepareForAction` 隐藏的应用
2.  释放文件锁
3.  发送 "Claude is done using your computer" 系统通知

Sources: [cleanup.ts](#root/IhAIJbM40zOb)

## 渲染层集成

### 工具结果渲染

`toolRendering.tsx` 为每个工具定义用户友好的渲染显示：

| 工具 | 渲染格式 |
| --- | --- |
| `left_click` | `(x, y)` |
| `left_click_drag` | `(x1, y1) → (x2, y2)` |
| `type` | `"text content..."` |
| `scroll` | `方向 ×次数 at (x, y)` |
| `computer_batch` | `N actions` |

Sources: [toolRendering.tsx](#root/w4m9HzCWpD7p)

### 会话上下文绑定

`wrapper.tsx` 中的 `buildSessionContext()` 构建会话上下文，包含：

*   **读取**：授权应用列表、权限标志、显示选择器、截图尺寸
*   **写入**：权限变更回调、显示选择回调、截图捕获回调
*   **锁检查**：异步文件锁操作

该上下文在首次 `.call()` 时构建并缓存，进程生命周期内复用。

Sources: [wrapper.tsx](#root/ogUhHNtt0nrs)

## 特性开关配置

### GrowthBook 门控

Computer Use 通过 GrowthBook JSON 特性 `tengu_malort_pedway` 配置：

```typescript
const DEFAULTS: ChicagoConfig = {
  enabled: true,
  pixelValidation: false,
  clipboardPasteMultiline: true,
  mouseAnimation: true,
  hideBeforeAction: true,
  autoTargetDisplay: true,
  clipboardGuard: true,
  coordinateMode: 'pixels',
}
```

坐标模式在首次读取时冻结，确保工具描述和执行器使用同一值。

Sources: [gates.ts](#root/26kitgzDtAvY)

## 相关文档

*   [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) - MCP 协议基础
*   [权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) - 安全架构
*   [沙箱安全机制](17-sha-xiang-an-quan-ji-zhi.md) - 安全隔离

## 相关条目
- [[12-mcp-xie-yi-ji-cheng]]
- [[17-sha-xiang-an-quan-ji-zhi]]
