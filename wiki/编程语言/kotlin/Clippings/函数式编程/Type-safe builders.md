## 类型安全的构建器

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在之前的章节中，我们已经了解了在 Kotlin 中使用函数的强大功能。我们也学习了使用和带有接收器的 lambda 表达式的重要性。

在本主题中，我们将重点讨论如何使用来实现 DSL（），并为我们的代码创建一个。

## Kotlin 中的建筑商

**建造者模式** 是一种创建型设计模式，它允许逐步构建复杂对象。它通过将构建逻辑与对象表示分离来创建对象，从而生成更易读、更易维护的代码。

传统的建造者模式通常由一个表示待构建对象的类和一个独立的建造者类组成。建造者类提供设置待构建对象属性的方法，从而实现流畅且可定制的构建过程。建造者模式通过提供清晰且可定制的方式来构建复杂对象，避免了使用或庞大的参数列表，从而提高了对象构建的可读性和灵活性。

```kotlin
class Person private constructor(
    val firstName: String,
    val lastName: String,
    val age: Int,
    val address: String
) {
    class Builder {
        private var firstName: String = ""
        private var lastName: String = ""
        private var age: Int = 0
        private var address: String = ""

        fun setFirstName(firstName: String): Builder {
            this.firstName = firstName
            return this
        }

        fun setLastName(lastName: String): Builder {
            this.lastName = lastName
            return this
        }

        fun setAge(age: Int): Builder {
            this.age = age
            return this
        }

        fun setAddress(address: String): Builder {
            this.address = address
            return this
        }

        fun build(): Person {
            return Person(firstName, lastName, age, address)
        }
    }
}

fun main() {
   val person = Person.Builder()
    .setFirstName("John")
    .setLastName("Doe")
    .setAge(30)
    .setAddress("123 Main St")
    .build()
}
```

不过，你可以利用 Kotlin 的函数式编程优势来实现这种模式：扩展函数、带接收器的 lambda 表达式或带接收器的函数字面量。我们来看一个例子：

```kotlin
data class Person(
    val firstName: String,
    val lastName: String,
    val age: Int,
    val address: String
)

class PersonBuilder {
    var firstName: String = ""
    var lastName: String = ""
    var age: Int = 0
    var address: String = ""

    fun build(): Person {
        return Person(firstName, lastName, age, address)
    }
}

fun person(init: PersonBuilder.() -> Unit): Person {
    val builder = PersonBuilder()
    builder.init()
    return builder.build()
}

fun main() {
    val person = person {
        firstName = "John"
        lastName = "Doe"
        age = 30
        address = "123 Main St"
    }
}
```

在这种方法中， `Person` 类保持不变，但 `PersonBuilder` 类被定义为一个可变的构建器类，用于表示 `person` 器的状态。person 函数被定义为一个，它接受一个带有接收器的 lambda 表达式（ `init: PersonBuilder.() -> Unit` ）来配置构建器。带有接收器的 lambda 表达式（ `init` ）允许您使用命名参数直接设置 `PersonBuilder` 对象的属性。配置构建器后，调用 `person` 函数会创建并返回相应的 `Person` 对象。这种方法提供了一种简洁且 **声明式的** 方式来使用构建器模式构建对象，充分利用了带有接收器的 lambda 表达式和不可变数据类的强大功能。

以下是另一个示例，展示了如何根据上述模式构建字符串。

```kotlin
fun buildString(action: StringBuilder.() -> Unit): String {
    val stringBuilder = StringBuilder()
    action(stringBuilder)
    return stringBuilder.toString()
}

fun main() {
    println(buildString {
        append("I Love ")
        append("learning Kotlin")
        append(" with Hyperskill")
    }) // I Love learning Kotlin with Hyperskill
}
```

## DSL

根据 Martin Fowler 的说法，领域特定语言 (DSL) 是一种专门用于解决特定类型问题的编程语言，与通用编程语言相对。在 Kotlin 中，凭借其强大的特性，您可以创建内部 DSL，利用扩展函数、lambda 表达式、带接收器的 lambda 表达式和来解决复杂的层次结构问题。这些语言结构允许您定义一个与问题领域紧密相关的 DSL，并为处理复杂的层次结构提供自然直观的语法。您可以创建内部 DSL，以更专注、更具表现力的方式解决特定领域内的特定问题，从而编写出更易于阅读、编写和维护的代码。

Kotlin 中使用 DSL 的示例包括使用 Kotlin 代码生成标记（例如 [HTML](https://github.com/Kotlin/kotlinx.html) 或 XML），或者在 [Ktor](https://ktor.io/docs/routing.html) 中为 Web 服务器配置路由。

## 类型安全的构建器

Kotlin 中的类型安全构建器基于两个主要概念：领域特定语言 (DSL) 和构建器设计模式。通过结合这两个概念，Kotlin 中的类型安全构建器使我们能够创建语法流畅易读的 API，代码块的结构类似于层次结构或标记语言。Kotlin 中的类型安全构建器通过类或中的扩展函数来定义。这些函数扩展了，并允许在编译时安全地构建和配置对象。通过使用类型安全构建器，Kotlin 编译器可以验证构建块中使用的值和属性的正确性，从而防止常见错误，并提供更安全、更不容易出错的开发体验。

例如，我们将编写一个字符串值树 `TreeNodeBuilder` 以层级结构组织节点。\`TreeNodeBuilder\` 类负责构建树结构。它保存当前正在构建的节点，并提供 `value` 和 `child` 等方法。\`value\` `value` 设置当前节点的值。\`child\` `child` 创建一个新的子节点，将其添加到当前节点，并返回一个指向该子节点的 \`TreeNodeBuilder\` 实例。\`parent\` `parent` 允许返回到父节点。\`build\` `build` 返回已构建树的根节点。

```kotlin
data class TreeNode(var value: String = "") {
    val children = mutableListOf<TreeNode>()

    fun addChild(child: TreeNode) {
        children.add(child)
    }
}

class TreeNodeBuilder(
    private val node: TreeNode = TreeNode(),
    private val parent: TreeNodeBuilder? = null) {

    fun value(value: String): TreeNodeBuilder {
        node.value = value
        return this
    }

    fun child(): TreeNodeBuilder {
        val childNode = TreeNode()
        node.addChild(childNode)
        return TreeNodeBuilder(childNode, this)
    }

    fun parent(): TreeNodeBuilder {
        return parent ?: throw IllegalStateException("Cannot go back to parent node. Already at the root.")
    }

    fun build(): TreeNode {
        return node
    }
}

fun buildTree(): TreeNodeBuilder {
    return TreeNodeBuilder()
}

fun main() {
    val tree = buildTree()
        .value("Root")
        .child()
            .value("Child 1")
            .child()
                .value("Grandchild 1.1")
            .parent()
            .child()
                .value("Grandchild 1.2")
            .parent()
        .parent()
        .child()
            .value("Child 2")
            .child()
                .value("Grandchild 2.1")
            .parent()
        .parent()
        .build()

    printTree(tree)
}

fun printTree(node: TreeNode, level: Int = 0) {
    val indentation = "  ".repeat(level)
    println("$indentation${node.value}")
    for (child in node.children) {
        printTree(child, level + 1)
    }
}
```

运行主函数后，它会打印出树状结构：树的每一层都缩进两个空格，并显示代表节点的字符串。这样就以可视化的方式呈现了字符串树的层次结构。

```kotlin
Root
  Child 1
    Grandchild 1.1
    Grandchild 1.2
  Child 2
    Grandchild 2.1
```

现在，我们将把这段代码转换成类型安全的构建器，以便将其用作领域特定语言 (DSL)。在本例中，类型安全的构建器 `TreeNodeBuilder` 提供了 `value` 和 `child` 等方法，这些方法可以链式调用来构建树结构。这使得树的构建方式更加声明式且易于阅读。最终，您将获得一个表示树数据结构的树对象。例如，我们编写一个树结构及其层级结构中的项 `TreeNode` 类外部的 `buildTree` 函数用于启动构建过程，它接受一个带有接收器的 lambda 表达式 `TreeNodeBuilder.() -> Unit` ）。在 `TreeNodeBuilder` 类内部，定义了 `value` 和 `child` 函数来配置和构建树结构。\`value\` `value` 设置当前正在构建的节点的值。\`TreeNodeBuilder\` `TreeNodeBuilder` 中的 `child` 函数用于向当前节点添加子节点。它接受一个带有接收器的 lambda 表达式（ `TreeNodeBuilder.() -> Unit` ），该表达式定义了子节点的配置。在 lambda 表达式内部，会创建一个新的 `TreeNodeBuilder` ，并且 lambda 表达式会在子节点构建器的范围内执行。然后，生成的子节点会被添加到当前节点的子节点列表中。

```kotlin
data class TreeNode(var value: String = "") {
    val children = mutableListOf<TreeNode>()

    fun addChild(child: TreeNode) {
        children.add(child)
    }
}

class TreeNodeBuilder(private val node: TreeNode = TreeNode()) {

    fun value(value: String) {
        node.value = value
    }

    fun child(block: TreeNodeBuilder.() -> Unit) {
        val childNode = TreeNode()
        val childBuilder = TreeNodeBuilder(childNode)
        childBuilder.block()
        node.addChild(childNode)
    }

    fun build(): TreeNode {
        return node
    }
}

fun buildTree(block: TreeNodeBuilder.() -> Unit): TreeNode {
    val builder = TreeNodeBuilder()
    builder.block()
    return builder.build()
}

fun main() {
    val tree = buildTree {
        value("Root")
        child {
            value("Child 1")
            child {
                value("Grandchild 1.1")
            }
            child {
                value("Grandchild 1.2")
            }
        }
        child {
            value("Child 2")
            child {
                value("Grandchild 2.1")
            }
        }
    }

    printTree(tree)
}

fun printTree(node: TreeNode, level: Int = 0) {
    val indentation = "  ".repeat(level)
    println("$indentation${node.value}")
    for (child in node.children) {
        printTree(child, level + 1)
    }
}
```

这样，你就能在视觉上得到与前一个例子相同的字符串树层次结构的表示。

```kotlin
Root
  Child 1
    Grandchild 1.1
    Grandchild 1.2
  Child 2
    Grandchild 2.1
```

## 使用带有构建器类型推断的构建器

从 Kotlin 1.7.0 版本开始，可以使用带有类型推断的构建器，这在使用时尤其有用。该特性使编译器能够根据构建器 lambda 参数中其他调用的类型信息来推断构建器调用的类型参数。

**使用示例**

考虑使用 `buildMap()` ：

```kotlin
fun addEntryToMap(baseMap: Map<String, Number>, additionalEntry: Pair<String, Int>?) {
    val myMap = buildMap {
        putAll(baseMap)
        additionalEntry?.let { put(it.first, it.second) }
    }
}
```

在这里，编译器根据 `putAll()` 和 `put()` 调用的信息，自动推断 `buildMap()` 调用的类型参数为 `String` 和 `Number` 。

**使用类型推断编写您自己的构建器**

要在构建器中启用：

1. 确保构建器的声明包含一个带有接收器的 lambda 参数。
2. 接收器类型应使用要推断的参数类型。例如： `fun <V> buildList(builder: MutableList<V>.() -> Unit) { ... }`
3. 接收器类型应提供公共成员或扩展，这些成员或扩展的签名中包含相应的类型参数。

**支持的功能**

1. 推断几种类型的论证。
2. 在一次调用中推断多个构建器 lambda 表达式的类型参数。
3. 推断类型参数为 lambda 表达式的参数或返回类型的类型参数。

**构建器类型推断的工作原理**

构建器类型推断基于“延迟类型变量”进行操作，这些变量在构建器推断分析期间出现在构建器 lambda 表达式内部。编译器使用它们来收集类型参数的信息。在构建器类型推断分析结束时，所有收集到的类型信息都会被考虑并尝试合并到最终的类型中。

## 作用域控制：@DslMarker

在 Kotlin 中， `@DslMarker` 注解用于定义 DSL 标记接口或注解。它允许您指定一个标记来指示 DSL 的作用域，并有助于在 DSL 中强制执行作用域规则。创建 DSL 时，通常需要限制某些函数或构建器在特定作用域内的可用性。\` `@DslMarker` 注解限制了 DSL 的作用域，使得嵌套代码块中只能访问最近的接收者。这有助于防止意外地误用外部作用域中的函数。让我们将此注解应用到我们的树结构定义中：

```kotlin
@DslMarker
annotation class TreeNodeDslMarker

data class TreeNode(var value: String = "") {
    val children = mutableListOf<TreeNode>()

    fun addChild(child: TreeNode) {
        children.add(child)
    }
}

@TreeNodeDslMarker
class TreeNodeBuilder(private val node: TreeNode = TreeNode()) {

    fun value(value: String) {
        node.value = value
    }

    fun child(block: TreeNodeBuilder.() -> Unit) {
        val childNode = TreeNode()
        val childBuilder = TreeNodeBuilder(childNode)
        childBuilder.block()
        node.addChild(childNode)
    }

    fun build(): TreeNode {
        return node
    }
}

fun buildTree(block: TreeNodeBuilder.() -> Unit): TreeNode {
    val builder = TreeNodeBuilder()
    builder.block()
    return builder.build()
}

fun main() {
    val tree = buildTree {
        value("Root")
        child {
            value("Child 1")
            child {
                value("Grandchild 1.1")
            }
            child {
                value("Grandchild 1.2")
            }
        }
        child {
            value("Child 2")
            child {
                value("Grandchild 2.1")
            }
        }
    }

    printTree(tree)
}

fun printTree(node: TreeNode, level: Int = 0) {
    val indentation = "  ".repeat(level)
    println("$indentation${node.value}")
    for (child in node.children) {
        printTree(child, level + 1)
    }
}
```

`@DslMarker` 注解应用于 `TreeNodeBuilder` 类，将其标记为 DSL 的一部分，并限制其作用域可见性。\` `@TreeNodeDslMarker` 注解作为 DSL 的标记，表明 \` `TreeNodeBuilder` 参与了 DSL 的作用域。通过应用 `@DslMarker` 注解，您可以清晰地控制 DSL 接收者的可见性，并防止意外使用外部作用域的函数。这提供了一种控制 DSL 函数和构建器可见性和作用域的方法。\` `@DslMarker` 是可选的，其使用取决于您对作用域和 DSL 设计的具体要求，但它有助于强制执行作用域规则，并更好地阐明 DSL 的预期用途。

## 结论

在本主题中，我们学习了如何使用类型安全的构建器来创建领域特定语言（DSL），以便以半声明式的方式构建复杂的层次化数据结构。您可以尝试在自己的项目中应用这种方法。

现在是时候做一些任务来检验你所学的知识了。准备好了吗？

21 名学员喜欢这部分理论， 74 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
