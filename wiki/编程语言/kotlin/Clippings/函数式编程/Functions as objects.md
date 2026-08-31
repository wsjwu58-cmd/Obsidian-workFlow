提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

我们知道如何声明函数、如何调用函数以及函数的作用。实际上，Kotlin 提供了一种像操作对象一样操作函数的方法。那么，让我们来学习如何将函数存储为对象以及如何使用它。

## 一等公民

在编程中，是以下对象：

1. 可以存储为变量，
2. 可以由函数返回，
3. 可以作为参数传递给函数，
4. 不要依赖他们的名声，
5. 可以在程序 **运行时** （程序正在运行时）创建。

例如，在 Kotlin 中， `Int` 类型是一等公民。为了阐明第四个要求，名为 `ten` 的 `Int` 变量并不一定实际值为 `10` 反之亦然：值为 `10` 变量也不一定必须存储在名为 `ten` 变量名下。您可以根据需要为同一个值创建任意多个不同名称的变量，而变量名的改变不会影响其值。

事实上，在 Kotlin 语言中，函数也是 **一等公民** 。让我们来证明这一点！在本主题中，我们将只介绍前四个要求。下一主题将讨论如何在运行时创建函数。

## 功能类型

首先，Kotlin 内置了对的支持。函数类型的如下：

```
(parameters' types) -> return value type
```

函数类型 **中间** 有 **箭头符号** （ -> ）， **左侧** 是 **用逗号分隔的带括号的参数类型** ， **右侧** 是 **返回值类型。因此，箭头似乎指向函数的输入和返回值** 。

让我们回顾一下前面章节中的一些函数，并用它们作为例子：

```kotlin
fun sum(a: Int, b: Int): Int = a + b
```

`sum` 的类型为 `(Int, Int) -> Int` 。

```kotlin
fun sayHello() {
    println("Hello")
}
```

`sayHello` 类型为 `() -> Unit` （此函数不接受任何参数，因此带有参数类型的括号为空，并且它不返回任何值，因此结果类型为 `Unit` ）。

## 函数引用作为对象

此外，Kotlin 允许获取 **函数引用** 。要获取引用，只需在其名称前加上双冒号 ( `::`:)，名称后无需添加括号和参数。例如 `::sum` 会返回一个 `(Int, Int) -> Int` 类型的对象。

现在我们可以将

```kotlin
val sumObject = ::sum
```

不要将此赋值与将函数结果保存为类似这样的值混淆： `val sumResult = sum(1, 2)` 。\`sumResult\` `sumResult` 值是 `Int` 类型，因为调用的 `sum` 函数的 **结果** 只是一个数字 。而 `sumObject` 值是用对 `sum` 函数的引用（ `::sum` ）初始化的，因此它的类型与 `sum` 函数的类型相同。

我们还可以显式指定 `sumObject` 值的类型：

```kotlin
val sumObject: (Int, Int) -> Int = ::sum
```

在这两种情况下，我们都有机会通过 **调用对象** 来调用原始 `sum` 函数： `sumObject(10, 20)` 返回 30 就像我们直接使用这些参数调用原始函数一样。

## 返回其他函数的函数

既然函数可以存储为对象，为什么不创建一个返回此类对象的函数呢？让我们来试试。请看下面的示例：

```kotlin
fun getRealGrade(x: Double) = x
fun getGradeWithPenalty(x: Double) = x - 1

fun getScoringFunction(isCheater: Boolean): (Double) -> Double {
    if (isCheater) {
        return ::getGradeWithPenalty
    }

    return ::getRealGrade
}
```

这里我们有一个实际的评分函数，它返回参数值；还有一个带惩罚的评分函数，它返回参数值减一（换句话说，就是参数值的 **减一** ）。此外，我们还有一个函数，它可以返回前两个函数中的一个。

因此，如果我们执行 `val wantedFunction = getScoringFunction(false)` ，则 \` `wantedFunction` 值将包含对诚实学生成绩函数的引用。查看 `getScoringFunction` 函数的实现，我们可以说，在这种情况下，\` `wantedFunction` 值包含对 \` `getRealGrade` 函数的引用。因此， `wantedFunction(9.0)` \` 的结果将等于 `9.0` 。

## 函数引用作为函数参数

此外，你还可以创建以其他 **函数作为参数的** 函数。让我们来创建这样一个函数：

```kotlin
fun applyAndSum(a: Int, b: Int, transformation: (Int) -> Int): Int {
    return transformation(a) + transformation(b)
}
```

它接收两个整数，使用给定的转换函数对它们进行转换，并返回转换后整数的和。我们可以声明一些转换函数：

```kotlin
fun same(x: Int) = x
fun square(x: Int) = x * x
fun triple(x: Int) = 3 * x
```

然后将它们传递给之前的函数：

```kotlin
applyAndSum(1, 2, ::same)    // returns 3 = 1 + 2
applyAndSum(1, 2, ::square)  // returns 5 = 1 * 1 + 2 * 2
applyAndSum(1, 2, ::triple)  // returns 9 = 3 * 1 + 3 * 2
```

## 实际应用

前面的例子似乎有点人为设定。那么，有没有更贴近现实的例子呢？嗯，你自己看看吧。

`String` 类型有一个用于过滤符号的 `filter` 方法。它是如何知道要从字符串中删除哪些符号，保留哪些符号的呢？答案很简单：这个方法接受一个 **谓词** 作为参数，然后用它来进行内部计算。谓词是一个接受参数并返回 `Boolean` 函数。因此，在 `filter` 方法中，谓词指示是否应该保留某个符号，其类型为 `(Char) -> Boolean` 。

我们来尝试使用这种方法。如果要从字符串中删除点号，我们可以声明以下谓词：

```kotlin
fun isNotDot(c: Char): Boolean = c != '.'
```

然后我们可以这样做：

```kotlin
val originalText = "I don't know... what to say..."
val textWithoutDots = originalText.filter(::isNotDot)
```

因此， `textWithoutDots` 字符串等于 `"I don't know what to say"` 。

## 结论

这就是这一庞大编程范式的基础。有了函数对象，我们就可以创建接收其他函数作为参数的函数。这种范式在 **Kotlin** 中被广泛应用。我们讨论了一些例子，但你肯定会在后续主题中找到更多。

620 名学员喜欢这篇理论文章， 65 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
