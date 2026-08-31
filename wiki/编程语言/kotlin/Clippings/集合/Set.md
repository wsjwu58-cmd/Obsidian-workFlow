提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经对集合及其不同类型（集合、列表、映射）和变体（可变、不可变）有了基本的了解。在本主题中，我们将更深入地了解一种特定类型：集合。

## 介绍

`Set` 是一个 **无序的** 元素集合，其中不允许有重复元素。它是一个 **不可变的** 集合，这意味着集合初始化后，其大小和单个元素都不能更改。

假设我们想在一天工作结束时记录咖啡馆顾客的信息。让我们尝试借助 `MutableList` 来实现：

```kotlin
val visitors = mutableListOf<String>("Vlad", "Vanya", "Liza")
println(visitors) // output: [Vlad, Vanya, Liza]
```

`MutableList` 真的是完成这项任务的最佳选择吗？首先，任何人都可以更改它的内容：

```kotlin
visitors[2] = "Nina"
println(visitors) // output: [Vlad, Vanya, Nina]
```

其次，你可能会不小心犯错，把同一个访客记录两次：

```kotlin
val visitors = mutableListOf<String>("Vlad", "Vanya", "Liza", "Vanya")
println(visitors) // output: [Vlad, Vanya, Liza, Vanya]
```

Set 可以帮助我们解决这个问题，因为 `Set` 是 **不可变的** ，它不允许重复元素：

```kotlin
val visitors = setOf<String>("Vlad", "Vanya", "Liza", "Liza")
println(visitors) // output: [Vlad, Vanya, Liza]
```

我们尝试创建一个包含两个相同元素的 `Set` ，但由于 `Set` 不支持重复元素，最终得到的集合只包含唯一元素，这正是我们需要的！当然， `Set` 是 **不可变的** ，所以没有人能够篡改它的内容。

## 初始化

`Set` 是一种。正如你从前面的例子中看到的，你可以使用 `setOf<E>` 来初始化它，其中 `E` 是集合中包含的元素的类型：

```kotlin
val languages = setOf<String>("English", "Russian", "Italian")
```

类型也可以从上下文中推导出来：

```kotlin
val languages = setOf("English", "Russian", "Italian")
```

如果需要一个空集，可以使用 `emptySet` 方法：

```kotlin
val numbers = emptySet<Int>()
println(numbers) // output: []
```

创建集合的另一种方法是调用构建器函数 `buildSet()` ：

```kotlin
val letters = setOf<Char>('b', 'c')

val set = buildSet<Char> {
    add('a')
    addAll(letters)
    add('d')
}
println(set) // output: [a, b, c, d]
```

## 方法和属性

让我们看看你已经知道的方法在 `Set` 中是如何工作的。

首先，我们来看看如何使用 `isEmpty` 和 `size` ：

```kotlin
val visitors = setOf("Andrew", "Mike")

println("How many people visited our cafe today? ${visitors.size}") // 2
println("Was our cafe empty today? It's ${visitors.isEmpty()}") // Was our cafe empty today? It's false
```

`indexOf(element)` 并 `contains` 按以下方式工作：

```kotlin
val visitors = setOf("Paula", "Tanya", "Julia")

println("Is it true that Tanya came? It's ${visitors.contains("Tanya")}") // Is it true that Tanya came? It's true
println("And what is her index? ${visitors.indexOf("Tanya")}" ) // And her index is 1
```

如果你想知道当天第一位或最后一位顾客是谁，也就是哪个元素位于第一个/最后一个位置，可以使用 `first()` 和 `last()` 方法。但由于集合是无序的，这些方法用处不大。

```kotlin
val students = setOf("Bob", "Larry")
println(students.first()) // Bob
println(students.last()) // Larry
```

使用 `joinToString()` 将 `Set` 转换为字符串，例如：

```kotlin
val visitors = setOf("Paula", "Tanya", "Julia")

val joinToString = visitors.joinToString()

println(joinToString) // Paula, Tanya, Julia
```

如果要检查特定集合中的所有元素是否都包含在 `Set` 中，请使用 `containsAll(elements)` 方法：

```kotlin
val studentsOfAGroup = setOf("Bob", "Larry", "Vlad")
val studentsInClass = setOf("Vlad")

println("Are all the students in the group in class today? It's ${studentsInClass.containsAll(studentsOfAGroup)}") 
// Are all the students in the group in class today? It's false
```

如果要将两个集合相加，只需使用“+”运算符；如果要将一个集合从另一个集合中减去，则使用“-”运算符。请注意，相加或相减后，您将得到一个新的集合：

```kotlin
val productsList1 = setOf("Banana", "Lime", "Strawberry")
val productsList2 = setOf("Strawberry")

val finalProductsList1 = productsList1 + productsList2
println(finalProductsList1) // [Banana, Lime, Strawberry]

val finalProductsList2 = productsList1 - productsList2
println(finalProductsList2) // [Banana, Lime]
```

想把一个 `MutableList` 转换成 `Set` ？没问题，使用 `toSet()` 方法即可：

```kotlin
val groceries = mutableListOf("Pen", "Pineapple", "Apple", "Super Pen", "Apple", "Pen")
println(groceries.toSet()) // [Pen, Pineapple, Apple, Super Pen]
```

## 遍历元素

你可以借助 `for` 循环遍历 `Set` 中的元素。我们来看一个例子：

```kotlin
val visitors = setOf("Vlad", "Liza", "Vanya", "Nina")

for (visitor in visitors) {
    println("Hello $visitor!")
}

// output:
// Hello Vlad!
// Hello Liza!
// Hello Vanya!
// Hello Nina!
```

## 结论

现在您了解了 `Set` 是什么以及它与 `MutableList` 的区别。当您不希望内容被更改，并且只想保留唯一元素时，请使用 `Set` 。您已经知道如何初始化一个 Set，检查它是否为空，检查它是否包含某个元素，查找元素的索引，将 Set 转换为字符串，以及使用 `for` 循环遍历 `Set` 。

准备好测试一下自己了吗？让我们开始练习题吧！

211 名学员喜欢这篇理论文章， 6 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
