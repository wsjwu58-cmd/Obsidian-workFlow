提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

你还记得 [枚举](https://hyperskill.org/learn/step/6245 "In Kotlin, enums are a container for a collection of constants. | They are a convenient way to store a fixed set of values, such as the days of the week or the suits in a deck of cards. Enums in Kotlin come with embedded properties and methods that allow you to access the name and order of the constants. You can retrieve all instances of an enum or just one of them. Additionally, you can extend your enum with custom behavior. Enums are a useful tool for improving code organization and readability. For example, you might create an enum for the colors of the rainbow, or for the status of an order.") 吗？枚举是用来存放 [常量](https://hyperskill.org/learn/step/10698 "In Kotlin, a constant is a type of property that is declared with the `val` keyword and cannot be modified once assigned. | Constant values are known at compile time and must be initialized with a value of a basic type. They should be named using screaming\_snake\_case. Constant variables can be accessed multiple times during program execution, but their value remains unchanged. Additionally, Kotlin provides the `const` keyword for declaring compile-time constant values, which can be used for top-level constants. Using constants is a good practice that can help avoid errors and make the code more readable.") 集合的容器。今天我们要讨论另一种容器——用于存放固定：或密封接口。让我们开始吧。

## 基本语法

要声明一个密封类或接口，我们只需要在类或接口前面加上 `sealed` [修饰符](https://hyperskill.org/learn/step/31660 "In Kotlin, a modifier is a keyword used to define the accessibility and mutability of variables or members of a class. | For instance, the `var` keyword is a modifier that indicates a variable can be changed, while `val` indicates a variable is immutable. Additionally, modifiers such as `private` and `public` determine the scope of variable or class visibility. For example, a property declared with the `private` modifier can only be accessed within the same file or class, while a `public` modifier allows it to be accessed from anywhere in the program where the object is available.") 即可：

```kotlin
sealed class CustomError 
sealed interface CustomErrors
```

由于密封类和密封很相似（唯一的区别在于类和接口），我们将只继续使用密封类示例。

密封类是，因此不能被实例化。以下代码会报错：

```kotlin
fun main() {
    // Sealed types cannot be instantiated
    val customError = CustomError()
}
```

当然，你可以 [延长](https://hyperskill.org/learn/step/7770 "In Kotlin, extend is a keyword used to create a subclass or a derived class that inherits properties and methods from a superclass or a base class. | It allows for code reuse and facilitates the implementation of inheritance hierarchy. When a class is extended, the subclass can inherit all the members (properties and methods) of the superclass, and it can also add new members or override existing ones. This way, the subclass can build upon the functionality of the superclass and provide additional features.") 它。

与普通类一样，你可以声明构造函数，但密封类中的构造函数必须是私有的或 [受保护的](https://hyperskill.org/learn/step/31660 "In Kotlin, the `protected` keyword is used to make a member of a class available only within the class itself and its subclasses. | This means that the member cannot be accessed from outside the class hierarchy. It provides a way to protect the member from tampering and ensures that the member can only be modified within the class or its subclasses. However, it also means that the member cannot be accessed from outside the class hierarchy, including any attempts to output its value. The `protected` modifier is similar to `private`, but with the added ability to be seen in subclasses. When a member is declared with the `protected` modifier, any subclass of the declaring class can see and access the member. This is in contrast to `private`, which makes the member completely inaccessible from outside the class. Using access modifiers like `protected` is a valuable tool in safeguarding communication and preserving the authenticity, integrity, and confidentiality of data.") ：

```kotlin
sealed class CustomError {
    
    constructor(type: String) {} // protected (default) 
    private constructor(type: String, code: Int) {} // private
    public constructor() {} //  Public gives error
}
```

你也可以像在任何普通类中一样使用 [主构造函数](https://hyperskill.org/learn/step/10740 "In Kotlin, a primary constructor is a special type of constructor that is declared as part of the class header, after the class name. | It can have parameters that are used to initialize class properties directly or within an initializer block. The primary constructor cannot contain any code, but initialization code can be placed in initializer blocks. If a class requires more complex initialization that cannot be covered by the primary constructor, secondary constructors can be used. These secondary constructors must delegate to the primary constructor either directly or indirectly through another secondary constructor.") ：

```kotlin
//primary constructor 
sealed class CustomError(type: String)
```

## 密封类与枚举

理解密封类的最佳方法之一是将其与枚举进行比较。简而言之，密封类类似于枚举，但更加灵活。这意味着什么呢？请看下面的例子：

```kotlin
enum class Staff(numberOfLessons: Int)  {
    TEACHER(2), MANAGER("Manager is managing")
}
```

枚举类型无法做到这一点，但密封类可以做到：

```kotlin
sealed class Staff {
    class Teacher(val numberOfLessons: Int) : Staff()
    class Manager(val Responsibility: String) : Staff()
    object Worker : Staff()
}
```

枚举常量只有一种类型，而密封类则提供了多个实例，具有更大的灵活性。我们可以得出结论：枚举用于表示一组固定的值，而密封类用于表示一组与其相同的固定子类。

枚举类型不能继承自类或接口，而密封类可以。请看下面的例子：

```kotlin
open class Person {
    fun whoAmI(name: String): String {
        return "I am $name"
    }
}

sealed class Staff : Person() {
    class Teacher(val numberOfLessons: Int) : Staff()
    class Manager(val Responsibility: String) : Staff()
    object Worker : Staff()
}

fun main() {
    val worker = Staff.Worker
    println(worker.whoAmI("Worker"))
}
```

我们声明了一个简单的 `Person` 类，它有一个，然后创建了一个密封类 `Staff` 来继承它，这赋予了我们之前讨论过的 [继承](https://hyperskill.org/learn/step/7770 "In Kotlin, inheritance is a mechanism that allows a class to inherit the properties and methods of another class, called the base or parent class. | This concept helps reduce boilerplate code by enabling the creation of extensions of a class or class model, which can be implemented later. Inheritance is used when the new class being created has something in common with an existing class. In Kotlin, a class can inherit from only one base class but can implement several interfaces. When a class inherits from a base class with constructor parameters, the derived class should take care of them. If the base class does not have any constructor parameters, the derived class can simply inherit from it by using empty parentheses. Inheritance ensures that both the base and derived classes are correctly initialized, and the derived class can take advantage of the base class's multiple constructors to create its own constructor scheme.") 能力。在 `main` 方法中，我们调用了 `worker` 中 `Person` 的方法。就这样。

另一方面，如果我们尝试使用枚举类型来实现这一点，则会抛出错误。下面的代码无法正常工作：

```kotlin
enum class Staff : Person() {
    //...//
}
```

## 密封类和 when 表达式

密封类通常与 `when` 表达式一起使用，因为每个类都被视为一个 case。举个例子：

```kotlin
sealed class Staff {
    class Teacher(val numberOfLessons: Int) : Staff()
    class Manager(val Responsibility: String) : Staff()
    object Worker : Staff()
}

fun listTheTasks(staff: Staff) = when (staff) {
    is Staff.Teacher -> println("The teacher has ${staff.numberOfLessons} lessons today")
    is Staff.Manager -> println("The manager is doing ${staff.Responsibility} today")
    Staff.Worker -> println("Worker is fixing the projector for profs in CS, all respect to him.")
}
```

我们声明了一个名为 `Staff` 密封类，其中包含两个类和一个对象。在没有状态的情况下，对象更合适。然后我们创建了一个名为 `listTheTasks` 函数。请注意，当对象是类时，\` `is` 必需的，而当是类时则不需要。由于我们已经处理了所有情况，所以没有 `else` 。

让我们运行一下这个函数：

```kotlin
fun main() {
    val teacher = Staff.Teacher(3)
    val worker = Staff.Worker
    listTheTasks(teacher)
    listTheTasks(worker)

}

// output:
// The teacher has 3 lessons today
// Worker is fixing the projector for profs in CS, all respect to him.
```

## 直接子类的位置

最后，还有一点需要注意。密封类和接口的直接子类必须声明在同一个包中。而间接子类则不受此限制。你可能会问，什么是直接子类和间接子类？下面我们用一个简单的例子来解释：

```kotlin
open class B : A() // class B is direct subclass of class A 
open class C : B() // class C is indirect subclass of class A and direct subclass of class B
```

如果父类和子类之间没有类，则为直接类。

官方 [文档](https://kotlinlang.org/docs/sealed-classes.html) 中写道：“密封类的所有直接子类在编译时都是已知的。密封类所在的模块/包之外，不会出现其他子类。”

## 结论

在本主题中，我们了解到密封类，顾名思义，“密封”限制了类层次结构，这在我们想要表示一组固定的子类时非常有用。

我们还了解到，密封类类似于枚举，但更加灵活。此外，我们也了解了如何将其与 `when` 结合使用，最后，我们讨论了密封类中类层次结构的限制。现在，让我们来练习一下。

44 名学员喜欢这部分理论内容， 8 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
