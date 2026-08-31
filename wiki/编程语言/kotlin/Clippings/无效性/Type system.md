提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

Kotlin 最重要的组成部分之一是，它是一种检测和防止程序出现非法状态的机制。类型系统为程序赋予了结构。如果没有结构，程序会变得极其复杂，程序员哪怕最轻微的错误都可能造成严重后果。借助类型系统，我们可以描述程序中各个组件之间的关系并赋予其意义，从而使程序更加简洁易读。

## 亚型和超型

Kotlin 中的类型组织成一个子类型-超类型关系的层级结构。那么，什么是子类型和超类型呢？让我们通过一个例子来了解一下。

你喜欢咖啡还是茶？它们都是饮品。我们可以说，咖啡和茶都属于饮品这一特定类别。换句话说，咖啡和茶是饮品的 **子类别** ，而饮品则是咖啡和茶的 **上位类别** 。

![certain types and subtypes](https://ucarecdn.com/41c926d0-f108-40d0-9ee7-73eced7c11de/)

因此， **子类型** 是一种与另一种数据类型（ *超类型* ）相关的数据类型，它与超类型共享一些共同的特征和行为规则。需要注意的是，不同 *子类型* 的行为规则可能有所不同，就像所有饮料都有某种颜色，但咖啡和茶的颜色就不同一样。

从逻辑上讲， **超类型** 是一种指定所有子类型将遵循的特征和行为规则的类型。

例如， `Number` 是所有表示数值类型的超类型； `Int` 和 `Double` 是 `Number` 类型的子类型。

![example of types and subtypes](https://ucarecdn.com/2347dcf1-ea0f-44bb-bfe8-8665aee5f5c1/)

## 类型检查

Kotlin 类型检查器会强制执行子类型与上类型之间的关系。例如，对于等待 `Number 的函数 ` *，* 你可以传递它的子类型 `Int` ：

```kotlin
fun calculate(number: Number) {}

val number: Int = 1
calculate(number)
```

但是，反过来却不行：

```kotlin
fun calculate(number: Int) {}

val number: Number = 1
calculate(number) // Error: Type mismatch: inferred type is Number but Int was expected
```

如果将 `Number` 传递给 `calculate` 函数，将会报错。现在让我们看看 `Number` 、 `Drink` 以及其他不能为 `null` 类型的超类型是什么。

## 根类型任意

在前面的章节中，你已经熟悉了可空类型和的概念。现在是时候深入了解 Kotlin 中这些类型的表示方式了。

在 Kotlin 中， `Any` 类型是所有不支持 \`null\` 类型的超类型。这意味着任何非空类型都是 ``Any 子类型 *。* 例如，你可以将非空的 `String` 赋值给 `Any` 类型：``

```kotlin
val message: Any = "Important message"
```

但是，您不能将空值赋给 `Any` 类型：

```kotlin
val message: Any = null  // Error: Null can not be a value of a non-null type Any
```

Type `Any` 也是 `Boolean` 等基本类型的超类型：

```kotlin
val isNull: Any = false
```

在 Kotlin 类型层次结构中， *\`Any\`* 类型位于不能为空的类型的顶端。例如， `Number` 类型是 *\`Any\`* 类型的子类型：

![Type Any is at the top of the Kotlin type hierarchy for types that cannot be null](https://ucarecdn.com/4dd59f84-7aa1-4c41-825d-b326a7c0aa7c/)

请注意， `Any` 类型不支持 `null` 。当我们讨论某个类型是 `Any` 子类型时，我们可以确信，尝试访问该类型时不会抛出 `NullPointerException` 。换句话说，Kotlin 保证 `Any` 类型的子类型永远不会为 `null` ，这意味着在处理 `Any` 类型时， `null` 检查变得毫无意义。

```kotlin
fun stringify(any: Any) {
    any?.toString()  // '?' can be omitted
    any!!.toString() // '!!' can be omitted
}
```

## 根类型： 任意？

如您所知，后缀“?”用于声明可以为空的变量。请注意，您不能将空值赋给非空变量。我们来看一个例子：

```kotlin
val number1: Number = null // Error: Null can not be a value of a non-null type Number
```
```kotlin
val number2: Number? = null // OK
```

`Any` 类型是所有不支持 null 类型的超类型，而 `Any?` 类型是可以为 null 或不为 null 的类型的超类型。  
由此可知，类型 `Any?` 是类型 `Any` 超类型：

![тип Any является супертипом для типа Any](https://ucarecdn.com/841f6033-0d40-4ce9-85d0-301f4c4ca66e/)

非空类型是其可空等价类型的子类型，例如，类型 `Number` 是类型 `Int` Number?`  的子类型，类型  ` 是类型 `Int?` 的子类型。让我们看看它是什么样子的：

![example of type and subtype hierarchy](https://ucarecdn.com/81310c7f-1f48-4048-a5e8-bf2e50a57600/)

这就是为什么你可以将非空的 `Number` 值存储在可为空的 `Number?` 变量中，但不能将可为空的 `Number?` 值存储在非空的 `Number` 变量中。

## 单元

`Unit` 类型可以用作不返回任何有意义值的函数的：

```kotlin
fun logCurrentState(): Unit { 
    println("Current state of a program: $state")
}
```

如果你编写一个函数但没有指定返回类型，编译器会将其视为 `Unit` 函数：

```kotlin
fun updateState(state: State) { 
    logCurrentState()
    this.state = state
    logCurrentState()
}

val result: Unit = logCurrentState()
```

与其他类型一样， `Unit` 是 `Any` 子类型。它也可以是可为空的 `Unit?` 而可为空的 Unit? 又是 `Any?` 的子类型。

`Unit?` 类型可以有两个值： `Unit` 值和 `null` 。

![Any and Unit type hierarchy](https://ucarecdn.com/cb5017d1-be80-4e66-a98b-20ddf0b3a52b/)

## 没有什么

在 Kotlin 类型层次结构的最底层是 `Nothing` 类型。

`Nothing` 是一种没有的类型。对于 Kotlin 中的某些函数来说，返回值的概念毫无意义，因为它们从不返回值，总是抛出异常。我们将在下一节更详细地探讨 Nothing，但你也可以 [在这里阅读相关内容。](https://hyperskill.org/learn/step/39052)

## 结论

我们从这个主题中学到的所有内容都可以概括为一个简洁的类型系统树：

![type system trees](https://ucarecdn.com/d365efa2-c7bb-42cc-82ca-9be2ea2e6e90/)

希望现在您对 Kotlin 的类型系统感到满意，并且能够描述程序中各个组件之间的关系。请记住：Kotlin 的类型系统是这门语言的重要组成部分，它能极大地帮助您解决问题。

378 名学习者喜欢这篇理论文章， 22 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
