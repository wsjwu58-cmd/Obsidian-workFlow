提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在本主题中，我们将探索 Kotlin 的，重点介绍 `if` 表达式的各种形式及其作为表达式风格结构的用法。

## 条件表达式

条件表达式允许程序根据的值执行不同的计算。条件表达式有多种形式，例如 **单个 if** 语句、 **if-else** 语句、 **if-else-if** 语句和嵌套 **if** 语句。

## 表达式风格的“if”

与其他一些编程语言不同，Kotlin 的 `if` 语句是一个表达式，而不是一个。这意味着它可以返回一个计算结果。结果必须是表达式体中的最后一个表达式。例如：

```kotlin
val max = if (a > b) {
    println("Choose a")
    a
} else {
    println("Choose b")
    b
}
```

在上面的例子中，变量 `max` 被赋值为语句体中最后一个表达式的值。需要注意的是，如果使用表达式风格的 `if` ，则必须包含一个 `else` 分支。

如果所有语句体都只包含一条语句，则可以省略大括号：

```kotlin
val max = if (a > b) a else b
```

有些情况下，你不需要声明新的变量来存储结果。例如，考虑以下示例：

```kotlin
fun main() {
    val a = readln().toInt()
    val b = readln().toInt()

    println(if (a == b) {
        "a equal b"
    } else if (a > b) {
        "a is greater than b"
    } else {
        "a is less than b"
    })
}
```

在上面的例子中， `if` 表达式直接传递给 `println()` 函数，而没有声明变量， `println()` 函数会打印结果。

## 成语

`if` 需要获取结果，建议使用表达式风格，因为它有助于避免因可变变量或遗忘更改而导致的潜在问题。例如：

```kotlin
val max = if (a > b) a else b // one line
```

总而言之，Kotlin 的 `if` 表达式提供了一种强大而灵活的方式来处理代码的条件执行。通过使用表达式风格的 `if` 语句，您可以利用其返回值的功能并简化代码。如果您了解 Java，可以将其映射到三元运算符：

```java
final String msg = num > 10 
  ? "Number is greater than 10" 
  : "Number is less than or equal to 10";
```

## 使用“when”作为比“if-else-if”链更强大的替代方案

Kotlin 提供了一种比 **if-else-if** 链更强大、更具表现力的替代方案，称为 `when` 表达式。when `when` 简化了处理多个条件的过程，并使代码更易读。

以下是如何使用 `when` 的示例：

```kotlin
val number = 5

when (number) {
    1 -> println("One")
    2 -> println("Two")
    3 -> println("Three")
    4 -> println("Four")
    else -> println("Number is greater than four")
}
```

在这个例子中， `when` 表达式会检查 `number` 变量的值是否符合不同的条件。如果该值符合某个条件，则会执行相应的代码块。

## 使用“when”作为表达式

与 `if` 表达式类似， `when` 也可以用作返回值的表达式。when `when` 返回的值是匹配分支中最后一个表达式的结果。

```kotlin
val number = 3
val message = when (number) {
    1 -> "One"
    2 -> "Two"
    3 -> "Three"
    4 -> "Four"
    else -> "Number is greater than four"
}

println(message) // Output: Three
```

## 在范围和条件中使用“when”

`when` 还可以与范围和更复杂的条件一起使用。例如：

```kotlin
val number = 15

when {
    number < 0 -> println("Negative number")
    number in 1..10 -> println("Number between 1 and 10")
    number % 2 == 0 -> println("Even number")
    else -> println("Odd number greater than 10")
}
```

在这个例子中， `when` 表达式会根据不同的条件（包括范围和自定义条件）检查 `number` 的值。

## 结论

总之，Kotlin 提供了诸如 `if` 和 `when` 表达式之类的强大结构来处理代码的条件执行。这些表达式可以返回值，从而使代码更加简洁和富有表现力。有效利用这些结构将有助于您编写更易读、更易维护的 Kotlin 代码。

1412 名学习者喜欢这篇理论文章， 23 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
