提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

如果你想创建一个超级英雄，你会怎么做？当然，你会打开你最喜欢的开发环境，创建一个 `Superhero` 类！

根据情况，我们的超级英雄需要一套特殊物品，例如魔法斗篷或锤子。这里可能会出现一个问题：如何最好地组织描述这些装备的类别？以及如何表明只有 `Superhero` 类别才能使用这些物品？

这时，我们的救星出现了——类。它们可以帮助我们按逻辑对类进行分组，并提高代码的封装性。

## 什么是嵌套类？

你可以在一个类中创建一个类，这样的类被称为 **嵌套类** 。

来看看我们的超级英雄：

```kotlin
class Superhero {
    class MagicCloak {
    }

    class Hammer {
    }
}
```

`MagicCloak` 和 `Hammer` 这两个类都是嵌套类。Superhero `Superhero` 通常被称为 *，* 而嵌套类及其属性、函数和构造函数都是外部类的 **成员** 。

问题在于， `MagicCloak` 和 `Hammer` 实际上并不与 `Superhero` 绑定，它们只是职业而已：

```kotlin
class Superhero {
    val power = 1000

    class MagicCloak {
        // you cannot access something from Superhero here
        val magicPower = 100
    }
    // you need to create a MagicCloak object to access its members
    val magicPower = power * MagicCloak().magicPower

    class Hammer {
        // you cannot access power property from Superhero here
        val mightPower = 100
    }
    val mightPower = power * Hammer().mightPower
}
```

如果需要在 `Superhero` 类之外使用 `MagicCloak` 和 `Hammer` ，则必须创建相应的对象：

```kotlin
val cloak = Superhero.MagicCloak()
val hammer = Superhero.Hammer()
```

如您所见，简单的嵌套类与外部类实际上并没有关联。在本主题中，我们将重点讨论嵌套类的一个特殊情况——。

## 内层阶级

普通的嵌套类不能访问其外部类的成员。但是，标记为 **内部类的嵌套类可以访问其外部** 类的成员。

我们来看另一个例子。假设你要编写一个名为 `Cat` 类来表示猫。猫可能有很多属性和功能，但我们也可能使用内部类结构。假设你想让一只猫戴上蝴蝶结，那么你需要创建一个新的 `Bow` 。这个 `Bow` 类需要非常小且具体，而且你知道没有猫就不会有蝴蝶结。解决方案是在 `Cat` 类内部创建一个 `Bow` 类：

```kotlin
class Cat(val name: String) {
    inner class Bow(val color: String) {
        fun printColor() {
            println("The cat named $name has a $color bow.")
        }
    }
}
```

我们来创造一只名叫鲍勃、系着红色蝴蝶结的猫：

```kotlin
fun main() {
    val cat: Cat = Cat("Bob")
    val bow: Cat.Bow = cat.Bow("red")

    bow.printColor()
}
```

我们创建了一个 `Cat` 实例，然后使用一种非常有趣的语法创建了一个 `Bow` 实例。

上述代码的输出结果为：

```
The cat named Bob has a red bow.
```

请记住，要使用内部类，我们必须创建外部类的实例 *。* 在我们的示例中，我们创建了一个 `Cat` 。您可以在外部类中自由使用内部类：

```kotlin
class Cat(val name: String) {
    inner class Bow(val color: String) {
        fun printColor() {
            println("The cat named $name has a $color bow.")
        }
    }
    val catBow = Bow("Green")
}
```

## 内部类的作用域

现在我们来讨论一下从内部类中可以看到什么，以及谁可以从外部访问内部类。

这是我们的 `Cat` 类，其中包含一个新函数 `sayMeow` ，以及一个内部类 `Bow` ，其中包含一个新函数 `putOnABow` 。

```kotlin
class Cat(val name: String) {
    fun sayMeow() {
        println("$name says: \"Meow\".")
    }

    inner class Bow(val color: String) {
        fun putOnABow() {
            sayMeow()
            println("The bow is on!")
        }

        fun printColor() {
            println("The cat named $name has a $color bow.")
        }
    }
}
```

你可以看到，在 `Bow` 类中，我们可以访问 `Cat` 类的所有成员： `name` 属性和 `sayMeow` 函数。

为了证明我们的代码有效，我们不妨创建一个名叫“公主”并系上金色蝴蝶结的猫咪？

```kotlin
fun main() {
    val cat: Cat = Cat("Princess")
    val bow: Cat.Bow = cat.Bow("golden")

    bow.printColor()
    bow.putOnABow()
}
```

是的，弓已经搭好了！

```
The cat named Princess has a golden bow.
Princess says: "Meow".
The bow is on!
```

你可能会遇到内部类成员与其外部类同名的情况。例如， `Cat` 和 `Bow` 都可能拥有 `color` 属性。在这种情况下，如何从内部类访问外部呢？ [限定的 this](https://kotlinlang.org/docs/this-expressions.html#qualified-this) 表达式可以帮到你！在内部类代码中写入 `this@Cat.color` 即可获取外部类的颜色值，而使用 `color` 或 `this.color` 则始终返回当前类的 color 属性值。

```kotlin
class Cat(val name: String, val color: String) {
    inner class Bow(val color: String) {
        fun printColor() {
            println("The cat named $name is ${this@Cat.color} and has a $color bow.")
        }
    }
}
```

现在让我们把所有规则汇总起来！

## 内类规则

内部类可以访问其外部类的所有成员。

要访问内部类，需要先实例化外部类，因为内部类与其包含类的相关联。在下面的示例中，内部类 `Inner` 的构造函数被调用，并传入包含类的实例：

```kotlin
val outer = Outer()
val inner = outer.Inner()
```

## 使用内部类的理由

你注意到我们的 `Superhero` 和 `Cat` 例子有什么共同点了吗？当然注意到了——我们都对外部世界隐藏了内部类。这提高了代码的 **封装性** ——现在只有 `Cat` 才能戴蝴蝶结了。

使用内部类结构，您可以更方便地 **组织** 代码。所有 `Superhero` 的魔法装备都集中在一个地方，这样更容易在类之间切换，也更容易理解代码结构。

## 结论

- 在一个类内部声明的类称为嵌套类。
- 内部类是嵌套类的一种特殊情况，它可以访问其外部类的成员。
- 内部类携带对外部类对象的引用，因此要使用内部类，我们必须先实例化一个外部类。
- 内部类的主要思想是隐藏部分代码，使其不被其他类直接访问，从而提高封装性。

272 名学习者喜欢这篇理论文章， 8 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
