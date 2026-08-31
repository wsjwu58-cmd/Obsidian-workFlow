提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

如何创建一个简单的数据存储类？除了存储信息之外，它还应该能够比较和复制对象。此外，能够立即输出数据也非常方便。通常，为了实现这些功能，该类必须包含一些方法： `equals()` 和 `hashCode()` 用于比较， `copy()` 用于复制， `toString()` 用于将对象转换为字符串，以及 \` `componentN()` 函数，这些函数按声明顺序对应于各个属性。但在 Kotlin 中，您无需实现所有这些函数，只需使用 即可。让我们仔细看看这类类。

## 数据类

首先，我们需要一个类，所以这里有一个不错的 `Client` 类：

```kotlin
class Client(val name: String, val age: Int, val gender: String)
```

目前它有 3 个属性，到目前为止一切顺利！但是为了正确地比较对象（即，通过它们的属性），我们需要实现 `equals()` 和 `hashCode()` 函数：

```kotlin
class Client(val name: String, val age: Int, val gender: String) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as Client

        if (name != other.name) return false
        if (age != other.age) return false
        if (gender != other.gender) return false

        return true
    }

    override fun hashCode(): Int {
        var result = name.hashCode()
        result = 31 * result + age
        result = 31 * result + gender.hashCode()
        return result
    }
}
```

为什么仅仅为了实现一些基本功能就需要这么长的代码？问得好，因为有了数据类，我们可以像这样简化它：

```kotlin
data class Client(val name: String, val age: Int, val gender: String)
```

等等！我的函数都去哪儿了？实际上，有了 `data` 关键字，你就不需要它们了。它会神奇地像你已经实现了所有函数一样正常工作。这个关键字还会为 `toString()` 、 `copy()` 和 `componentN()` 函数提供默认行为（\`equals\` 和 \`hashCode\`）。我们稍后会详细介绍 `copy()` 和 `componentN()` ，但现在你需要记住以下几条规则：

1\. 你只能依赖构造函数内部的属性。例如，以下修改后的 `Client` 类：

```kotlin
data class Client(val name: String, val age: Int, val gender: String) {
    var balance: Int = 0
}
```

所有这些函数都不会考虑 `balance` 字段，因为它不在构造函数内部。

2\. 除了 `copy()` 之外，你可以重写所有这些函数：

```kotlin
data class Client(val name: String, val age: Int, val gender: String) {
    var balance: Int = 0

    override fun toString(): String {
        return "Client(name='$name', age=$age, gender='$gender', balance=$balance)"
    }

}
```

现在 `balance` 字段也参与了 `toString()` 函数的调用。

3\. 数据类的主构造函数必须至少有一个参数，并且所有这些参数都必须是 `val` 或 `var` 。

## 复制和组件 N

说实话，Java 中并没有很方便的复制对象的方法，但 Kotlin 就不同了。例如，如果我们有一个 `Client` 类的实例，想要复制同一个客户端，只是名字不同，该怎么办？很简单！

```kotlin
fun main() {
    val bob = Client("Bob", 29, "Male")
    val john = bob.copy(name = "John")
    println(bob)
    println(john)
}
```

如您所见，我们刚刚使用了 `copy()` 函数，该函数会自动接收 `data` 。输出结果如下：

```kotlin
Client(name='Bob', age=29, gender='Male', balance=0)
Client(name='John', age=29, gender='Male', balance=0)
```

componentN() 函数对应于属性的声明顺序：component1()、component2()、……，涵盖所有数据类属性。为数据类生成的 Component 函数使得它们可以用于

```kotlin
fun main() {
    val bob = Client("Bob", 29, "Male")
    println(bob.name) // Bob
    println(bob.component1()) // Bob
    println(bob.age)  // 29
    println(bob.component2()) // 29
    println(bob.gender) // Male
    println(bob.component3()) // Male
    
    // destructuring
    val (name, age, gender) = bob
    println(name) // Bob
    println(age)  // 29
    println(gender) // Male
}
```

## 成语

正如我们所展示的，数据类是组织数据或创建 DTO（数据传输对象）的便捷方式。因此，请在 [获得社区认可](https://kotlinlang.org/docs/idioms.html#create-dtos-pojos-pocos) 后使用它！

```kotlin
data class Customer(val name: String, val email: String)
```

## 结论

现在您知道如何使用 `data` 关键字简化样板代码了。它不仅可以缩短代码长度，还能节省您的时间。请明智地使用它！

## 相关条目
- [[Kotlin基础语法梳理]]
