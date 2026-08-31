## 继承和构造函数

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

**继承** 是重用现有类的强大工具。通过继承，Kotlin 确保基类和派生类都能正确初始化。派生类可以利用的来创建自己的多构造函数方案。

## 继承和主构造函数

最简单的情况是基类没有构造函数参数。在下面的例子中， `Fiction` 类继承自 `Book` 类，而 Book 类没有构造函数参数。请注意， `Book` 的括号是必需的，以便对其进行初始化。

```kotlin
open class Book

class Fiction : Book()
```

当基类带有构造函数参数时，派生类应该处理这些参数。如果基类没有正确初始化，Kotlin 将不允许程序编译。以下示例展示了通过初始化基类的一些情况。这里，我们定义了一个名为 `Book` ，并从中继承了 `ExtBook` 、 `NoInfoBook` 和 `FictionBook` 类。

```kotlin
val genre: String = "Unknown", val isbn: Long = 0)

class ExtBook(val publisher: String = "Unknown", title: String,
              genre: String = "Unknown", author: String = "Unknown",
              isbn: Long = 0) : Book(title, author, genre, isbn)

class NoInfoBook(title: String, author: String = "Unknown") : Book(title, author)

class FictionBook(title: String, author: String = "Unknown",
              isbn: Long = 0) : Book(title, author, genre = "fiction", isbn)
```

`ExtBook` 类新增了一个名为 `publisher` 属性，该属性必须用 `var` 或 `val` 声明。所有其他参数都不是新增属性，它们用于基类 `Book` 的相应属性。

`NoInfoBook` 类只有两个参数，用于初始化基类。基类的所有其他参数都采用默认值。

最后， `FictionBook` 类只有 3 个参数，用于初始化基类的 3 个参数。第四个参数名为 `genre` ，在 `Book` 括号内显式设置。

## 继承和辅助构造函数

基类可以有多个构造函数，包括一个主构造函数和多个辅助构造函数。派生类可以通过实现多个构造函数来使用其中一个或多个构造函数来初始化基类。在下面的示例中，继 `Base` 类的 `Derived` 类有多个构造函数。

```kotlin
open class Base(val beta: Int, val gamma: Int, var message: String = "") {
    constructor(beta: Int, message: String = "") : this(beta, 0, message)
}

class Derived(val alpha: Int, beta: Int, gamma: Int, message: String = "") : Base(beta, gamma, message) {
    constructor(alpha: Int, beta: Int, message: String = "") : this(alpha, beta, 0, message)
}
```

在上面的例子中， `Base` 类可以通过 4 种不同的方式初始化。例如：

```kotlin
Base(10)                    // beta is set
Base(10, 20)                // beta and gamma are set
Base(10, 20, "My message")  // beta, gamma, and a message are set
Base(10, "My message")      // beta and a message are set
```

`Base` 类的通过关键字 `this` 将操作委托给主构造函数。

`Derived` 类声明了与 `Base` 类相同的参数列表、类似的辅助构造函数，以及一个名为 `alpha` 新属性。因此，派生类可以以与 `Base` 类类似的方式进行初始化。例如：

```kotlin
Derived(0, 10)
Derived(0, 10, 20)
Derived(0, 10, 20, "My message")
Derived(0, 10, "My message")
```

当然，如果我们想要限制 `Derived` 类的初始化方式，就应该进一步使用辅助构造函数。在下面的示例中，我们使用辅助构造函数显式地定义了 `Derived` 类的每种可能的构造函数。与前面的示例一样， `Derived` 类添加了一个名为 `alpha` 的新属性。

```kotlin
open class Base(val beta: Int, val gamma: Int = 0, var message: String = "")

class Derived : Base {
    val alpha: Int

    constructor(alphaConstr: Int, beta: Int) : super(beta) {
        alpha = alphaConstr
    }

    constructor(alphaConstr: Int, beta: Int, gamma: Int) : super(beta, gamma) {
        alpha = alphaConstr
    }

    constructor(alphaConstr: Int, beta: Int, gamma: Int, message: String) : super(beta, gamma, message) {
        alpha = alphaConstr
    }

    constructor(alphaConstr: Int, beta: Int, message: String) : super(beta, message = message) {
        alpha = alphaConstr
    }
}
```

每个二级构造函数都通过关键字 `super` 调用 `Base` 类构造函数。这里，我们不能有主构造函数。另外，请注意类名后面没有括号。

新属性 `alpha` 定义在类括号内，但未赋值。这是因为其值会在每个二级构造函数中设置。因此，可以确保 `alpha` 会被初始化。

这里我们定义了 4 个构造函数来匹配 `Base` 类的不同构造函数，但我们可以将它们限制为只需要的那些。

## 继承和初始化

如果一个类有一个主构造函数、一些 `init` 块和一些辅助构造函数，那么执行顺序如下：

- 即使调用了辅助构造函数，主构造函数仍然会被调用。主构造函数会首先通过关键字 `this` 被调用；
- 所有 `init` 块，按其出现的顺序依次执行；
- 第二个构造函数块，以防此构造函数被调用。

在继承的情况下，基类首先被初始化：可以通过派生类调用其主构造函数或辅助构造函数来实现。因此，顺序如下：

- 即使通过派生类调用基类的辅助构造函数，基类的主构造函数仍然成立；
- 基类 `init` 块，按其出现的顺序依次执行；
- 基类辅助构造函数块，以防此构造函数被调用；
- 即使调用了派生类的辅助构造函数，派生类的主构造函数仍然有效；
- 派生类 `init` 块，按其出现的顺序依次执行；
- 派生类辅助构造函数块，以防此构造函数被调用。

以下代码示例展示了上述内容。代码中包含一个 `Base` 和一个 `Derived` 类，两者都具有主构造函数、 `init` 块和辅助构造函数。 `Derived` 类通过辅助构造函数进行初始化。

```kotlin
open class Base(val message: String, val email: String) {
    init { println("Base class init") }
    constructor(email: String) : this("No message", email) { println("Base class secondary") }
}

class Derived(email: String) : Base(email) {
    init { println("Derived class init") }
    constructor() : this("example.com") { println("Derived class secondary") }
}

fun main() {
    val myDerived = Derived()
}
```

当 `Derived` 类通过辅助构造函数初始化时，代码块按以下顺序执行：

以上代码输出结果可以验证这一点：

```
Base class init
Base class secondary
Derived class init
Derived class secondary
```

## 结论

使用 **继承** 很容易。但是，为了充分利用 `Base` 类，你需要应用正确的构造函数并注意 `Base` 类的初始化。在本主题中，我们学习了实现这一点的不同方法。

106 名学员喜欢这篇理论文章， 13 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
