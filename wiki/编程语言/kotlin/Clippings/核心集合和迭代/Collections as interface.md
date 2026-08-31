提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

Kotlin 集合为各种数据操作提供了便捷的方式。它们还实现了接口，因此可以用来操作不同类型的数据。例如，你可以编写一个函数来打印 `Set` 和 `List` 中的每个元素。让我们来看看它是如何工作的。

## 可迭代的

我们已经了解到 Kotlin 中有两个通用接口： `Iterable` 和 `MutableIterable` 。它们提供了处理元素序列的方法。

继承自 `Iterable` 的类都拥有一组通用方法： `iterator()` 、 `forEach()` 、 `contains()` 、 `count()` 、 `drop()` 、 `filter()` 等。与 `Iterable` 不同的是， `MutableIterable` 还支持在迭代过程中移除元素。例如，可以使用 `remove()` 和 `removeAll()` 方法。有趣的是，它们都包含 `drop()` 方法，该方法用于移除特定元素。但与 `MutableIterable` 中的 `remove()` （它会真正移除特定对象中的特定元素）不同， `drop()` 方法会返回一个新对象。

请注意，在遍历 `List` （或 `Set` ）的过程中，每个迭代器只能使用一次。如果想再次使用，则必须创建一个新的迭代器。不过，您也可以将迭代与 `for` 循环或 `forEach()` 结合使用。

## 集合接口

现在，我们来看看 Kotlin 集合中的继承机制。在下面的图中，你可以看到不同类之间的关系。前面我们已经讨论过两个可迭代接口。接口 `Collection<T>` 和 `MutableCollection<T>` 都继承自它们。反过来， `List` 和 `Set` 又继承自 `Collection<T>` ，而 `MutableList` 和 `MutableSet` 则继承自 `MutableCollection<T>` 。

                                                                              ![relationships between different classes in Kotlin collections](https://ucarecdn.com/c42163ac-1820-4e52-9c61-eead8d6637e3/)

`Collection<T>` 是（ `List` 和 `Set` 层次结构的根。它提供了诸如 `size` 、 `get()` 、 `find()` 、 `filter()` 、 `count()` 等方法。MutableCollections `MutableCollections<T>` 是 `MutableList` 和 `MutableSet` 的根，它支持使用以下方法添加和删除元素： `add()` 、 `addAll()` 、 `remove()` 、 `removeAll()` 、 `retainAll()` 和 `drop()` 。

`Collection` 和 `MutableCollection` 分别继承自 `Iterable` 和 `MutableIterable` 。因此，这些接口支持其父接口的所有方法。

然而，尽管我们也称 Map 为集合，但它们并不代表 `Collection` 或 `Iterable` 接口。这意味着 Map 的方法与其他集合不同。这是合乎逻辑的，因为 Map 包含键值对，而 `Set` 或 `List` 只包含单个元素，所以我们需要为它们单独编写方法。遗憾的是，我们不能将 `Map` 与 `Collection` 接口一起使用。

## 收藏

让我们看看如何使用这些接口。例如，我们想要打印集合中的所有元素。在这种情况下，我们可以使用 for 循环、 `iterator()` 或 `forEach()` 方法：

```kotlin
// All realizations of the function printAll do the same thing.

fun printAll(strings: Collection<String>) {
    for(str in strings) print("$str ")
}

fun printAll(songs: Collection<String>) {
    songs.forEach { print("$it ") }
}

fun printAll(songs: Collection<String>) {
    val songsIterator = songs.iterator() // We create iterator, which will help us go through the List

    while (songsIterator.hasNext()) { // hasNext() checks if our iterator contains next element
        print("${songsIterator.next()} ") // next() moves the pointer to the next element of iterator
    }
}

val listOfSongs = listOf("Creep", "Idioteque", "Street Spirit", "Paranoid Android") // We can also use setOf()
printAll(listOfSongs) // Creep Idioteque Street Spirit Paranoid Android
```

太棒了！我们现在可以同时使用 `Set` 和 `List` 这两种不可变集合了。

在遍历 `List` （或 `Set` ）的过程中，每个迭代器只能使用一次。如果想再次使用，则必须创建一个新的 `iterator()` 。

所有集合都有一些通用的方法。

- `count()` 返回满足条件的元素数量。
- `drop()` 返回一个不包含前 `n` 元素的新 `List` 。
- `containsAll()` 检查集合是否包含另一个集合中的所有元素，并返回 `true` 或 `false` 。

例如：

```kotlin
fun countElements(strings: Collection<String>) = strings.count { it.matches("\\w+".toRegex()) }

fun dropElements(songs: Collection<String>) = songs.drop(2).toSet()

fun compareCollections(old: Collection<String>, new: Collection<String>) = old.containsAll(new)

val setOfSongs = setOf("Creep", "Idioteque", "Street Spirit", "Paranoid Android")
val listOfSongs = listOf("Creep", "Idioteque", "Street Spirit", "Paranoid Android")

println(countElements(setOfSongs)) // output: 2
println(dropElements(listOfSongs)) // output: [Street Spirit, Paranoid Android]
println(compareCollections(listOfSongs, setOfSongs)) // output: true
```
- `joinToString()` 将集合作为具有特定分隔符的字符串返回。
- `find()` 返回符合模式的第一个元素。
- `filter()` 返回一个符合条件的元素 `List` 。
- `minus()` 返回不包含条件中指定的元素的集合。
- `random()` 返回集合中的一个随机元素。

例如：

```kotlin
fun convertToString(strings: Collection<String>) = strings.joinToString(" | ")

fun findElement(strings: Collection<String>) = strings.find { it.contains("I") }

fun filterElements(strings: Collection<String>) = strings.filter { it.contains("t") }

fun returnRandomElement(strings: Collection<String>) = strings.random()

fun decreaseCollection(strings: Collection<String>) = strings.minus("Creep") 
// minus could have a collection as parameter

val listOfSongs = listOf("Creep", "Idioteque", "Street Spirit", "Paranoid Android")
val setOfSongs = setOf("Creep", "Idioteque", "Street Spirit", "Paranoid Android")

println(convertToString(listOfSongs)) // output: Creep | Idioteque | Street Spirit | Paranoid Android
println(findElement(setOfSongs)) // output: Idioteque
println(filterElements(listOfSongs)) // output: [Idioteque, Street Spirit]
println(returnRandomElement(setOfSongs)) // output: Street Spirit
println(decreaseCollection(setOfSongs)) // output: [Idioteque, Street Spirit, Paranoid Android]
```

请注意， `drop()` 或 `minus()` 不会更改原始集合；相反，它们会创建一个新集合，因此它们也适用于 `Collection<T>` ，一种不可变类型。

## 可变集合

现在，我们来考虑一下 `MutableCollection` 的用法。它可以使用 `Collection` 的所有方法，但它也有一些特定的操作。

请注意，与 `drop()` 或 `minus()` 不同， `MutableCollection` 特定方法会修改原始集合。因此，使用这些方法的函数会返回一个——操作成功则返回 `true` ，操作失败则返回 `false` 。您已经学习过这些方法，它们在将 `MutableCollection` 作为函数参数时工作方式相同。

- `addAll()` 将一个集合中的所有元素添加到另一个集合中。
- `add()` 函数会将一个元素添加到集合中。
- `clear()` 会移除集合中的所有元素。
- `remove()` 从集合中删除某个元素的第一个实例。

请看以下示例：

```kotlin
fun addCollection(old: MutableCollection<String>, new: Collection<String>) {
    old.addAll(new)
}

fun addNewElement(old: MutableCollection<String>) {
    old.add("Spectre")
}

fun clearCollection(old: MutableCollection<String>) {
    old.clear()
}

fun removeElement(old: MutableCollection<String>): Boolean {
    return old.remove("Creep")
}

val oldSongs = mutableSetOf("Creep", "Street Spirit")
val newSongs = listOf("Creep", "Street Spirit", "Paranoid Android")

clearCollection(oldSongs)
println(oldSongs) // []

addCollection(oldSongs, newSongs)
println(oldSongs) // [Creep, Street Spirit, Paranoid Android]

addNewElement(oldSongs)
println(oldSongs) // [Creep, Street Spirit, Paranoid Android, Spectre]

removeElement(oldSongs)
println(oldSongs) // [Street Spirit, Paranoid Android, Spectre]
println(removeElement(oldSongs)) // false because this collection doesn't contain "Creep"
```

`retainAll()` 方法会保留集合中的唯一元素——仅保留那些也包含在指定集合中的元素。

```kotlin
fun retainAllFromCollection(old: MutableCollection<String>, new: Collection<String>) {
    old.retainAll(new)
}

val oldSongs = mutableSetOf("Creep", "Street Spirit", "Paranoid Android")
val newSongs = listOf("Spectre", "Street Spirit")
retainAllFromCollection(oldSongs, newSongs)
println(oldSongs) // [Street Spirit]
```

因此，您可以使用 `Collection` 和 `MutableCollection` 接口对其继承者执行任何通用操作，而无需考虑它们的类型。

## 函数和集合

将集合视为接口，并考虑到数据类型的继承性，您可以创建用于处理不同数据的函数。而且这不仅限于 `Collection` 类型——您还可以创建带有特定类型参数（例如 `List` 或 `Set` 的函数，这些参数的父类型可以是 unit。

```kotlin
fun processNumbers(list: List<Number>) {
    list.forEach { print("$it ") }
}

val numbers1 = listOf(0, 12, 10)
val numbers2 = listOf(0.0, 12.0, 10.0)
val numbers3 = listOf(423324534536356, 4L, 56L)

processNumbers(numbers1) // 0 12 10
processNumbers(numbers2) // 0.0 12.0 10.0
processNumbers(numbers3) // 423324534536356 4 56
```

然而，在这些情况下，您可用的方法非常有限——只有那些可以应用于父通用方法。例如，如果您尝试将列表中的每个元素加 1，编译器会发现问题：

```kotlin
fun processNumbers(list: List<Number>) {
    list.forEach { print(it + 1) }
}
```

编译器的响应是：“未解析的引用。由于不匹配，以下候选对象均不适用……”

这是因为抽象类 `Number` 不支持任何计算操作——这些操作只在某些类中实现，例如 `Int` 或 `Double` 。但是 `Number` 支持不同的转换操作，例如 `toDouble()` 、 `toInt()` 或 `toChar()` ：

```kotlin
fun processNumbers(list: List<Number>) {
    list.forEach { print("${it.toChar()} ") }
}

val numbers1 = listOf(41, 42, 43)
processNumbers(numbers1) // ) * +
```

## 结论

在本主题中，我们了解到集合也是接口。你可以使用它们对不同类型的数据进行通用操作。我们也看到，即使我们将 `Map` 称为集合，但这种数据类型并不继承自 `Collection` 。

现在，您可以编写通用函数来处理不同的集合类型，例如 `Set` 或 `List` 、 `MutableSet` 或 `MutableList` 。无需关心它们的类型：重要的是它们继承自 `Collection` 或 `MutableCollection` 。

另外，请记住 `Set` 不继承自 `MutableCollection` ，同样 `MutableList` 也不继承自 `Collection` 。

89 名学员喜欢这篇理论文章， 8 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
