提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经对集合及其不同类型（集合、列表、映射）和变体（可变、不可变）有了基本的了解。在本主题中，我们将更深入地了解一种特定类型：映射。

## 地图集

`Map` 是一个，它存储键值对（ **键** 和 **值** ），并支持高效地检索与每个键对应的值。正如你所记得的， **不可变** 意味着集合一旦初始化就不能更改其大小和内容。需要注意的是， `Map` 键是唯一的：换句话说，一个 `Map` 中每个键只能对应一个值。

假设你正在帮助一所学校编写一个程序来跟踪学生的成绩。你目前的任务是保存学生信息及其最终成绩（1 到 5 分）。让我们借助 `Map` 来完成这项任务：

```kotlin
val students = mapOf(
   "Zhenya" to 5,
   "Vlad" to 4,
   "Nina" to 5
)
println(students) // output: {Zhenya=5, Vlad=4, Nina=5}
```

但为什么要用 `Map` ？我们不能用 `MutableList` 实现同样的效果吗？当然可以。为此，我们实际上需要两个列表：一个用于存储键，另一个用于存储键值：

```kotlin
val studentsName = mutableListOf("Zhenya", "Vlad", "Nina")
val studentsMarks = mutableListOf(5, 4, 5)
println("${studentsName[0]}=${studentsMarks[0]}, ${studentsName[1]}=${studentsMarks[1]}, ${studentsName[2]}=${studentsMarks[2]}")
// output: Zhenya=5, Vlad=4, Nina=5
```

它能很好地存储数据，但如果我们需要查看，例如，妮娜的成绩呢？如果我们使用 `MutableList` ，我们就需要遍历每个元素，找出妮娜的排名。

另一方面，如果我们使用 `Map` ，就可以非常轻松地获取与键对应的值。让我们看看它是如何工作的：

```kotlin
val grade = students["Nina"]
println("Nina's grade is: $grade") // output: Nina's grade is: 5
```

这样是不是方便多了？ `Map` 本身就提供了这项功能以及其他一些功能。

## 地图元素

`Map` 中的条目由特殊的 `Pair` 类型表示，该类型专用于表示两个值的通用对。我们来看一个例子：

```kotlin
val (name, grade) = Pair("Zhenya", 5) // easy way to get the first and the second values
println("Student name is: $name And their grade is: $grade")
// output: Student name is: Zhenya And their grade is: 5
```

访问 Pair 元素的另一种方法是使用 \` `.first` 和 \` `.second` 。这种方法比较繁琐，所以建议使用 `()` 语句。请看：

```kotlin
val p = Pair(2, 3)
println("${p.first} ${p.second}") // 2 3
val (first, second) = p 
println("$first $second")         // 2 3
```

您可能已经注意到，我们使用 `to` 构造函数在 `Map` 中创建一个条目。这里， `to` 是创建 `Pair` 简化构造函数：

```kotlin
val (name, grade) = "Vlad" to 4
println("Student name is: $name And their grade is: $grade")
// output: Student name is: Vlad And their grade is: 4
```

## 初始化

`Map` 是一种 **泛型** 类型。正如你从前面的例子中看到的，你可以这样初始化它： `mapOf<K, V>(vararg pairs: Pair<K,V>)` ，其中 `K` 是键类型， `V` 是值类型。

```kotlin
val staff = mapOf<String, Int>("John" to 1000)
```

类型也可以从上下文中推导出来：

```kotlin
val staff = mapOf("Mike" to 1500)
```

如果需要一个空映射，可以使用 `emptyMap<K, V>` 方法：

```kotlin
val emptyStringToDoubleMap = emptyMap<String, Double>()
```

创建地图的另一种方法是调用构建器函数 `buildMap()` ：

```kotlin
val values = mapOf<String, Int>("Second" to 2, "Third" to 3)

val map = buildMap<String, Int> {
    put("First", 1)
    putAll(values)
    put("Fourth", 4)
}
println(map) // output: {First=1, Second=2, Third=3, Fourth=4}
```

## 方法和属性

让我们来看一些 `Map` 的基本属性和方法：

- `size` 指定 `Map` 的大小。
- `isEmpty()` 显示映射是否为空。

如果想通过键获取元素，可以像使用 `Mutablelist` 一样：使用 `[key]` 。也可以使用 `get(key)` 方法获取元素。这两种方法都会返回与给定键对应的值。

假设人力资源部门也需要你的帮助。你掌握着潜在员工的信息以及他们期望的薪资：

```kotlin
val employees = mapOf(
    "Mike" to 1500,
    "Jim" to 500,
    "Sara" to 1000
)
```

假设我们需要知道有多少候选人，并且具体要了解迈克希望挣多少钱：

```kotlin
if (!employees.isEmpty()) {
    println("Number of employees: ${employees.size}")
    println("Mike wants to earn ${employees["Mike"]}")
}
```

好！如果我们想知道吉姆是否愿意成为我们的员工呢？让我们使用 `containsKey(key)` 来找出答案：

```kotlin
val isWanted = employees.containsKey("Jim")
println("Does Jim want to be our employee? It's $isWanted")
```

由于预算紧张，我们来看看是否有候选人愿意以 500 美元的薪水工作。为此，我们将使用 `containsValue(value)` 方法：

```kotlin
val isAnyoneWilling = employees.containsValue(500)
println("Is anyone willing to earn $500? It's $isAnyoneWilling")
```

当然，还有许多其他有用的 `Map` 方法：请访问 [kotlinlang.org](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-map/) 并熟悉它们！

## 遍历元素

我们来看看如何遍历 `Map` 中的元素。您可以使用 `for` 循环结构：

```kotlin
val employees = mapOf(
    "Mike" to 1500,
    "Jim" to 500,
    "Sara" to 1000
)

for (employee in employees)
    println("${employee.key} ${employee.value}")

for ((k, v) in employees)
    println("$k $v")
```

这两种构造方法都会得到相同的结果：

```kotlin
// Mike 1500
// Jim 500
// Sara 1000
```

## 成语

有很多惯用法可以用来操作 `Map` 集合。甚至 [创建 Map](https://kotlinlang.org/docs/idioms.html#read-only-map) 也有相应的惯用法！正如你所看到的，Kotlin 社区认可这种简洁的 `Map` 初始化方式：

```kotlin
val map = mapOf("a" to 1, "b" to 2, "c" to 3)
```

另一个有用的惯用法允许你 [访问元素](https://kotlinlang.org/docs/idioms.html#access-a-map-entry) 。在 `Map` 集合中，你可以使用键来查找对应的值。一种方法是使用函数 `get(key)` 。这条语句有点冗长，所以最好直接写成 `[key]` ：

```kotlin
println(map.get("a")) // 1
println(map["b"])     // 2, idiomatic way
```

最后，还有一种 [遍历映射](https://kotlinlang.org/docs/idioms.html#traverse-a-map-or-a-list-of-pairs) 的惯用法。你几乎总是需要操作映射元素的键和值。因此，你可以使用这种惯用法轻松访问它们：

```kotlin
for ((k, v) in map) {
    println("$k -> $v")
}
```

## 结论

现在你应该对 `Map` 集合类型有了相当不错的理解。记住， `Map` 是不可变的，所以它的大小和内容都不能改变。你知道如何检查 Map 是否为空，如何检查它是否包含特定的键或值，如何通过键获取值，以及如何计算集合的大小。你可以使用 `for` 循环遍历 `Map` 元素。

准备好回答问题和完成任务了吗？开始吧！

332 名学习者喜欢这篇理论文章， 5 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
