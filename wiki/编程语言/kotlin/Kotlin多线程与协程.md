---
created: 2026-08-31
updated: 2026-08-31
sources: [Kotlin 官方 Coroutines basics, Coroutines guide, Coroutine context and dispatchers, Shared mutable state and concurrency]
tags: [Kotlin, 多线程, 协程, 并发, type/教程, status/已实践]
---

# Kotlin 多线程与协程

> 线程是操作系统调度的执行载体；协程是可以挂起和恢复的计算。协程降低线程占用和异步代码复杂度，但不会自动消除并发竞态。

## 1. 版本与依赖

本文示例按 **Kotlin 2.4.10 + kotlinx-coroutines 1.11.0** 编写。Kotlin 标准库只提供协程所需的低层抽象；`launch`、`async`、`Dispatchers`、`Flow`、`Channel` 等来自 `kotlinx.coroutines`。

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.4.10"
    application
}

repositories { mavenCentral() }

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.11.0")
}
```

Kotlin/JVM 可以直接使用 Java 的 `Thread`、`ExecutorService`、`AtomicInteger` 和锁。Kotlin Multiplatform 的共享代码不要依赖 JVM 专属线程 API；优先把并发协议放在 `kotlinx.coroutines`，把平台线程池接入留给平台实现。

## 2. 并发、并行、线程、协程

| 概念 | 解决的问题 | 关键特征 |
| --- | --- | --- |
| 线程 | 执行代码 | OS 调度，创建和栈内存成本较高 |
| 并发 | 多个任务在时间上交错推进 | 不一定同时运行 |
| 并行 | 多个任务同时运行 | 需要多核和多执行线程 |
| 协程 | 以轻量任务表达并发 | 在挂起点释放线程，可在不同线程恢复 |

在 JVM/Native 上，协程最终仍运行在线程上。`delay` 会挂起协程而不是阻塞线程；但普通阻塞调用（同步文件、数据库、`Thread.sleep`）仍会占住线程，不能因为包在 `launch` 里就变成非阻塞。

## 3. JVM 线程：少量、明确、可回收

```kotlin
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

fun main() {
    val pool = Executors.newFixedThreadPool(2)
    try {
        val tasks = (1..4).map { id ->
            pool.submit {
                println("task=$id thread=${Thread.currentThread().name}")
            }
        }
        tasks.forEach { it.get(5, TimeUnit.SECONDS) }
    } finally {
        pool.shutdown()
        if (!pool.awaitTermination(5, TimeUnit.SECONDS)) {
            pool.shutdownNow()
        }
    }
}
```

- `Thread { ... }.start()` 适合演示或极少量独立线程；业务代码通常交给有界线程池。
- 线程池需要限制并发度、设置队列/拒绝策略，并在生命周期结束时 `shutdown`；不能无限创建线程。
- `join` / `Future.get` / `awaitTermination` 会阻塞调用线程；在 UI 或服务器请求线程上使用前要评估超时与资源占用。
- 共享可变变量的 `counter++` 不是原子操作；`@Volatile` 只保证单次读写可见性，不保证“读-改-写”整体原子。
- 计数器可用 `AtomicInteger`；复杂不变量可用锁、线程封闭、消息传递或不可变快照。

## 4. 协程的最小构件

```kotlin
import kotlinx.coroutines.*

suspend fun fetchName(): String {
    delay(100) // 挂起，不占用当前线程
    return "Kotlin"
}

fun main() = runBlocking {
    try {
        coroutineScope {
            val first = async { fetchName() }
            val second = async { fetchName() }
            println("${first.await()} + ${second.await()}")
        }
    } catch (e: CancellationException) {
        throw e // 取消是正常控制流，不要吞掉
    } catch (e: Exception) {
        println("request failed: ${e.message}")
    }
}
```

- `suspend` 表示函数允许在挂起点暂停，不代表函数自动新建线程或一定异步。
- `launch` 返回 `Job`，适合不需要结果的任务；`async` 返回 `Deferred<T>`，通过 `await()` 获取结果。
- `runBlocking` 会阻塞当前线程，主要用于命令行入口、测试或桥接不支持 `suspend` 的旧 API；服务端业务不要到处嵌套它。
- `coroutineScope` 等待所有子协程结束，并把失败向上传播；这就是结构化并发的基本边界。

## 5. CoroutineContext 与调度器

| 调度器 | 适用场景 | 注意 |
| --- | --- | --- |
| `Dispatchers.Default` | CPU 密集型计算 | 共享后台线程池，不要放长时间阻塞 IO |
| `Dispatchers.IO` | 阻塞式 IO 适配 | 仍然是阻塞线程，只是使用 IO 线程池 |
| `Dispatchers.Main` | UI 状态更新 | 依赖平台；共享代码不要硬编码平台 UI 调度器 |
| `Dispatchers.Unconfined` | 特殊低层场景 | 不应作为一般业务默认调度器 |
| `withContext(...)` | 切换上下文并等待结果 | 作用域结束后回到原上下文 |

调度器决定“在哪些线程执行”，作用域决定“生命周期归谁管理”。`launch` 不指定调度器时继承父作用域；协程可能在一个线程挂起、在另一个线程恢复，不要用线程名当作业务身份。

```kotlin
suspend fun calculate(): Long = withContext(Dispatchers.Default) {
    (1L..1_000_000L).sum()
}

suspend fun readBlockingFile(): String = withContext(Dispatchers.IO) {
    java.nio.file.Files.readString(java.nio.file.Path.of("input.txt"))
}
```

生产代码应把 `CoroutineScope` 作为组件生命周期的一部分（例如服务关闭时取消），避免 `GlobalScope` 产生无法回收的后台任务。

## 6. 并发组合与异常

- 独立计算需要并发时，在同一个 `coroutineScope` 中启动多个 `async`，最后集中 `await`。
- `withContext` 更像“切换上下文执行一段工作并返回结果”；不要为了并发把所有代码改成 `async`。
- 普通子协程抛出非 `CancellationException` 异常时，会取消父作用域和兄弟协程；这让失败不会悄悄脱离请求生命周期。
- 需要兄弟任务相互独立时使用 `supervisorScope` 或 `SupervisorJob`，并在边界记录异常；监督不是忽略错误。
- `CoroutineExceptionHandler` 只适合处理未捕获的“根协程”异常，不能替代业务层的 `try/catch` 或 `await`。

## 7. 取消、超时与资源释放

```kotlin
import kotlinx.coroutines.*
import kotlin.time.Duration.Companion.seconds

suspend fun requestWithTimeout(): String = withTimeout(2.seconds) {
    try {
        delay(500)
        "ok"
    } finally {
        // 关闭文件、取消订阅、释放临时资源
        println("request cleanup")
    }
}
```

- `Job.cancel()` 是协作式取消；挂起函数通常会检查取消状态，纯 CPU 循环需要主动调用 `ensureActive()` / `yield()`。
- `CancellationException` 表示正常取消，捕获后如果不能完成清理，应重新抛出。
- `withTimeout` 超时会取消其内部作用域；所有资源必须放在 `finally` 或使用 `use` 中。
- 不要在 `finally` 中继续执行不可取消的长任务；必要时只做短小清理，或明确使用 `NonCancellable` 保护必须完成的收尾。

## 8. 共享状态与线程安全

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

suspend fun safeCounter(): Int {
    val mutex = Mutex()
    var counter = 0
    coroutineScope {
        repeat(100) {
            launch(Dispatchers.Default) {
                repeat(1_000) {
                    mutex.withLock { counter++ }
                }
            }
        }
    }
    return counter
}
```

选择顺序通常是：

1. 优先不共享可变状态，使用局部变量和不可变结果。
2. 简单原子操作使用 `AtomicInteger` 等线程安全结构。
3. 一段需要保持一致性的临界区使用 `Mutex.withLock`；它挂起等待，不像 `synchronized` 那样直接阻塞线程。
4. 能按单一所有者组织的状态使用线程封闭或 actor/消息传递。
5. 复杂跨模块状态考虑不可变状态容器和单向事件流，明确谁可以写入。

`Flow` 默认按顺序在同一协程中执行，适合表达可取消的数据流；`Channel` 是协程间非阻塞通信原语，发送或接收会在无法继续时挂起。两者都需要明确背压、缓冲、取消和收集者生命周期。

## 9. 生产落地检查清单

- 计算任务放 `Default`，阻塞 IO 放 `IO`，UI 更新回到 `Main`；不要用一个调度器包打天下。
- 业务组件持有自己的作用域，在关闭时取消；不要使用 `GlobalScope` 隐式逃逸。
- 每个 `launch` 都要有可追踪的生命周期；每个 `async` 都要保证 `await`，否则异常可能延迟暴露。
- 所有超时、取消、重试和资源清理都写在边界处；不要捕获 `Exception` 后吞掉取消。
- 共享状态先设计所有权，再选择原子类、`Mutex`、线程封闭或消息传递；协程数量多不等于数据自动安全。
- 对外部阻塞库做适配隔离，避免在 `Default`、主线程或有限并发的请求线程中直接阻塞。
- 使用日志记录请求 ID、协程名和业务阶段；需要时启用 `-Dkotlinx.coroutines.debug`，不要只看线程名。

## 10. 常见误区

| 误区 | 正确理解 |
| --- | --- |
| 协程等于线程 | 协程是轻量任务，最终仍由线程执行 |
| `suspend` 会自动并行 | `suspend` 只允许挂起；并发要显式使用作用域和构建器 |
| `delay` 等同 `Thread.sleep` | `delay` 释放线程；`Thread.sleep` 会阻塞线程 |
| `@Volatile` 能修复计数器 | 只保证可见性，不保证复合操作原子性 |
| `launch` 后马上读共享变量 | `launch` 是异步启动，必须 `join` / `coroutineScope` 等待 |
| 到处用 `runBlocking` | 它会阻塞线程，只用于入口/测试/桥接 |
| 使用 `GlobalScope` 省事 | 任务失去调用方生命周期，容易泄漏和难以取消 |
| 捕获所有异常并继续 | 取消是协作式控制流，必须保留 `CancellationException` |
| 无限创建专用线程 | 线程是昂贵资源；复用受控线程池或标准调度器 |

## 参考资料

- [Kotlin 官方 Coroutines basics](https://kotlinlang.org/docs/coroutines-basics.html)：挂起函数、构建器和结构化并发。
- [Kotlin 官方 Coroutines guide](https://kotlinlang.org/docs/coroutines-guide.html)：`launch`、`async`、Flow、Channel、取消、异常和共享状态总览。
- [Kotlin 官方 Coroutine context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html)：上下文、调度器、线程切换和调试。
- [Kotlin 官方 Shared mutable state and concurrency](https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html)：原子类、线程封闭和 `Mutex`。
- [Kotlin 官方 Coroutine exceptions handling](https://kotlinlang.org/docs/exception-handling.html)：取消异常、父子关系和监督作用域。
- [kotlinx.coroutines 官方 API：Channel](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/)：协程间非阻塞通信和缓冲。
- [kotlinx.coroutines 官方 API：Flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/)：冷流与顺序执行语义。

## 相关条目

- [[Kotlin基础语法梳理]]
- [[java高级技术]]
- [[Stream]]
