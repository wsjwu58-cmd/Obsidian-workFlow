提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

继承是我们之前在讨论类时已经介绍过的一个概念。它通过引入创建类扩展（甚至是类模型或抽象）的方法，极大地减少了样板代码的数量，这些扩展可以在以后实现。

当我们需要某个类继承另一个类的属性并扩展它的功能，而无需重复编写代码时，就可以使用继承。简而言之，当我们需要创建的类与已有的类有一些共同之处时，继承就非常有用。

## 接口继承

同样的模式也适用于接口，但它们更进一步。Kotlin 中的类不能继承多个，但它们可以实现多个接口（类可以继承基类，而基类又可以继承另一个类，但这与的一般概念并不完全相同）。

类和语法相同：新接口的名称放在冒号 ( `:` ) 之前，位于 `interface` 关键字之后；冒号之后是基接口的名称——新接口继承其属性的接口：

```kotlin
interface Animal {
    val amountOfLimbs: Int
    fun move()
    fun communicate()
}

interface Bird : Animal {
    val canFly: Boolean
    val flyingSpeed: Int
    fun buildNest()
}
```

在这个例子中，由于鸟类具有一些动物的属性和特征，因此 `Bird` 接口是从 `Animal` 接口派生而来，同时添加了一些它自己的方法和属性。

## 派生接口的实现

实现派生接口的主要规则是，类必须同时实现基接口和派生接口中的方法和属性：

```kotlin
interface Animal {
    val numberOfLimbs: Int
    fun move()
    fun communicate()
}

class Parrot : Bird // : Animal
{
    // These properties are inherited from the Animal interface...
    override val numberOfLimbs: Int = 2

    override fun move() {
        fly()
    }

    override fun communicate() {
        speak()
    }

    // ...while these ones are specifically from the Bird interface

    override val canFly: Boolean = true

    override val flyingSpeed: Int = 20

    override fun buildNest() {
        collectMaterials()
        findGoodPlace()
        buildSmallNest()
    }
}
```

在这个例子中， `Parrot` 是一种鸟，而鸟是一种动物，所以 `Parrot` 既具有 `Bird` 的特征，又具有 `Animal` 的特征。

## 多重继承

然而，这并非实现具有多个接口特征的鸟类实例的唯一方法。我们还可以利用 **多重继承** ：一个类可以实现多个不同的接口。

在这里，我们将鸟类的 `Flying` 特性分离到另一个接口中。在实际模拟中，这样做的一个合理理由是，鸟类并非唯一能够飞行的生物，因此我们可以让 `Insect` 类（或接口）也实现 `Flying` 接口。

```kotlin
interface Bird : Animal {
    fun buildNest()
}

interface Flying {
    val flyingSpeed: Int
    val flyingManeuverability: Int
}

class Owl : Bird, Flying {

    // Flying interface
    override val flyingSpeed: Int = 100
    override val flyingManeuverability: Int = 95

    // Bird interface
    override fun buildNest() {
        buildSmallNest()
    }

    // Animal Interface
    override val numberOfLimbs: Int = 2

    override fun move() {
        fly()
    }

    override fun communicate() {
        coo()
    }

}

// Reusing the Flying interface
interface Insect : Flying
{
    // ...
}

class Fly : Insect, Animal {
    // ...
}
```

然而，有时当一个类实现多个接口时，我们可能会遇到它继承了同一个方法或属性的多个实现的情况。这会导致冲突，我们将在下一节讨论如何解决这些冲突。

## 继承自多个接口

就像类可以实现多个接口一样，一个接口也可以派生自多个其他接口。

```kotlin
interface FlyingBird : Bird, Flying  
{  
    /* ... */  
}
```

那么我们的 `Owl` 类看起来就会像这样：

```kotlin
class Owl : FlyingBird {  
  
 // FlyingBird interface, derived from Flying
 override val flyingSpeed: Int = 100  
 override val flyingManeuverability: Int = 95  
  
 // FlyingBird interface, derived from Bird
 override fun buildNest() {  
        buildSmallNest()  
    }
    
    /* ... */

}
```

## 结论

现在你知道，继承作为程序员工具箱中的一项重要工具，不仅可以应用于类，还可以应用于接口，从而构建更加复杂的结构或层次。我们不仅可以从一个接口继承，而这个接口本身又可以继承自另一个接口，而且我们还可以做一些仅使用类无法实现的事情——例如同时从多个接口继承属性——这就像创建一个用逗号分隔的列表一样简单。

99 名学员喜欢这篇理论文章， 1 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
