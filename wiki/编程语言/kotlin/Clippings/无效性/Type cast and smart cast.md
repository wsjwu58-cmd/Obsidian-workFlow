## 类型选角和智能选角

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

和类型转换在任何编程语言中都至关重要。类型检查允许开发者验证对象是否属于特定数据类型，而允许程序员将对象从一种类型转换为另一种类型。Kotlin 作为一种静态类型语言，其诸多特性使得类型检查和类型转换的使用既简便又安全。

## is 和!is 运算符

Kotlin 中的 \` `is` 和 `!is` 运算符用于类型检查。它们允许开发者检查对象是否属于特定的数据类型。\`is\` `is` 符在对象属于指定类型时返回 \`true\`，否则返回 \`false\`。相反，\` `!is` 运算符在对象不属于指定类型时返回 \`true\`，否则返回 \`false\`。

例如：

```kotlin
val obj: Any = "Hello, Kotlin"
if (obj is String) {
   println(obj.uppercase())
} else {
   println("obj is not a String")
}
```

在上面的代码中，我们使用 \` `is` 运算符来检查 `obj` 变量是否为 `String` 。如果它是 `String` ，则将其转换为大写并打印出来。否则，打印一条消息，说明 `obj` 不是 `String` 。这是一个 \` `is` 运算符的一个很好的例子，但我们也要记住 Kotlin 中的惯用法，这是这门编程语言的优势之一。Kotlin 中常用的惯用法之一是：

```kotlin
when (x) {
    is Foo -> ...
    is Bar -> ...
    else   -> ...
}
```

举个例子来说明我们如何运用它：

```kotlin
fun processInput(input: Any) {
    when (input) {
        is Int -> println("Input is an integer")
        is String -> println("Input is a string")
        is Double -> println("Input is a double")
        else -> println("Unknown input")
    }
}
```

在这个例子中， `processInput` 函数接受一个 `Any` 类型的参数，这意味着它可以接受任何类型的对象。在函数内部，我们使用 `when` 和 \` `is` 来检查输入对象的类型。根据输入对象的类型，我们会打印一条消息，指示其类型。如果输入对象不是预期类型之一，则打印“未知输入”消息。

## 智能投屏

Kotlin 还有一个名为特性。智能类型转换用于简化处理可空类型的代码。当使用 `is` 运算符检查可空类型时，Kotlin 会自动将该对象转换。

例如：

```kotlin
fun printLength(obj: Any) {
   if (obj is String) {
      println(obj.length)
   }
}
```

在上面的代码中，我们使用 \` `is` 运算符检查 \` `obj` 变量是否为 `String` 。如果是 `String` ，则打印其长度。由于 Kotlin 会自动将 `obj` 变量强制转换为非空类型，因此我们不需要使用任何类型转换运算符。

## “不安全”的演员

Kotlin 有一个不安全的类型转换运算符，用 `as` 表示。\`as\` `as` 用于将对象强制转换为非空类型。如果对象无法转换为指定的类型， `as` 运算符会抛出 \`ClassCastException\` 异常。

例如：

```kotlin
val obj: Any = "Hello, Kotlin"
val str: String = obj as String // Unsafe cast operator
println(str.uppercase())
```

在上面的代码中，我们使用 `as` 运算符将 `obj` 变量强制转换为 `String` 。如果 `obj` 不是 `String` ， `as` 运算符会抛出 ClassCastException 异常。

## “安全”（可为空）类型转换运算符

Kotlin 还提供了一个安全类型转换运算符，用 `as?` 关键字表示。\`as `as?` 运算符用于将对象强制转换为可空类型。如果对象无法转换为指定的类型，\` `as?` \` 运算符将返回 `null` 。

例如：

```kotlin
fun main() {
    val obj: Any = 123
    val str: String? = obj as? String // Safe (nullable) cast operator
    if (str != null) {
        println(str.uppercase())
    }
}
```

在上面的代码中，我们使用 `as?` 运算符将 `obj` 变量强制转换为 `String` 。由于 `obj` 不是 `String` ， `as?` 运算符返回 `null` 。因此， `println` 不会打印任何内容。

## 结论

总之，类型转换和智能转换是 Kotlin 中的重要特性，它们允许检查对象并将其转换为不同的类型。当处理不同类型的对象以及执行需要特定类型的操作时，它们非常有用。现在让我们通过练习来更好地记住这个主题。

119 名学员喜欢这篇理论文章， 7 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
