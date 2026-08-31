提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

有时，将一个对象解构为多个变量会很方便。例如，为了更好地操作对象，或者为了使代码更简洁。在本主题中，我们将了解如何实现这一点。

## 基本解构

假设你有一个 `User` ，用于存储用户信息。它有诸如 String `name` 、Int `age` 和 Boolean `isAdmin` 之类的字段。

```kotlin
data class User(val name: String, val age: Int, val isAdmin: Boolean)

val anonym = User("Anonym", 999, false)
```

好了，这就是我们需要的全部内容！现在我们可以将所有变量从类中分离出来，并将它们作为单独的对象进行操作：

```kotlin
val (userName, userAge, isAdmin) = anonym
println(userName)  // prints Anonym
println(userAge)   // prints 999
println(isAdmin)   // prints false
```

此功能称为 **。** 解构声明可以一次性创建多个变量。我们声明了三个新变量： `userName` 、 `userAge` 和 `isAdmin` 。

解构声明使用 `componentN()` 运算符，它返回类中的第 n 个元素。上面的代码编译成以下代码：

```kotlin
val userName = anonym.component1()
val userAge = anonym.component2()
val isAdmin = anonym.component3()
```

## 无需数据类的解构

即使不使用数据类，也可以使用解构赋值。我们只需要手动定义一个 `componentN` **运算符** 。运算符类似于函数，但使用特殊的符号来对操作数/值执行操作。例如， `+` 是一个执行加法的运算符。就是这样！你可以把它想象成一个函数。现在让我们尝试重写一些用于解构赋值的运算符：

```kotlin
class User(val name: String, val age: Int, val isAdmin: Boolean){
    operator fun component1(): String = name
    operator fun component2(): Int = age
    operator fun component3(): Boolean = isAdmin
}

// now we can use default destructuring syntax
fun checkIsAdmin(suspiciousUser: User) {
    // destructuring
    val (name, age, isAdmin) = suspiciousUser

    if (isAdmin)
        println("Have a nice day!")
    else
        println("Sorry, you should not be here.")
}
```

`componentN` 函数的工作原理依赖于每个类变量的位置。但这存在问题，因为类本身并非基于位置关系，因此很容易出错。

请注意，我们不能在数据类中重写 `componentN` 运算符，因为 Kotlin 会自动处理：

```kotlin
// Error: Conflicting overloads: public final operator fun component1(): String defined in StoreClass
data class StoreClass(val info: String) {
    operator fun component1() = info
}
```

## 使用列表和循环进行解构

解构声明也适用于列表和循环，因为 `List` 是一个实现了 `componentN` 运算符的类。现在，让我们提取前 3 个元素：

```kotlin
fun processList(customerInfo: MutableList<String>) {
    if (customerInfo.size < 3) return
    val (firstName, lastName, city) = customerInfo
    showCustomerName(firstName, lastName)
    findPopularSellersInCity(city)
}
```

如果列表元素超过 3 个，剩余的元素将不会被处理，程序会继续执行。同样地，如果列表元素少于 3 个，则会发生错误，程序会崩溃。为了避免这种情况，我们添加了一个 if 判断语句。

请注意，我们可以从一个包含超过 N 个元素的列表或类中获取前 N 个元素。这在某些情况下可能很有用。

for 循环中的解构也涉及到 `componentN` 运算符。现在，让我们把公司所有非管理员用户的数据发送给分析师：

```kotlin
fun processAnalytics(usersData: MutableList<User>) {
    for ((name, age, isAdmin) in usersData) {
        if (!isAdmin)
            sendAnalyticsToCompany(name, age)
    }
}
```

这样， `MutableList<User>` 中的每个元素都将被解构。

## 变量下划线

当我们开始使用解构声明时，Kotlin 编译器可能会警告我们解构声明中存在未使用的变量。IDE 的默认解决方案是将未使用的变量重命名为“\_”（ **下划线** ），但这存在一些缺点。例如，我们尝试从其他地方复制粘贴一些代码：

```kotlin
val usersData = mutableListOf<User>()
for ((_, _, isAdmin) in usersData) {
    // /~
}
```

看起来很眼熟，对吧？在上面的例子中， `componentN` 运算符跳过了 `name` 和 `age` 属性，因此它们不能在循环中使用。

另一个实用功能是 **尾随逗号** 。你可以在参数列表末尾添加逗号，它就能正常工作。这非常方便，因为你可以复制粘贴额外的参数而无需添加逗号。

```kotlin
val usersData = mutableListOf<User>()
for ((name, age, ) in usersData) {
    // /~
}
```

## 结论

解构声明是一种便捷的特性，它允许以类似元组的方式声明新变量，从而生成更简洁易读的代码。然而，它的位置机制与类变量的关联性本质上不同，这可能会导致错误。

200 名学员喜欢这篇理论文章， 8 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
