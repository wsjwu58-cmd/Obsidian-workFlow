## 可比对象和比较对象

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在 Kotlin 中，Comparable 和 Comparator 是两个接口，允许开发者比较相同或不同类的对象。这两个接口通常用于根据一个或多个属性对对象集合进行排序。本文将概述 Kotlin 的 Comparable 和 Comparator 接口，解释它们的用法，并阐述它们之间的区别。

## Kotlin 可比接口

Comparable 接口用于定义对象的自然排序。当一个类实现 Comparable 接口时，它必须重写 **compareTo()** 方法：

```kotlin
public operator fun compareTo(other: T): Int
```

该方法接受一个与参数类型相同的对象，并返回一个整数值。该整数值指示该对象是小于（返回 -1）、等于（返回 0）还是大于（返回 1）被比较的另一个对象。

例如，请看以下代码：

```kotlin
data class Person(val name: String, val age: Int): Comparable<Person> {
  override fun compareTo(other: Person): Int {
    return this.age - other.age
  }
}
```

在这段代码中， `Person` 类实现了 并重写了 `compareTo()` 方法。compareTo `compareTo()` 方法根据年龄比较 `Person` 对象，如果当前对象的年龄小于另一个对象的年龄，则返回一个负整数；如果当前对象的年龄大于另一个对象的年龄，则返回一个正整数；如果两个对象的年龄相等，则返回零。

现在，如果我们有一个 `Person` 对象列表，我们可以按年龄对其进行排序，如下所示：

```kotlin
val people = listOf(Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20))
val sortedPeople = people.sorted()
```

在这段代码中， `sorted()` 函数使用 `compareTo()` 方法定义的自然顺序对 `Person` 对象列表进行排序。

实现 Comparable 接口的类支持一些有用的扩展函数，其中包括以下函数：

**coerceAtLeast()** – 此函数检查调用对象是否大于某个最小对象。如果大于，则返回当前对象；否则，返回最小对象。

```kotlin
fun <T : Comparable> T.coerceAtLeast(minimumValue: T): T
```

例子：

```kotlin
fun main() {
    val people = listOf(
        Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20)
    )

    val minimum = Person("Jack", 28)
    println(people[0].age.coerceAtLeast(minimum.age)) // 28
    println(people[1].age.coerceAtLeast(minimum.age)) // 30
}
```

**coerceAtMost()** – 此函数检查调用对象是否小于给定的最大对象。如果小于，则返回当前对象；否则，返回最大对象。

```kotlin
fun <T : Comparable> T.coerceAtMost(maximumValue: T): T
```

例子：

```kotlin
fun main() {
    val people = listOf(
        Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20)
    )

    val maximum = Person("Jack", 28)
    println(people[0].age.coerceAtMost(maximum.age)) // 25
    println(people[1].age.coerceAtMost(maximum.age)) // 28
}
```

**coerceIn()** – 此函数检查调用对象是否在最小值和最大值之间的指定范围内。如果对象在范围内，则返回对象本身；如果对象小于最小值，则返回最小值；如果对象大于最大值，则返回最大值。

```kotlin
fun <T : Comparable> T.coerceIn(
    minimumValue: T?, 
    maximumValue: T?
): T
```

例子：

```kotlin
fun main() {

    println(25.coerceIn(18..28)) // 25
    println(15.coerceIn(18..28)) // 18
    println(30.coerceIn(18..28)) // 28
}
```

## Kotlin 比较器接口

Comparator 接口用于定义对象的自定义排序方式。当一个类实现 Comparator 接口时，它必须重写 **compare()** 方法。该方法接受两个相同类型的对象作为参数，并返回一个整数值。如果两个参数相等，则返回 0；如果第一个参数小于第二个参数，则返回负数；如果第一个参数大于第二个参数，则返回正数。其工作原理如下：

```kotlin
data class Person(val name: String, val age: Int)

class PersonAgeComparator : Comparator<Person> {
    override fun compare(p1: Person, p2: Person): Int {
        return p1.age - p2.age
    }
}
```

在这个例子中，我们有一个 `Person` 和一个 `PersonAgeComparator` 类，后者实现了 `Comparator<Person>` 接口。compare `compare()` 方法接受两个 `Person` 对象作为参数，并比较它们的年龄。如果 `p1` 的年龄小于 `p2` 的年龄，则返回一个负数；如果 `p1` 的年龄大于 `p2` 的年龄，则返回一个正数；如果年龄相等，则返回 0。

Comparator 接口实例的使用示例：

```kotlin
data class Person(val name: String, val age: Int)

fun main() {
    val ageComparator = Comparator<Person> { p1, p2 -> p1.age - p2.age }

    val people = listOf(
        Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20))
    val sortedPeople = people.sortedWith(ageComparator)
    println(sortedPeople)
}
```

打印输出：

```kotlin
[Person(name=Charlie, age=20), Person(name=Alice, age=25), Person(name=Bob, age=30)]
```

在这段代码中， `ageComparator` 是 Comparator 接口的一个实例，它根据年龄比较 `Person` 对象。sortedWith `sortedWith()` 函数使用 `ageComparator` 定义的自定义排序规则对 `Person` 对象列表进行排序。

Comparator 接口包含一些有趣的方法，其中包括以下几种：

**reversed()** – 此函数接受一个比较器作为参数，并返回一个与传入的比较器顺序相反的比较器：

```kotlin
fun <T> Comparator<T>.reversed(): Comparator<T>
```

例子：

```kotlin
data class Person(val name: String, val age: Int)

fun main() {
    val ageComparator = Comparator<Person> { p1, p2 -> p1.age - p2.age }.reversed()

    val people = listOf(
        Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20))
    val sortedPeople = people.sortedWith(ageComparator)
    println(sortedPeople)
}
```

打印输出：

```kotlin
[Person(name=Bob, age=30), Person(name=Alice, age=25), Person(name=Charlie, age=20)]
```

您可以在 [Kotlin 文档](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-comparator/) 中查看更多方法。

## 可比对象与比较对象之间的差异

Comparable 和 Comparator 的主要区别在于，Comparable 定义了对象的自然顺序，而 Comparator 定义了对象的自定义顺序。当比较同一类的对象时，建议实现 Comparable 接口以提供自然顺序。当比较不同类的对象或需要自定义顺序时，建议实现 Comparator 接口。

## 结论

Comparable 和 Comparator 是强大的接口，允许开发者基于一个或多个属性对对象集合进行排序。比较同一类的对象时，实现 Comparable 接口可以提供自然的排序。比较不同类的对象或需要自定义排序时，实现 Comparator 接口。Kotlin 标准库提供了许多接受 Comparator 接口的函数，使开发者能够以简单高效的方式对集合进行排序。现在，让我们解决一些问题来更好地记住这些内容。

52 名学员喜欢这篇理论文章， 5 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
