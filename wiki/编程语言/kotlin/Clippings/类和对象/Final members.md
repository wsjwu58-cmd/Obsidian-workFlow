提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在本主题中，我们将讨论 Kotlin 编程语言中的 **final 成员** 概念。在 Java 和 C++ 等编程语言中， `final` 用于表示某个值、方法或类不能被修改或重写。然而，在 Kotlin 中，情况略有不同。

## 理解 Kotlin 中的“final”

在 Kotlin 中，所有类和方法默认都是 final 的。这意味着，如果你在 Kotlin 中声明了一个类，除非你明确地将其声明为 `open` ，否则你将无法继承它。同样，Kotlin 中的方法和属性默认也是 final 的，并且它们在子类中无法被重写，除非它们被声明为 `open` 。

请看这个例子：

```kotlin
class MyFinalClass {
    fun myFinalMethod() {
        println("This method cannot be overridden!")
    }
}

class MyChildClass : MyFinalClass() { // Error! Cannot inherit MyFinalClass
    override fun myFinalMethod() { // Error! Cannot override myFinalMethod
        println("I'm trying to override your method!")
    }
}
```

在这个例子中，我们不能继承 `MyFinalClass` 或重写 `myFinalMethod` 因为它们默认都是 final 的。

你可能想知道 Kotlin 为什么采用这种方式。答案很简单：这种方式有助于编写更安全、更可预测的代码。毕竟，如果一个类或方法可以被任意继承或重写，就可能导致不良后果。当你显式地将一个类或方法声明为 `open` 时，就明确地表明了你允许继承或重定义的意图。

让我们仔细看看 Kotlin 中的 `final` 概念，并看一些它的使用示例。

## “决赛”与“公开赛”

如您所知，在 Kotlin 中，所有类和 `final` 类的成员都是默认的，这意味着它们不能被重写。如果您希望类继承或重写某个方法，则需要使用关键字 \` `open` 。

```kotlin
open class MyBaseClass {
    open fun myMethod() {
        println("Basic implementation")
    }
}

class MyDerivedClass : MyBaseClass() {
    override fun myMethod() {
        println("Overridden implementation")
    }
}
```

在这个例子中， `MyBaseClass` 和 `myMethod` 被声明为 open，因此 `MyDerivedClass` 可以继承 `MyBaseClass` 并重写 `myMethod` 。

## “final”在“open”之后

需要注意的是，你可以对重写的方法或属性使用 `final` ，以防止它们被重新定义。举个例子：

```kotlin
open class MyBaseClass {
    open fun myMethod() {
        println("Basic implementation")
    }
}

open class MyIntermediateClass : MyBaseClass() {
    final override fun myMethod() {
        println("An overridden implementation that cannot be redefined further")
    }
}

class MyDerivedClass : MyIntermediateClass() {
    override fun myMethod() { // Error! Cannot override myMethod
        println("I'm trying to override your method!")
    }
}
```

在这个例子中， `MyIntermediateClass` 中的 `myMethod` 被声明为 `final` ，这意味着它不能在 `MyDerivedClass` 中被重写。

## 结论

总之，Kotlin 中的 `final` 能够更有效地控制继承和重定义，从而使代码更安全、更易于维护。这是 Kotlin 众多吸引开发者的特性之一。

61 名学员喜欢这篇理论文章， 2 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
