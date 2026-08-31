## Lambda 表达式

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

我们已经知道如何声明具有固定名称的函数。现在，让我们来了解最后一个核心特性：在运行时创建无需预定义名称的函数。这就是 lambda！Lambda 是最重要的特性之一，在现代编程中被广泛使用。

## 没有名称的函数

要创建一个不与其名称绑定的 Kotlin 函数，可以使用 **匿名** 函数或 ：

- `fun(arguments): ReturnType { body }` – 这通常被称为“匿名函数”。
- `{ arguments -> body }` – 这通常被称为“lambda 表达式”。

为了更好地理解，请看下面的例子。这里声明了两个函数：它们的声明方式不同，但功能相同：

```kotlin
fun(a: Int, b: Int): Int {
    return a * b
} // normal function but no name 

{ a: Int, b: Int -> a * b } // we shifted the parameter or argument in the curly braces
```

如你所见，它们计算的是两个数的乘积。

这两个函数都具有合理的类型： `(Int, Int) -> Int` 。因此，这里的类型与前面主题中讨论的顶级函数的类型工作方式相同。

请注意，如果要声明一个 **不带参数的 lambda** 表达式，则不需要编写“箭头符号”。不带参数的 lambda 表达式定义如下： `{ body }` 。

你可能会问：如何使用一个没有已知名称的函数？答案是：有几种方法。

例如，您可以将函数赋值给一个变量，然后通过调用该变量来调用它：

```kotlin
val mul1 = fun(a: Int, b: Int): Int {
    return a * b
}

val mul2 = { a: Int, b: Int -> a * b }

println(mul1(2, 3))  // prints "6"
println(mul2(2, 3))  // prints "6" too
```

此外，您还可以将此类函数作为参数传递，或者从另一个函数返回此类函数。

最后，你可以在函数定义后紧跟括号并附上所需的参数，从而直接调用该函数。然而，这样做意义不大。因此，大多数情况下，人们会使用前面提到的三种方法。

创建这两个函数的过程非常相似，但 lambda 表达式的语法更简洁方便。因此，在实际应用中，lambda 表达式几乎总是用于在运行时创建函数。此外，有些程序员并不遵循 Kotlin 官方的命名规则，他们会使用“”而不是“lambda 表达式”。尽管大家都能理解，但我们建议您使用规范的命名规则。

出于同样的方便考虑，现在我们只讨论 lambda 函数。

## Lambda 表达式和语法糖

有一些方法可以在不改变代码逻辑的情况下，使代码更易于人类阅读。如果编程语言中存在这样的方法，并且它与相关，我们就称之为。Kotlin 提倡函数式编程，因此它也有相应的语法糖。

让我们回顾一下将函数作为参数传递的例子：

```kotlin
fun isNotDot(c: Char): Boolean = c != '.'
val originalText = "I don't know... what to say..."
val textWithoutDots = originalText.filter(::isNotDot) 
println(textWithoutDots) // I don't know what to say
```

简而言之，我们创建了 `isNotDot` 函数，它返回 `Boolean` ，然后使用 `originalText.filter` 函数遍历字符串中的每个字符，应用 `isNotDot` 函数，最后返回一个不包含任何点号的字符串。该过滤器会排除字符串中任何返回值为 false 的字符。

以防万一，这里有一个专门用于 [筛选集合中元素的](https://hyperskill.org/learn/step/22367) 主题。

现在，让我们重写它以传递一个 lambda 表达式：

```kotlin
val originalText = "I don't know... what to say..."
val textWithoutDots = originalText.filter({ c: Char -> c != '.' })
println(textWithoutDots) // I don't know what to say
```

成功了！首先，我们不需要先指定一个函数，然后再引用它。

Kotlin 可以推断许多对象的类型，因此这里无需指定 `c` 类型：

```kotlin
originalText.filter({ c -> c != '.' })
```

其次，有时 lambda 表达式会作为最后一个参数传递。在这种情况下，Kotlin 提供了一种方法来消除括号序列 ({ })，并将 lambda 表达式写在括号之外：

```kotlin
originalText.filter() { c -> c != '.' }
```

如果执行该操作后括号为空，则可以将其删除：

```kotlin
originalText.filter { c -> c != '.' }
```

请注意，有时函数引用比 lambda 表达式更易读，两者之间并没有绝对的优劣之分。但是，如果代码非常复杂，与其复制粘贴 lambda 表达式，不如使用函数引用，这样更便于维护和重用。

## 单个参数的隐式名称：它

最后，当 lambda 表达式只有一个参数时，可以省略该参数。该参数以 `it` 为名。\`it\` `it` 类型由传递给 lambda 表达式的参数类型推断得出。最终移除点号的代码版本如下：

```kotlin
val originalText = "I don't know... what to say..."
val textWithoutDots = originalText.filter { it != '.' }
```

相当厉害吧？

在 Kotlin 中，从 lambda 表达式返回值是通过 `return@label` 实现的，其中 `label` 是一个标签，通常与调用 lambda 表达式的上下文中的的名称相匹配。例如，当在高阶函数中使用 `someLambda` 作为 lambda 表达式时，lambda 表达式的返回值将类似于 `return@someLambda` 。

这在诸如 `forEach` 、 `map` 、 `let` 等函数中使用 lambda 表达式时尤其有用。使用 `return@label` 返回可以在不中断外部函数执行的情况下退出 lambda 表达式。

以下是 Kotlin 中使用 `return@label` 的示例：

```kotlin
listOf(1, 2, 3, 4).forEach { 
    if (it == 3) return@forEach  // Skipping number 3
    println(it)
}
println("End")
```

在这个例子中，当 `it` 等于 3 时，lambda 表达式会被中断，并继续执行 `forEach` 循环的下一次迭代。循环结束后， `println("End")` 将会执行。

## 结论

Lambda 表达式是 Kotlin 和中最重要、最强大的特性之一。在本主题中，我们学习了匿名函数和 Lambda 表达式的概念。Lambda 表达式帮助我们在运行时创建函数。这在调用 Kotlin中的函数（例如，处理数据的函数）时非常方便，因为它有助于减少代码长度。最后，我们希望已经让您相信，函数在 Kotlin 语言中是。

145 名学员喜欢这篇理论文章， 9 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
