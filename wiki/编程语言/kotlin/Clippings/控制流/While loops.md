## while 循环

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

当某个条件为 `true` ，有多种方法可以重复执行一段代码。在本主题中，我们将学习如何使用两种循环来实现： `while` 和 `do...while` 。它们的区别在于重复执行的顺序和条件判断的方式。

## while 循环

`while` 循环包含一个代码块和一个 **条件判断** ，该条件判断是一个。如果条件为 `true` ，循环就会执行相应的语句。这些语句会一直重复执行，直到条件变为 `false` 。由于该循环会在执行 **前** 检查条件判断，因此它也被称为 **预测试循环** 。请看以下示例：

```kotlin
while (condition) {
    // body: do something repetitive
}
```

循环体可以包含任何类型的语句：声明变量、从标准输入读取数据、条件表达式，甚至嵌套循环。

如果条件始终为 `true` 您还可以编写一个无限循环 ：

```kotlin
while (true) {
    // body: do something indefinitely
}
```

我们稍后会更详细地研究。

现在，请看下面的例子。该程序使用 ，仅当变量小于 `5` 时才打印整数。

```kotlin
fun main() {
    var i = 0

    while (i < 5) {
        println(i)
        i++
    }

    println("Completed")
}
```

让我们解释一下这个循环的工作原理。首先， `i` 被赋值为 `0` 在循环第一次执行之前，程序会检查表达式 `i < 5` 是否为 `true` 。由于 `i` 为 0，循环被激活。循环体包含两条语句：第一条语句显示 `i` 的当前值，第二条语句将其加 `1` 之后，再次计算表达式 `i < 5` 此时 `i` 变为 `1` ，结果也为 `true` ，因此循环重复进行。直到 `i` 变为 `5` `i < 5` 变为 `false` ，循环结束。程序继续执行下一条语句并打印 Completed 。这就是循环的输出：

```
0
1
2
3
4
Completed
```

循环可以用来处理字符、字符串以及任何其他数据类型。下面的程序会在一行中显示英文字母。

```kotlin
fun main() {
    var letter = 'A'
    
    while (letter <= 'Z') {
        print(letter)
        letter++
    }
}
```

程序首先读取字母 `A` ，然后循环执行，直到字母变为 `Z` 程序还会打印当前字符，然后继续处理下一个字符。因此，输出结果为：

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

可以使用递增运算符获取下一个字符（根据 Unicode 表）。

我们的第三个示例包含一个程序，该程序从标准输入读取任意数量的单词，然后将它们打印出来。它使用 `Scanner` 类的 `hasNext` 函数来检查输入是否已有值。

```kotlin
import java.util.*

fun main() {
    val scanner = Scanner(System.\`in\`)
    while (scanner.hasNext()) {
        val next = scanner.next()
        println(next)
    }
}
```

输入：

```
Kotlin is a modern language
```

输出：

```
Kotlin
is
a
modern
language
```

当您不知道输入数据的大小时，对于字符串，请使用 `scanner.hasNext()` 对于整数，请使用 `scanner.hasNextInt()` 请注意，在 IDEA 中，您可以通过按 **Ctrl+D** 来停止控制台中的输入。

## 执行...while 循环

`do...while` 循环首先执行，之后程序会检查一个条件。如果条件为 `true` ，则循环重复执行，直到条件变为 `false` 。由于 `do...while` 循环在执行后检查条件，因此它也被称为 **后测循环** 。与 `while` 循环在执行前检查条件不同， `do..while` while 循环是一个退出条件循环。因此，循环体至少会被执行一次。

这个循环包含三个部分： `do` 关键字、循环体和 `while(condition)` ：

```kotlin
do {
    // body: do something
} while (condition)
```

以下程序从标准输入读取一个整数并显示该数字。如果用户输入 `0` ，程序将打印 0 然后停止。以下示例展示了循环的工作原理：

```kotlin
fun main() {
    do {
        val n = readln().toInt()
        println(n)
    } while (n > 0)
}
```

> [!primary] Primary
> 你可以在循环体中设置一个变量，然后在条件中使用它。

输入：

```
1
2
4
0
```

输出：

```
1
2
4
0
```

就像 `while` 循环一样， `do...while` 循环也可以是无限的。

## 结论

本主题介绍了两种基本但非常实用的循环： `while` 和 `do...while` 。它们都包含循环体和条件判断，唯一的区别在于执行顺序。while `while` 在执行循环体之前检查条件判断，而 `do...while` 循环在第一次执行循环体之后检查条件判断。

实际上，程序员使用 `do..while` 循环的频率远不如 `while` 循环。一个使用 while 循环的典型例子是：一个程序会从标准输入读取数据，直到用户输入某个特定的数字或字符串。现在你已经了解了这些循环的基础知识。让我们来练习一下！

938 名学习者喜欢这篇理论文章， 7 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
