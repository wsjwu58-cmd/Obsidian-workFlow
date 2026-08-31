## Lambda 接收器

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

正如我们在之前的文章中看到的，Kotlin 中的 **函数** 是：我们可以创建返回函数的函数，甚至可以将函数作为参数。你可能还记得，在 Kotlin 中可以使用 **lambda 表达式** （函数，即未声明但直接作为表达式传递的函数）。借助 lambda 表达式，我们可以动态地编写函数的行为并将其用作函数参数。我们还可以将函数的行为存储为一个变量。此外，Kotlin 还引入了，它提供了一种无需类继承即可扩展现有类并添加新功能的方法。

在本主题中，您将学习如何将这两个概念结合起来：我们将讨论“扩展 lambda”，技术上称为“ **带接收器的 lambda** ”，并学习如何在我们的代码中使用它们。

## 接收者

首先，什么是 **接收器** ？在 Kotlin 中，每一段代码都必须有一个（或多个）关联的类型来接收它。

在扩展函数的上下文中，接收器是一个对象实例，它通过函数扩展自身的功能。可以省略接收器，以便直接访问接收器的成员。以下代码展示了一个检查整数是否为偶数的扩展函数。它展示了如何访问整数本身，也就是我们操作的接收器（ `this` ）：

```kotlin
fun Int.isEven() = this % 2 == 0

fun main() {
    println("Is 2 even?: ${2.isEven()}") // true
    println("Is 3 even?: ${3.isEven()}") // false
}
```

**带有接收器的 lambda** 表达式是一种定义行为的方式，类似于扩展函数，它使用 来操作对象。要将 lambda 表达式转换为带有接收器的 lambda 表达式，您可以将 lambda 表达式的某个参数赋予接收器的特殊状态，这样您就可以直接引用其成员而无需任何限定符。

## 使用带有接收器的 lambda 函数

使用带有接收器的 lambda 表达式，您可以指定 lambda 表达式主体中方法的解析方式。接收器是一种扩展函数类型。它允许在 lambda 表达式主体中访问接收器的可见方法和属性，而无需任何额外的限定符。

我们可以通过实现一个的 sum 函数来探索这个概念。

```kotlin
val sum: (Int, Int) -> Int = { a, b -> a + b }
fun main() {
    println(sum(1, 2)) // 3
}
```

我们可以使用带有接收器的 lambda 函数来重写我们的代码。

```kotlin
val sum: Int.(Int) -> Int = { a -> this + a }

fun main() {
    println(sum(1, 2)) // 3
    println(1.sum(2)) // 3
}
```

函数类型可以选择性地具有额外的，该类型在表示法中的点之前指定： `A.(B) -> C { body }` 表示可以在A 上调用的函数，该对象具有参数 B，返回值 C，并在函数体中执行任何操作。

在函数字面量 **内部** ，可以使用表达式 `this` 访问接收器对象的成员。

我们必须强调 **接收者的上下文** 。Kotlin 中的普通 lambda 函数（第一种情况）如下：一组显式参数和 lambda 函数体，用箭头分隔： `(A,B) -> C` ，在本例中为： `(Int, Int) -> Int` 。

要将其转换为带有接收器的 lambda 表达式，我们需要将移到括号外。它既类似于 lambda 表达式，也类似于扩展函数，因此您可以将这些概念结合起来使用。由于接收器的上下文，您可以使用扩展函数。我们可以使用 `this` ，这样就可以对其值加上参数进行 `sum` 。因此，它可以定义为 `A.(B) -> C` ，在本例中为 `Int.(Int)->Int` ，其中 \`A\` 是接收器，我们可以使用 `this` 对其进行操作，参见 `sum(1,2)` 。此外，由于隐式的 `this` ，我们也可以像使用扩展函数一样使用带有接收器的 lambda 表达式，参见 \` `1.sum(2)` 。

让我们尝试将这段示例代码推广到一个代码块中，该代码块允许我们使用带有接收器的 lambda 表达式对整数执行一系列操作。我们将接收器用作扩展，并期望该函数块中的整数处理函数能够处理它，从而得到一个整数值。

```kotlin
// Extension function for Int, which applies function f to the current Int
fun Int.opp(f: Int.() -> Int): Int = f()

fun main() {
    // Use the opp function to multiply the number 10 by 2
    var res = 10.opp { this.times(2) }
    println(res) // 20

    // Another way to use the opp function to add 10 to the number 10
    // We can omit "this" as the context explicitly refers to the current Int
    res = 10.opp { plus(10) }
    println(res) // 20

    // Yet another way to multiply the number 10 by 2 using the opp function
    res = 10.opp { this * 2 }
    println(res) // 20
}
```

如上所示，我们直接调用 `f()` 函数，它等价于 `this.f()` 。同样，每个不带限定符的函数调用都使用 Integer 实例作为接收器。

## 使用 lambda 函数和接收器

当接收者类型可以从上下文推断出来时，Lambda 表达式可以用作带有接收者的函数字面量。它们最重要的应用示例之一是或领域特定语言 ( **DSL** )。(DSL) 允许我们使用声明式语法轻松地对复杂结构进行编码。以下代码展示了如何将类型安全构建器与 `StringBuilder` 类结合使用，从而高效地执行多个字符串操作。例如，使用 `append` 方法，我们可以指定的字符序列；最后，在完成所有操作后，我们返回最终的字符串。

```kotlin
// Safe Builder String with Lambda with receiver
fun myString(init: StringBuilder.() -> Unit): String {
    return StringBuilder().apply(init).toString()
}

fun main() {
    val str = myString {
        append("Hello, ".uppercase())
        append("World!")
    }
    println(str) // HELLO, World!
}
```

最后，标准库和第三方库广泛使用带有接收器的 lambda 表达式来改善开发者的体验。这是执行 DSL 操作的基础。apply `apply()` 就是一个例子。

```kotlin
fun MutableMap<String, Any>.apply(block: MutableMap<String, Any>.() -> Unit): MutableMap<String, Any> {
    block()
    return this
}

fun main() {
    val student: MutableMap<String, Any> = mutableMapOf(
        "name" to "John",
        "age" to 20
    )

    student.apply {
        this["name"] = (this["name"] as String).uppercase()
        this["age"] = (this["age"] as Int) + 1
    }

    println(student) // {name=JOHN, age=21}
}
```

基本上，所有 `apply` 函数都会调用提供的接收器上的扩展的参数，并返回接收器本身。

## 结论

在本主题中，我们了解了如何利用带有接收器的 lambda 表达式来创建更好、更易读的程序结构。

带有接收器的 Lambda 表达式是通用化代码块的绝佳工具，它允许我们执行一系列操作或构建领域特定语言 (DSL)。使用带有接收器的 Lambda 表达式的优势在于能够重用代码、创建抽象或定义原始类型的扩展，从而为各种字面量（例如日期）创建易读的，或为对象创建构建器。

准备好回答问题和完成任务了吗？开始吧！

74 名学员喜欢这部分理论内容， 26 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
