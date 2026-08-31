## for 循环和列表

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在 Kotlin 中， `for` 循环是一个方便的工具，它允许你遍历整个。让我们来看看它的几种用法。

## 遍历 MutableList

处理每个可变列表元素的最简单方法是使用以下模板：

```kotlin
for (element in mutList) {
    // body of loop
}
```

假设我们有一个包含星期几的可变列表。让我们打印出一周中的每一天：

```kotlin
fun main() {
    val daysOfWeek = mutableListOf("Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat")
    
    for (day in daysOfWeek){
        println(day)
    }
}
```

之后，程序将输出以下内容：

```
Sun
Mon
Tues
Wed
Thur
Fri
Sat
```

同样，你可以处理可变的整数、字符或任何其他数据类型的列表。

## 按索引迭代

可以直接在循环中通过索引访问元素。为此，必须使用 `mutList.indices` 属性，该属性表示 `mutList` 有效索引范围。

请查看 `daysOfWeek` 可变列表：

```kotlin
fun main() {
    val daysOfWeek = mutableListOf("Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat")

    for (index in daysOfWeek.indices){
        println("$index: ${daysOfWeek[index]}")
    }
}
```

程序将输出以下内容：

```
0: Sun
1: Mon
2: Tues
3: Wed
4: Thur
5: Fri
6: Sat
```

## 按范围索引迭代

我们讨论了遍历可变列表的两种方法。当需要处理列表中的每个元素时，这两种方法非常有用。然而，有时您可能需要访问特定的子列表。在这种情况下，您可以指定所需的索引范围。

可变列表的第一个元素的索引始终为 0。

请查看以下程序：

```kotlin
fun main() {
    val daysOfWeek = mutableListOf("Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat")

    for (index in 1..5) {
        println("$index: ${daysOfWeek[index]}")
    }
}
```

它只会打印工作日：

```
1: Mon
2: Tues
3: Wed
4: Thur
5: Fri
```

要在范围中使用可变列表的最后一个索引，需要访问 `mutList.lastIndex` 。因此，我们可以这样修改代码：

```kotlin
for (index in 1 until daysOfWeek.lastIndex) {
    println("$index: ${daysOfWeek[index]}")
}
```

显示的日期与之前相同：

```
1: Mon
2: Tues
3: Wed
4: Thur
5: Fri
```

如果要按遍历可变列表，请使用范围参数中的 `downTo` 。还可以使用 `step` 指定索引之间的偏移量。

以下程序将以 2 为步长，反向打印日期：

```kotlin
fun main() {
    val daysOfWeek = mutableListOf("Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat")

    for (index in daysOfWeek.lastIndex downTo 0 step 2) {
        println("$index: ${daysOfWeek[index]}")
    }
}
```

输出：

```
6: Sat
4: Thur
2: Tues
0: Sun
```

因此，您可以按正序或逆序遍历整个可变列表或其一部分，并根据需要执行任意步骤。

## 读取 MutableList 元素

有些任务需要你从输入中读取可变列表元素。

例如，下面的程序读取整数并按相反的顺序打印它们。

```kotlin
fun main() {
    val size = readln().toInt()
    val mutList: MutableList<Int> = mutableListOf()
    for (i in 0 until size) {
        mutList.add(readln().toInt())
    }

    for (i in mutList.lastIndex downTo 0) {
        print("${mutList[i]} ")
    }
}
```

以下是输入内容：

```
5
1
2
3
4
5
```

程序将输出以下内容：

```
5 4 3 2 1
```

您可以将此程序用作模板来开发您自己的解决方案。

## 结论

在本主题中，我们讨论了在 Kotlin 中使用 `for` 循环遍历可变列表的几种方法：遍历列表中的每个元素、按元素索引遍历以及按范围索引遍历。由此可见，Kotlin 赋予了你很大的自由度。有些应用场景需要从输入中读取可变列表元素。现在你也知道如何操作了。准备好练习了吗？

631 名学习者喜欢这篇理论文章， 12 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
