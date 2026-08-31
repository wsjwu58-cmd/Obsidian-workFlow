提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经知道如何创建与类关联的单例。然而，在很多情况下，一个类只需要一个单例，而使用类的完整名称可能显得冗长。例如，您可能只需要存储一个公共属性。在这种情况下，您可以使用 Kotlin 的另一个特性：。

## 伴随物

类内部的可以用 **companion** 关键字标记：

```kotlin
class Player(val id: Int) {
    companion object Properties {
        /* Default player speed in playing field - 7 cells per turn */
        val defaultSpeed = 7

        fun calcMovePenalty(cell: Int): Int {
            /* calc move speed penalty */
        }
    }
}

/* prints 7 */
println(Player.Properties.defaultSpeed)
```

伴生对象是附加到单例对象，因此必须访问外部类才能访问它。它让我们能够理解当前对象与外部类之间存在某种关联。例如，我们可以将所有玩家的默认速度存储在 `Player` 伴生对象中。这也意味着每个 `Player` 都包含对该伴生对象的引用，并且每次都会返回该伴生对象的实例。

到目前为止，我们一直使用的是带名称的伴随对象。但是，与不同，伴随对象的名称可以省略。让我们来试试：

```kotlin
class Player(val id: Int) {
    companion object {
        /* Default player speed in playing field - 7 cells per turn */
        val defaultSpeed = 7

        fun calcMovePenalty(cell: Int): Int {
            /* calc move speed penalty */
        }
    }
}

/* prints 7 */
println(Player.defaultSpeed)
```

如您所见，即使省略伴随对象的名称，我们仍然可以通过外部类声明访问它。如果需要以某种方式使用它，我们可以手动定义它。如果伴随对象没有名称，我们也可以使用默认名称 `Companion` 。

```kotlin
/* prints 7 too */
println(Player.Companion.defaultSpeed)
```

## 伴随对象和外部类

伴生对象与外部类紧密关联。您可以在外部类中自由使用伴生对象的属性和函数。例如：

```kotlin
class Deck {
    companion object {
        val size = 10
        val height = 2
        fun volume(bottom: Int, height: Int) = bottom * height
    }

    val square = size * size             //100
    val volume = volume(square, height)  //200
}
```

但如果外部类有一个与伴生对象同名的属性会发生什么情况呢？在这种情况下，外部类的属性会覆盖伴生对象的属性。

```kotlin
class Deck {
    companion object {
        val size = 10
    }
    val size = 2
    val square = size * size // 4
}
```

在这种情况下，如果您想使用同伴的属性，则必须使用同伴的名称；如果同伴没有命名，则使用默认名称“同伴”：

```kotlin
class Deck {
    companion object {
        val size = 10
    }
    val size = 2
    val square = Companion.size * Companion.size // 100
}
```

与嵌套对象的情况类似，你不能在内部类中使用外部类的属性和函数。例如，你不能这样做：

```kotlin
class Deck() {    
    val size = 2
    object Properties {
        val defaultSize = size // you cannot get this variable
    }
}
```

## 伴随对象的局限性

每个类只能有一个伴生对象。这意味着你不能为一个类创建多个伴生对象，因为 Kotlin 不支持这种行为，即使它们的名称不同。如果尝试这样做，将会发生错误：

```kotlin
class BadClass {
    companion object Properties {
    
    }

    companion object Factory {
    
    }
}

// Compilation error
// Error: Only one companion object is allowed per class
```

但是，我们可以创建一个伴随对象和多个嵌套对象：

```kotlin
class Player(val id: Int) {
    companion object Properties {
        /* Default player speed in playing field - 7 cells per turn */
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

/* also prints 7 */
println(Player.defaultSpeed)

/* prints 13 */
println(Player.Factory.create(13).id)
```

还有一个限制：我们不能在另一个单例（或伴生对象）中创建伴生对象，因为这违反了全局访问原则。

```kotlin
object OuterSingleton {
    companion object InnerSingleton { // Modifier 'companion' is not applicable inside 'object'  
  
    }
}
```

## 其他语言中的类似物

如果你之前接触过其他编程语言，可能会对伴生对象感到有些困惑。与它最接近的概念是 `static` 成员。 `static` 表示带有此字段和方法对于类的所有对象都是通用的，无需创建类的实例即可使用。你可能会在多种编程语言中遇到这个关键字。

例如，在 Java 中， `static` 的用法如下所示：

```java
class Dog {
    public static int numOfPaws = 4;

    public static String createSound() {
        return "WUF-WUF";
    }
}
/*prints WUF-WUF*/
System.out.println(Dog.createSound());
```

如您所知，Kotlin 没有 `static` 关键字。如果您需要类的所有实例都具有某些共同属性，可以使用伴生对象：

```kotlin
class Dog {
    companion object {
        val numOfPaws: Int = 4
        fun createSound(): String = "WUF-WUF"
    }
}
/*prints WUF-WUF*/
println(Dog.createSound())
```

如您所见，使用伴生对象时，您无需创建类实例即可使用此函数！请记住，伴生对象与 Java 的 `static` 初始化器不同。在 Kotlin 中，伴生对象是一个嵌套对象，它封装了整个类通用的所有方法和字段。

## 结论

让我们回顾一下！声明伴生对象是组织数据的一种好方法。它类似于嵌套对象，但与类的关联更紧密。你可以像操作伴生对象自身的属性一样，从外部类自由地操作它的属性。当你需要一个与类关联的单例时，可以使用伴生对象：使用伴生对象比使用嵌套类更可取。现在，让我们开始练习吧！

224 名学习者喜欢这篇理论文章， 8 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
