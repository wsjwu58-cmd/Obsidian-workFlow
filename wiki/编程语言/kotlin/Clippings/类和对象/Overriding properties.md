提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

属性重写是 Kotlin 的一项重要特性。它允许我们在子类中修改已定义的属性的行为。这意味着我们可以在中定义一个属性，然后在派生类中重写它。就像在面向对象编程中继承和扩展方法一样，我们也可以在 Kotlin 中扩展属性。

## 属性和方法重写的基础知识

在 Kotlin 中，属性（property）取代了我们通常在其他语言（例如 Java）中看到的字段（field）。属性提供了一种机制，可以将数据封装在对象中，并控制如何访问和操作这些数据。属性重写允许我们更改派生类中属性的行为或值，从而提供新的灵活性。，如果 `Vehicle` 类中有一个 `speed` 属性，我们可以在 `Car` 类中重写它，使其具有特定的值。

`override` 关键字用于在子类中重写属性和方法。在 Kotlin 中，属性和方法的运作方式不同。方法是执行特定操作的函数，而属性则代表数据。这种区别至关重要，因为方法通常包含逻辑，而属性包含状态或数据。在我们的 `Vehicle` 和 `Car` 示例中， `accelerate()` 方法可以提高速度，而 `speed` 本身则是一个属性。

## 实践中的属性优先权

让我们深入研究一些代码，以演示覆盖是如何工作的：

```kotlin
open class Vehicle {
    open val speed: Int = 0
}

class Car: Vehicle() {
    override val speed: Int = 60
}

fun main() {
    val car = Car()
    println(car.speed) // Output: 60
}
```

在上面的例子中，我们在基类 `Vehicle` 中定义了一个 `speed` 属性，然后在子类 `Car` 中重写了该属性。这意味着所有 `Car` 对象的默认 `speed` 都为 60，这与通用的 `Vehicle` 不同，后者的 `speed` 默认为 0。

## 使用 getter 和 setter 覆盖属性

在 Kotlin 中，属性自带 getter 和 setter 函数。这些函数控制属性的访问和修改方式。重写属性时，我们也可以修改 getter 和 setter 函数。

例如：

```kotlin
open class Vehicle {
    open val speed: Int 
        get() = 0
}

class Car: Vehicle() {
    override val speed: Int 
        get() = 60
}
```

在这个例子中，我们不仅重写了属性，还重写了 `speed` 属性的 getter 方法。无论对属性进行任何修改，每次访问 `Car` 对象的 `speed` 时，它始终返回 60。

## 重写抽象属性

抽象属性略有不同。它们在中声明，没有初始化器，并且必须在任何非抽象子类中重写。

```kotlin
abstract class Vehicle {
    abstract val speed: Int
}

class Car: Vehicle() {
    override val speed: Int = 60
}
```

在这种情况下， `Vehicle` 并未指定任何速度：每种特定类型的 `Vehicle` 都必须定义自己的 `speed` 。 `Car` 通过将 `speed` 设置为 60 来实现这一点。

## 结论

总之，属性重写是 Kotlin 中一个强大的工具，它使我们能够创建更灵活、更易复用的代码。它增强了继承的原则，允许我们不仅扩展方法，还可以扩展属性。现在是练习时间，开始吧！

32 名学员喜欢这部分理论内容， 2 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
