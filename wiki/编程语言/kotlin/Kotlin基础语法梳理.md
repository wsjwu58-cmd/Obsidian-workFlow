---
created: 2026-08-31
updated: 2026-08-31
sources: [Kotlin 官方 Basic syntax, Kotlin Clippings]
tags: [Kotlin, 基础语法, 复习, type/教程, status/已实践]
---

# Kotlin 基础语法梳理

> 这是一张 Kotlin 复习地图：先掌握语言骨架，再按主题进入 Clippings。并发和协程不属于基础语法细节，单独见 [[Kotlin多线程与协程]]。

## 1. 一句话心智模型

Kotlin 是静态类型、空安全、以表达式为中心、面向对象与函数式编程并存的语言；写代码时优先让类型系统表达约束，再用简洁语法减少样板代码。

## 2. 程序结构与变量

```kotlin
package demo.app

import kotlin.math.roundToInt

fun main() {
    val raw: String = "42"          // val：引用不可重新赋值
    var count = raw.toInt()         // var：变量可重新赋值，类型可推断
    count += 1
    println("count=$count, rounded=${3.6.roundToInt()}")
}
```

- `package` 和 `import` 位于文件顶部；包名不必与磁盘目录相同。
- `val` 是只读变量，不等于对象深度不可变；`val list = mutableListOf(1)` 仍可修改列表内容。
- `var` 只有在确实需要重新绑定时使用；优先 `val`，有利于读代码和并发安全。
- 常见类型：`Int`、`Long`、`Double`、`Float`、`Boolean`、`Char`、`String`、`Any`、`Unit`、`Nothing`。
- 类型推断适合局部变量；公共 API、复杂泛型和空值边界建议显式写类型。

## 3. 字符串、运算与相等

```kotlin
val name = "Kotlin"
val message = "hello, $name; length=${name.length}"
val sameValue = "a" == "a"       // 结构相等：调用 equals
val sameObject = name === name     // 引用相等：是否为同一对象
```

- 字符串模板使用 `$name` 或 `${expression}`，不要用字符串拼接堆叠表达式。
- `==` 比较值，`===` 比较引用；数据类会按属性生成结构相等语义。
- Kotlin 没有传统的三元运算符，`if` 和 `when` 本身就是表达式。

## 4. 函数、参数与返回值

```kotlin
fun sum(a: Int, b: Int): Int = a + b

fun greet(name: String, prefix: String = "Hello"): String =
    "$prefix, $name"

fun logAll(vararg values: String) {
    values.forEach(::println)
}

val text = greet(name = "Kotlin")
```

- 表达式函数体适合短逻辑；多分支或需要调试时使用块函数体和显式 `return`。
- 命名参数提高调用可读性，默认参数减少重载数量，`vararg` 接收可变数量参数。
- `Unit` 表示没有有意义的返回值，通常可以省略；`Nothing` 表示函数不会正常返回（例如始终抛异常）。
- 扩展函数给已有类型增加调用语法，但不能访问其私有成员，也不会真正修改原类型。

## 5. 条件、循环与范围

```kotlin
fun classify(score: Int): String = when {
    score < 0 -> "invalid"
    score >= 90 -> "A"
    score >= 60 -> "pass"
    else -> "fail"
}

for (i in 0 until 5 step 2) print("$i ") // 0 2 4
```

- `if`、`when` 能返回值；分支作为表达式时必须覆盖所有可能路径，通常用 `else` 收口。
- `for (item in items)` 依赖 `iterator()`；`indices` 遍历索引，能避免手写边界。
- `1..5` 包含末端，`until` 不包含末端，`downTo` 倒序，`step` 设置步长。
- `while` / `do-while` 适合条件驱动循环；集合遍历优先使用迭代器或集合函数。

## 6. 空安全与类型检查

```kotlin
fun printLength(value: String?) {
    val length = value?.length ?: 0
    println(length)
}

fun describe(value: Any): String = when (value) {
    is String -> "string(${value.length})" // 智能转换
    is Int -> "int($value)"
    else -> "other"
}
```

- `String` 与 `String?` 是不同类型；只有带 `?` 的类型才能接收 `null`。
- `?.` 是安全调用，`?:` 是 Elvis 运算符，`!!` 是强制断言，应尽量让编译器和业务校验替代它。
- `is` / `!is` 做类型检查并触发智能转换；`as?` 转换失败返回 `null`，比 `as` 更适合不确定输入。
- 平台类型（如未标注空值的 Java API 返回值）是 Kotlin 空安全的边界，应尽早转成明确的可空/不可空类型。

## 7. 集合：只读接口与可变实现

```kotlin
val numbers: List<Int> = listOf(1, 2, 3)
val evenSquares = numbers
    .filter { it % 2 == 0 }
    .map { it * it }

val mutable = mutableListOf(1)
mutable += 2
```

- `List` / `Set` / `Map` 表示只读视图，`MutableList` / `MutableSet` / `MutableMap` 才暴露修改操作。
- “只读”不等于底层对象永远不可变；跨线程或跨模块共享时要控制所有权，必要时复制或使用线程安全结构。
- `map` 转换元素，`filter` 保留元素，`fold` 聚合状态，`associate` 构造映射；链式操作要留意中间集合带来的开销。
- `ArrayDeque` 适合双端队列；需要按键查值时用 `Map`；需要去重时用 `Set`。

## 8. 类、对象与类型建模

```kotlin
data class User(val id: Long, val name: String)

sealed interface LoadState {
    data object Loading : LoadState
    data class Success(val user: User) : LoadState
    data class Error(val cause: Throwable) : LoadState
}

fun render(state: LoadState): String = when (state) {
    LoadState.Loading -> "loading"
    is LoadState.Success -> state.user.name
    is LoadState.Error -> "error"
}
```

- 主构造函数可以直接声明属性；`init` 用于构造期校验；次构造函数只在确有多种初始化协议时使用。
- 类默认 `final`；只有设计为可继承的类/成员才标记 `open`，覆盖成员必须显式 `override`。
- `data class` 适合值对象，会生成 `equals`、`hashCode`、`toString`、`copy` 和解构组件。
- `sealed class` / `sealed interface` 用有限状态建模，配合 `when` 可让编译器检查分支完整性。
- `object` 表示单例；`companion object` 提供与类关联的工厂或常量；嵌套类默认不持有外部类引用，`inner` 才会持有。
- 接口只描述能力；委托（`by`）适合把实现转交给另一个对象，避免继承层级膨胀。

## 9. 高阶函数、Lambda 与作用域函数

```kotlin
fun transform(input: String, f: (String) -> String): String = f(input)

val result = transform("kotlin") { it.uppercase() }
val builder = StringBuilder().apply {
    append("Kotlin ")
    append("DSL")
}.toString()
```

- 函数类型写作 `(A, B) -> R`；Lambda 是值，可以作为参数、返回值或变量。
- `it` 适合单参数短 Lambda；复杂 Lambda 显式命名参数更清楚。
- `let` 以 `it` 处理临时值/可空值，`run` 和 `with` 以 `this` 配置对象并返回结果，`apply` 配置对象后返回对象，`also` 做附加动作后返回对象。
- 作用域函数是语法工具，不要嵌套到无法分辨 `this` / `it` 的程度。
- 函数引用（`::name`）、接收器 Lambda 和类型安全构建器，是集合 API、DSL 与协程 API 的基础。

## 10. 异常、可见性与泛型

```kotlin
fun parsePort(raw: String): Int = try {
    raw.toInt().also { require(it in 1..65535) }
} catch (e: NumberFormatException) {
    throw IllegalArgumentException("port must be an integer", e)
}
```

- Kotlin 没有受检异常；仍应捕获能处理的异常，并保留原因链，不要用空 `catch` 吞掉故障。
- `public` 是默认可见性；`private`、`protected`、`internal` 用于收紧边界。
- 泛型让容器和函数复用类型约束；`out` 适合生产者，`in` 适合消费者，遵循“生产者 out、消费者 in”。
- `lateinit` 和惰性初始化要有明确生命周期；并发场景下不要把它们当作线程安全保证。

## 11. 复习顺序

1. 先通读变量、函数、字符串、条件和循环，能独立写出小程序。
2. 再掌握空安全、集合和类型检查，这是 Kotlin 与 Java 使用体验差异最大的部分。
3. 接着学习类、接口、数据类、密封类型、对象、委托和函数式编程。
4. 最后进入 [[Kotlin多线程与协程]]，理解线程、调度器、挂起、取消和共享状态。
5. 写生产代码时回看 Clippings 的细节页，再用官方文档确认版本相关行为。

## 12. Clippings 导航

### 控制流与集合

- [[For loop and ranges]] · [[If expression]] · [[Loops repeat statement]] · [[When expression]] · [[While loops]]
- [[For loop and lists]] · [[List]] · [[Mutable List]] · [[Work with MutableLists]] · [[Map]] · [[Mutable Map]] · [[Set]] · [[Mutable Set]] · [[Multi-dimensional list]]
- [[ArrayDeque]] · [[Collections as interface]] · [[Comparable and Comparator]] · [[For loop and iterables]] · [[Iterators]] · [[Mutable Map and Mutable Set as interfaces]] · [[Stack]]

### 空安全、类与对象

- [[Avoiding NPEs. Null safety]] · [[Nullable and non-nullable types]] · [[Null and collections]] · [[Type cast and smart cast]] · [[Type system]]
- [[Constructors]] · [[Secondary constructor]] · [[Overriding constructors]] · [[Inheritance in Kotlin]] · [[Inheritance and constructors]] · [[Final members]]
- [[Introduction to interfaces]] · [[Interface inheritance]] · [[Abstract classes]] · [[Overriding functions]] · [[Overriding properties]] · [[Argument naming in overridden functions]] · [[Visibility modifiers for members]]
- [[Data class]] · [[Destructuring declarations]] · [[Enum]] · [[Sealed class and interface]] · [[Pair and Triple]] · [[toString() 1]]
- [[Member functions]] · [[Property accessors]] · [[Lazy initialization]] · [[Nested and inner classes]] · [[Object declarations]] · [[Companion object]]

### 函数式编程与委托

- [[Functions as objects]] · [[Lambda expressions]] · [[Function references]] · [[Currying]] · [[Lambda with receiver]]
- [[Scope functions let, run, and with]] · [[Scope functions apply and also]] · [[Type-safe builders]]
- [[Delegate]] · [[Class delegation]] · [[Standard delegates]]

### Gradle 与项目基础设施

- [[Gradle overview]] · [[Basic project with Gradle]] · [[Building apps using Gradle]] · [[Gradle build configuration]] · [[Dependency management repositories]]

## 参考资料

- [Kotlin 官方 Basic syntax overview](https://kotlinlang.org/docs/basic-syntax.html)：程序结构、变量、函数、类、控制流、集合、空安全和类型检查。
- [Kotlin 官方语言文档](https://kotlinlang.org/docs/reference/)：当前稳定版、标准库、集合、协程和 Kotlin Multiplatform 文档入口。
- [Kotlin 官方 Coding conventions](https://kotlinlang.org/docs/coding-conventions.html)：命名、格式和 API 设计约定。

## 相关条目

- [[Kotlin多线程与协程]]
