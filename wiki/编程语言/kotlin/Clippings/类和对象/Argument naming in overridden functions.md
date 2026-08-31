## 重写函数中的参数命名

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在本主题中，我们将探讨函数中参数的命名问题。对于希望编写简洁易懂代码的人来说，这个主题至关重要，而这正是 Kotlin 语言的主要目标之一。

## 函数重写的基础知识

在 Kotlin 中，如同大多数编程语言一样，类可以相互继承。继承后，类可以 [重写](https://hyperskill.org/learn/step/7884 "In Kotlin, overriding a property is the ability to modify the behavior of an already defined property in a base class from a derived class. | This feature allows for the extension of properties, similar to how methods are inherited and extended in object-oriented programming. Properties in Kotlin take the place of fields seen in other languages, such as Java, and provide a way to encapsulate data within an object and control how that data is accessed and manipulated. Overriding a property enables changing the behavior or value of a property in a derived class, providing an additional layer of flexibility.") 父类的函数来修改或 [扩展](https://hyperskill.org/learn/step/7770 "In Kotlin, extend is a keyword used to create a subclass or a derived class that inherits properties and methods from a superclass or a base class. | It allows for code reuse and facilitates the implementation of inheritance hierarchy. When a class is extended, the subclass can inherit all the members (properties and methods) of the superclass, and it can also add new members or override existing ones. This way, the subclass can build upon the functionality of the superclass and provide additional features.") 其。为此，Kotlin 使用 `override` 。让我们来看一个简单的例子：

```kotlin
open class Animal {
    open fun makeSound() {
        println("The animal makes a sound")
    }
}

class Dog : Animal() {
    override fun makeSound() {
        println("The dog barks")
    }
}
```

这里， `Animal` 基类有一个开放的 `makeSound()` 函数。Dog `Dog` 继承自 `Animal` 类，并重写了 `makeSound()` 函数。

## 覆盖属性

属性和方法的重写机制基本相同。在派生类中的属性时，必须使用 `override` 关键字，并且属性类型必须兼容。已声明的属性可以通过带有初始化器的属性或带有 `get` 方法的属性进行重写。允许使用 `var` 属性重写 `val` 属性，但反之则不允许。这是因为 \` `val` 属性本身就包含一个 `get` ，而当使用 `var` 重写时，派生类中还会声明一个 `set` 方法。

```kotlin
open class Shape {
    open val vertexCount: Int = 0
}

class Triangle : Shape() {
    override val vertexCount = 3
}
```

另一个例子：

```kotlin
interface Shape {
    val vertexCount: Int
}

class Polygon : Shape {
    override var vertexCount: Int = 0  // Can be set to any number later
}
```

## 重写函数中的参数名称

函数通常可以有多个参数，为了提高 Kotlin 代码的，可以在调用时使用命名参数。但是，在重写函数时，命名参数需要格外小心，以避免混淆和错误。保持参数名称与父类一致非常重要，这样才能确保与使用命名参数的函数调用兼容。

假设我们有以下基本类：

```kotlin
open class Shape {
    open fun draw(color: String, strokeWidth: Int) {
        println("Drawing a shape with the color $color and stroke width $strokeWidth")
    }
}
```

如果要在派生类中重新定义 `draw()` 函数，则必须存储参数名称：

```kotlin
class Circle : Shape() {
    override fun draw(color: String, strokeWidth: Int) {
        println("Drawing a circle with the color $color and stroke width $strokeWidth")
    }
}
```

现在，如果我们使用命名参数调用 `draw()` 函数，代码就能正常运行：

```kotlin
fun main() {
    val shape: Shape = Circle()
    shape.draw(color = "red", strokeWidth = 3)
```

现在让我们来看一个更复杂的例子，其中重写函数中使用了命名参数。

```kotlin
open class Vehicle {
    open fun move(speed: Int, direction: String) {
        println("The vehicle is moving at $speed km/h $direction")
    }
}

class Car : Vehicle() {
    override fun move(speed: Int, direction: String) {
        println("The car is moving at $speed km/h $direction")
    }
}

class Bicycle : Vehicle() {
    override fun move(speed: Int, direction: String) {
        println("The bicycle is moving at $speed km/h $direction")
    }
}
```

在上面的例子中，我们有一个基类 `Vehicle` 和两个派生类： `Car` 和 `Bicycle` 。所有类都有一个 `move()` 函数，它接受两个参数： `speed` 和 `direction` 。在派生类中， `move()` 函数被重写，同时保留了参数名称。这使得我们可以毫无问题地使用命名参数：

```kotlin
fun main() {
    val vehicle1: Vehicle = Car()
    val vehicle2: Vehicle = Bicycle()

    vehicle1.move(speed = 60, direction = "north")
    vehicle2.move(speed = 15, direction = "south")
}
```

输出结果为：

```
The car is moving at 60 km/h north
The bicycle is moving at 15 km/h south
```

## 论证命名指南

- 重写函数时务必保存参数名称。这可以确保与使用命名参数的函数调用兼容。
- 使用能够反映参数用途的有意义的参数名称。这有助于提高代码的可读性和理解性。
- 当调用带有大量参数或参数值难以从上下文中理解的函数时，请使用命名参数。这将使代码更易读、更易理解。

## 结论

在本主题中，我们探讨了在 Kotlin 中重新定义函数时保留参数名称的重要性。这可以确保与使用命名参数的函数调用兼容，并使代码更易读易懂。使用命名参数时，务必遵循命名规范，并尽量选择有意义的名称，避免触发参数赋值操作。我们还讨论了 [属性重写](https://hyperskill.org/learn/step/30920 "In Kotlin, property overriding is the ability to modify the behavior of an already defined property in a base class within a derived class. | This feature allows you to extend properties, similar to how methods are inherited and extended in object-oriented programming. Properties in Kotlin replace the traditional fields seen in other languages, like Java, and offer a way to encapsulate data within objects and control their access and manipulation. Property overriding enables you to change the behavior or value of a property in a derived class, providing an additional layer of flexibility. For example, you can override a property in a class to assign a specific value. The 'override' keyword is used to override both properties and methods in a subclass. It's important to note that properties and methods operate differently in Kotlin. A method is a function that performs a certain operation, whereas a property represents data.") 的问题，以及在重写属性中将 `val` 属性更改为 `var` 可能性。

34 名学员喜欢这部分理论内容， 5 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
