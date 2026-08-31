提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

Kotlin 语言不允许直接重写构造函数。但是，通过继承和多态，我们可以在子类中扩展父类的构造函数。本主题将讨论如何实现这一点。

## Kotlin 构造函数简介

**构造函数** 是创建类时调用的一种特殊方法。它用于类的属性。

在 Kotlin 中，构造函数有两种类型：

- **主构造函数** ：它在类头中声明，可以包含初始化类属性的参数。
- **辅助构造函数** ：它在类体内部声明，可以有各种参数。
```kotlin
class Person(val name: String) {  // Primary constructor

    constructor(name: String, age: Int) : this(name) {  // Secondary constructor
        // Initialization code
    }
}
```

## 覆盖的基本原则

在面向对象编程 (OOP) 的背景下， **重写** 是一种机制，它允许子类提供其对父类中已定义的方法的实现。

遗憾的是，在 Kotlin 中（像大多数其他编程语言一样），构造函数不能直接重写。

```kotlin
open class Person(val name: String) 

class Employee(name: String, val id: Int) : Person(name)  // In this case, we use the superclass 
                                                          // constructor but do not override it.
```

## Kotlin 中的构造函数重写

如前所述，Kotlin 中构造函数不能被重写。但是，你可以在子类中定义构造函数，这些构造函数可以使用或“扩展”父类的构造函数。

声明子类时，我们可以使用关键字 `open` 、 `final` 和 `override` 来控制继承和多态性。

- `open` ：允许子类继承或重写函数和属性。
- `final` ：它阻止子类重写函数或属性。
- `override` ：子类可以使用它来覆盖超类的函数或属性。
```kotlin
open class Person(open val name: String)

class Employee(override val name: String, val id: Int) : Person(name)  // We override the property name.
```

在处理继承和多态的构造函数时，可能会出现一些常见的错误和问题。其中最常见的错误之一是在子类中没有调用父类的构造函数：

```kotlin
open class Person(val name: String)

class Employee(val id: Int) : Person // Error: superclass constructor call is required
```

## 构造函数重写在实践中

尽管 Kotlin 中不能直接重写构造函数，但在定义子类时仍然可以使用超类的构造函数，这是面向对象编程中继承的一个重要元素。

```kotlin
open class Person(val name: String) {
    fun talk() {
        println("$name is talking")
    }
}

class Employee(name: String, val id: Int) : Person(name) {
    fun work() {
        println("$name is working with id $id")
    }
}

fun main() {
    val person = Person("John")
    person.talk()  // Outputs: John is talking

    val employee = Employee("Jane", 123)
    employee.talk()  // Outputs: Jane is talking
    employee.work()  // Outputs: Jane is working with id 123
}
```

在上面的例子中， `Employee` 类继承自 `Person` 类，并使用其构造函数设置 `name` 属性。这是一个继承的例子，其中子类（ `Employee` ）使用了父类（ `Person` ）的构造函数。Employee `Employee` 还添加了一个新的属性 `id` 。

在 `main` 函数中，我们创建了 `Person` 和 `Employee` 两个类的实例。这两个实例都调用了 `talk` 方法。尽管 `talk` 方法定义在 `Person` 类中，但由于继承关系， `Employee` 类的实例也可以使用它。work `work` 是 `Employee` 类特有的，只能在 `Employee` 的实例上调用。

## 结论

理解 Kotlin 中构造函数使用方法的关键概念是继承和多态。遗憾的是，Kotlin 不支持直接重写构造函数，但可以在创建子类时扩展父类的构造函数，这在面向对象编程中扮演着重要角色。请注意，在 Kotlin 和许多其他语言中，“重写构造函数”通常指的是在创建子类时使用或“扩展”父类的构造函数，而不是直接重写它们。

37 名学员喜欢这部分理论内容， 11 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
