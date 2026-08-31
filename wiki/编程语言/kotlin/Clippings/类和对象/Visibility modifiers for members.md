## 成员可见性修饰符

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

所有类成员——字段、方法和属性——都有可见性。可见性修饰符允许您为类成员设置有效作用域。也就是说，它们定义了给定变量或方法可以使用的上下文。可见性修饰符是特殊的关键字，用于定义代码的哪一部分可以使用它们。Kotlin 中有四个访问修饰符： **\`private\`** 、 **\`protected\`** 、 **\`internal\`** 和 **\`public\`** 。

## 公众成员

`public` 用于告诉编译器某些内容应该对所有人开放。通过将类的实例声明为 \`public\` 修饰符，你可以在程序中任何可以访问该对象的地方引用它的任何字段。

```kotlin
public class Student {

    public var name: String   // property is public and visible everywhere

}
```

## 私人会员

同时， `private` 修饰符与 `public` 正好相反。使用 `private` 时，数据仅在特定类中可用。让我们通过添加 \`private\` 访问修饰符和一个新的变量 `id` 来使前面的示例更加复杂。如果属性是通过构造函数设置的，那么也可以在构造函数中为属性指定可见性修饰符：

```kotlin
class Student(val name: String, private val id: Int)
```

如您所见，由于 `id` 具有私有修饰符，因此从外部无法访问它：

```kotlin
val mark: Student = Student("Mark", 01)

println("Name: ${mark.name}  Id: ${mark.id}")  //Cannot access 'id': it is private in 'Student'
```

为了防止字段被篡改，我们使用了 \` `private` 关键字——它使得类的成员仅在类内部可用。现在，除了该类的方法之外，这些字段无法在任何地方被修改。但是，您也无法从外部获取它们的值，任何输出尝试都会导致错误。

我们可以使用后备属性来定义 getter 和 setter，并对私有字段进行更多控制。

## 受保护成员

`protected` 与 `private` 区别在于，protected 可以在子类中使用。例如：

```kotlin
open class Person {
    protected open val name: String = ""
    private val age: Int = 0
}

class Student : Person() {
    override val age = 18 // age is private and this will NOT work
    override val name = "Eyad" // this will work
}

class Teacher {
    private val person = Person()

    fun printPerson(): String {
        return person.name // Cannot access 'name': it is protected in 'Person'
    }
}
```

## 内部成员

`internal` 修饰符表示，看到声明类的人可以看到它的 `internal` 成员：

```kotlin
class Bank {
    internal val accountNumber: Long = 5L

    internal fun getBranch(): String {
        return "Branch is Alex"
    }
}

class BankController {
    private val bank = Bank()

    fun getUserAccountNumber(): Long {
        return bank.accountNumber // same module
    }
}
```

## 类中构造函数的可见性

你还可以为构造函数指定修饰符：例如，将类的设为私有。请记住添加显式的 `constructor` 关键字：

```kotlin
class Student private constructor(val name: String) {
    var age: Int = 0

    constructor(name: String, _age: Int) : this(name) {
        age = _age
    }
}
```

在这种情况下，主构造函数是私有的，因此只能从同一个类内部访问（例如，调用时）。相应地，从外部创建此类的对象，只能使用辅助构造函数：

```kotlin
val anna: Student = Student("Anna")     //Cannot access '<init>': it is private in 'Student'
val mark: Student = Student("Mark", 23)

println("Name: ${anna.name}  Age: ${anna.age}")
println("Name: ${mark.name}  Age: ${mark.age}")
```

## 公共和私人职能

私有函数用于隐藏内部底层逻辑实现，使公共函数更加简洁易读。以下示例展示了 `printInfo()` 和 `getAge()` 函数。我们将 \` `getAge()` 函数设置为私有，因此该函数无法从外部访问。而 `printInfo()` 函数是公开的，我们可以从中获取学生信息。

```kotlin
fun main() {
    val anna = Student("Anna", 9, 19)
    anna.printInfo()
    anna.getAge()     //Cannot access 'getAge': it is private in 'Student'
}

class Student(
    private val name: String,
    private val id: Int,
    private val age: Int
) {

    fun printInfo() {
        println("Id: $id Name: $name")
    }

    private fun getAge() {
        print("Age: $age ")
    }
}
```

请注意，局部变量和函数不能设置可见性修饰符。局部变量和函数仅在定义它们的函数内部可用。我们稍后会讨论继承和子类。

## 结论

那么，让我们修改一下访问修饰符的名称：

- **公开数据** ——数据随处可得；
- **私有** 数据——仅在类内部可用；
- **受保护的** ——与私有相同，只是数据可以在子类中查看；
- **内部成员** ——谁能看到声明类，谁就能看到它的。

40 名学员喜欢这部分理论， 4 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
