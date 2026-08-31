提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在前面的章节中，你已经熟悉了 `Map` 现在，我们将来看一下…… `MutableMap` 何时以及如何使用它，以及它与……究竟有何不同 `Map` 。

## 介绍

`MutableMap` 是一个集合，它存储对象对（键和值），并支持高效地检索与每个键对应的值。与 **不可变的** `Map` 集合不同， MutableMap 是 **可变的** ，或者说是可修改的：您可以自由地添加和删除对象对。

假设你有一份员工名单，其中包含了他们的薪资信息：

```kotlin
val staff = mapOf(
   "John" to 500,
   "Mike" to 1000,
   "Lara" to 1300
)
println(staff) // output: {John=500, Mike=1000, Lara=1300}
```

好了，我们已经有了员工名单和薪资信息，现在可以轻松查到每位员工的薪资。但是如果我们新招了一名员工呢？  
我们知道， `Map` 是一个：我们无法修改它的源数据。因此，要向 `Map` Map `  中添加新员工，我们需要创建另一个  ` 。

```kotlin
var staff = mapOf( // you cannot reassign an immutable reference, so you need to use var
   "John" to 500,
   "Mike" to 1000,
   "Lara" to 1300
)
staff += "Jane" to 700 // reassignment
println(staff) // output: {John=500, Mike=1000, Lara=1300, Jane=700}
```

这正是 `MutableMap` `MutableMap` 用武之地。MutableMap 支持添加元素：

```kotlin
val staff = mutableMapOf(
   "John" to 500,
   "Mike" to 1000,
   "Lara" to 1300
)

staff["Nika"] = 999

println(staff) // output: {John=500, Mike=1000, Lara=1300, Nika=999}
```

这是 `MutableMap` 为我们提供的开箱即用的功能之一，它允许我们轻松修改映射内容。

## 初始化

您可以通过多种方式创建 `MutableMap` ：

```kotlin
val students = mutableMapOf<String, Int>("Nika" to 19, "Mike" to 23)
println(students) // output: {Nika=19, Mike=23}
```

类型也可以从上下文中推导出来：

```kotlin
val carsPerYear = mutableMapOf(1999 to 30000, 2021 to 202111)
println(carsPerYear) // output: {1999=30000, 2021=202111}
```

您还可以借助 `toMutableMap()` 函数将 `Map` 转换为 `MutableMap` ：

```kotlin
val mapCarsPerYear = mapOf(1999 to 30000, 2021 to 202111)
val carsPerYear = mapCarsPerYear.toMutableMap()
carsPerYear[2020] = 2020
println(carsPerYear) // output: {1999=30000, 2021=202111, 2020=2020}}
```

## 添加元素

此外， `MutableMap` 还提供了用于更改内容的附加功能：

- `put(key, value)` 将指定的值与映射中指定的键关联起来；是 `mutableMap[key] = value` 的简写形式；
- `putAll(Map)` 使用指定映射中的键/值对更新映射；
- `putIfAbsent(key, value)` 如果键不在映射中，则放入值；否则，映射将保持不变。

我们来看一个例子。假设我们招收了一些学生组成一个小组，然后决定将另一个城市的学生也加入到这个小组中：

```kotlin
val groupOfStudents = mutableMapOf<String, Int>() // empty mutable map
groupOfStudents.put("John", 4)
groupOfStudents["Mike"] = 5
groupOfStudents["Anastasia"] = 10

val studentsFromOregon = mapOf("Alexa" to 7)

groupOfStudents.putAll(studentsFromOregon)
    
println(groupOfStudents) // output: {John=4, Mike=5, Anastasia=10, Alexa=7}
```

当您尝试将映射中的指定值与已存在的键关联时，现有值将被覆盖。我们来看一个例子：

```kotlin
val groceries = mutableMapOf<String, Int>() 

groceries["Potato"] = 5  
println(groceries)  // output: {Potato=5}
    
groceries["Potato"] = 10     
println(groceries)  // output: {Potato=10}
```

您还可以使用 plusAssign 运算符语法向映射中添加元素，如下例所示：

```kotlin
val groceries = mutableMapOf<String, Int>()

groceries += mapOf("Potato" to 5)
groceries += "Sprite" to 1

println(groceries)  // output: {Potato=5, Sprite=1}
```

## 移除元素

您可能还需要从 `Map` 中移除部分或全部元素。让我们看看如何操作：

- `remove(key)` removes the specified key and its corresponding value from the map;
- `clear()` removes all elements from the map.
```kotlin
val groceries = mutableMapOf(
    "Potato" to 10,
    "Coke" to 5,
    "Chips" to 7
)

groceries.remove("Potato")
println(groceries) // output: {Coke=5, Chips=7}

groceries.clear()
println(groceries) // output: {}
```

You can also remove an element from the map using the minusAssign operator syntax. Take a look at an example:

```kotlin
val cars = mutableMapOf<String, Double>()
cars["Ford"] = 100.500
cars["Kia"] = 500.15
    
println(cars)  // output: {Ford=100.5, Kia=500.15}
    
cars -= "Kia"   
println(cars)  // output: {Ford=100.5}
```

## Conclusion

Now you know the difference between `Map` and `MutableMap`. `Map` is an immutable collection, so it makes sense to use it when you don't want the contents to change. If you do, then `MutableMap` is a better choice, and now you know how to initialize it, add and remove elements, and iterate through them.

252 learners liked this piece of theory. 2 didn't like it. **What about you?**

Report a typo

## 相关条目
- [[Kotlin基础语法梳理]]
