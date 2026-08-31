提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

## 编写成员功能

有时，你需要将数据本身以及行为都存储在对象中。为属于同一类的所有对象实现通用行为。

成员函数看起来像是放置在中的函数。在下面的示例中，我们声明了一个包含一个名为 `print()` 的函数的类：

```kotlin
class MyClass {
    fun print() = println("Hello from print")
}
```

这个函数被称为 **成员** 函数，因为它操作类的特定对象并可以访问其字段。它是一个：

```kotlin
class MyClassWithProperty(var property: Int) {
    fun printProperty() {
        println(this.property)
    }
}
```

您可能还记得， `this` 表示类的当前。在上面的示例中，它是一个可选关键字，因此您可以省略它。

与函数一样，成员函数可以接受参数并返回任何类型的值，包括与已定义类相同的类型。

> [!primary] Primary
> 注意， 成员函数 是 Kotlin 中对位于类内部的函数的 **正式名称** 。这类函数通常被称为 方法 。

## 调用成员函数

我们来看下面的例子。它会打印出特定对象字段的值：

```kotlin
val myObject = MyClassWithProperty(10)
myObject.printProperty()  // prints "10"
```

所以，要调用成员函数，你需要创建一个类的对象。然后，在对象名称后面加一个点，并在括号中写出函数名称以及所需的参数。

## 以猫为例

举个更复杂的例子，我们考虑一个表示猫的类。

猫会睡觉。此外，猫会发出两种声音中的一种：“喵”或“zzz”。这取决于它的状态。最后，猫是可以被叫醒的。

这里我们添加了一些给课程成员的注释。阅读这些注释有助于更好地理解课程的逻辑。

```kotlin
import kotlin.random.Random // library for getting random numbers

class Cat(val name: String) {

    /** The current state of the cat (by default a cat isn't sleeping). */
    var sleeping: Boolean = false

    /**
     * A cat says "meow" if it is not sleeping, otherwise, it says "zzz".
     * After a cat says "meow", it can sometimes fall asleep.
     */
    fun say() {
        if (sleeping) {
            println("zzz")
        } else {
            println("meow")

            if (Random.nextDouble() < 0.1) { //generates a double value between 0 and 1.0 
                sleeping = true
            }
        }
    }

    /** The function wakes the cat. */
    fun wakeUp() {
        sleeping = false
    }
}
```

现在，我们可以创建一个类的实例并调用它的函数。别忘了，你刚刚创建的这只猫可不是在睡觉。

```kotlin
fun main() {
    val pharaoh = Cat("Pharaoh")  // Create a cat named "Pharaoh"

    repeat (5) {
        pharaoh.say()  // it says "meow" or "zzz"
    }

    pharaoh.wakeUp()  // wake the cat up
    pharaoh.say()  // it says "meow"
}
```

由于 `say` 函数内部使用了 `Random.nextDouble()` 程序的输出结果可能会有所不同。以下是一个可能的输出示例：

```
meow
meow
meow
zzz
zzz
meow
```

因此，成员函数允许程序员操作类的特定对象并执行某些操作。与以往一样，函数将一系列操作组合在一个有意义的名称下。

617 名学习者喜欢这篇理论文章， 10 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
