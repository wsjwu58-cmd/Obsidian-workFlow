提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经对集合、它们的不同类型（集合、列表、映射）以及变体（可变、不可变）有了基本的了解。在本主题中，我们将更深入地了解一种特定类型。 `List` 。

## 介绍

`List` 是一种 **不可变** 集合。初始化后，其大小无法更改。这种类型允许元素重复，并按特定顺序存储元素。

假设我们要保存去年驾驶过的车辆信息。让我们借助 `List` 来实现：

```kotlin
val cars = listOf<String>("BMW", "Honda", "Mercedes")
println(cars) // output: [BMW, Honda, Mercedes]
```

理论上，我们可以使用 `MutableList` 来保存这类信息：

```kotlin
val cars = mutableListOf<String>("BMW", "Honda", "Mercedes")
println(cars) // output: [BMW, Honda, Mercedes]
```

然而，这样做并不好，因为任何人都可以随时更改 `MutableList` 的内容：

```kotlin
cars[0] = "Renault"
println(cars) // output: [Renault, Honda, Mercedes]
```

如果你希望列表内容保持不变，这可能会是个问题。 `List` 是 **不可变的** ，所以我们的内容不会被改变。如果你尝试修改列表中的内容，你会收到一个错误：

```kotlin
val cars = listOf<String>("BMW", "Honda", "Mercedes")
cars[0] = "Renault" // Error
```

## 初始化

`List` 是一种 **泛型** 类型。正如你从前面的例子中看到的，你可以使用 `listOf<E>` 来初始化它，其中 `E` 是列表中包含的元素的类型：

```kotlin
val textUsMethod = listOf<String>("SMS", "Email")
```

类型也可以从上下文中推导出来：

```kotlin
val textUsMethod = listOf("SMS", "Email")
```

如果需要一个空列表，可以使用 `emptyList` 方法：

```kotlin
val staff = emptyList<String>()
println(staff) // output: []
```

创建列表的另一种方法是调用构建器函数 - `buildList()` 。

```kotlin
val names = listOf<String>("Emma", "Kim")

val list = buildList {
    add("Marta")
    addAll(names)
    add("Kira")
}
println(list) // output: [Marta, Emma, Kim, Kira]
```

## 方法和属性

让我们回顾一下 `List` 的属性和方法：

- `size` 返回 `List` 的大小。
- `isEmpty()` 显示列表是否为空。

此外， `List` 还有一个 `get(index)` 方法，它会返回指定位置的 **元素** 。你也可以使用 `[index]` 来获取 **元素** 。记住，索引从零开始！

假设你有一份派对宾客名单：

```kotlin
val partyList = listOf("Fred", "Emma", "Isabella", "James", "Olivia")
```

我们如何知道何时开始派对？让我们使用 `isEmpty` 方法检查客人是否已到场。如果派对现场不为空，我们想知道有多少位客人，并找出谁能获得第一杯迎宾鸡尾酒！

我们将得到类似这样的结果：

```kotlin
if (!partyList.isEmpty()) {
    val size = partyList.size
    val whoIsFirst = partyList[0]
    println("The party will not be lonesome! We already got $size people. And $whoIsFirst was the first to arrive today!")
    // The party will not be lonesome! We already got 5 people. And Fred was the first to arrive today!
}
```

让我们看看如何使用其他熟悉的方法：

- `indexOf(element)` 返回指定元素首次出现的索引。如果列表中不存在该元素，则函数返回 `-1` 。
- `contains(element)` 如果指定的元素在列表中，则返回 `true` 如果不在列表中，则返回 `false` 。

艾玛认为她有权先喝一杯鸡尾酒。但事实果真如此吗？让我们来验证一下：

```kotlin
println("Emma came in ${partyList.indexOf("Emma") + 1}") // Emma came in 2
```

看来艾玛没得第一，她得了第二。现在，詹姆斯（像往常一样）想知道伊莎贝拉来没来：

```kotlin
println("Guys, is it true that Isabella came? It's ${partyList.contains("Isabella")}") // Guys, is it true that Isabella came? It's true
```

还有许多其他有用的 `List` 方法：请访问 [kotlinlang.org](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-list/) 并熟悉它们！

## 遍历元素

您可以使用 `for` 循环遍历 `List` 中的元素。我们来看一个例子：

```kotlin
val participants = listOf("Fred", "Emma", "Isabella")

for (participant in participants) {
    println("Hello $participant!")
}

// Hello Fred!
// Hello Emma!
// Hello Isabella!
```

在这个例子中，我们遍历 `participants` 并将它们打印到控制台。

## 成语

`List` 是编程中非常常见的数据结构。不出所料，它也有自己的一套编程惯例。

您已经了解了几种创建 `List` 的方法。和往常一样，Kotlin 社区建议使用最简洁的方法。您可以在 [kotlinlang.org](https://kotlinlang.org/docs/idioms.html#read-only-list) 上找到它。

```kotlin
val list = listOf("a", "b", "c")
```

## 结论

现在您了解了 Kotlin 中 `List` 和 `MutableList` 的主要区别。简单回顾一下：当您不希望内容发生变化时，请使用 `List` 。

你知道如何初始化列表、检查列表是否为空、检查列表是否包含特定元素、通过索引获取元素或找到元素的索引，以及如何计算列表的大小。你可以使用 `for` 循环遍历 `List` 的元素。这并非全部，但足以让你入门！接下来，我们来做一些练习。

424 名学习者喜欢这篇理论文章， 4 名学习者不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
