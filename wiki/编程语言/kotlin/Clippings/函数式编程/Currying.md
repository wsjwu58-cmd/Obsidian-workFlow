提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

柯里化是 Kotlin 中一个非常棒的概念。它允许你将一个带有多个参数的函数转换成一系列只带有一个参数的函数。本文将深入探讨柯里化的细节，全面阐述其应用、优势和实际应用案例。

## 理解

本质上， **柯里化** 是函数式编程中的一种技巧，它将一个具有多个参数的函数转换成一系列只有一个参数的函数。换句话说，它将一个接受多个参数的函数分解成一系列只接受一个参数的函数。让我们通过一个例子来理解柯里化的基本概念：

```kotlin
fun  ((T1, T2) -> R).curried() = 
    fun(p1: T1) = fun(p2: T2) = this(p1, p2)
```

在这个例子中，我们创建了一个柯里化函数。函数 `curried()` 接受一个带有两个参数的函数，并返回一个接受一个参数的函数，该函数再返回另一个也接受一个参数的函数。与一次性接收所有参数不同，该函数先接收第一个参数，然后返回一个接收第二个参数的新函数。

## 申请

为了理解柯里化如何应用，考虑一个计算商品享受特定折扣后总价的函数。该函数接受两个参数：原价和折扣率。

```kotlin
fun calculateTotalPrice(price: Double, discount: Double): Double {
    return price - (price * discount / 100)
}
```

我们可以使用柯里化技术将此函数转换为一系列函数，每个函数接受一个参数。

```kotlin
fun calculateTotalPrice(price: Double): (Double) -> Double {
    return { discount -> price - (price * discount / 100) }
}
```

现在，我们可以创建一个针对特定折扣率的新函数。这个新函数以原价为参数，并返回折扣后的价格。

```kotlin
val calculateWith30PercentOff = calculateTotalPrice(100.0)
println(calculateWith30PercentOff(30.0))  // Output: 70.0
```

在这个例子中， `calculateWith30PercentOff` 是一个由柯里化函数 `calculateTotalPrice` 创建的新函数。它以原始价格作为参数，并应用 30% 的折扣。

## 咖喱烹饪实战

现在让我们来看一个更复杂的例子，以了解柯里化如何在实际应用中使用。假设我们正在开发一个快递服务软件，其中有一个函数可以根据包裹的重量、到目的地的距离以及配送类型（标准或快递）来计算配送费用。

```kotlin
fun calculateDeliveryCost(weight: Double, distance: Double, type: String): Double {
    val baseCost = if (type == "standard") 5.0 else 10.0
    val weightCost = weight * 0.5
    val distanceCost = distance * 0.3
    return baseCost + weightCost + distanceCost
}
```

这个函数运行良好，但可以通过柯里化进行改进。我们可以对这个函数进行柯里化，从而为特定的重量、距离和配送方式创建新的函数。

```kotlin
fun calculateDeliveryCost(weight: Double): (Double) -> (String) -> Double {
    return { distance -> { type -> 
        val baseCost = if (type == "standard") 5.0 else 10.0
        val weightCost = weight * 0.5
        val distanceCost = distance * 0.3
        baseCost + weightCost + distanceCost
    }}
}
```

现在，我们可以为特定的重量和距离创建新的函数。例如，我们可以创建一个函数，用于处理一个重10公斤、需要运送50公里的包裹。

```kotlin
val calculateFor10KgAnd50Km = calculateDeliveryCost(10.0)(50.0)
println(calculateFor10KgAnd50Km("standard")) // Output: 25.0
println(calculateFor10KgAnd50Km("express"))  // Output: 30.0
```

这样，我们可以针对不同的场景创建特定的功能，使我们的代码更加模块化和可重用。

## 深度探索

柯里化提供了几个可以显著提升 Kotlin 代码质量的优势：

- **代码重用性** ：柯里化允许你从现有函数创建新函数，并预先填充一些参数。这有助于提高代码重用性。你可以从一个通用函数生成任意数量的特定函数，每个函数都针对特定的用例进行定制。
- **延迟计算** ：柯里化允许你延迟计算。你可以创建一个带有部分参数的函数，然后稍后使用剩余的参数执行它。这在计算成本高昂且需要将其分散到一段时间内执行的场景中尤其有用。
- ：柯里化允许你创建高阶函数。它允许你将函数作为参数传递，并将其作为结果返回。高阶函数是函数式编程的基石，而柯里化提供了一种创建它们的直接方法。
- **函数组合** ：柯里化可以简化函数组合。这种技术可以将简单的函数组合起来，构建更复杂的函数。通过柯里化，您可以轻松地组合函数，从而提高代码的可读性和可维护性。

## 结论

**柯里化** 是函数式编程中一项强大的技术，在 Kotlin 中也能派上用场。它允许你将一个带有多个参数的函数转换成一系列只有一个参数的函数。这可以提高代码的复用性，实现延迟计算，简化函数组合，并允许创建高阶函数。需要记住的关键概念是，柯里化后的函数会为每个参数返回一个新函数，从而实现灵活的编程模式。深入理解柯里化，你就能编写出更模块化、更易复用、更易于维护的 Kotlin 代码。

24 名学员喜欢这部分理论， 9 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
