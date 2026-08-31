提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

Kotlin 提供了一个特殊的 `when` 表达式，可以根据变量的值执行不同的操作。当有多个选项需要选择时，这是一种非常便捷的方法。此表达式可以替代 `if` ，并使您的代码更易读。

## 替代方案

例如，下面的程序对两个整数进行加法、减法和乘法运算。它根据 `when` 来决定执行哪种运算：

```kotlin
fun main(){
    val (var1, op, var2) = readln().split(" ")

    val a = var1.toInt()
    val b = var2.toInt()

    when (op) {
        "+" -> println(a + b)
        "-" -> println(a - b)
        "*" -> println(a * b)
        else -> println("Unknown operator")
    }
}
```

让我们仔细看看。这里， `when` `op` ，并逐个将其与所有值进行匹配，直到找到合适的值为止。它有三个常规分支——\` `"+"` 、 `"-"` 和 `"*"` ，以及一个 `else` 分支。如果没有值与运算符匹配，则会执行 \` `else` 分支。您可以跳过 `else` 分支，它是可选的。如果您使用 `if` 编写相同的代码，则可读性会降低。

如果需要处理多个情况，您可以将它们合并并用逗号分隔。您可以在一个分支中合并任意数量的值。您还可以添加尾随逗号。如果您需要添加很长的情况列表，这将非常有用。以下是之前程序的修改后代码片段：

```kotlin
when (op) {
    "+", "plus" -> println(a + b)
    "-", "minus", -> println(a - b) // trailing comma
    "*", "times" -> println(a * b)
    else -> println("Unknown operator")
}
```

这段代码既适用于 `5 + 8` 输入，也适用于 `5 plus 8` 。

您还可以使用包含多条语句的复杂代码块作为分支：

```kotlin
when (op) {
    "+", "plus" -> {
        val sum = a + b
        println(sum)
    }
    "-", "minus" -> {
        val diff = a - b
        println(diff)
    }
    "*", "times" -> {
        val product = a * b
        println(product)
    }
    else -> println("Unknown operator")
}
```

如您所见， `when` 表达式有多种用法。尽量选择最易读的用法。

## 当作为一种表达方式

`When` 可以返回结果。在这种情况下，每个分支都应该返回一些内容，并且 **需要** 一个 else 分支。在下面的代码示例中，每个分支都返回相应操作的结果。

```kotlin
val result = when (op) {
    "+" -> a + b
    "-" -> a - b
    "*" -> a * b
    else -> "Unknown operator"
}
println(result)
```

您无需声明额外的变量，可以直接将结果传递给函数。请看下面的示例：

```kotlin
println(when(op) {
    "+" -> a + b
    // ...
    else -> "Unknown operator"
})
```

如果您不需要在其他地方使用结果，或者您希望代码简洁，请使用这种表示法。

如果一个分支包含一个用 `{...}` 括起来的多条语句块，则最后一行必须是单个值或一个复杂表达式，该表达式将被执行并作为 `when` 表达式的结果返回。请查看上面示例中修改后的分支：

```kotlin
"+" -> {
    val sum = a + b
    sum
}
```

在分支中使用不带 `{...}` 简短形式，可以使你的代码更容易理解。

## 分支条件和范围

如果您使用过其他编程语言，例如 Java 或 C#，您可能会注意到 `when` 与 `switch` 语句类似。\`when\` `When` 提供了更复杂的检查，而不仅仅是直接匹配值。

以下程序读取三个整数 `a` 、 `b` 和 `c` ，然后尝试利用 `a` 和 `b` 计算 `c` 。如果计算 `c` 方法有很多种，它只会打印出第一种：

```kotlin
fun main(){
    val (var1, var2, var3) = readln().split(" ")

    val a = var1.toInt()
    val b = var2.toInt()
    val c = var3.toInt()

    println(when (c) {
        a + b -> "$c equals $a plus $b"
        a - b -> "$c equals $a minus $b"
        a * b -> "$c equals $a times $b"
        else -> "We do not know how to calculate $c"
    })
}
```

如果输入值为 `5 3 2` 则程序输出 `2 equals 5 minus 3` 如果输入值为 `0 0 0` ，则输出 `0 equals 0 plus 0` 。

另一个有趣的用法是检查某个值是否属于某个范围。请看：

```kotlin
when (n) {
    0 -> println("n is zero")
    in 1..10 -> println("n is between 1 and 10 (inclusive)")
    in 25..30 -> println("n is between 25 and 30 (inclusive)")
    else -> println("n is outside a range")
}
```

如果整型变量 `n` 为 `0` ，程序执行第一个分支。如果 `n` 属于 1 到 10 的范围（包含 1 和 10），则执行第二个分支。如果 `n` 属于 25 到 30 的范围（包含 25 和 30 的边界），则执行第三个分支。如果 `n` 不等于 `0` 且不属于上述任何范围，则执行 `else` 分支。

您也可以像合并单个值一样，用逗号分隔多个范围。格式如下：

```kotlin
in a..b, in c..d -> println("n belongs to a range")
```

## 没有论据

你可以使用不带参数的 `when` 表达式。在这种情况下，每个分支条件都是一个简单的布尔表达式，当条件为 `true` 时，该分支就会执行。如果多个条件都为 `true` ，则只会执行第一个条件。

下面这个程序展示了它的工作原理：

```kotlin
fun main(){
    val n = readln().toInt()
    
    when {
        n == 0 -> println("n is zero")
        n in 100..200 -> println("n is between 100 and 200")
        n > 300 -> println("n is greater than 300")
        n < 0 -> println("n is negative")
        // else-branch is optional here
    }
}
```

每个分支条件都是一个，其中可以包含任何产生布尔值的操作。

## 结论

在本主题中，我们介绍了 `when` 语句的几种用法。它支持复杂的值匹配，有助于简化代码，使其更易于理解。在练习中，尝试使用 `when` 的不同形式。不要害怕尝试。记住： `when` 是一种功能强大的结构设计，具有多种可能性。

1043 名学习者喜欢这篇理论文章， 6 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
