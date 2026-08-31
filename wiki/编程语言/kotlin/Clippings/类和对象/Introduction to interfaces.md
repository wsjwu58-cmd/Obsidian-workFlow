提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

有时，在使用类时，我们大概知道一个类应该做什么，但我们并不需要——或者由于某些原因无法——一次性编写整个类的代码。这时， **接口** 就派上用场了。让我们来看看接口是什么，以及它们是如何工作的。

## 什么是接口？

想象一下，你想养只宠物，但还没决定养猫、狗，还是蜥蜴。你只希望你的宠物能在屋里跑来跑去，发出一些声音。很多宠物都能做到这一点，即使它们的方式各不相同。所以，只要我们知道它们能做到我们想要它们做的事，任何宠物都符合你的定义。接口，或者说实现类的契约，也是如此：接口定义了实现类必须拥有的方法和属性。一个类可以用自己的方式实现这些方法，但只要它能完成它应该做的事情，我们就没问题。

我们已经熟悉类的概念——它是面向对象编程中不可或缺的一部分。例如，如果我们正在编写一个模拟程序或游戏，其中会用到动物，我们就可能需要一些类来表示它们：

```kotlin
class Cat() {
    val numberOfLimbs: Int = 4
    fun move() {
        run()
    }

    fun communicate() {
        sayMeow()
    }
}

class Parrot {
    val numberOfLimbs: Int = 2
    fun move() {
        fly()
    }

    fun communicate() {
        talk()
    }
}
```

一般来说，如果我们需要实现同一类别的多个实体，它们必须具有一些共同的属性。就像上面的例子一样：尽管这些动物之间存在明显的差异，但它们都有四肢，并且都具备移动和某种形式的交流能力。

接口提供了一种构建类骨架的方法。就我们的目的而言，我们可以说所有动物都具有：

- 一定数量的肢体；
- 行动能力；
- 沟通能力。

因此，我们为某一类动物构建的“骨架”必然包含腿的数量以及 `move` 和 `communicate` 方式等字段。这可以通过使用接口来实现。

重要提示：所有动物都各不相同。鸟类和猫的运动方式截然不同：鸟类用翅膀飞行，而猫则用脚跳跃和奔跑。接口无需了解具体细节：它只需声明如果 X 是一种动物，那么它就可以移动。具体的移动方式取决于接口的实现——即实现该接口的类。

把它想象成一个输入输出固定的盒子。我们不知道里面发生了什么，但只要我们知道它是一只 `Animal` ，它就能 `move` 。不管用什么方式。

## 执行

在 Kotlin 中，接口的定义方式与类类似，只是没有构造函数——接口不能存储状态。

这意味着我们不能创建接口的，但我们可以创建实现该接口的类的实例。

```kotlin
interface Animal {
    val numberOfLimbs: Int
    fun move()
    fun communicate(): String
}
```

这里我们有一个简单的接口——一个代表不同动物的类的“框架”。现在，我们只需要学习如何基于这个结构创建类。

简单回顾一下，接口意味着任何实现该接口的对象，在我们的例子中，都需要具备一定数量的腿（或者至少有一个对应的变量）以及用于通信和移动的方法。但是，实现该接口的类可能各不相同，因此在它们各自的具体情况下，这些实现的细节可能会有所不同。猫的移动方式与鸟不同，但由于它们都实现了相同的 `Animal` 接口，因此可以保证它们能够移动，也就是说，在我们的模拟中，它们都拥有 `move` 函数。接口的方法，就像任何其他方法一样，可能会返回一些值（如上例中的 `communicate` ）。

该接口的实现方式与继承另一个类类似：

```kotlin
class MyAnimalClass : Animal {
    /* ... */    
}
```

然后，接口中声明的每个字段或方法都需要在类中使用关键字 `override` 进行声明，因为它表明我们用实现的具体形式“覆盖”了接口的一般情况。  
如果在这个新类中我们需要一些不属于我们正在实现的接口的方法，则应省略 `override` 。

```kotlin
interface Animal {
    fun myAnimalMethod() { /* ... */
    }
    // The body of the method is going to be replaced by the implementation of MyAnimalClass.
}

class MyAnimalClass : Animal {
    override fun myAnimalMethod()
    /* ... */
}
```

## 例子

让我们来看一个更深入的例子，该例子将介绍我们的 `Animal` 界面：

```kotlin
class Cat : Animal {
    override val numberOfLimbs: Int = 4

    override fun move() {
        run()
    }

    override fun communicate(): String {        
        return sayMeow()
    }
}
```

注意：猫是一种动物，具有特定的移动方式，这与界面中所述的所有动物的一般移动能力不同。

```kotlin
class Parrot : Animal {
    override val numberOfLimbs: Int = 2

    override fun move() {
        fly()
    }

    override fun communicate(): String {
        return speak()
    }
}
```

注意：鹦鹉也是一种动物，但它属于特定类型（鸟类），而且它的结构也不同：它只有两条下肢，而且它的移动方式与猫不同。

实现接口时有一点很重要：继承自该接口的类必须实现接口的所有抽象成员（即没有具体实现的函数和方法）。否则，我们会收到错误提示。

```kotlin
class Cat : Animal {
    override val numberOfLimbs: Int = 4

    override fun move() {
        run()
    }

/*  an error here

    override fun communicate(): String {
        return sayMeow()
    }
*/
}
```

注意：请注意，如果我们删除注释部分（本质上是使模拟的猫无法交流），我们将在类声明中收到一个错误，指出我们没有实现接口的成员。

这就像造车一样——如果我们按照蓝图组装，但漏装了一些零件，汽车就无法正常行驶。我们正在实现的类也是如此。

另外，请注意，我们不必重写每个属性或方法：如果它们有（我们将在下一部分讨论），则无需重写。但是，如果默认实现不符合您的目标，则可以进行重写。

## 添加默认实现

由于接口不能维护状态（它只是其他类需要实现的契约），因此我们不能用以下方式构造接口：

```kotlin
interface Animal {
    val numberOfLimbs: Int
    fun move()
    fun communicate(): String
    val age = 10 // Error: Property initializers are not allowed in interfaces
}
```

但是，我们可以使用 getter 来实现同样的效果（不过，你不能使用 setter，因为没有实例可以赋值）：

```kotlin
interface Animal {
    val numberOfLimbs: Int
    fun move()
    fun communicate(): String

    val age: Int
        get() = 10
}
```

由于方法代表一系列操作或某种行为，因此默认实现也适用于它们：

```kotlin
interface Animal {
    val numberOfLimbs: Int
    fun move()
    fun communicate(): String

    val age: Int
        get() = 10

    // Default implementation of a method
    fun printNumberOfLimbs() {
        print(numberOfLimbs)
    }
}
```

注意：默认实现允许您跳过重写派生类中的某些属性或方法，但默认功能不足以满足需求的情况除外。

## 不仅仅是一种模式

目前看来，接口似乎是构建类的一种便捷模式。然而，事实并非如此，因为接口主要用作与特定对象交互的模型。接口可以比作契约，因为使用该接口的对象保证具备接口中定义的一系列特性。因此，我们知道一个类应该具备哪些特性，并且可以确信任何实现了特定接口的类都将拥有 `method1` 和 `method2` 此外，接口还定义了我们与实现该接口的类进行交互的方式。

```kotlin
interface DataHolder {
    val id: Int
    val description: String
    val currentState: String

    fun printInfo()
    fun updateInfo()
    fun clearInfo()
}

class Entity : DataHolder {
    /* some code */
}
```

注意：任何实现了 `DataHolder` 接口的对象，我们都可以预期它将拥有上面列出的方法。

“契约”一词很好地描述了接口的概念，因为在使用接口的实现时，我们可以保证获得某些特定的方法和属性。

## 结论

接口提供了一种简洁的方式来概括我们的代码并保持代码的清晰：首先明确我们期望从类中获得什么，然后我们就可以创建一个后续依赖的结构。如果一个类实现了某些接口，我们就可以预先知道它将拥有这些接口承诺的所有功能。在面向对象编程（OOP）的上下文中，接口体现了抽象和封装的概念。

145 名学员喜欢这篇理论文章， 4 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
