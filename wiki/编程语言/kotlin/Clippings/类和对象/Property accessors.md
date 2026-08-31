提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

正如您所知，Kotlin 中的每个类都可以拥有零个或多个 **属性** 。您几乎会在所有类中使用属性。在本主题中，我们将深入探讨如何使用属性，例如更改属性值和获取属性值。

## 属性获取器

假设你有一个简单的 `Client` ，它只有一个属性 `name` ：

```kotlin
class Client {
    val name = "Unknown"
}

val client = Client()
```

您已经知道如何获取属性名称：只需在对象名称后输入点号和属性名称即可：

```kotlin
client.name
```

这看起来很简单，但实际上，当你想获取某个属性的值时，你需要调用一个名为 **getter 的** 特殊 get() 函数。它的实际代码如下：

```kotlin
class Client {
    val name = "Unknown"
        get() {
            return field
        }
}

// or with omitted curly brackets and the body of the get() function

class Client {
    val name = "Unknown"
        get() = field
}
```

这个函数不接受任何参数（你只需要请求一个值，没有其他要求），并返回一个值。当你尝试获取一个值时，你会得到 `get()` 函数的结果。那么， `field` 是什么呢？Kotlin 中的每个属性都有其 ，其中包含一个属性值，可以使用 `field` 来访问该值。

在这种情况下，你的 getter 方法只会返回 `name` 变量的值。这是预期行为，所以 Kotlin 会自动生成这个函数，你不需要自己编写。如果你想修改 getter 方法的逻辑，你应该自己编写 `get()` 函数。

有时，您需要执行一些不符合这种隐式支持字段方案的操作，这时您可以始终使用。例如，我们可以使用它来保存可变值信息，并始终返回一个只读值。

```kotlin
class IntegerRepository {
    private val _list = mutableListOf<Int>()
    val list: List<Int> get() = _list // backing property
}

fun main() {
    val repository = IntegerRepository()
    repository.list.add(1) // Error: variable list is a read-only collection
    println(repository.list)
}
```

## 自定义 getter

每次访问 `name` 时，我们都打印出客户的姓名：

```kotlin
class Client {
    val name = "Unknown"
        get() {
            println("Somebody wants to know $field name")
            return field
        }
}

val client = Client()

val name = client.name // prints Somebody wants to know Unknown name
println(name)          // prints Unknown
```

的另一个用途是返回其他值。例如，您的任务可能是将完整的客户信息存储在一个变量中。如果您更改了某个客户的某些信息，则也需要更改此变量。如果使用自定义 getter，则可以按需生成信息。在下面的示例中， `Client` 类获取一个 `age` 属性来存储客户的年龄，以及 `info` 属性来返回有关客户的信息：

```kotlin
class Client {
    var name: String = "Unknown"
    var age: Int = 18
    val info: String
        get() {
            return "name = $name, age = $age"
        }
}

val client = Client()
println(client.info) // name = Unknown, age = 18
client.name = "Lester"
client.age = 20
println(client.info) // name = Lester, age = 20
```

## 物业设定者

现在您知道可以自定义获取属性值的过程。同样，也可以修改更改属性值的过程！让我们来看一个简单的例子：

```kotlin
class Client {
    var name = "Unknown" // default value
}

val client = Client()
client.name = "Ann"      // name property now stores "Ann"
```

当你想设置某个属性的值时，应该调用一个名为 **setter 的** 特殊 set() 函数。它的代码如下所示：

```kotlin
class Client {
    var name = "Unknown"
        set(value) {
            field = value
        }
}
```

此函数接受一个参数（按照惯例命名为 `value` ，但您可以使用其他名称），并且不返回任何值。如您所知， `field` 包含属性的当前值，您可以通过重新赋值来更改它。

在这种情况下，你的 setter 方法只会将 `name` 变量的值更改为接收到的值。这是预期行为，Kotlin 会自动生成此函数，你无需自己编写 setter 方法。

## 自定义设置器

`set()` 函数是一个强大的工具，可以自定义 setter 的逻辑。例如，我们可以每次更改 `name` 属性时都打印出客户的姓名：

```kotlin
class Client {
    var name = "Unknown"
        set(value) {
            println("The name is changing. Old value is $field. New value is $value.")
            field = value
        }
}

val client = Client()
client.name = "Ann"   // The name is changing. Old value is Unknown. New value is Ann.
```

您可能已经注意到，setter 仅在您尝试更改属性时调用，而不是在属性时调用。

另一种使用方法是，如果您想为属性赋不同的值。例如，我们添加一个 `age` 属性来存储客户的年龄。当然，年龄不能为负数。如果您需要考虑这一点，可以添加一个自定义 setter：

```kotlin
class Client {
    var name = "Unknown"
    var age = 18
        set(value) {                      
            field = if (value < 0) {
                println("Age cannot be negative. Set to $defaultAge")
                defaultAge
            } else
                value
        }
    val defaultAge = 18
}

val client = Client()
client.age = -1      // Age cannot be negative. Set to 18.
println(client.age)  // 18
```

## 附加功能

你可以为你的属性同时实现 setter 和 getter：

```kotlin
class Client {
    var name = "Unknown"
        get() {
            println("Somebody wants to know $field name")
            return field
        }
        set(value) {
            println("The name is changing. Old value is $field. New value is $value.")
            field = value
        }
}
```

如果想在构造函数中为属性添加 getter 和/或 setter，只需将该属性“移”出即可。请记住，在这种情况下，您需要使用另一个变量，而不是构造函数中的属性：

```kotlin
class Client(name: String, age: Int) {
    var fullName: String = name
        set(value) {
            println("The name is changing. Old value is $field. New value is $value.")
            field = value
        }
    var age: Int = age   // this is a new property, not a property from the constructor
        set(value) {
            println("The age is changing. Old value is $field. New value is $value.")
            field = value
        }
}
```

请记住，初始化属性时，setter 方法不会被调用。构造函数也是如此，因为它们会初始化属性。让我们仔细看看：

```kotlin
class Client(name: String) {
    var name: String = name
        set(value) {
            println("The name is changing. Old value is $field. New value is $value.")
            field = value
        }
}

val client = Client("Annie")  // without output
client.name = "Ann"           // The name is changing. Old value is Annie. New value is Ann.
```

你不能对 `val` 类型的变量使用 setter 方法： `set()` 函数会重新赋值，而 `val` 不允许这样做。当然，你可以通过其他方式改变 `val` 属性的内部状态，例如，使用它自己的 setter 方法。

```kotlin
class Passport(number: String) {
    var number = number
    set(value) {
        println("Passport number has changed.")
        field = value
    }
}

class Client {
    val passport = Passport("1234567")
}

val client = Client()
println(client.passport.number)       // 1234567
/*
client.passport = Passport("2345678") // This will not work.
*/
client.passport.number = "2345678"    // This will change the passport number
                                      // prints Passport number has changed
println(client.passport.number)       // 2345678
```

## 结论

Kotlin 属性是处理一种非常实用的方式。现在您已经了解了默认的 getter 和 setter 方法及其自定义方式。这是一个非常强大的工具，可以帮助您处理许多场景，例如日志记录和输入处理。

403 名学习者喜欢这篇理论文章， 17 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
