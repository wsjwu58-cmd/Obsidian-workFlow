## Kotlin 中的继承

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

尽管 Kotlin 具有丰富的函数式编程风格，但它本质上是一种面向对象编程 (OOP) 语言，因此在设计和编写 Kotlin 程序时，您可以运用 OOP 原则。如果您熟悉 OOP 原则，那么您可能听说过继承。Kotlin 是如何处理继承的呢？让我们一起来看看！

## 打开它

以下是在 Kotlin 中创建类的通常方法：

```kotlin
class Book(val pages: Int, val author: String)
```

如果你的代码看起来像这样，你就创建了一个 final 类。这意味着这个类以后将无法被继承。你只是禁止了继承。不过别担心，这在 Kotlin 中完全没问题，因为 Kotlin 默认所有类都是封闭的，不允许继承。正如著名软件工程师 [Joshua Bloch](https://en.wikipedia.org/wiki/Joshua_Bloch) 所说：“ *要么设计并记录继承，要么就禁止继承* 。”

所以，如果您确实确定需要扩展您的 `Book` 类（父类），这里有一个简单的方法：

```kotlin
open class Book(val pages: Int, val author: String)
```

如您所见，我们刚刚添加了 `open` 关键字，现在我们的类可以进行扩展了。首先，让我们修改它：

```kotlin
fun getFullInfo(): String {
        return "$pages pages, $author author, $$cost cost"
    }
}
```

然后将其扩展：

```kotlin
class Comics(pages: Int, author: String, cost: Float) : Book(pages, author, cost)
```

如您所见，我们创建了一个新的 `Comics` 类（子类），作为 `Book` 类的扩展。目前我们还没有添加任何额外的逻辑，只是将所有参数直接传递给了 `Book` 主构造函数。让我们通过一个实际示例来验证一下：

```kotlin
fun main() {
    val spidermanBook = Comics(60, "The Universe", 8.99F)
    print(spidermanBook.getFullInfo())
}
// output: 60 pages, The Universe author, $8.99 cost
```

我们创作了一本多么棒的漫画书啊！

## 延长

我们还可以向子类添加更多功能：

```kotlin
class Booklet(pages: Int, cost: Float) : Book(pages, "", cost) {
    fun getUSDCost(): String {
        return "$$cost cost"
    }

    fun getEuroCost(): String {
        return "€$cost cost"
    }
}
```

并加以利用：

```kotlin
fun main() {
    val centralBooklet = Booklet(5, 0.14F)
    print(centralBooklet.getUSDCost())
}
// output: $0.14 cost
```

因此，我们的继承层次结构将如下所示：

![The image shows an example of an inheritance hierarchy](https://ucarecdn.com/c4aa31bd-4ecc-438e-be21-d5478c558377/)

当然，有了这种强大的方法，我们也可以让它变得更加复杂：

![The image shows an example of a complex inheritance hierarchy](https://ucarecdn.com/ec6381dc-74e0-4658-8e76-d45672c718c8/)

## 重复使用

你还可以利用子类做更多的事情。让我们创建一个函数来判断你的书是否足够长：

```kotlin
fun isBigBook(book: Book): Boolean {
    return book.pages >= 100
}
```

请注意，此函数可用于父类和子类：

```kotlin
fun main() {
    val spidermanBook = Comics(113, "The Universe", 8.99F)
    val centralBooklet = Booklet(5, 0.14F)
    println(isBigBook(spidermanBook))
    println(isBigBook(centralBooklet))
}
// output: true false
```

如您所见，继承机制非常强大。我们可以将 `Book` 实例的任何子实例传递给 `isBigBook()` 函数。

## 结论

如何继承类完全取决于你，但如果你将父类标记为 `open` ，子类始终可以访问父类的逻辑。你还可以向子类添加任意数量的函数。不过，有一点很重要：不要开放所有类，只开放你需要扩展的类。

331 名学习者喜欢这篇理论文章， 4 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
