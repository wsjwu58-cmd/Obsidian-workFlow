提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

你已经知道如何声明带有简单属性的简单类。现在让我们来学习另一种类：构造函数。

## 默认构造函数

**构造函数** 是类的成员，用于初始化类的新对象。换句话说，构造函数通过定义对象的属性来设置新对象的状态。因此，当你创建一个对象时，你实际上是在调用构造函数。

为了提供更多示例，我们使用 `Size` ：

```kotlin
class Size {
    var width: Int = 1
    var height: Int = 1
}
```

我们先回顾一下如何创建对象。我们写上类名，后面跟着一个空括号：

```kotlin
val size = Size()
```

这实际上是一个 **构造函数调用** ，就像调用一个不带参数的函数一样。每个类都需要一个构造函数，因此如果没有显式定义，编译器会自动生成一个不带参数的，该构造函数只创建一个对象，内部没有任何逻辑。

## 主要构造

通常情况下，你在创建对象之前就已经知道它的属性。为了使代码更简洁，你可以在构造函数中设置这些属性：只需让构造函数接收所需的参数即可。

**主构造函数** 是实现此目的的正确工具。它不包含任何代码，仅用于初始化类的实例及其属性。要定义主构造函数，应将类初始化参数放在类名后的括号内。

`Size` 的主构造函数如下所示：

```kotlin
class Size(width: Int, height: Int) {
    val width: Int = width
    val height: Int = height
    val area: Int = width * height
}
```

通常，要定义构造函数，应该在参数之前加上 `constructor` 的主构造函数允许省略该关键字。

总之，定义主构造函数的另一种合理方式如下所示：

```kotlin
class Size constructor(width: Int, height: Int) {
    val width: Int = width
    val height: Int = height
    val area: Int = width * height
}
```

## 财产申报

你可以 **在** 主构造函数中声明简单的属性 。要声明，请在参数名称前的括号中放入关键字 `val` 。对于可变属性，请使用关键字 `var` 。

例如，让我们将属性 `width` 从 中移出来：

```kotlin
class Size(val width: Int, height: Int) {
    val height: Int = height
    val area: Int = width * height
}
```

现在让我们把剩余的属性 `height` 放到主构造函数中：

```kotlin
class Size(val width: Int, val height: Int) {
    val area: Int = width * height
}
```

## 默认参数和命名参数

主构造函数中的默认值设置方式与类体中的设置方式相同。您可以使用关键字 `val` 或 `var` 声明属性，并将默认值放在赋值运算符之后：

```kotlin
class Size(var width: Int = 1, var height: Int = 1) {
    val area: Int = width * height
}
```

在主构造函数中创建具有类的对象时，可以通过省略参数来使用默认值：

```kotlin
val size = Size() // width == 1, height == 1
```

创建类的实例时，您可以直接提供值而不指定属性名称，也可以使用 **命名参数** ：

```kotlin
val size1 = Size(3, 5) // width == 3, height == 5
val size2 = Size(width = 3, height = 5) // width == 3, height == 5
val size3 = Size(height = 5, width = 3) // width == 3, height == 5
```

创建对象时，也可以省略一些具有默认值的属性。但请记住，如果在主构造函数中打破参数顺序，则应始终使用命名参数：

```kotlin
val sizeWide = Size(10) // width == 10, height == 1
val sizeHigh = Size(height = 10) // width == 1, height == 10
```

主构造函数是简洁定义类的一种便捷方式。如果您想避免冗余代码，请尽量使用主构造函数和默认参数。

## 单线类

如果除了主构造函数中的成员之外没有其他类成员，我们可以省略空的大括号。假设我们的示例中缺少 `area` 属性：

```kotlin
class Size(val width: Int, val height: Int)
```

在现实生活中，你经常会遇到这类类。例如， **数据类** ——主要用途是存储数据的类——就是这样定义的。你稍后会学习到它们。

## 初始化

主构造函数不能包含任何代码：它们只根据传入的参数设置类属性的值。有时，我们希望根据其他属性的值或其他信息来源来设置某些属性。在这种情况下，我们会使用，初始化块以关键字 \` `init` 为前缀：

```kotlin
class Size(_width: Int, _height: Int) {
    var width: Int = 0
    var height: Int = 0

    init {
        width = if (_width >= 0) _width else {
            println("Error, the width should be a non-negative value")
            0
        }
        height = if (_height >= 0) _height else {
            println("Error, the height should be a non-negative value")
            0
        }
    }
}
```

关键字 `init` 表示一段代码块，它作为主构造函数的扩展。例如，以下代码会在主构造函数中设置对象属性后打印一条消息：

```kotlin
class Size(val width: Int, val height: Int) {
    init {
        println("Initializer block that prints the width ($width) and the height ($height)")
    }
}
```

类体中可能包含多个初始化块。在这种情况下，属性初始化块和 `init` 块会按照它们出现的顺序执行：

```kotlin
class Size(_width: Int, _height: Int) {
    // 1: the width property is initialized
    val width = _width

    // 2: 1st init block is executed
    init {
        println("First initializer block that prints the width $width")
    }

    // 3: the height property is initialized
    val height = _height

    // 4: 2nd init block is executed
    init {
        println("Second initializer block that prints the height $height")
    }

    // 5: the area property is initialized
    val area = width * height
}
```

在上面的示例中，参数名称以下划线开头（ `_width` 、 `_height` ），以区别于类成员（ `width` 、 `height` ）。这是一种被多种编程语言广泛接受的实用编码约定。

## 结论

让我们回顾一下我们已经学到的关于构造函数的知识：

- 任何 Kotlin 类都有一个构造函数来初始化其对象。
- 如果类的构造函数没有显式定义，则会设置一个不带参数的隐式。该构造函数会创建一个对象，但不初始化其属性。
- 可以通过调用构造函数。
- 声明构造函数的方法有很多种，但主构造函数是最简洁的。
- 当需要在对象创建期间执行某些代码时，可以将初始化块与构造函数一起使用。

508 名学习者喜欢这篇理论文章， 27 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
