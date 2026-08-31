提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

你对集合已经相当了解了。在之前的章节中，你已经熟悉了 `List` 。在本章节中，我们将回到你已经熟悉的 `MutableList` 集合。你已经知道如何使用 `MutableList` ，所以我们将回顾这些知识，并讨论它的使用场景、与 `List` 区别以及它的主要用途。

## 介绍

我们来回顾一下： `List` 是一个集合。List 本身就有很多方法和属性。由于 `List` 是不可变的 `List` 所以你无法修改它的元素。现在我们将学习它的可变兄弟——List。  
  
`MutableList` 是 `List` 的另一种形式。它允许元素重复，并按特定顺序存储元素。与 `List` 不同， `MutableList` 是一个可变或可修改的 `MutableList` ，允许您添加和删除元素。MutableList 包含诸如 `add` 、 `remove` 和 `clear` 的函数。

想象一下，你决定 `List` 下所有你去过的地方：

```kotlin
val places = listOf<String>("Paris", "Moscow", "Tokyo")
println(places) // output: [Paris, Moscow, Tokyo]
```

你一直在旅行，最近一次旅行的目的地是圣彼得堡。你想把它添加到你的地点 `List` 中，但遇到了一个问题：你无法向 `List` 中添加新条目，因为它是 **不可变的** 。你可以通过重新赋值来解决这个问题，但这是一种缓慢且低效的方法：

```kotlin
var places = listOf<String>("Paris", "Moscow", "Tokyo") // note var keyword
places += "Saint-Petersburg" // reassignment, slow operation
println(places) // output: [Paris, Moscow, Tokyo, Saint-Petersburg]
```

这时 `MutableList` 就派上用场了。正如我们之前所说， `MutableList` 支持添加元素。所以，让我们切换到 `MutableList` 并添加另一个元素：

```kotlin
val places = mutableListOf<String>("Paris", "Moscow", "Tokyo")
places.add("Saint-Petersburg")
println(places) // output: [Paris, Moscow, Tokyo, Saint-Petersburg]
```

## 主要区别：

1. **可变性** ：
	- `MutableList` 允许你在创建后对其进行更改。
		- 列表（例如 `listOf` ）只能读取，不能修改。
2. **功能** ：
	- `MutableList` 包含 `add` 、 `remove` 和 `clear` 等函数。
		- 这些 [函数](https://hyperskill.org/learn/step/0 "In Kotlin, a function is a sequence of instructions that performs a specific action, such as printing data to standard output or calculating a square root. | It is a named block of code that can be invoked from a program using its name followed by parentheses. If a function takes one or more arguments (input data), they should be passed in the parentheses. Functions can return a result that can be assigned to a variable. Some functions, like regular math functions, take arguments and produce a result.") 不适用于不可变列表。

## 初始化

以下是如何 `MutableList` 方法：

```kotlin
val cars = mutableListOf("Ford", "Toyota", "Audi", "Mazda", "Tesla")
println(cars) // output: [Ford, Toyota, Audi, Mazda, Tesla]
```

就是这样！这里，我们甚至不需要指定对象的类型，因为它可以从上下文中推导出来。但是请注意，如果您创建一个空的 `MutableList` ，则必须指定类型：

```kotlin
val cars = mutableListOf<String>()
println(cars) // output: []
```

您还可以借助 `toMutableList()` 函数将 `List` 转换为 `MutableList` 。如果您想将 `MutableList` 转换为 `List` ，可以使用 `toList()` ：

```kotlin
val cars = listOf("Ford", "Toyota").toMutableList()
cars.add("Tesla")
println(cars) // output: [Ford, Toyota, Tesla]
val carsList = cars.toList()
```

## 添加和替换元素

`MutableList` 与 `List` 具有相同的属性和方法： `size` 、 `get(index)` 、 `isEmpty()` 、 `indexOf(element)` 、 `contains(element)` 等。

由于 `MutableList` 特殊之处在于它可以被修改，因此它还具有更改内容的额外功能：

- `add(element)` 方法用于向列表中添加一个额外的元素。
- `set(index, element)` 将指定位置的元素替换为指定的元素。简写形式：  
	`mutableList[index] = 元素`
- `addAll(elements)` 将指定集合中的所有元素添加到列表末尾。

我们来看几个例子。假设你正准备去买菜，所以你列了一张所需商品的 `List` ：

```kotlin
val products = listOf("Milk", "Cheese", "Coke")
```

你改变主意了：突然，你决定还要买些薯片，或许还要买水而不是牛奶。让我们更新一下商品清单：

```kotlin
val finalList = products.toMutableList()
finalList.add("Chips")
finalList[0] = "Water" // or finalList.set(0, "Water")
println(finalList) // output: [Water, Cheese, Coke, Chips]
```

假设你爸爸进来给了你一张购物清单。好的，我们也把这些商品添加到我们的清单里：

```kotlin
val products = mutableListOf("Milk", "Cheese", "Coke")
val dadsProducts = listOf("Banana", "Watermelon", "Apple")

products.addAll(dadsProducts)

println(products) // output: [Milk, Cheese, Coke, Banana, Watermelon, Apple]
```

## 移除元素

您可能还需要从列表中删除部分或全部元素。让我们看看如何做到这一点：

- `removeAt(index)` 删除指定索引处的元素。
- `remove(element)` 删除指定元素的第一个出现位置。
- `clear()` 会移除当前集合中的所有元素。

让我们回到购物清单。当你穿衣服的时候，你渐渐意识到冰箱里其实已经有了这些东西。于是，你决定逐一清理清单上的这些商品：

```kotlin
val products = mutableListOf("Milk", "Cheese", "Coke")

products.removeAt(0)
println(products) // output: [Cheese, Coke]

products.remove("Coke")
println(products) // output: [Cheese]

products.clear()
println(products) // output: []
```

这并非所有可用方法的完整列表。要了解其他 `MutableList` 方法，请访问 [kotlinlang.org](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-list/) 。

## 遍历元素

您可以使用 `for` 循环遍历 `MutableList` 中的元素。以下是一个示例：

```kotlin
val products = mutableListOf("Cheese", "Milk", "Coke")

for (product in products) {
    println("$product")
}

// Cheese
// Milk
// Coke
```

我们遍历了 `MutableList` ，并打印出每个产品的名称。

## 结论

现在您了解了 `List` 和 `MutableList` 的区别。List 是 **不可变的** ，因此当您不希望其内容发生改变时 `List` 请使用它。MutableList `MutableList` 适用于您知道其内容将来可能需要修改的情况。现在您知道如何初始化 `MutableList` ，以及如何添加、替换和删除其中的元素。您也知道如何使 `List` 可变，以及如何使用 for 循环遍历其元素。请注意，如果您是一位经验丰富的程序员，您可以使用不可变列表来解决与此主题相关的问题，但由于我们只是在学习阶段，因此我们将使用。

367 名学习者喜欢这篇理论文章， 6 名学习者不喜欢。 **你呢？**

报告拼写错误

### 相关主题[列表](https://hyperskill.org/learn/step/10730)

## 相关条目
- [[Kotlin基础语法梳理]]
