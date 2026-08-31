提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

你已经知道如何使用。但是，它们也有局限性。例如，你可能需要为同一个类创建多个不同的构造函数，但仅靠一个主构造函数是无法实现的。这时，辅助构造函数或自定义构造函数就派上用场了。

## 自定义构造函数

你可以为类声明函数，也可以声明主构造函数，或者不声明主构造函数。

要声明，请在类体内部写入关键字 \` `constructor` ，并在关键字后用括号括起构造函数的参数。然后，将构造函数逻辑放在花括号内：

```kotlin
class Size {
    var width: Int = 0
    var height: Int = 0

    constructor(_width: Int, _height: Int) {
        width = _width
        height = _height
    }
}
```

现在你可以用一行代码创建对象，就像使用主构造函数一样：

```kotlin
val size1 = Size(3, 4)
val size2 = Size(5, 1)
```

注意：您必须使用隐式构造函数或声明自己的构造函数，但不能同时使用两者：

```kotlin
class Size {
    var width: Int = 0
    var height: Int = 0

    constructor(_width: Int, _height: Int) {
        width = _width
        height = _height
    }
}

val size = Size() // Error! No values passed for parameters _width and _height
```

你可以显式地创建一个的副本（可以删除空的花括号）：

```kotlin
// preferable solution
class Size() { 
    var width: Int = 0
    var height: Int = 0
}

// or this way

class Size {
    var width: Int = 0
    var height: Int = 0

    constructor() {
    }
}
```

## 多个构造函数

为一个类创建多个构造函数几乎和创建单个构造函数一样简单，但需要注意一个特殊的限制：每个辅助构造函数都必须具有唯一的签名。您不能将相同的签名用于主构造函数或任何其他构造函数。

构造函数签名由参数的数量、类型和顺序组成。要创建一个有效的构造函数，需要确保它具有唯一的参数列表。例如，请查看 `Size` 类的以下构造函数：

```kotlin
class Size {
    var width: Int = 0
    var height: Int = 0

    constructor(_height: Int) {
        height = _height
    }

    constructor(_width: Int, _height: Int) {
        width = _width
        height = _height
    }

    constructor(_width: Int, _height: Double) {
        width = _width
        height = _height.toInt()
    }

    constructor(_height: Double, _width: Int) {
        width = _width
        height = _height.toInt()
    }
}
```

以下代码将使用不同的构造函数创建四个具有相同属性值的 `Size` 对象：

```kotlin
val size1 = Size(7) // uses 1st constructor
val size2 = Size(0,7) // uses 2nd constructor
val size3 = Size(0, 7.0) // uses 3rd constructor
val size4 = Size(7.0, 0) // uses 4th constructor
```

请记住，构造函数签名是由参数的类型定义的，而不是由参数的名称定义的。例如，即使这两个构造函数看起来不一样，编译器也无法区分它们：

```kotlin
constructor(width: Int, height: Int) {}
constructor(x: Int, y: Int) {}
```

因此，如果在同一个类中实现这些构造函数，将会引发错误。

## this 关键词

在类代码中，您还可以使用表示当前对象的特殊关键字 `this` 来访问对象成员。

例如，你可以使用它将构造函数参数命名为与类属性相同的名称。让我们修改类 `Size` ：

```kotlin
class Size {
    var width: Int = 0
    var height: Int = 0

    constructor(width: Int, height: Int) {
        this.width = width
        this.height = height
    }
}
```

在上面的代码中，如果没有 `this` ，将会报错，因为名称将被解释为构造函数参数，而不是类成员。

## 省略默认值

如你所记得，如果在构造函数中为属性值赋值，则无需提供：

```kotlin
class Size (var width: Int, var height: Int) {
    // whatever you want
}
```

对于辅助构造函数也是如此。让我们将 `Size` 类中的 `var` 改为 `val` ，这样属性就无法被重新赋值。为了演示，我们再添加一个属性 `area` ，它将根据构造函数参数进行计算：

```kotlin
class Size {
    val width: Int
    val height: Int
    val area: Int

    constructor(width: Int, height: Int) {
        this.width = width
        this.height = height
        this.area = width * height
    }
}
```

看起来像是重新赋值，但你只是在初始化值，所以没有问题。

请注意，在辅助构造函数中不能使用 `val` 和 `var` 关键字。

```kotlin
class Size {
    constructor(val width: Int, val height: Int) { // error, val is not allowed
    }
}
```

## 构造函数委托

如果一个类有一个主构造函数，那么每个从构造函数都需要调用主构造函数，可以直接调用，也可以通过其他从构造函数间接调用。这称为 **委托** 。

要将构造函数委托给同一类的另一个构造函数，需要在构造函数参数之后、构造函数体之前使用关键字 `this` ：

```kotlin
class Size(val width: Int, val height: Int) {
    var area: Int = width * height

    constructor(width: Int, height: Int, outerSize: Size) : this(width, height) {
        outerSize.area -= this.area
        println("Updated outer object's area is equal to ${outerSize.area}")
    }
}
```

委托给主构造函数会成为辅助构造函数的第一条语句，因此属性会在辅助构造函数代码执行之前初始化。如果存在初始化块，它们也会在辅助构造函数之前执行。如果类没有主构造函数，则委托会隐式发生。

## 构造函数执行

让我们来看一个例子，看看类代码是按什么顺序执行的：

```kotlin
class Size(val width: Int, val height: Int) {
    var area: Int = width * height

    init {
        println("Object with area equal to $area is created")
    }

    constructor(width: Int, height: Int, outerSize: Size) : this(width, height) {
        outerSize.area -= this.area
        println("Updated outer object's area is equal to ${outerSize.area}")
    }
}

fun main() {
    val outerObject = Size(5, 8)
    val innerObject = Size(2, 3, outerObject)
}
```

创建 `outerObject` 时，直接调用主构造函数，初始化属性并执行 `init` 块。创建 `innerObject` 时，先调用次要构造函数，进行属性初始化并执行初始化代码块，最后执行次要构造函数的代码。

结果如下：

```
Object with area equal to 40 is created
Object with area equal to 6 is created
Updated outer object's area is equal to 34
```

## 结论

在开始练习之前，让我们先回顾一下本主题的要点。

- 类还可以声明辅助构造函数。它们必须以关键字 `constructor` 为前缀。
- 同一个类中的每个构造函数都必须具有唯一的签名。
- 可以使用 `this` 关键字访问类代码中的对象成员。
- 如果在构造函数中已为属性值赋值，则可以省略默认值。
- 中的代码实际上成为了主构造函数的一部分。
- 次要构造函数代码在主构造函数、初始化块和属性初始化之后执行。

357 名学习者喜欢这篇理论文章， 35 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
