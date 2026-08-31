提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

大多数编程工作都涉及重用已有的代码，有时只需稍作修改。例如，在面向对象编程（Kotlin 就是如此）中，代码重用的主要工具是继承（以及相应的组合），我们已经讨论过。在本主题中，我们将探讨继承的替代方案—— **委托** 。

## 委托语法

委托是指使用某个对象而不是提供实现的过程，我们将深入了解它的具体工作原理。

假设我们有一段相当简单的代码——一个接口及其实现：

```kotlin
interface MyInterface {
    fun print()
    val msg: String
}

class MyImplementation : MyInterface {
    override fun print() {
        println(msg)
    }

    override val msg: String = "MyImplementation sends regards!"
}
```

这里没有什么新内容：接口声明了一个属性和一个函数，而类实现了它们。

现在，假设我们需要创建一个新类，该类 1) 具有自身的功能，并且 2) 同时实现给定的接口。我们会遇到复制粘贴代码的问题：我们已经有了这个接口的实现，但我们需要一个不同的类，而这个新类仍然需要实现这个接口。

这就是委托发挥作用的地方：我们可以愉快地编写新类，当需要使用接口的实现时，只需引用已有的实现，Kotlin 就会处理剩下的工作。就像这样：

```kotlin
class MyNewClass(base: MyInterface) : MyInterface by base {  
    override val msg = "Delegate sends regards."  
}
```

好的，但是在这个语境中，“by”和“base”分别是什么意思呢？让我们仔细看看。

```kotlin
class MyNewClass(  
        base: MyInterface) 
        // ^ Here we expect an implementation of MyInterface as a parameter (named "base")  
        : MyInterface by base { 
        // ^ And here we state that MyInterface is implemented by the previously obtained parameter, the one named "base"  
    override val msg = "Delegate sends regards."  
}
```

本质上，在这个类的构造函数中，我们需要一个实现了 `MyInterface` 接口的对象，用冒号 ( `:` ) 标记，然后使用关键字 `by` 告诉派生类，每当它被要求执行 `MyInterface` 接口“承诺”的任何操作时，它将使用提供的对象来执行。

代码如下：

```kotlin
// We create an instance of class, implementing MyInterface
val delegate = MyImplementation()  

// Then we pass this implementation instance as a parameter
val delegatingObj = MyNewClass(delegate)  
println(delegatingObj.msg)
```

它将打印：

```kotlin
Delegate sends regards.
```

## 通过重写来解决复杂问题

但是，这段代码究竟会做什么呢？

```kotlin
val delegate = MyImplementation()
val delegatingObj = MyNewClass(delegate)

delegatingObj.print()
```

请注意，在前面的例子中，我们访问了委托类 `MyNewClass` 特意重写的 `msg` 属性。现在我们访问的是 `MyNewClass` 中没有重写的 `print()` 方法，你认为代码会打印什么？

请花点时间思考答案，然后再继续阅读。

这段代码会打印出以下行：

`MyImplementation 向您致以问候！`

让我们再来看一下带有委托的类：

```kotlin
class MyNewClass(base: MyInterface) : MyInterface by base {  
    override val msg = "Delegate sends regards."  
}
```

它本身没有名为 `print()` 的方法。但它有一个 `base` ，它是 `MyInterface` 的一个实现，而 \`MyInterface\` 本身就包含 `print()` 函数，当我们编写 `delegate.print()` 时，就会调用这个函数。因此， `MyNewClass` 类只是将这项任务 **委托给** 了 `MyImplementation` （委托类）。\`MyImplementation\` 包含一个重写的 `msg` ，其内容为“ `MyImplementation` `MyImplementation sends regards!` ，所以代码会将 `MyImplementation sends regards!` 打印到控制台。

使用委托时，请注意区分委托类的重写属性/方法和仅使用基类实现及其数据的属性/方法。

## 回调和日志记录器示例

在上面的例子中，我们主要使用委托来覆盖接口设置的一些属性并执行一些简单的操作。接下来，让我们来看一个更复杂的情况，其中涉及两个委托！

> [!warning] Warning
> 这个例子比我们之前遇到的例子复杂两倍，所以如果看起来不清楚也不用担心——一旦你对委托的结构有了更好的直觉，它就会更有意义。

首先，让我们了解一下我们将要使用的两个接口：

- `ICallbackReceiver` ：此接口概述了回调的结构。当我们需要用函数调用“包围”某个操作时，可以使用此接口。这些函数调用在执行某个操作之前（ `onBeforeAction()` ）和之后（ `onAfterAction()` ）执行某些 `action()` 。
- `ILogger` ：此接口仅用于格式化输出。但是，当用于委托时，它会使所有输出遵循相同的模式，这对于日志记录非常有用。

以下是这些接口的代码示例：

```kotlin
// Defines the contract for callbacks
interface ICallbackReceiver {
    fun onBeforeAction()
    fun onAfterAction()
    fun action(function: () -> Unit) {
        onBeforeAction()
        function()
        onAfterAction()
    }
}

// Defines the contract for logging
interface ILogger {
    fun getStubDateTime() = "05.11.2022-14:31:04" // placeholder date and time

    val format: String
        get() = "[${getStubDateTime()}]: "

    fun print(s: String)
}
```

现在，让我们为这些接口提供实现：

- `BasicLogger` ： `ILogger` 接口的一个简单实现。它会将格式化的输出打印到控制台。
- `ConsoleNotifier` ：它实现了两个接口：
	- `ICallbackReceiver` 接口，同时定义在主操作之前和之后要执行的操作。
		- `ILogger` ， `BasicLogger` 对象会委托它向控制台打印消息，而不是通常的 `println()` 。

以下是它们的代码示例：

```kotlin
// Simple implementation of ILogger interface
class BasicLogger : ILogger {
    override fun print(s: String) = println(format + s)
}

// Implementation of ICallbackReceiver that uses BasicLogger for printing
class ConsoleNotifier(logger: ILogger) : ICallbackReceiver, ILogger by logger {
    val onBeforeStr = "OnBefore!"
    val onAfterStr = "OnAfter!"

    // "print" is delegated to "logger"
    override fun onBeforeAction() = print(onBeforeStr)
    override fun onAfterAction() = print(onAfterStr)
}
```

最后，我们将创建一个名为 `ExampleParser` 类，该类使用委托机制实现这两个接口。请注意， `ExampleParser` 类本身不需要知道如何处理回调或打印消息，它只是将这些职责委托给其他知道如何处理的对象。

```kotlin
// Class implementing both interfaces by delegation
class ExampleParser(notifier: ConsoleNotifier, logger: BasicLogger) :
    ICallbackReceiver by notifier,
    ILogger by logger {

    fun start() = action { parseFiles() }

    fun parseFiles() {
        print("Parsing...")
        // do some file parsing
    }
}
```

请记住，还有另一种指定 `ExampleParser` 类构造函数的方法，这种方法使其更加灵活，并可接受 `ICallbackReceiver` 和 `ILogger` 接口的任何实现。这意味着您可以传递任何实现了这些接口的对象，而不仅仅是 `ConsoleNotifier` 和 `BasicLogger` 。这提供了更大的灵活性，并且通常是一种更好的实践，因为它遵循了“面向接口编程，而非面向实现编程”的原则，而这正是面向对象编程的关键原则。

这是 `ExampleParser` 的改进版本：

```kotlin
class ExampleParser(notifier: ICallbackReceiver, logger: ILogger) :
    ICallbackReceiver by notifier,
    ILogger by logger {
    ...
}
```

现在，运行以下代码后，将创建 `BasicLogger` 和 `ConsoleNotifier` 的实例。这些实例随后将传递给 `ExampleParser` 的构造函数。当调用 `ExampleParser` 的 `start()` 函数时，它将使用 `BasicLogger` 中定义的格式打印消息，并且在解析文件前后还会调用 `ConsoleNotifier` 中定义的函数。

```kotlin
fun main() {
    val loggerInstance = BasicLogger()
    val dateTimeNotifier = ConsoleNotifier(loggerInstance)

    val simpleParser = ExampleParser(dateTimeNotifier, loggerInstance)
    simpleParser.start()
}
```

输出结果如下所示：

```kotlin
[05.11.2022-14:31:04]: OnBefore!
[05.11.2022-14:31:04]: Parsing...
[05.11.2022-14:31:04]: OnAfter!
```

## 结论

委托机制使得代码重用更加便捷，这得益于 Kotlin 语言层面对委托机制的良好支持。我们无需在类内部编写代码来实现特定功能（甚至可能需要从现有实现中复制代码），而是可以引入一个已经具备所需功能的对象，并利用该对象来获得理想的结果。

76 名学员喜欢这部分理论内容， 28 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
