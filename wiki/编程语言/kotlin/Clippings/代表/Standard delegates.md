提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

除了类委托之外，Kotlin 还提供了一项强大的功能，称为。该特性允许将属性的 getter 和 setter 方法委托给另一个对象。在重用通用行为、分离逻辑或仅计算一次值时，此功能非常有用。虽然创建和使用委托属性的详细信息将在另一篇文章中介绍，但这里我们将提供一个简要概述。我们还将探讨 Kotlin 中的 **属性** 。

## 委托属性概述

与传统属性不同，委托属性并非由支持。相反，它们 **将获取和设置属性值的操作委托给另一段代码** 。这种抽象使得相似属性之间可以共享功能。例如，您可以将属性值存储在映射中，而不是使用单独的字段。

委托属性的使用方法是：声明属性本身及其使用的委托。\`by\` `by 表明该属性由提供的委托控制 ` 而不是由其自身字段控制。

例如：

```kotlin
class Example {
    var p: String by Delegate()
}
```

语法如下： `val/var <property name>: <Type> by <delegate>`.

在底层，委托具有 `getValue()` 和 `setValue()` 方法，它们分别接管了属性对应的 `get()` 和 `set()` 方法。

## 标准代表

Kotlin提供了一组 **标准委托** ，可用于创建：

1. ：该值仅在首次访问时计算。
2. ：监听器会收到此属性更改的通知。
3. ：允许 lambda 函数决定是否接受或拒绝新值。
4. **NotNull 属性** ：非空属性的属性委托，该属性必须在访问之前进行初始化。
5. **将属性存储在映射中** ：与其为每个属性使用单独的字段，不如将属性存储在映射中。

让我们进一步探讨它们中的每一个。

**1) 惰性属性：** `lazy` 函数接受一个 lambda 表达式，并返回一个 `Lazy<T>` 实例，该实例作为实现惰性属性的委托。首次调用 `get()` 函数会执行传递给 `lazy()` lambda 表达式，并将结果保存下来。后续调用 `get()` 函数只需返回已保存（缓存）的结果即可。

我们举个例子：

```kotlin
val lazyValue: String by lazy {
    print("Computed! ")
    "Hello"
}

fun main() {
    println(lazyValue) // Computed! Hello
    println(lazyValue) // Hello
}
```

在这个例子中，lambda 表达式内部的代码仅在第一次访问 `lazyValue` 属性时执行，并将结果缓存起来。之后，对该值的任何额外访问都只会检索缓存的值，而不会执行任何代码，因此第二个 `println()` 只会打印值 `"Hello"` 。

**2) 可观察属性：** `observable` 委托允许在属性值发生变化时触发 lambda 函数，从而发出更改通知或更新其他相关属性。

我们来看一个例子：

```kotlin
import kotlin.properties.Delegates

class User {
    var rank: String by Delegates.observable("<no rank>") {
        prop, old, new -> println("${prop.name}: $old -> $new")
    }
}

fun main() {
    val user = User()
    user.rank = "first"  // rank: <no rank> -> first
    user.rank = "second" // rank: first -> second
}
```

在这个例子中， `User` 类有一个 `rank` 属性，该属性被委托给一个 `observable` 委托。这个 `observable` 委托接受两个参数：属性的初始值（本例中为 `"<no rank>"` ）和一个 lambda 函数，该函数会在属性值改变时被调用。

lambda 函数接受三个参数：要更改的属性的引用 ( `prop` )、属性的旧值 ( `old` ) 和属性的新值 ( `new` )。在本例中，lambda 函数会在 `rank` 属性更改时，简单地打印出该属性的名称及其旧值和新值。

> [!warning] Warning
> 在代码中使用 `observable` 、 `vetoable` 或 `notNull` 委托时，必须导入 `kotlin.properties.Delegates` 包。

**3) 可否决属性：** `vetoable` 委托的工作方式与 `observable` 委托类似，但有一些关键区别。lambda 函数会在设置新值之前被调用，它允许该函数决定是否接受或拒绝新值。

我们来看一个例子：

```kotlin
import kotlin.properties.Delegates

var max: Int by Delegates.vetoable(0) { prop, old, new ->
    new > old
}

fun main() {
    println(max) // 0
    max = 10
    println(max) // 10
    max = 5
    println(max) // 10
}
```

在这个例子中， `vetoable` 委托确保 `max` 只能被设置为大于其当前值的值。如果尝试将其设置为更小的值，则新值将被丢弃，属性将保留旧值。

**4) NotNull 属性：** `notNull` 是一个属性委托，用于表示非空属性，该属性必须在访问之前进行初始化。

我们举个例子：

```kotlin
import kotlin.properties.Delegates

class Person{
    var name: String by Delegates.notNull()
}

fun main() {
    val person = Person()
    person.name // Throws IllegalStateException:
                // Property name should be initialized before get.
    person.name = "Ahmed Omar"
    println(person.name) // Prints "Ahmed Omar"
}
```

在这个例子中， `notNull` 委托确保 `Person` 类的 `name` 属性在被访问之前先被初始化。如果在 name 属性被初始化之前尝试访问它，则会抛出异常。

**5) 将属性存储在映射中：** 属性可以存储在 `MutableMap` 或 `Map` 中，分别用于支持可变属性或属性。

请看以下示例：

```kotlin
class User(val map: MutableMap<String, Any?>) {
    var name: String by map
    var age: Int     by map
}

fun main() {
    val user = User(mutableMapOf(
        "name" to "Ahmed Omar",
        "age"  to 25
    ))

    println(user.name) // Prints "Ahmed Omar"
    println(user.age)  // Prints 25

    user.name = "Ahmed Omar"
    user.age = 30

    println(user.name) // Prints "Ahmed Omar"
    println(user.age)  // Prints 30
}
```

在这个例子中，定义了 `User` 类，它接受一个 `MutableMap` 作为构造函数参数。User 类的 `name` 和 `age` 属性被 `User` 给 `map` 属性，这意味着它们的值存储在 map 中，而不是每个属性都存储在单独的字段中。

## 实际应用案例

Kotlin 中的标准委托属性可以在各种实际场景中使用。其中包括：

1. **延迟初始化** ： `lazy` 委托可以用于仅在首次访问属性时才对其进行初始化；它适用于计算成本高昂或可能根本不需要的属性。
2. **观察属性变化** ： `observable` 委托可用于观察属性的变化，并在属性发生变化时执行操作，例如更新 UI 或验证新值。
3. **否决属性更改** ：可以使用 `vetoable` 委托，根据自定义逻辑否决对属性的更改，例如确保值保持在特定范围内或满足特定条件。
4. **NotNull 属性** ：当属性必须先初始化才能访问，并且在初始化之前访问该属性会导致抛出异常时，可以使用 `notNull` 委托。这对于确保在使用对象之前满足某些前提条件非常有用。
5. **将属性存储在映射中** ：可以使用 `map` 和 `mutableMap` 委托将属性存储在映射中，而不是为每个属性使用单独的字段；它们对于动态数据结构或序列化和反序列化对象非常有用。

## 结论

Kotlin 中的标准委托属性提供了一种灵活高效的方式来实现属性的通用行为。它们可以简化代码，提高组合性和模块化程度，并提供更改对象行为的灵活性，从而提升 Kotlin 代码的整体效率和可读性。

17 位学员喜欢这篇理论文章， 0 位学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
