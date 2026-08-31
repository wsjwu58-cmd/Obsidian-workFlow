提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在编程中，当我们想要执行特定操作时，例如计算一个数的绝对值或找出成绩最好的学生，我们会使用函数。然而，函数存在一个“小”问题：它们只能返回特定类型的值。如果我们想要返回多个不同类型的值该怎么办？Kotlin 提供了两个特殊的类来帮助我们处理这种情况： **Pair** 和 **Triple** 。让我们来看看它们是如何工作的。

## 一对

Pair 是 Kotlin 中一个简单的数据类型，用于在单个实例中存储两个类型相同或不同的值。这两个值之间不需要存在任何关系。Pair 具有值语义，也就是说，如果两个 Pair 元素都相等，则这两个 Pair 也相等。

要创建一个新的 Pair 实例，我们使用一个 Pair 构造函数，并传入所有数据的值和类型。Kotlin 可以根据这些值推断数据类型。

```kotlin
val pair = Pair(1, "one")
println(pair) // (1, one)
```

我们可以使用 infix 函数 `to` 创建一个新的 Pair 对象：

```kotlin
val pair = 1 to "one"
println(pair) // (1, one)
```

## 如何使用 Pair

为了处理这些值，我们可以使用 **第一个** 和 **第二个** 属性，或者使用 `componentN` 方法从 Pair 中提取值 `componentN` 中的 N 值表示组件的编号；例如， `component1` 表示 Pair 的第一个属性或值。

```kotlin
val pairOne = Pair("Hi", "I am a Pair")
val pairTwo = "Hi" to "I am another Pair"

// Properties
println(pairOne.first) // Hi
println(pairOne.second) // I am a Pair

// Methods
println(pairTwo.component1()) // Hi
println(pairTwo.component2()) // I am another Pair
```

对于 Pair 类型，我们可以使用两个特殊方法 **——toString()** 和 **toList()：**

- **toString()** 返回包含 Pair 的第一个值和第二个值的字符串表示形式：
```kotlin
val pair = Pair("marks", listOf(8.0, 9.0, 10.0))
println(pair) // (marks, [8.0, 9.0, 10.0]) toString() is implicit
println(pair.toString()) // (marks, [8.0, 9.0, 10.0])
```
- **toList()** 将 Pair 对象转换为列表：
```kotlin
val pair = Pair("marks", listOf(8.0, 9.0, 10.0))
println(pair.toList()) // [marks, [8.0, 9.0, 10.0]]
```

此外，我们可以使用 **copy()** 方法复制 Pair 对象，并使用参数名称（例如 first 和 second）更改其属性： `myCopy = pair.copy(first = "new Value", second = 3)`

```kotlin
val pair = Pair("marks", listOf(8.0, 9.0, 10.0))
val other = pair.copy()
println(pair) // (marks, [8.0, 9.0, 10.0])
println(other) // (marks, [8.0, 9.0, 10.0])
```

使用 `copy()` 方法，您可以基于另一个 \`Pair\` 对象创建一个新的 \`Pair\` 对象，或者修改其某些属性。您必须保持属性的顺序。请记住：\`Pair\` 对象的属性是不可变的，并且是只读的。您必须创建一个新的 \`Pair\` 对象来修改其值，或者使用 `copy` 函数创建一个新的 \`Pair\` 对象，并根据之前的对象为其赋值。

```kotlin
val pair = Pair("marks", listOf(8.0, 9.0, 10.0))
val other = pair.copy("other")
val grades = pair.copy(second = listOf(9.0, 7.0, 8.5))
val myCopy = pair.copy(first = "other", second = listOf(1.0, 2.0, 3.0))
println(pair) // (marks, [8.0, 9.0, 10.0])
println(other) // (other, [8.0, 9.0, 10.0])
println(grades) // (marks, [9.0, 7.0, 8.5])
println(myCopy) // (other, [1.0, 2.0, 3.0])
```

## 三倍

Triple 和 Pair 一样，是 Kotlin 中一个简单的数据类型，它表示单个实例中相同或不同类型的三个值。  
与 Pair 的情况类似，Tripleobject 的每个属性的类型也可以从上下文中推导出来。

```kotlin
val triple = Triple(1, "A", true)
println(triple)
```

## 如何使用 Triple

为了处理这些值，我们可以使用 **第一** 、 **第二** 和 **第三** 属性，或者使用 **componentN** 方法来提取值 `componentN` 中的 N 值表示组件的编号；例如， `component1` 表示三元组的第一个属性或值。

```kotlin
val triple = Triple(1, "I am", "Triple")

// Properties
println(triple.first) // 1
println(triple.second) // I am
println(triple.third) // Triple

// Methods
println(triple.component1()) // 1
println(triple.component2()) // I am
println(triple.component3()) // Triple
```

与 Pair 类型一样，我们也有两个特殊方法 **——toString()** 和 **toList()** ：

- **toString()** 返回 Triple 的字符串表示形式，包括其第一个、第二个和第三个值：
```kotlin
val triple = Triple("marks", "Kotlin", listOf(8.0, 9.0, 10.0))
println(triple) // (marks, Kotlin, [8.0, 9.0, 10.0])
```
- **toList()** 将 Triple 转换为列表：
```kotlin
val triple = Triple("marks", "Kotlin", listOf(8.0, 9.0, 10.0))
println(triple.toList()) //[marks, Kotlin, [8.0, 9.0, 10.0]]
```

最后，我们可以使用 **copy()** 方法来复制 Triple 对象：

```kotlin
val triple = Triple("marks", "Kotlin", listOf(8.0, 9.0, 10.0))
val other = triple.copy()
println(triple) // (marks, Kotlin, [8.0, 9.0, 10.0])
println(other) // (marks, Kotlin, [8.0, 9.0, 10.0])
```

与 Pair 类似，使用 `copy()` 方法，您可以基于另一个 Triple 创建一个新的 Triple，或者更改其某些属性。您必须保持属性的顺序。请记住：Triple 的属性是不可变的，并且是只读的。您必须创建一个新的 Triple 来更改其值，或者使用 `copy` 函数创建一个新的 Triple，并根据先前的对象为其分配所需的值。

```kotlin
val triple = Triple("marks", "Kotlin", listOf(8.0, 9.0, 10.0))
val other = triple.copy("other", third=listOf(7.0, 9.0, 8.5))
val course = triple.copy(second = "Kotlin Triple")
println(triple) // (marks, Kotlin, [8.0, 9.0, 10.0])
println(other) // (other, Kotlin, [7.0, 9.0, 8.5])
println(course) // (marks, Kotlin Triple, [8.0, 9.0, 10.0])
```

## 结论

现在您已经了解如何在 Kotlin 中轻松返回两个或三个值。请记住，Pair 和 Triple 中的值可以是不同类型的，并且您可以通过它们的属性轻松访问这些值。现在，您可以使用 Pair 和 Triple 来优化您的代码，而无需定义包装类来绕过函数只能返回一个值的限制。准备好回答问题和完成练习了吗？开始吧！

82 名学员喜欢这篇理论文章， 2 名学员不喜欢。 **你呢？**

报告拼写错误

### 相关主题[列表](https://hyperskill.org/learn/step/10730)

## 相关条目
- [[Kotlin基础语法梳理]]
