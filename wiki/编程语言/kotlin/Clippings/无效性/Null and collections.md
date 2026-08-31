提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

我们已经学习了 Kotlin 中的空安全机制。在本主题中，我们将探讨如何处理集合中的空值，集合比其他数据类型更为复杂。我们还将讨论处理可空元素的便捷方法。

## 集合和可空集合

可空集合和包含可空元素的非空集合本质上是同一枚硬币的两面。此外，我们还需要理解空集合和可空集合之间的区别。让我们来看以下四种情况：

```kotlin
val list = listOf<String>()

var nullableList: List<Int>? = listOf<Int>(1, 2, 4, 6)

val listWithNullableElements: List<Int?> = listOf<Int?>(1, 2, 4, null, null)

var absolutelyNullableList: List<Int?>? = listOf<Int?>(1, 2, 4, null, null)
```

第一种情况是一个简单的空列表。我们可以像处理普通列表一样处理它，无需担心 `NullPointerException` 。这个列表是真实的，不包含空值，它只是为空而已。

第二种情况是可空列表：此类列表中的元素不可为空，它们必须是实数整数。但变量 `nullableList` 可以为 `null` 。因此，在处理可空列表时，我们必须使用安全调用运算符、检查、Elvis 运算符等。例如：

```kotlin
val list: List<Int> = nullableList? ?: listOf<Int>()
```

第三种情况，我们有一个包含可空元素的列表。它的类型不可为空，但其中的元素可以为空。

```kotlin
val num: Int = listWithNullableElements[1]? ?: 150
```

第四种情况，我们将第二种和第三种情况的方法结合起来：

```kotlin
val num: Int = absolutelyNullableList?[1]? ?: 150
```

基本原则是：如果可以返回空集合，那就比返回 null 和使用可空类型要好。然而，有时我们确实需要处理空集合。例如，如果我们声明一个变量（ `var` ，而不是 `val` ），它可以接收值，也可以接收 `null` 值（它等于“不存在的元素”、“没有答案”或“没有结果”）。

## 从包含空元素的序列创建非空集合

有时你会遇到包含 `null` 元素序列，需要用它们创建一个不包含 `null` 集合。在这种情况下，可以使用特殊函数 `listOfNotNull()` 和 `setOfNotNull()` ，它们可以帮助我们删除所有空元素，并默认返回非空类型的只读集合。下面我们来看看它是如何工作的：

```kotlin
val list = listOfNotNull(1, null, 50, 404, 42, null, 42, 404) // [1, 50, 404, 42, 42, 404]
val set = setOfNotNull(1, null, 50, 404, 42, null, 42, 404) // [1, 50, 404, 42]
```

所有空元素都会从新集合中删除。如果您的元素序列仅包含 `null` 元素，这些方法将返回一个空集合（但不是 `null` ！）。请记住，如果您需要可变集合，只需使用 `toMutableList()` 或 `toMutableSet()` 进行转换即可。

## 可空集合的函数

Kotlin 为包含可空元素的集合提供了一些便捷的工具： `isNullOrEmpty()` 、 `getOrNull()` 、 `firstOrNull()` 、 `lastOrNull()` 和 `randomOrNull()` 。让我们一起来看看吧！

`isNullOrEmpty()` 函数在集合为空或等于 `null` 时返回 `true` ；在所有其他情况下返回 `false` 。

```kotlin
val emptySet: Set<Int>? = setOf()
val nullSet: Set<Int>? = null
val set = setOf<Int?>(null, null)

println(emptySet.isNullOrEmpty()) // true because the collection is empty
println(nullSet.isNullOrEmpty()) // true because the collection is equal to null
println(set.isNullOrEmpty()) // false because the collection has two elements with null value
```

`getOrNull()` 函数返回列表或数组中的一个元素，但如果该元素不存在，则返回 `null` （它不适用于 `Set` ）。

```kotlin
val list = listOf(0, 1, 2)
println(list.getOrNull(2)) // 2
println(list.getOrNull(3)) // null because this list doesn’t have a fourth element and numbering starts with 0
```

你可能会说可以直接使用 `list[3]` ，但那样会抛出异常，而 `getOrNull()` 在任何情况下都会返回一个值。randomOrNull `randomOrNull()` 函数的工作方式与前者类似：如果集合为空，则返回 `null` 否则返回一个随机元素。

```kotlin
val list = listOf(0, 1, 2)
val list1 = listOf<Int>()

println(list.randomOrNull()) // returns some element
println(list1.randomOrNull()) // null because the collection is empty
```

`firstOrNull()` 和 `lastOrNull()` 函数允许我们设置特定条件。如果至少存在一个元素满足该条件，它们将返回该元素。

```kotlin
val list = listOf(0, 1, 1, 2, 5, 7, 6)
val num = list.firstOrNull { it > 3 }
val num1 = list.lastOrNull { it == 1 }
```

## 最小值和最大值元素可为空

Kotlin 提供了许多便捷的集合比较工具，也适用于可空元素。以下是一些示例：

1. `minOrNull()` / `maxOrNull()` – 返回集合中的最大或最小元素，如果集合为空则返回 `null` 。
2. `minByOrNull()` / `maxByOrNull()` – 返回满足条件的第一个最大或最小集合元素，或者 `null` 。
3. `minOfOrNull()` / `maxOfOrNull()` – 返回条件中标记的元素的特征值或 `null` 。
4. `minWithOrNull()` / `maxWithOrNull()` – 返回满足 `compareBy {}` 块中指定条件的第一个元素或 `null` 。
5. `minOfWithOrNull()` / `maxOfWithOrNull()` – 返回 `compareBy {}` 块中指定的条件所标记的元素的特征值或 `null` 。

这里我们只提及这些功能——您可以在“ [集合的聚合操作](https://hyperskill.org/learn/step/23322) ”主题中找到详细信息和示例。

> [!warning] Warning
> 然而，这里有个小问题：所有这些函数都有不带“OrNull”的对应版本。这些对应版本曾经是合法的工具。但在 Kotlin 1.4.0 中，这些对应版本，例如 `min()` 、 `max()` 、 `minBy()` )、 `maxBy()` ()、 `minWith()` 和 `maxWith()` ，被重命名为 `minOrNull()` 、 `maxOrNull()` 等等，而原先的版本则被标记为已弃用。不过，在 Kotlin 1.7.0 中，它们作为不可为空的替代方案重新引入，取代了它们各自的“OrNull”对应版本。现在，它们会返回一个集合元素或抛出一个异常。请谨慎使用它们！

## 结论

我们已经探讨了包含可空元素的集合以及一些便捷的操作方法。以下是几个要点：

1. Kotlin 中有可空集合、包含可空元素的集合和空集合。它们彼此之间各不相同。
2. `listOfNotNull()` 和 `setOfNotNull()` 函数允许我们从可为空的数据序列创建非空集合。
3. 我们可以检查集合是否为空，或者是否包含满足某些条件的元素，并确保不会收到异常。
4. 我们可以使用比较函数 `maxOrNull()` / `minOrNull()` 等来选择和显示集合元素或其参数。
5. 这些函数有非空的对应函数，它们在 `maxOrNull()` 等情况下会返回一些值或异常，而不是返回 `null`

65 名学员喜欢这篇理论文章， 3 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
