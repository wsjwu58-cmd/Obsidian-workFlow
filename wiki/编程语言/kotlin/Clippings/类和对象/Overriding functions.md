提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

和其他 **面向对象编程** 语言一样，Kotlin 也支持 **继承** 。它在一个非常实用的功能中得以实现：。想知道它的作用吗？让我们一起来看看！

## 覆盖它

当然，我们需要一个合适的类示例。让我们创建一个名为 `Transport` 类，并为其添加 `cost` 属性：

```kotlin
open class Transport(val cost: Int) {
    fun getFullInfo(): String {
        return "$$cost cost"
    }
}
```

这是一个很典型的可供扩展的类，对吧？请记住它是 `open` 。但现在我们要将 `getFullInfo()` \` 函数也标记为 `open` ，并添加一个不带 `open` 修饰符的函数：

```kotlin
open class Transport(val cost: Int) {
    open fun getFullInfo(): String {
        return "$$cost cost"
    }

    fun getTax(): String {
        return "$${(cost * 0.25).roundToInt()} tax"
    }
}
```

现在我们可以为 `Transport` 类添加自己的 `getFullInfo()` 函数了：

```kotlin
open class Ship(cost: Int, val color: String) : Transport(cost) {
    override fun getFullInfo(): String {
        return super.getFullInfo() + ", $color color"
    }
}
```

Kotlin 中，默认情况下任何被重写的函数都是 **开放的** 。这意味着你也可以在子类中重写函数。此外，如果你想调用父函数，可以使用 `super` ，就像我们在上面的例子中所做的那样。还有两点：

1. 如果你忘记使用 `override` ，编译器会发出警告，因为不能有两个具有相同参数的 `getFullInfo()` 函数。
2. 您也无法重写 `getTax()` 函数，因为它没有被 `open` 。

这两种情况下，源代码都无法编译。让我们在下一个示例中检查一下我们新创建的类：

```kotlin
fun main() {
    val transport = Transport(1000)
    val ship = Ship(2000, "marine")
    println(transport.getFullInfo())
    println(ship.getFullInfo())
}
```

输出结果应如下：

```kotlin
$1000 cost
$2000 cost, marine color
```

## 重复使用

关于 `open` 函数，还有一个很有用的特性。我们将通过以下函数来观察它：

```kotlin
fun getTransportInfo(transport: Transport): String {
    return "transport info: " + transport.getFullInfo()
}
```

如您所见，它可以处理 `Transport` 类。此外，它还可以轻松处理该类的任何子类：

```kotlin
fun main() {
    val transport = Transport(1000)
    val ship = Ship(2000, "marine")
    println(getTransportInfo(transport))
    println(getTransportInfo(ship))
}
```

输出结果如下：

```kotlin
transport info: $1000 cost
transport info: $2000 cost, marine color
```

瞧！ `getTransportInfo()` 函数可以很好地与 `Transport` 类及其子类的任何已打开函数一起使用。这就是 Kotlin 继承的真正强大之处！

## 结论

现在你了解了 Kotlin 中继承的另一个概念。它允许我们构建更灵活的类层次结构。你可以控制何时使用的函数，何时创建自己的函数。接下来，让我们开始练习，学习如何使用 **重写函数** 。

301 名学员喜欢这篇理论文章， 7 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
