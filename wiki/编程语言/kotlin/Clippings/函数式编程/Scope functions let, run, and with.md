## 作用域函数：let、run 和 with

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

## 介绍

我们已经了解了是什么，以及 `apply` 和 `also` 函数是如何工作的。在本主题中，我们将介绍另外三个函数： `with` 、 `let` 和 `run` 。它们返回上一个表达式的结果，使代码更易读、更简洁。

## 和

我们先从 `with` 开始——它是三个函数中最简单的。以下是 `with` 函数的主要特点：

- 可通过 `this` 方式获得。
- 它返回 lambda 表达式的结果。
- 它不是一个。

当我们说 \` `with` 不是一个扩展函数时，是什么意思呢？这意味着上下文对象作为参数传递——它被包含在括号中。然而，在 lambda 表达式内部，我们的对象可以作为接收器（ `this` ）使用。

`with` 用于两种情况：

首先，当我们想对上下文对象进行一些操作，但不想获取结果时，可以使用 \`with\`。记住，\` `with` 会返回 lambda 表达式的结果，但根据 Kotlin 代码规范，当我们不需要特定结果时，应该使用这个作用域函数。的确，“\` `with` 中发生的一切，都留在 `with` ”。

```kotlin
val musicians = mutableListOf("Thom York", "Jonny Greenwood", "Colin Greenwood")
with(musicians) {
    println("'with' is called with the argument $this")
    println("List contains $size elements")
} // We print the needed data and don't try to get a certain result
```

此外，当我们想要创建一个辅助对象，其参数或函数可用于计算结果时，我们会使用 `with` 。重要的是，这个新对象是作为辅助对象使用的（我们将在 `run` 中使用真正的对象）。

```kotlin
val musicians = mutableListOf("Thom York", "Jonny Greenwood", "Colin Greenwood")
val firstAndLast = with(musicians) {
    "First list element - ${first()}," +
    " last list element - ${last()}"
}
println(firstAndLast) // We create a new variable firstAndLast and pass the result of calculations inside the function body to it. After that we print this variable.
```

当我们使用 `with` ，它听起来像是：“好的，让我们对某个对象进行一些操作”。请注意， `with` 写在对象本身的左侧——它是唯一具有这种语法的作用域函数。

## 让

以下是 `let` 函数的主要特点：

- 上下文对象可 `it` 使用。
- 它返回 lambda 表达式的结果。

`let` 通常用于以下两种情况：

首先，当我们想使用 `?` 和非空对象时——是的，\` `let` 允许我们这样做。让我们看看：在下面的代码中，我们尝试对一个可空字符串（ `String?` ）执行一些操作。如果我们使用标准方法，编译器会抛出错误。为了避免这种情况，我们可以在调用 `let` 时检查 `str` 是否为空。请记住， `let` 返回的是 lambda 表达式的结果，在本例中是 `it.length` 即最后一个 （lambda 表达式体中的最后一行）的长度。

```kotlin
val str: String? = "Jonny Greenwood"  
//processNonNullString(str)       // compilation error: str can be null

val length = str?.let {
    println("let() is called on $it")       
    processNonNullString(it)      // OK: 'it' is not null inside '?.let { }'
    it.length
}
```

其次，当我们想要使用作用域有限的时，可以使用 `let` 。在这种情况下， `let` 可以提高代码的可读性。请看下面的代码：我们不需要修改 `musicians` 的第一个元素，但我们可以像操作一个名为 `firstItem` 作用域有限的元素一样操作它（大多数情况下，我们使用 `it` 或 \` this ）。

```kotlin
val musicians = listOf("Thom York", "Jonny Greenwood", "Colin Greenwood")
val modifiedFirstItem = musicians.first().let { firstItem ->
    println("The first item of the list is '$firstItem'")
    if (firstItem.length >= 5) firstItem else "!" + firstItem + "!"
}.uppercase()
println("First item after modifications: '$modifiedFirstItem'")
```

你可以说：“嘿，我可以用 `with` 来实现。” 理论上来说，确实可以。但先等等，我们得先弄清楚 `run` 工作原理。

## 跑步

现在，我们来看一下 `run` 函数的特点：

- 上下文对象可通过 `this` 方式获得。
- 它返回 lambda 表达式的结果。

`run` 类似于 `with` ，但它是一个扩展函数。因此， `run` 执行与 `with` 相同的操作，但调用方式类似于 `let` 。

什么时候可以使用 `run` ？主要在以下两种情况下：

首先，当我们想要一个新对象并将 lambda 表达式的结果传递给它时，这一点很重要——我们的新对象是独立且有价值的，这与使用 `with` 函数的情况不同。例如，在下面的代码中，我们创建了一个名为 `result` 新对象，将一个新值传递给 `service` 元素 \` `port` ，并将 `query()` 函数与 \` `prepareRequest()` 函数结合后的结果（以字符串作为参数）传递给 \` `result` 。注意！ `service.port` 的值已更改。

```kotlin
class MultiportService(var url: String, var port: Int) {
    fun prepareRequest(): String = "Default request"
    fun query(request: String): String = "Result for query '$request'"
}

fun main() {
    val service = MultiportService("https://example.kotlinlang.org", 80)

    val result = service.run {
        port = 8080
        query(prepareRequest() + " to port $port")
    }
}
```

其次，当我们想要使用一个没有扩展名的函数并执行一个包含多个运算符的代码块时，我们不需要使用上下文对象，而只需组织一些与变量 `hexNumberRegex` 相关的代码即可。

```kotlin
fun main() {
    val hexNumberRegex = run {
        val digits = "0-9"
        val hexDigits = "A-Fa-f"
        val sign = "+-"

        Regex("[$sign]?[$digits$hexDigits]+")
    }

    for (match in hexNumberRegex.findAll("+1234 -FFFF not-a-number")) {
        println(match.value)
    }
}
```

> [!warning] Warning
> 我们两次惊讶地发现这些函数可以互换使用。没错，它们确实可以互换，我们将在下一节中详细解释这种混淆。但现在，您可以先查看官方 [文档](https://kotlinlang.org/docs/scope-functions.html#distinctions) 。

## 结论

所以，我们已经弄清楚了如何使用三个作用域函数，它们返回 lambda 计算结果。

- `with` 是一个非扩展函数，用于对函数调用进行分组。
- `let` 通常可以帮助我们使用安全调用运算符 `?` 或在局部作用域中引入表达式作为变量。
- `run` 用于配置对象或配置对象并返回特定结果。

现在，是时候练习一下了。

86 名学员喜欢这部分理论， 18 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
