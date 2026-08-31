提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在 Kotlin 中，类描述了一个可以多次实例化并以多种方式实例化的通用结构。有时我们只需要一个实例，不多也不少。它可以帮助你组织代码库，并将类似的方法集中在一起。在本主题中，你将学习如何在 Kotlin 中使用来实现这一点。

## 辛格尔顿

**单例模式** 是一种设计模式，它确保一个类只有一个实例，并且可以全局访问该实例。这意味着我们可以在代码中的任何位置获取单例类的。举个简单的例子：玩棋盘游戏时，所有玩家都在棋盘上进行操作。棋盘就是一个特定的单一区域，用于存储游戏的全局状态。

在继续之前，让我们快速回顾一下单例模式的主要特点：

- 单例类只有一个实例。
- 单例类提供全局访问点。

## 对象声明

单例模式非常实用，Kotlin 提供了一种专门用于声明单例的结构： **对象声明** 。这是一个特殊的类，它使用 **object** 关键字来创建单例。这个关键字隐藏了所有复杂的步骤，因此您无需考虑如何实现此模式：只需使用 **对象声明** 即可。

我们来看一个例子：

```kotlin
object PlayingField {

    fun getAllPlayers(): Array<Player> {
        /* ... */
    }
    
    fun isPlayerInGame(player: Player): Boolean {
        /* ... */
    }

}
```

使用对象声明时，构造函数不可用，因为 Kotlin 会自动创建对象。要获取游戏场地的实例，请使用 `PlayingField` 声明。我们可以在任何地方使用它，它每次都会返回同一个对象。

```kotlin
fun startNewGameTurn() {
    val players = PlayingField.getAllPlayers()
    if (players.size < 2) {
        return println("The game cannot be continued without players")
    }
    for (player in players) {
        nextPlayerTurn(player)
    }
}

fun nextPlayerTurn(player: Player) {
    if (!PlayingField.isPlayerInGame(player)) {
        return println("Current player lost. Next...")
    }
    /* Player actions here */
}
```

## 嵌套对象

很多时候，你需要创建一个与另一个类有某种关联的单例。例如，你创建了一个 `Player` 类来存储游戏中不同角色的信息。所有这些角色可能有一些共同的特征，例如速度。我们该如何存储这些信息呢？

当然，您可以使用对象声明来创建类似这样的对象：

```kotlin
object PlayerProperties {
    /* Default player speed in playing field – 7 cells per turn */
    val defaultSpeed = 7

    fun calcMovePenalty(cell: Int): Int {
        /* calc move speed penalty */
    }
}
```

然而，可能会有很多类和相关的单例，这会使代码混乱且难以阅读。另一种存储此类信息的方法是使用。

对象声明可以嵌套在类声明中。是在另一个类内部创建的；没有声明，就无法访问嵌套类。

```kotlin
class OuterClass {  
   //outer class code  
    class NestedClass {  
      //nested class code  
    }  
}
```

现在，让我们更仔细地看一下嵌套对象的构造：

```kotlin
class Player(val id: Int) {
    object Properties {
        /* Default player speed in playing field – 7 cells per turn */
        val defaultSpeed = 7

        fun calcMovePenalty(cell: Int): Int {
            /* calc move speed penalty */
        }
    }
}

/* prints 7 */
println(Player.Properties.defaultSpeed)
```

对象 `Properties` 作用域为 `Player` ，这意味着我们只能通过 `Player.Properties` 访问它。这就是创建与特定类关联的单例的方法。

您还可以在外部类中使用嵌套对象的属性和函数。这对于存储类所有实例共有的数据以及初始化变量非常有用。例如：

```kotlin
class Player(val id: Int) {
    object Properties {
        val defaultSpeed = 7
    }
    
    val superSpeed = Properties.defaultSpeed * 2 // 14
}
```

反过来则不然。你不能在内部类中使用外部类的属性和函数。例如，你不能这样做：

```kotlin
class Player(val id: Int) {    
    val speed = 7
    object Properties {
        val defaultSpeed = speed // you cannot get this variable
    }
}
```

如您所见，它与其他语言中的 **静态成员** 类似。Kotlin 默认不提供静态成员，但如果您需要与类相关的某些内容，可以使用嵌套对象。

## 编译时常量

如您所知，有时需要在代码中使用永远不会改变的值。我们称它们 **为常量值** 。因此，如果您知道对象的某个是常量，则可以将其声明为 `const` ：

```kotlin
object Languages {
    const val FAVORITE_LANGUAGE = "Kotlin"

    // ...
}
```

这类常量的值在编译时就已经确定，因此被称为。请注意，常量必须满足以下要求：首先，它必须初始化为 `String` 类型或基本类型（ `Int` 、 `Double` 等）的值。此外，它不能是 [自定义的 getter](https://hyperskill.org/learn/step/10511) 方法。请记住，常量命名必须使用 SCREAMING\_SNAKE\_CASE 格式。

顺便一提，如果我们知道游戏中的 `defaultSpeed` 属性是一个常量，那么我们可以对上面的示例进行如下修改：

```kotlin
object Properties {
    /* Constant default player speed */
    const val DEFAULT_SPEED = 7

    // ...
}
```

你可以像这样从对象外部访问此属性：

```kotlin
object Properties {
    /* Constant default player speed */
    const val DEFAULT_SPEED = 7

    // ...
}

fun main() {
    println(Properties.DEFAULT_SPEED) // 7
    
    // ...
}
```

你可能会问：为什么不直接把所有常量都声明为顶层常量呢？为什么我们需要在对象中声明它们？

一般来说，两种方法都可行，具体取决于实际情况。事实上，随意使用顶层属性会降低代码的可读性和组织性，从而导致令人不快的错误。如果将所有常量都声明在文件顶部，最终可能会发现一个地方有数百个彼此无关的声明。因此，如果一个常量指向某个特定对象，最好在该对象内部声明它。

> [!primary] Primary
> 最好在与其相关的对象中声明常量。

## 对象和嵌套对象

我们来讨论一下其他特性。有时，您可能需要为一个类创建多个单例。您可以在另一个类中声明任意数量的对象：

```kotlin
class Player(val id: Int) {
    object Properties {
        /* Default player speed in playing field – 7 cells per turn */
        val defaultSpeed = 7

        fun calcMovePenalty(cell: Int): Int {
            /* calc move speed penalty */
        }
    }

    /* creates a new instance of Player */
    object Factory {
        fun create(playerId: Int): Player {
            return Player(playerId)
        }
    }
}

/* prints 7 */
println(Player.Properties.defaultSpeed)

/* prints 13 */
println(Player.Factory.create(13).id)
```

在这个例子中，我们创建了一个额外的单例，它可以创建类的新实例。这种模式称为 **工厂模式** ，在处理复杂情况时非常有用。您可以 [在这里](https://hyperskill.org/learn/step/17108) 阅读更多关于这种模式的信息。这种模式通常通过嵌套对象来实现。

嵌套对象的另一个有用特性是，你可以在一个对象内部声明任意数量的对象。

```kotlin
object Game {
    object Properties {
        val maxPlayersCount = 13
        val maxGameDurationInSec = 2400
    }

    object Info {
        val name = "My super game"
    }
}
```

这有助于整理单例中的数据。

## 数据对象

在 Kotlin 中打印普通对象声明时，包含对象的名称和对象的哈希值。

```kotlin
object MyObject

fun main() {
    println(MyObject) // MyObject@1f32e575
}
```

就像 [数据类](https://hyperskill.org/learn/step/8526) 一样，你可以使用 \`data\` 修饰符标记对象声明。这会指示编译器为你的对象生成一些函数：

- toString() 返回
- equals()/hashCode() 对
```kotlin
data object MySingleton

fun main() {
    println(MySingleton) // MySingleton
}
```

您不应将此功能与数据类中已有的功能混淆。数据对象声明旨在用作单例对象，不会生成 `copy()` \` 函数。单例模式将类的实例化限制为单个实例，允许创建实例副本会违反这一原则。与数据类不同，数据对象没有任何数据属性。由于尝试解构没有数据属性的对象是没有意义的，因此不会生成 `componentN()` 函数。

## 成语

如您所见，单例模式是一个强大的工具。在许多语言中，您需要自己编写这样的类，但 Kotlin 推荐使用 [对象声明](https://kotlinlang.org/docs/idioms.html#create-a-singleton) 作为标准解决方案。

```kotlin
object Resource {
    val name = "Name"
}
```

此外，我们可以使用作用域函数 `apply` 配置对象的属性。

```kotlin
val myRectangle = Rectangle().apply {
    length = 4
    breadth = 5
    color = 0xFAFAFA
}
```

## 概括

对象声明是一项非常有用的特性。我们主要可以使用 `object` 关键字来创建单例对象。对象声明的另一个用途是嵌套对象。它提供了一种简便的方法，可以创建一个与整个类而非单个实例关联的结构。如果能够明智且正确地使用对象声明，可以提升您的编程体验，并使您的代码更易读。

291 名学习者喜欢这篇理论文章， 27 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
