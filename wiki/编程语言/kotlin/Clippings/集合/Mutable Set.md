提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在前面的章节中，您已经熟悉了 `Set` 以及它与 `MutableList` 的区别。现在，我们将了解 `MutableSet` ：它的使用场景和方式，以及它与 `Set` 和 `MutableList` 的具体区别。

## 介绍

`MutableSet` 是一个 **无序的** 元素集合，不允许重复元素。与 **不可变的** `Set` 集合不同， MutableSet 是 **可变** 的，可以自由地添加和删除元素。

想象一下，你正在列一张需要购买的食品杂货清单：

```kotlin
val groceries = setOf("Banana", "Strawberry")
println(groceries) // [Banana, Strawberry]
```

但如果您之后想起需要添加更多元素呢？这正是 `MutableSet` `MutableSet` 用武之地。MutableSet 支持添加元素：

```kotlin
val groceries = mutableSetOf("Banana", "Strawberry")
groceries.add("Water")
println(groceries) // [Banana, Strawberry, Water]
```

你可能会问：为什么不直接使用 `MutableList` 呢？与 `MutableSet` 不同， `MutableList` 允许存在重复项：

```kotlin
val groceries = mutableSetOf("Banana", "Banana", "Strawberry")
println(groceries) // [Banana, Strawberry]

val secondGroceries = mutableListOf("Banana", "Banana", "Strawberry")
println(secondGroceries) // [Banana, Banana, Strawberry]
```

## 创建 MutableSet

你可以按以下方式初始化 `MutableSet` ：

```kotlin
val students = mutableSetOf("Joe", "Elena", "Bob")
println(students) // [Joe, Elena, Bob]
```

在这里，我们甚至不需要指定对象的类型，因为它可以从上下文中推导出来。但是请注意，如果您创建一个空的 `MutableSet` ，则必须指定类型：

```kotlin
val points = mutableSetOf<Int>()
println(points) // []
```

您还可以借助 `toMutableSet()` 函数将 `Set` 转换为 `MutableSet` ：

```kotlin
val students = setOf("Joe", "Elena", "Bob").toMutableSet()
students.add("Bob")
println(students) // [Joe, Elena, Bob]
```

## 添加元素

`MutableSet` 与 `Set` 具有相同的属性和方法： `size` 、 `isEmpty()` 、 `indexOf(element)` 、 `contains(element)` 、 `first()` 、 `last()` 等。

此外， `MutableSet` 还提供了用于更改其内容的附加功能：

- `add(element)` 是一个将指定元素添加到集合中的方法；
- `addAll(elements)` 将指定集合中的所有元素添加到集合中。

我们来看一个例子。假设你和同事搭档，任务是快速准确地记下录音内容。你们决定一起转录，然后合并结果，具体流程如下：

```kotlin
val words = mutableSetOf<String>("Apple", "Coke")
val friendsWords = mutableSetOf<String>("Banana", "Coke")

words.add("Phone")
words.add("Controller")

friendsWords.add("Phone")
friendsWords.add("Pasta")
friendsWords.add("Pizza")

words.addAll(friendsWords)

println(words) // [Apple, Coke, Phone, Controller, Banana, Pasta, Pizza]
```

## 移除元素

您可能还需要从集合中移除部分或全部元素。让我们看看该如何操作。

- `remove(element)` 删除指定的元素；
- `clear()` 从当前集合中移除所有元素；
- `removeAll(elements)` 会移除所有也包含在指定集合中的元素（参见下面的示例）。
```kotlin
val groceries = mutableSetOf("Apple", "Water", "Banana", "Pen")

groceries.remove("Apple")
println(groceries) // [Water, Banana, Pen]

val uselessGroceries = setOf("Banana", "Pen")
groceries.removeAll(uselessGroceries)
println(groceries) // [Water]

groceries.clear()
println(groceries) // []
```

当然， `MutableSet` 还有许多其他有用的方法：请访问 [kotlinlang.org](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-set/) 并熟悉它们！

## 遍历元素

您可以使用 `for` 循环遍历 `MutableSet` 中的元素。以下是一个简单的示例：

```kotlin
val places = mutableSetOf("Saint-Petersburg", "Moscow", "Grodno", "Rome")

for (place in places) {
    println(place)
}

// Saint-Petersburg
// Moscow
// Grodno
// Rome
```

## 结论

现在您了解了 `Set` 和 `MutableSet` 的区别。Set 是一个 **不可变** `Set` ，因此当您不希望其内容发生变化时，使用它很合适。如果您希望内容发生变化，那么 MutableSet 是更好的选择，现在您也知道如何初始化它、添加和删除元素以及遍历它们。请注意，如果您是一位经验丰富的程序员，您也可以使用不可变集合来解决本主题中的问题，但由于我们只是在学习阶段，所以请使用。

196 名学习者喜欢这篇理论文章， 2 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
