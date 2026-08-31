提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

很多时候，你需要重复执行某些操作。例如，如果你想计算 1 到 100 之间所有数字的总和（不使用公式），你需要依次将这些数字相加。为此，你可以使用 `for` 循环和范围，这些你都已经很熟悉了。让我们仔细看看！

## for 循环

Kotlin 提供了 `for` 循环来遍历范围、数组和其他元素集合。我们稍后会详细介绍它们。

这是 `for` 循环的语法：

```kotlin
for (element in source) {
    // body of loop
}
```

此循环 **体** 由一个或多个语句组成，这些语句针对指定 *源* 中的每个 *元素* 执行。循环在处理完最后一个元素后停止。

## 遍历范围

使用 `for` 循环的最简单例子是打印整数范围内的每个元素。

```kotlin
for (i in 1..4) {
    println(i)    
}
```

这个循环会打印出从 1 到 4 的每个数字。

```
1
2
3
4
```

也可以遍历一系列字符：

```kotlin
for (ch in 'a'..'c') {
    println(ch)
}
```

此循环输出：

```
a
b
c
```

请注意，我们不能使用类似 `"da".."dd"` 这样的字符串范围来获得所需的结果 `"da" "db" "dc" "dd"` 。在这个范围内，我们只能使用单个字符。从现在开始，所有示例都将涉及数字，因为遍历字符的操作始终相同。

## 遍历字符串

此外，您还可以遍历字符串。以下代码会打印 `String` 中的每个符号：

```kotlin
val str = "Hello!"
for (ch in str) {
    println(ch)    
}
```

这段代码会输出：

```
H
e
l
l
o
!
```

## 按逆序迭代

你也可以按相反的顺序遍历一个范围。

```kotlin
for (i in 4 downTo 1) {
    println(i)
}
```

此循环打印从 4 到 1 的数字。

```kotlin
4
3
2
1
```

> [!warning] Warning
> **请注意** ，要按相反顺序迭代范围，需要使用 `in 4 downTo 1` ，而不是 `in 4..1` 。

## 不包括上限

如果需要从某个范围中排除上限，我们可以从该范围中减去 1，或者用 `until` 代替 `..` ：

```kotlin
for (i in 1 until 4) {
    println(i)
}
```

这个循环会打印出从 1 到 3 的数字。

## 指定步骤

如果我们不指定步长，则默认步长为 1（例如 `1, 2, 3, ...` ）。但是，如果我们想要更改步长，则需要显式指定。

在下面的示例中，我们只打印 `1..7` 范围内的奇数。

```kotlin
for (i in 1..7 step 2) {
    println(i)
}
```

这个循环会打印出四个数字：

```kotlin
1
3
5
7
```

你也可以用它来进行反向迭代。

```kotlin
for (i in 7 downTo 1 step 2) {
    println(i)
}
```

此循环输出：

```kotlin
7
5
3
1
```

## 例如：一个数的阶乘

让我们编写一个程序来计算给定整数的阶乘。这是一个经典问题。n 的阶乘是 1 到 **n** （包含 1 和 n **）** 所有整数的乘积。假设 0 的阶乘是 1，那么 1 的阶乘也是 1。

```kotlin
fun main() {
    val n = readln().toInt()
    var result = 1 // starting value of the factorial

    for (i in 2..n) { // the product from 2 to n
        result *= i
    }

    println(result)
}
```

上面的程序从标准输入读取一个整数。我们假设阶乘的初始值为 1，然后依次将其乘以 2 到 **n 的** 数字。如果输入数字为 1，则结果为 1。如果输入数字为 5，则结果为 120。

## 例如：偶数乘法表

你可以将一个 `for` 循环嵌套在另一个 `for` 循环体中，因为循环本质上就是普通语句。程序员经常使用来处理多维结构，例如表格（矩阵）、数据立方体等等。

例如，下面的代码打印出 2 到 10 的偶数的乘法表。

```kotlin
fun main() {
    for (i in 2..10 step 2) {
        for (j in 2..10 step 2) {
            print(i * j)
            print('\t')  // print the product of i and j followed by one tab
        }
        println()
    }
}
```

它打印出：

```java
4   8   12  16  20  
8   16  24  32  40  
12  24  36  48  60  
16  32  48  64  80  
20  40  60  80  100
```

## 成语

本主题中的几乎所有内容都是 [惯用语](https://kotlinlang.org/docs/idioms.html#iterate-over-a-range) ！不同类型的范围可能难以理解，但它们提供了一种非常方便且易于阅读的代码编写方式。这里我们快速回顾一下遍历基本范围的语法：

```kotlin
for (i in 1..6) { ... }        // closed range: 1, 2, 3, 4, 5, 6
for (i in 1 until 6) { ... }   // half-open range: 1, 2, 3, 4, 5
for (x in 1..6 step 2) { ... } // step 2: 1, 3, 5
for (x in 6 downTo 1) { ... }  // closed range, backward order: 6, 5, 4, 3, 2, 1
```

## 结论

是一个非常强大的工具。你几乎会在所有程序中用到它。记住，你可以使用各种不同的范围；在某些特殊情况下，它们会非常方便。祝你任务顺利！

1107 名学习者喜欢这篇理论文章， 13 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
