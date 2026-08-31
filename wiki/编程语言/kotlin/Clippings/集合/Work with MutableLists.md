提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

Kotlin 提供了许多实用函数，在处理列表和修改其内容时非常方便。在本主题中，我们将介绍几类常用函数，并通过示例演示如何使用它们。

## 输出列表

第一个函数是 `joinToString()` 。它可以帮助我们使用 `separator` 符属性以不同的方式输出列表。

使用 `joinToString()` 查看生成的列表并打印其内容：

```kotlin
val southernCross = mutableListOf("Acrux", "Gacrux", "Imai", "Mimosa")
println(southernCross.joinToString())   //  Acrux, Gacrux, Imai, Mimosa
```

请记住， `joinToString()` 函数会按照存储顺序从可变列表中取出元素，并将其表示为逗号分隔的字符串行。

您还可以使用其他分隔符来分隔元素：

```kotlin
println(southernCross.joinToString(" -> "))   //  Acrux -> Gacrux -> Imai -> Mimosa
```

## 处理多个列表

现在，让我们来看看在使用多个字符串列表时，你可能需要了解的一些事项。

- 可以合并。

您可以像以下示例所示那样连接多个列表：

```kotlin
val southernCross = mutableListOf("Acrux", "Gacrux", "Imai", "Mimosa")
val stars = mutableListOf("Ginan", "Mu Crucis")

val newList = southernCross + stars
println(newList.joinToString())    //  Acrux, Gacrux, Imai, Mimosa, Ginan, Mu Crucis
```
- 可变列表可以进行比较。

您可以使用运算符 `==` 和 `!=` 来比较列表——包括它们的内容和大小：

```kotlin
val firstList = mutableListOf("result", "is", "true")
val secondList = mutableListOf("result", "is", "true")
val thirdList = mutableListOf("result")

println(firstList == secondList)  //  true
println(firstList == thirdList)   //  false
println(secondList != thirdList)  //  true
```

请注意，只有当两个列表的元素完全匹配且排列顺序相同时，才会返回 `true` 。

## 更改列表内容

关键字 `val` 和 `var` 告诉你如何处理变量的值/引用。

**var** – 分配给变量的值/引用可以随时更改。  
**val** – 值/引用只能赋给变量一次，并且在执行过程中不能更改。

无论你使用关键字 `val` 还是 `var` ，你仍然可以通过索引编辑现有元素的值。这是因为当我们更改列表的内容时，我们不会创建一个新列表（列表的链接不会改变）：

```kotlin
val southernCross = mutableListOf("Acrux", "Gacrux", "Imai", "Mimosa")
var stars = mutableListOf("Ginan", "Mu Crucis")
southernCross[1] = "star"
stars[1] = "star"

println(southernCross[1]) // star
println(stars[1]) // star
```

可以通过多种方式删除列表元素并向列表中添加新元素。

您可以使用 `add` 、 `remove` 和 `clear` 函数来更改列表：

```kotlin
val southernCross = mutableListOf("Acrux", "Gacrux", "Imai", "Mimosa")
val stars = mutableListOf("Ginan", "Mu Crucis")
val names = mutableListOf("Jack", "John", "Katie")
val food = mutableListOf("Bread", "Cheese", "Meat")
val fruits = mutableListOf("Apple", "Banana", "Grape", "Mango")

southernCross.removeAt(0)
southernCross.remove("Mimosa")

stars.add("New star")
stars.add(0, "First star")

names.clear()

food.addAll(fruits)

println(names) // []
println(southernCross.joinToString()) // Gacrux, Imai
println(stars.joinToString()) // First star, Ginan, Mu Crucis, New star
println(food.joinToString()) // Bread, Cheese, Meat, Apple, Banana, Grape, Mango
```
- `add(element)` 和 `add(index, element)` 函数会在列表中的任意位置插入新元素。如果不指定索引，则元素会被添加到列表末尾。
- `list1.addAll(list2)` 将 `list2` 中的所有元素添加到 `list1` 的末尾。
- `remove(element)` 和 `removeAt(index)` 函数都用于从列表中删除元素。前者从列表中删除指定元素的单个实例（如果元素删除成功，则返回 `true` ，否则返回 `false` ）。后者删除指定位置的元素，并返回被删除的元素。
- `clear()` 会删除列表中的所有元素。

此外，您可以使用 `+=` 向列表中添加新元素：

```kotlin
val vowels = mutableListOf('a', 'o', 'i', 'e', 'u')
val intList1 = mutableListOf(1, 2, 3, 4, 5)
val intList2 = mutableListOf(5, 4, 3, 2, 1)
    
vowels += 'y'
intList1 += intList2

println(vowels)   // [a, o, i, e, u, y]
println(intList1) // [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
```

## 复制列表内容

Kotlin 没有直接复制现有列表的函数。但是，你可以使用 `toMutableList()` 函数来实现：

```kotlin
val list = mutableListOf(1, 2, 3, 4, 5)
val copyList = list.toMutableList()

print(copyList) // [1, 2, 3, 4, 5]
```

此函数创建一个新的 MutableList，并将 `list` 的内容添加到新列表中。其工作原理如下：

```kotlin
val list = mutableListOf(1, 2, 3, 4, 5)
val copyList = mutableListOf<Int>()
copyList.addAll(list)

print(copyList) // [1, 2, 3, 4, 5]
```

## 其他实用功能

在处理列表及其内容时，有些操作会非常有用：

- `list.isEmpty()` 和 `list.isNotEmpty()` – 检查列表是否为空。
- `list.subList(from, to)` – 创建一个较小的列表（子列表），其中包含原始列表中索引为以下各项的元素： `from` 、 `from + 1` 、...、 `to - 2` 、 `to - 1` 索引为 `to` 元素不包含在内。
```kotlin
val numbers = mutableListOf(1, 2, 3, 4, 5)
var sublist = mutableListOf<Int>()
if (numbers.isNotEmpty() && numbers.size >= 4) {
     sublist = numbers.subList(1, 4)
}

print(sublist) // [2, 3, 4]
```
- `list.indexOf(element)` – 查找列表中某个元素的索引。如果列表中不存在该元素，则此函数返回 -1。否则，通过计算出的索引访问列表时，即可找到该元素。
```kotlin
val numbers = mutableListOf(1, 2, 3, 4, 5)

if (5 in numbers) {
    println(numbers.indexOf(5)) // 4
}

print(numbers.indexOf(7)) // -1
```
- `list.minOrNull()` 和 `list.maxOrNull()` – 查找列表中的最小和最大元素。
- `list.sum()` – 返回列表中元素的总和。
- `list.sorted()` 和 `list.sortedDescending()` – 从可用列表中构建排序列表（升序或降序）。
```kotlin
val numbers = mutableListOf(1, 2, 3, 4, 5)
    
val vowels = mutableListOf('e', 'a', 'y', 'i', 'u', 'o')
    
println(numbers.minOrNull()) // 1
println(numbers.maxOrNull()) // 5
println(numbers.sum())      // 15
    
println(vowels.sorted()) // [a, e, i, o, u, y]
println(vowels.sortedDescending()) // [y, u, o, i, e, a]
```

## 结论

现在让我们总结一下！你已经掌握了一些在处理可变列表时常用的函数和技巧。

现在你可以：

- 使用 `joinToString()` 将列表中的内容合并成一个字符串并输出；
- 使用 `==` 和 `!=` 比较两个可变列表；
- 向列表中添加新元素或从列表中删除元素；
- 对列表和列表元素执行各种操作。

> [!primary] Primary
> 内容真不少！好消息是：你可以用同样的方法处理任何类型的可变列表。祝你好运！

770 名学习者喜欢这篇理论文章， 6 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
