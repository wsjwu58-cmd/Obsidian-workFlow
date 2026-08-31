提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

如您所知，遍历集合或数组有多种方法。例如，您可以使用 `for` 循环来实现此目的。此外，Kotlin 标准库提供了一种称为 **迭代器的** 特殊结构。无论集合或数组存储什么内容，您都可以使用这两种方法。在本主题中，您将深入了解迭代器的机制和用法。

## 迭代器和不可变集合

迭代器允许按顺序访问集合中的元素，而无需考虑它们的类型。它可以被视为指向集合中某个元素的可移动指针。

要使用迭代器，应该调用 `iterator()` 函数。\`iterator `iterator()` 函数返回一个可以遍历集合的特殊对象。

创建迭代器变量时，它指向集合中第一个元素 **之前的** 位置。如果要移动到下一个元素，请调用 \` `next()` \` 函数。该函数返回当前元素并将迭代器的指针移动到下一个元素。\`hasNext `hasNext()` 函数可以帮助你判断迭代中是否还有剩余元素：如果迭代中仍有元素，则返回 \`true\`。

迭代器可以用于不同类型的集合： `List` 、 `Map` 和 `Set` 。

让我们来看一个它在集合中的应用示例：

```kotlin
var set = setOf("cat", "dog", "crocodile", "snake")
var iterator = set.iterator()

while (iterator.hasNext()) {
    print(iterator.next() + " ") // cat dog crocodile snake
}
```

这里我们有一个字符串集合，并为其创建一个迭代器。我们借助 `hasNext()` 和 `next()` 空集合）尝试从迭代器调用 `next()` ，则会抛出 `NoSuchElementException` 。在这种情况下，您应该为该集合创建一个新的迭代器。

下面你可以看到迭代器是如何遍历集合的。

收藏的开始：

                                                                              ![start moving the interetor through collections](https://ucarecdn.com/838be3da-1852-4ee4-88ad-5d3bcdc948b0/)

下一步：

                                                                              ![the next step is to move the interetor through collections](https://ucarecdn.com/994f4322-80f6-42ca-a02c-6fd91e9ecec7/)

收藏的结束：

                                                                              ![end of moving the interetor through collections](https://ucarecdn.com/d6ffaa5f-e030-44a6-9483-7658cd62608f/)

迭代器支持 `forEach()` \` 函数，而不是 `for` 循环。该函数接受一个操作，并对集合中的每个元素执行该操作。您可以在其中使用 lambda 表达式和方法引用。

让我们来看一个使用 `forEach()` 函数处理 map 的例子：

```kotlin
var map = mapOf("John" to "chocolate", "Mary" to "sweets", "Sara" to "marmalade")
var iterator = map.iterator()

iterator.forEach { (key, value) ->
    println("$key likes $value")
}

/*
  John likes chocolate
  Mary likes sweets
  Sara likes marmalade
*/
```

`forEach()` 函数接收 `println()` 函数并输出映射中的每个条目。

如您所见，使用迭代器，我们可以遍历并读取值，但无法修改集合本身。下一段将介绍如何使用迭代器修改集合。

## 迭代器和可变集合

另一种特殊的迭代器变体是 `MutableIterator` 。它与之前的迭代器不同之处在于，它可以处理可变集合，即创建后可以修改的集合。MutableIterator 继承 `Iterator` `MutableIterator` 并提供了 `remove()` 函数，该函数会移除迭代器返回的最后一个集合元素。

使用迭代器（ `for...in` 循环不同）处理可变集合的一个重要方面是，它能够改变可变集合，因为 Kotlin 中的标准 `for` 循环不允许我们这样做。

```kotlin
val food = mutableSetOf("donuts", "cakes", "tarts")
val mutableIterator = food.iterator()

mutableIterator.next()
mutableIterator.remove()
println("Result : $food")// Result: [cakes, tarts]
```

如您所见，为了能够从集合中删除一个元素，您需要调用 `next()` 因为我们只能删除迭代器返回的元素。

## 列表迭代器

列表有一种特殊的迭代器，称为 `ListIterator` 。它允许你双向遍历列表：向前和向后，而 `Set` 或 `Map` 的迭代器只能向前遍历。此外， `ListIterator` 还可以获取下一个元素和上一个元素的位置。

除了常见的 `Iterator` 方法外， `ListIterator` 还具有以下自身特有的方法：

- `fun nextIndex(): Int` 返回调用 `next()` 函数将返回的元素的索引；
- `fun previous(): T` 返回列表的前一个元素，并将迭代器的指针向后移动；
- `fun hasPrevious(): Boolean` 返回“true”，表示当前元素之前是否存在迭代元素；
- `fun previousIndex(): Int` 返回调用 `previous()` 函数将返回的元素的索引。

我们来看一个例子：

```kotlin
val strings = listOf("i", "like", "donuts")
val listIterator = strings.listIterator()

println("Iterating forwards:")
while (listIterator.hasNext()) listIterator.next()

println("Iterating backwards:")
while (listIterator.hasPrevious()) {
    print("index: ${listIterator.previousIndex()}")
    println(", value: ${listIterator.previous()}")
}
```

结果如下：

```
Iterating forwards:
Iterating backwards:
index: 2, value: donuts
index: 1, value: like
index: 0, value: i
```

首先，我们遍历了列表直到末尾。然后，我们再次遍历了列表，但这次是反向遍历。正如你所看到的，即使到达最后一个元素， `ListIterator` 仍然可以使用。

可变列表有其自身的 `Iterator` 版本，称为 `MutableListIterator` `MutableListIterator` 独特之处在于，它不仅可以删除元素，还可以在遍历集合时替换元素和添加新元素。

```kotlin
val words = mutableListOf("i", "know", "Claire")
val mutableListIterator = words.listIterator()

mutableListIterator.next()
mutableListIterator.next()
mutableListIterator.set("don't know")// i , don't know, Claire
mutableListIterator.add("John")
println(words)// i, don't know, John, Claire
```

我们将迭代器的指针移动到第三个元素，迭代器返回了第二个元素。然后，我们使用 `set()` 函数替换了第二个元素。\`set `set()` 函数会替换 \` `next()` 或 `previous()` 返回的最后一个元素。\`add `add()` 会在 `next()` 返回的元素之前向列表中添加一个新元素。

## 结论

Kotlin 标准库的 `Iterator` 提供了处理不同类型集合的便捷方法。通过调用 `iterator()` 函数，您可以获得一个 `Iterator` 对象，用于遍历集合。

通常， `Iterator` 提供多种方法： `forEach` 方法允许对集合中的每个元素执行给定的操作， `next()` 方法允许移动到下一个元素，而 `hasNext()` `Iterator` 则告诉我们迭代过程中是否还有剩余元素。Iterator 也用于遍历不可变集合，其继承者 `MutableIterator` 允许你删除元素。

`ListIterator` 是一种特殊的迭代 `List` 实现，它允许你双向迭代列表；而 `MutableListIterator` 则允许在过程中替换和添加元素。

115 名学员喜欢这篇理论文章， 3 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
