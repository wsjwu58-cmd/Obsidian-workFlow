提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经熟悉一维列表。现在，我们将学习 Kotlin 中的二维甚至更高维的。您将学习如何创建这类列表以及如何管理其内容。

## 列表的列表

首先，让我们弄清楚 **多维列表** 的含义。

简而言之，我们可以说多维列表是列表的列表。也就是说，为了创建一个多维列表，我们需要将一个列表作为另一个列表的元素。最终，我们就得到了一个多维列表。

这样的列表使得表示多维事物变得非常容易：例如，具有长度、高度和宽度的三维物体。我们所处的宇宙可以用四个维度来描述，时间是第四维度，因此它是四维的。更高维度，例如五维等等，很难想象，但当你将这个概念付诸实践时，你会发现它们非常方便，而且并不复杂！

让我们来看一些更实际的例子。剧院里的座位可以用二维列表来表示：一个索引代表行数，另一个索引代表该行中的座位号。如果你想编写一款使用地图的游戏，例如海战游戏，二维列表在设置地图坐标方面会非常有用。此外，一些数学结构也可以方便地用多维列表来表示。

首先，让我们来看一个在实践中经常用到的多维列表的特殊情况： **二维列表** 。

## 创建二维列表

一维列表可以用单个元素序列表示，而二维列表更直观的表示方法是使用 **矩阵** 或 **表格** 。如果你的程序中需要处理矩阵或表格，那么将其表示为二维列表的形式就更有意义了。

让我们创建一个二维可变整数列表， `Int` 有 3 行 4 列，所有元素均为 0（零）。它的样子如下：

```kotlin
val mutList2D = mutableListOf(
    mutableListOf<Int>(0, 0, 0, 0),
    mutableListOf<Int>(0, 0, 0, 0),
    mutableListOf<Int>(0, 0, 0, 0)
)
```

您只需 `mutList2D` 的每个元素定义为一个包含四个零的列表即可！可以这样理解：

| 0 | 0 | 0 | 0 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

我们可以说，包含四个零元素的列表 **嵌套** 在 `mutList2D` 中。包含其他列表的列表称为 **主** 列表。

注意一个有趣的特点：嵌套列表的长度不一定必须相同。在下面的示例中，每个新嵌套列表的长度都不同：

```kotlin
val mutList2D = mutableListOf(
    mutableListOf<Int>(0),
    mutableListOf<Int>(1, 2),
    mutableListOf<Int>(3, 4, 5)
)
```

> [!primary] Primary
> 您可以创建同一个二维列表中元素数量不同的嵌套列表。

## 访问元素

我们来看看如何访问列表中的元素。原理与一维列表完全相同。只是现在我们需要写 **两个** 索引：首先是主列表中元素的索引，然后是嵌套列表的索引。

让我们回到 `mutList2D` 。假设我们需要访问位于第一行第一列的元素。我们该如何找到这个元素呢？正如你所记得的， `mutList2D` 是一个列表的列表。所以，首先根据它在主列表中的索引选择一个嵌套列表。这个原理与一维列表类似。

首先，进入嵌套列表，选择具有相应索引的内部列表：

```kotlin
val mutList2D = mutableListOf(
    mutableListOf<Int>(0, 1, 2),   //[0]
    mutableListOf<Int>(3, 4, 5)    //[1]  
)
```

| **mutList2D\[0\]** | **0** | **1** | **2** |
| --- | --- | --- | --- |
| **mutList2D\[1\]** | 3 | 4 | 5 |

其次，在这个嵌套列表中，使用索引选择所需的元素，就像我们在处理一维列表时一样：

| **mutList2D\[0\]\[0\]** | **mutList2D\[0\]\[1\]** | **mutList2D\[0\]\[2\]** |
| --- | --- | --- |
| **0** | 1 | 2 |

让我们打印 `mutList2D[0][0]` ： `mutList2D` 的第一行第一列的元素：

```kotlin
val mutList2D = mutableListOf(
    mutableListOf<Int>(0, 1, 2),   //[0]
    mutableListOf<Int>(3, 4, 5)    //[1]  
)

println(mutList2D[0][0])    // 0
```

> [!warning] Warning
> 请记住，所有列表的索引都从 0 开始！

以下代码将显示二维列表 `mutList2D` 的所有元素：

```kotlin
print(mutList2D[0][0])  // 0
print(mutList2D[0][1])  // 1
print(mutList2D[0][2])  // 2
print(mutList2D[1][0])  // 3
print(mutList2D[1][1])  // 4
print(mutList2D[1][2])  // 5
```

## 创建不同类型的二维列表

嵌套列表不一定是 `Int` 类型：正如你所记得的，Kotlin 提供了多种列表类型。例如，你可以创建一个字符串列表的列表，如下例所示。

您还可以明确定义嵌套列表中元素的类型：

```kotlin
val mutListOfString2D = mutableListOf(
    mutableListOf<String>("to", "be", "or"),
    mutableListOf<String>("not", "to", "be")
)
```

为了创建嵌套的原始值列表，你可以使用特定类型的列表，就像我们创建一维列表一样： `Int` 、 `Long` 、 `Double` 、 `Float` 、 `Char` 、 `Short` 、 `Byte` 和 `Boolean` 。

例如，我们来考虑创建一个字符类型的：

```kotlin
val mutListOfChar2D = mutableListOf(
    mutableListOf<Char>('A', 'R', 'R'),
    mutableListOf<Char>('A', 'Y', 'S')
)
```

你可以这样想象：

| A | R | R |
| --- | --- | --- |
| A | Y | S |

此外，嵌套列表可以是不同类型的。例如，您可以创建一个二维列表，其中同时存储 `Int` 和 `String` 列表：

```kotlin
val mutListOfStringAndInt2D = mutableListOf(
    mutableListOf<String>("Practice", "makes", "perfect"),
    mutableListOf<Int>(1, 2)
)
```

> [!primary] Primary
> 您可以同时在同一个二维列表中创建不同类型的嵌套列表。

## 使用二维列表的特点

让我们来看看处理二维列表的一些实用且有趣的特性。您可能还记得，我们可以使用 `joinToString()` 函数将列表中的所有元素打印成一个字符串。对于嵌套列表，此方法同样适用。只是现在您必须指定要转换为字符串的嵌套列表的索引：

```kotlin
val mutListString = mutableListOf(
    mutableListOf<String>("A", "R", "R", "A", "Y")
)
print(mutListString[0].joinToString())    // A, R, R, A, Y
```

对于多维列表，这种方法并不总是方便。为了将所有列表的内容获取到单个字符串中，只需打印主列表即可：

```kotlin
val mutListOfChar2D = mutableListOf(
mutableListOf<Char>('k'),
mutableListOf<Char>('o', 't'),
mutableListOf<Char>('l', 'i', 'n'))

println(mutListOfChar2D)    // [[k], [o, t], [l, i, n]]
```

## 多维列表（>2）

我们终于可以开始处理更复杂的概念了。有些列表的维度超过两个。虽然理解起来可能比较困难，但别担心：你会慢慢习惯的。

你可以想象这样一个三维列表：

| \[0, 1\] | \[2, 3\] |
| --- | --- |
| \[4, 5\] | \[6, 7\] |

在二维列表的每个元素中，都存在另一个嵌套列表。

你可以把它想象成一个立方体或长方体：它正好有三个维度——长、宽和高。考虑以下实际情况：假设你需要确定一辆车在多层停车场的具体位置。那么，你需要设定三个数字，也就是三个坐标：楼层、行数和在行中的位置。

以下代码创建了您刚才看到的三维可变列表：

```kotlin
val mutList3D = mutableListOf(
    mutableListOf(mutableListOf<Int>(0,1), mutableListOf<Int>(2,3)),
    mutableListOf(mutableListOf<Int>(4,5), mutableListOf<Int>(6,7))
)

println(mutList3D)  // [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
```

因此，为了引用此类列表中的元素，我们需要 **三个** 索引：

```kotlin
println(mutList3D[0][0][1])   // 1
println(mutList3D[1][0][1])   // 5
println(mutList3D[1][1][1])   // 7
```

您可以类比创建更多维度的列表——4维、5维、6维等等——根据需要进行扩展。只需记住，多维列表中的元素拥有的索引数量与该列表的维度数量相同。

## 结论

让我们回顾一下。您已经了解了什么是多维列表以及如何在 Kotlin 中创建它们。以下是需要记住的要点：

- 多维列表本质上是一个列表的列表。
- 要查找多维列表中的元素，需要的索引数量等于列表的维度数量。
- 您可以明确指定不同类型的嵌套列表，而不仅仅是 `Int` 。
- 您可以在多维列表中组合不同类型和大小的列表。
- 要打印所有列表元素，可以使用 `joinToString()` 函数。
- 索引从0开始。

511 名学习者喜欢这篇理论文章， 15 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
