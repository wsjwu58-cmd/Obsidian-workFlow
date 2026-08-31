提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

有时我们需要将信息以字符串形式提交，例如，在控制台中进行调试。如何将非文本对象表示为字符串，以便以可读的方式输出呢？这时我们就需要用到 `toString()` 函数了。

## 介绍

假设我们有三个盒子，分别装着三种不同的浆果：覆盆子、草莓和蓝莓。我们需要知道每个盒子的重量。让我们打印出来：

```kotlin
val raspberryWeight = 10
val strawberryWeight = 15
val blueberryWeight = 20

println(raspberryWeight) //10
println(strawberryWeight) //15
println(blueberryWeight) //20
```

看起来没问题。现在我们创建一个 `BerryHolder` 类来存储盒子的重量。我们再试着打印一下这些值：

```kotlin
class BerryHolder(val weight: Int)

val raspberryWeight = BerryHolder(10)
val strawberryWeight = BerryHolder(15)
val blueberryWeight = BerryHolder(20)

println(raspberryWeight) // BerryHolder@6f496d9f
println(strawberryWeight) // BerryHolder@723279cf
println(blueberryWeight) // BerryHolder@10f87f48
```

嗯，这显然不是我们想看到的结果。

为什么会发生这种情况？要弄清楚这一点，我们需要真正理解 `fun println(message: Any?)` 的工作原理。如果我们查看 `println()` 的签名，就会发现它接收一个 `Any?` 类型的 `message` 。请记住，在 Kotlin 中， `Any?` 是 \`any\` 类的超类，包括标准类和自定义类。因此， `println()` 必须接受一个任意类型的对象并返回文本，也就是 `String` 类型的数据。

如果我们需要管理一个函数对完全不同类型的对象的行为，则必须在输出之前将要打印的对象转换为 `String` 类型。\`println `println()` 函数会隐式调用 `toString()` 函数，该函数会将 `message` 转换为字符串。

`toString()` 函数专门用于将对象表示为字符串。那么，为什么它对不同类型的对象处理方式截然不同呢？

## 默认行为

`toString()` 函数是为 `Any?` 类型定义的。这意味着所有类都继承了 `Any?` 的所有方法，包括 `toString()` 方法。

关键在于，对于 `Any?` 类型 `toString()` 方法会返回类名和地址作为字符串。对于某些类，会进行调整以进行正确处理。例如，考虑 `Int` 或 `Double` ：

```kotlin
val nonString = 1.0

println(nonString.toString())   // 1.0
println(nonString)  // 1.0

/* The output is the same: println just implicitly called toString() for Double object */
```

然而，对于大多数类，默认情况下， `toString()` 方法仍然返回类名和对象在内存中的地址。通常，我们希望以其他方式获取对象的文本信息，因此为我们的数据类型重写 `toString()` 方法就很有意义了。

## 重写 toString() 方法

看来我们的问题可以通过重新定义 `toString()` 方法来解决。\`toString `toString()` 会自动为所有你创建的类定义，你可以为任何类重写它。重写方法与其他函数相同。让我们以 \` `BerryHolder` 类为例：

```kotlin
class BerryHolder(val weight: Int) {
    override fun toString(): String {
        return weight.toString()
    }
}
println(BerryHolder(10)) // 10
```

成功了！这次打印我们类的对象按预期进行。

让我们来看一个更复杂的例子。假设我们正在开发一个电子图书馆。首先，我们有一个名为 `User` 类，其中包含用户的 ID 和登录信息。我们希望能够将该类的对象信息输出为 `String` ，以便我们可以看到完整的信息以及简要说明。类似这样： `User{id=id_value, login=login_value, email=email_value}` 。

让我们重写 `User` 类的 `toString()` 函数：

```kotlin
class User(val id: Int, val login: String, val email: String) {
    override fun toString(): String {
            return "User{id=$id, login=$login, email=$email}"
    }
}
    
val user = User(1, "uncle_bob", "rmartin@objectmentor.com")
println(user) // User{id=1, login=uncle_bob, email=rmartin@objectmentor.com}
```

输出结果符合我们的使用需求，易于阅读，而且没有内存寻址。太好了！

## 重写 toString()：继承

重写 `toString()` 方法的另一个原因是处理超类或父类。这里同样适用继承的一般规则。如果父类中定义了 `toString()` 方法，则派生类将使用这个特定的重写版本。

让我们回到之前的例子。电子图书馆的数据库可能不仅包含用户数据，还包含作者数据。让我们扩展 `User` 类，添加 `Author` 类，该类将包含出版物（ `books` ）列表：

```kotlin
open class User(val id: Int, val login: String, val email: String) {
    override fun toString(): String {
        return "User{id=$id, login=$login, email=$email}"
    }
}

}

val user = User(1, "marys01", "mary0101@gmail.com")

println(user)   // User{id=1, login=marys01, email=mary0101@gmail.com}
println(author) // User{id=2, login=srafael, email=rsabatini@gmail.com}
```

`Author` 类未定义 `toString()` 方法。虽然该函数看似默认有效，但由于 `Author` 继承自父类 `User` ，因此会使用父类的重写方法。

现在，如果我们修改 `Author` 类并添加对 `toString()` 方法的特定重写，将会出现以下重写情况：

```kotlin
override fun toString(): String {
        return "Author{id=$id, login=$login, email=$email}, books: $books"
    }
}

val user = User(1, "marys01", "mary0101@gmail.com")

    
println(user)   // User{id=1, login=marys01, email=mary0101@gmail.com}
println(author) // Author{id=2, login=ohwilde, email=wilde1854@mail.ie}, books: Someone’s portrait
```

## 使用超类定义

可能需要在子类中调用父类的 `toString()` 实现。正如你从继承中学到的，可以使用 `super` 来做到这一点：

```kotlin
override fun toString(): String {
            return "Author: ${super.toString()};\nBooks: $books"
        }
}
```

在这里，我们使用了超类的 `toString()` 方法，并对其进行了补充，使其适用于派生类。

我们来看看它是如何工作的。输入一些 `Author` 类的值并输出它们：

```kotlin
val author1 = Author(1, "uncle_bob",
                    "rmartin@objectmentor.com",
                    "\n1.\"Clean Code: A Handbook of Agile Software Craftsmanship\" \n2.\"Agile Software Development: Principles, Patterns and Practices\"")
val author2 = Author(2, "ltlst",
                    "leotolstoy@mail.com",
                    "\n1.\"Anna Karenina\" \n2.\"The Death of Ivan Ilyich\" \n3.\"War and Peace\"")

println(author1)
println()
println(author2)
```

现在，让我们看看程序运行后会显示什么结果：

```kotlin
/*  Author: User{id=1, login=uncle_bob, email=rmartin@objectmentor.com};
    Books: 
    1."Clean Code: A Handbook of Agile Software Craftsmanship" 
    2."Agile Software Development: Principles, Patterns and Practices"
    
    Author: User{id=2, login=ltlst, email=leotolstoy@mail.com};
    Books: 
    1."Anna Karenina" 
    2."The Death of Ivan Ilyich" 
    3."War and Peace"
*/
```

如您所见，我们使用了父类 `User` 的 `toString()` 函数定义，并将其添加到 `Author` 类中。结果是 Author 类的 toString() 函数被重写，而重写 `Author` 函数使用了 `User` 的 `toString()` 函数定义。

## 概括

`toString()` 函数用于将非字符串对象转换为字符串。它在很多情况下都非常有用，例如在调试时。在本主题中，我们了解了它的工作原理，并学习了如何为我们正在使用的类重写它。要为子类重写 `toString()` 函数，所有标准的继承规则都必须适用。现在，你已经准备好使用 `toString()` 来解决各种复杂的任务了！

260 名学员喜欢这篇理论文章， 1 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
