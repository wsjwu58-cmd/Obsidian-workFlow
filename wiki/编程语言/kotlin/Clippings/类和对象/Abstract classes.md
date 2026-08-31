提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

假设你想创建一个动物园的模拟程序。你已经构思了各种不同的动物物种，现在你想定义它们的行为。你希望你的动物能够进食、睡觉、发出声音和四处走动。所有动物都应该能够做到这些，但它们具体如何做应该取决于它们的物种。

实际上，这意味着你需要为每种动物创建一个类，并定义相应的方法。为了简化和规范化这个过程，你应该使用。在本主题中，我们将讨论什么是抽象类以及如何在代码中使用它们。

## 理解抽象类

**抽象类** 就像一张蓝图，可以用来创建其他类。我们并不直接使用蓝图，而是基于蓝图创建新对象，并对这些对象进行操作。

让我们回到动物园的例子。你可以创建一个抽象类 `Animal` ，它定义了所有动物的共同行为，例如进食和睡觉。这个类还会包含发出声音和移动的抽象方法，因为不同的动物会发出不同的声音，以不同的方式移动。创建好 `Animal` 类之后，你可以用它来创建特定动物的子类，例如 `Cat` 和 `Dog` ，这些子类会提供各自对这些抽象方法的实现。

通过这种方式使用抽象类，您可以确保所有子类都具有一致的接口并共享共同的行为，同时允许它们拥有各自独特的行为。这可以使您的代码更易于 **组织** 、 **重用** 和 **维护** 。

总而言之，抽象类是不能直接实例化的类，但它可以作为其他类的蓝图。它就像一个部分实现的类，提供了一种子类可以继承和构建的通用结构和行为。

## 宣言

在 Kotlin 中，抽象类是在类声明中使用 `abstract` 来声明的。

```kotlin
abstract class Animal
```

与其他类一样，抽象类也可以有构造函数。这些构造函数用于初始化类的属性，并有助于确保子类满足某些要求或具有初始值。

```kotlin
abstract class Animal(val id: Int)
```

抽象类可以同时包含抽象成员和非抽象成员（属性和方法）。要将成员声明为抽象成员，必须显式使用 `abstract` 关键字。请注意，抽象成员在其类中没有实现对象（实现）。

```kotlin
abstract class Animal(val id: Int) {
    val name: String // We get here a compile-time error: property must be initialized or be abstract
    
    abstract fun makeSound()

    fun isSleeping(): Boolean {
        ...
        return false
    }
}
```

在这个例子中，类 `Animal` 使用 `abstract` 声明为抽象类 。它包含一个没有初始化器的成员属性，因此该属性必须是抽象的，否则会报错。此外，该类还有两个：第一个是抽象函数 `makeSound()` ，它没有实现；第二个是非抽象函数 `isSleeping()` ，它提供了一个可供子类继承的通用实现。

如果在创建抽象类之后，我们尝试创建它的对象，将会得到一个编译时错误：我们不能创建抽象类的实例。

> [!primary] Primary
> 默认情况下，Kotlin 中的抽象类可以 `open` 扩展，它们的抽象方法和属性可以被重写。

## 执行

当一个类继承一个抽象类时，它必须为抽象类中声明的所有抽象成员提供实现。

```kotlin
abstract class Animal {
    abstract fun move()
    abstract fun makeSound()

    fun eat(): Boolean = false
    fun sleep(): Boolean = false
}

class Cat : Animal() {
    override fun move() {
        // Implementation specific to how the cat moves
    }

    override fun makeSound() {
        // Implementation specific to what sound the cat makes
    }
}
```

在这个例子中，类 `Cat` 继承自抽象类 `Animal` 。它必须重写并提供 `Animal` 类中声明的 `move()` 和 `makeSound()` 函数的具体实现。这样可以确保每个子类都提供其自身对这些抽象方法的实现。

我们不能直接创建抽象类的对象，但我们可以创建抽象类类型的引用，并将具体子类的对象赋值给这些引用。例如：

```kotlin
val cat: Animal = Cat()
cat.move()
cat.makeSound()
```

## 遗产

抽象类也可以作为其他抽象类的。在这种情况下，子类负责实现从父类及其直接抽象父类继承的所有抽象方法。

```kotlin
abstract class Animal {
    abstract fun makeSound()
}

abstract class Mammal : Animal() {
    abstract fun eat()
}

class Cat : Mammal() {
    override fun makeSound() {
        println("Meow!")
    }

    override fun eat() {
        println("The cat is eating.")
    }
}
```

在这个例子中， `Animal` 类是一个抽象类，它包含抽象函数 `makeSound()` 。 `Mammal` 类继承自 `Animal` ，并添加了一个额外的抽象函数 `eat()` 。 `Cat` 类则继承自 `Mammal` ，并实现了 `makeSound()` 和 `eat()` 函数。

通过这种方式使用抽象类，我们可以建立一个层级结构，其中每一层都提供更专业化的行为。在上述例子中， `Mammal` 继承自 `Animal` ，添加了哺乳动物特有的行为；而 `Cat` 进一步继承自 `Mammal` ，定义了猫科动物特有的行为。

在 Kotlin 中，也可以使用两个关键字将非抽象的 `open` 成员重写为抽象成员，从而使抽象类继承自开放类： `abstract override` 。

```kotlin
open class Polygon {
    open fun draw() {
        // Some default polygon drawing method
    }
}

abstract class WildShape : Polygon() {
    // Classes that inherit WildShape need to provide their own draw method instead of using the default on Polygon
    abstract override fun draw()
}
```

## 抽象类与接口

面向对象编程中常见的问题之一是抽象类和接口之间的区别。在 Kotlin 中，这两个概念都用于定义类可以实现或继承的契约或行为。然而，它们之间存在一些关键差异，这些差异会影响它们的使用和设计方式。

|  | 抽象类 | 接口 |
| --- | --- | --- |
| 实例化 | 它们不能直接实例化。它们的作用是作为子类继承的基类。 | 它们不能直接实例化。它们定义了方法和属性的契约，实现类必须遵守这些契约。 |
| 构造函数 | 它们可以拥有构造函数，包括主构造函数和辅助构造函数。子类负责调用相应的父类构造函数。 | 它们不能有构造函数。它们只声明方法和属性，没有任何实现。 |
| 状态 | 它们可以拥有成员变量和非抽象方法，并具有。它们还可以保存状态和维护内部数据。 | 它们不能保存状态或定义成员变量，它们纯粹用于声明行为。 |
| 遗产 | 子类只能继承一个抽象类。在 Kotlin 中，类继承仅限于单个类，而抽象类提供了一种建立继承层次结构的方法。 | 实现类可以实现多个接口。Kotlin 支持通过接口进行多重继承，允许类同时实现多个接口。 |
| 摘要成员和非摘要成员 | 它们可以同时拥有抽象方法和属性以及非抽象方法和属性。子类必须为抽象成员提供实现，同时继承非抽象成员。 | 它们可以声明抽象方法或具有默认实现的方法。这两种类型的方法都可以由实现类进行重写。 |

在抽象类和接口之间进行选择时，请考虑以下准则：

- 当您需要提供默认实现或需要在基类中维护内部状态时，请使用抽象类。
- 当您想要定义多个不相关类可以实现的行为契约，或者需要实现多重继承时，请使用接口。

## 结合使用抽象类和接口

在 Kotlin 中，可以结合使用抽象类和接口来创建更灵活的类层次结构。这种方法允许你通过接口引入公共成员并定义契约，从而提供一个通用且可扩展的结构。具体类可以继承抽象类，并根据需要实现其他接口。

让我们来看一个简单的例子来理解这个概念：

```kotlin
interface Shape {
    fun calculateArea(): Double
    fun calculatePerimeter(): Double
}

abstract class AbstractShape : Shape {
    // Common behavior or properties for shapes can be implemented here
}

class Rectangle(private val width: Double, private val height: Double) : AbstractShape() {
    override fun calculateArea(): Double {
        return width * height
    }

    override fun calculatePerimeter(): Double {
        return 2 * (width + height)
    }
}

class Circle(private val radius: Double) : AbstractShape() {
    override fun calculateArea(): Double {
        return Math.PI * radius * radius
    }

    override fun calculatePerimeter(): Double {
        return 2 * Math.PI * radius
    }
}
```

在这个例子中，我们有一个名为 `Shape` 接口，它包含两个方法： `calculateArea()` 和 `calculatePerimeter()` 。抽象类 `AbstractShape` 实现了 `Shape` 接口，为不同的形状提供了一个通用的基础。然后，我们有两个具体类 `Rectangle` 和 `Circle` ，它们继承自 `AbstractShape` ，并分别实现了各自形状的面积和周长计算方法。

通过同时使用抽象类和接口，你的代码会变得更加灵活。抽象类可以封装通用行为和状态，而接口则为实现类建立契约。这种组合使你能够设计出易于维护、可扩展且符合良好面向对象原则的类层次结构。

## 最佳实践

在使用抽象类时，需要牢记一些最佳实践：

- 使用抽象类来定义 **通用** 接口和行为。抽象类是为相关类定义通用接口和行为的有效工具。使用抽象类可以封装通用功能，并为子类提供一致的结构。
- **避免过度使用** 抽象类。虽然抽象类很有用，但切记不要过度使用。只有当相关类之间确实需要通用接口和行为时，才应使用抽象类。否则，请考虑使用接口或组合。
- 设计时要考虑 **可扩展性** 。设计抽象类时，要考虑它们未来可能如何扩展。确保类层次结构足够灵活，能够容纳新的子类而无需进行重大更改。
- 提供 **清晰的文档** 。抽象类可能很复杂，因此为使用或扩展它们的开发人员提供清晰的文档至关重要。务必记录类的用途、方法以及使用上的任何要求或限制。
- 考虑将接口与抽象类 **结合** 使用。抽象类和接口可以共同构建更灵活的类层次结构。可以考虑使用接口来定义行为契约，同时使用抽象类来提供通用实现并维护状态。

## 结论

让我们总结一下你在这个主题中学到的内容：

- 抽象类使用 `abstract` 关键字声明。
- 抽象类不能直接实例化。
- 抽象类的子类必须提供所有抽象方法的实现。
- 抽象类可以拥有具有通用实现的非抽象方法。
- 抽象类可以作为其他抽象类的基础，从而创建继承层次结构。
- 抽象类可以提高代码重用性，并强制相关类之间保持一致的结构。
- 抽象类可以实现接口，从而结合继承的共享行为和接口定义的契约。

还要记住，抽象知识是通过实践转化为具体技能的。所以，你还在等什么？让我们一起解决问题吧！

42 名学员喜欢这部分理论内容， 3 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
