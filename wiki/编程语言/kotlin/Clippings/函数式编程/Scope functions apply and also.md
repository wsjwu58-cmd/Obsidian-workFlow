## 作用域函数：apply 和 also

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

## 介绍

Kotlin 中有很多糖，可以让你的代码更易读、更清晰。就是其中一个例子。它们将代码组织成便于理解的代码块，也方便后续的维护工作。在本主题中，我们将探讨什么是作用域函数，以及其中两个函数 \` `apply` 和 \` `also` 工作原理。

## 作用域功能

Kotlin 中有五个作用域函数： `let` 、 `run` 、 `with` 、 `apply` 和 `also` 。它们本身并不执行任何具体操作，只是用于组织代码并在对象上下文中执行某些操作。这些函数会为对象创建一个临时作用域，并调用 lambda 表达式中的代码。在 lambda 表达式内部，我们可以使用关键字 `it` 或 `this` 与对象进行交互（我们将在后续章节中讨论它们）。

听起来有点抽象，没错，但我们来看一个例子——它既简单又酷！我们有一个 `Musician` 数据类，其中包含一些关于名人的信息：他们的姓名、演奏的乐器以及他们所在的乐队名称。众所周知，Nirvana 乐队解散后，Dave Grohl 组建了 Foo Fighters 乐队。他最初是乐队的鼓手，后来开始弹吉他。现在，我们需要相应地修改我们的对象。为此，我们将使用作用域函数之一 `apply` 。

```kotlin
data class Musician(var name: String, var instrument: String, var band: String)

fun main() {
    Musician("Dave Grohl", "Drums", "Nirvana").apply {
        println(this)
        band = "Foo Fighters"
        instrument = "Guitar"
        println(this)
    }
}
// Output:
// Musician(name=Dave Grohl, instrument=Drums, band=Nirvana)
// Musician(name=Dave Grohl, instrument=Guitar, band=Foo Fighters)
```

瞧！Dave 成功修改了他的属性：乐队名称和乐器。我们也得到了一段清晰易读的代码。

现在让我们看看去掉作用域函数后这段代码会是什么样子。

```kotlin
data class Musician(var name: String, var instrument: String, var band: String)

fun main() {
    val dave = Musician("Dave Grohl", "Drums", "Nirvana")
    println(dave)
    dave.band = "Foo Fighters"
    dave.instrument = "Guitar"
    println(dave)
}
```

我们可以看到，如果没有 `apply` 代码会变得更冗长，并且会引入一个新的变量。此外，使用 `apply` 的代码中，操作被清晰地分组，而没有 `apply` 时，所有操作都位于同一层级。如果我们再添加更多操作，代码可能会变得难以阅读。

现在，让我们详细了解两个作用域函数 `apply` 和 `also` 并讨论它们的工作原理和作用范围。你会发现它们非常相似。

## 申请

`apply` 函数有两个主要特点：

- 可通过 `this` 方式获取。
- 该函数返回上下文对象。

`apply` 通常用于对象设置——例如，如果您想为类方法或参数赋新值。它的意思类似于“嘿，把这些设置应用到这个对象及其参数上！”。请注意，在这种情况下，您需要有权访问对象参数。

你还记得电台司令乐队的 Jonny Greenwood 吗？现在让我们来输入他的资料！

```kotlin
data class Musician(var name: String, var instrument: String = "Guitar", var band: String = "Radiohead")

fun main() {
    Musician("Jonny Greenwood").apply {
      instrument = "Harmonica" // here we can also use this.instrument
      band = "Pavement"     
    }
}
```

我们修改了对象并设置了 Jonny 的一些参数——现在他可以在 Pavement 乐队的专辑《Terror Twilight》（1999 年）中演奏口琴了。真是个有才华的人！

注意我们是如何访问类参数的：我们本可以使用 `this.instrument` 来引用它们，但 `this` 可以省略。再看看这段代码的可读性——从它的结构中，我们可以立即看到将新设置应用到 \` `Musician()` 对象实例的代码块。

请记住， `apply` 会返回上下文对象。这意味着我们可以将该对象传递到调用链的更下游，并对其进行其他操作。例如，我们可以使用一些新参数复制该对象：

```kotlin
fun main() {
    val thom = Musician("Jonny Greenwood")
        .apply {
            instrument = "Harmonica"
            band = "Pavement"
        }.copy(name = "Thom York") // After .apply we have an instance of Musician()
}
```

## 还

以下是 `also` 函数的两个主要特点：

- 上下文对象可 `it` 使用。
- 该函数返回上下文对象。

`also` 的用法与 `apply` 类似，但建议在操作整个对象且不关心其参数或方法时 `also` 。它的意思类似于“嘿，现在对这个对象做点什么，并且（在执行主要操作之前）同时执行一个额外的操作”。例如，假设我们年迈的 Jonny 决定学习一种新乐器：

```kotlin
val instruments = mutableListOf("Guitar", "Harmonica", "Bass guitar")

instruments
    .also { println("Right now I can play these instruments: $it") }
    .add("Theremin")
```

我们声明一个变量，给它传递一些值，同时使用 `also` 函数调用 `println()` 函数。

同时， `also` 还有一个有趣的特性——它似乎会立即执行操作（实际上，它会在操作执行之前返回上下文）。看看这个技巧是如何运作的：

```kotlin
var a = 10
var b = 5
a = b.also { b = a }
println("a = $a, b = $b") // Output: a = 5, b = 10
```

伟大的！

## 结论

我们已经学习了五个作用域函数，并深入研究了其中两个—— `also` \`apply\` 和 `apply` 。以下是简要总结：

- Kotlin 中有五个作用域函数，可以帮助我们组织代码并对对象进行一些操作。
- 我们需要使用 `apply` 来设置对象参数。
- 我们 `also` 必须使用它来对对象进行一些额外的操作。

在下一个主题中，我们将考虑 `with` 、 `run` 和 `let` 的用法——这三个函数都会返回 lambda 的结果。

103 名学员喜欢这篇理论文章， 7 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
