提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

类委托是 Kotlin 中的一种机制，它允许你将一个类的接口或功能的实现委托给另一个类。这提供了灵活性，并避免了与相关的问题。

## 委托：示例

下面你可以看到一个类委托的示例。要实现类委托，需要使用 `by` 关键字（我们稍后会讨论这个）。

```kotlin
interface Drawable {
    fun draw()
}

class Circle : Drawable {
    override fun draw() {
        println("Drawing a circle")
    }
}

class DrawingBoard(private val drawable: Drawable) : Drawable by drawable

fun main() {
    val circle = Circle()
    val drawingBoard = DrawingBoard(circle)
    drawingBoard.draw() // "Drawing a circle"
}
```

## 使用类委托的优势

- 它简化了代码：类委托通过将接口或功能的实现委托给另一个类来避免代码重复。
- 它提高了组合性和模块化程度：您可以组合不同的对象来创建新功能，而无需使用继承。
- 它避免了多重继承问题：与继承不同，委托不会导致与多重继承相关的问题，例如“菱形问题”。
- 它提供了改变对象行为的灵活性：您可以轻松替换委托来改变对象的行为，而无需更改。

以下是使用类委托改变对象行为的示例：

```kotlin
interface Greeting {
    fun greet()
}

class EnglishGreeting : Greeting {
    override fun greet() {
        println("Hello!")
    }
}

class FrenchGreeting : Greeting {
    override fun greet() {
        println("Bonjour!")
    }
}

class Greeter(private val greeting: Greeting) : Greeting by greeting

fun main() {
    val englishGreeting = EnglishGreeting()
    val frenchGreeting = FrenchGreeting()
    
    val greeter1 = Greeter(englishGreeting)
    val greeter2 = Greeter(frenchGreeting)
    
    greeter1.greet() // "Hello!"
    greeter2.greet() // "Bonjour!"
}
```

在上面的例子中， `Greeter` 类将 `Greeting` 接口的实现委托给不同的委托人，从而在不更改源代码的情况下改变对象的行为。

## 关键词“by”

在 Kotlin 中，关键字 `by` 用于将一个类的接口或功能的实现委托给另一个类。

以下是使用 `by` 关键字的示例：

```kotlin
interface Printable {
    fun print()
}

class Printer : Printable {
    override fun print() {
        println("Printing a document")
    }
}

class OfficePrinter(private val printer: Printer) : Printable by printer

fun main() {
    val printer = Printer()
    val officePrinter = OfficePrinter(printer)
    officePrinter.print() // "Printing a document"
}
```

在这个例子中， `OfficePrinter` 类使用 `by` 关键字 `Printable` 接口的实现委托给 `Printer` 类。

## 继承和委托之间的区别

遗产：

- 类继承父类的功能和属性。
- 阶级之间存在着紧密的联系。
- 可能会出现多重继承问题，例如“菱形继承问题”。

以下是继承的一个例子：

```kotlin
open class Vehicle {
    fun move() {
        println("Vehicle is moving")
    }
}

class Car : Vehicle()

fun main() {
    val car = Car()
    car.move() // "Vehicle is moving"
}
```

代表团：

- 接口或功能的实现被传递给另一个类。
- 它提供了灵活性和模块化，并有助于避免多重继承问题。

以下是一个授权的例子：

```kotlin
interface Movable {
    fun move()
}

class Vehicle : Movable {
    override fun move() {
        println("Vehicle is moving")
    }
}

class Car(private val movable: Movable) : Movable by movable

fun main() {
    val vehicle = Vehicle()
    val car = Car(vehicle)
    car.move() // "Vehicle is moving"
}
```

在上面的例子中， `Car` 类没有依赖继承，而是将 `Movable` 接口的实现委托给了 `Vehicle` 类，从而提供了代码的灵活性和模块化。

## 使用类委托实现接口

1\. 创建接口

首先，您必须定义用于委托的接口。在本例中，我们创建一个名为 `Eatable` 接口：

```kotlin
interface Eatable {
    fun eat()
}
```

2\. 创建委托类

接下来，我们创建一个实现 `Eatable` 接口的类。在这个例子中，我们创建一个名为 `Apple` 类，它实现了 `Eatable` 接口：

```kotlin
class Apple : Eatable {
    override fun eat() {
        println("Eating an apple")
    }
}
```

3\. 创建一个使用委托的类

现在，让我们创建一个名为 `Person` 类，它将使用委托来实现 `Eatable` 接口：

```kotlin
class Person(private val eatable: Eatable) : Eatable by eatable
```

以下是使用 `Person` 类和 `Apple` 的代理类的示例：

```kotlin
class Banana : Eatable {
    override fun eat() {
        println("Eating a banana")
    }
}

fun main() {
    val banana = Banana()
    val person = Person(banana)
    person.eat() // "Eating a banana"
}
```

因此，借助 Kotlin 的类委托，您可以轻松灵活地实现接口并改变对象的行为。

## 结论

类委托在 Kotlin 中扮演着重要的角色，它提供了一种灵活高效的方式来实现接口和功能。它是 Kotlin 的关键机制之一，有助于创建简洁、模块化且易于维护的代码。它消除了继承的限制，为开发者提供了更多调整和扩展代码的选择。

30 名学员喜欢这部分理论内容， 4 名学员不喜欢。 **你觉得呢？**

报告拼写错误

### 相关主题[代表](https://hyperskill.org/learn/step/21405)

## 相关条目
- [[Kotlin基础语法梳理]]
