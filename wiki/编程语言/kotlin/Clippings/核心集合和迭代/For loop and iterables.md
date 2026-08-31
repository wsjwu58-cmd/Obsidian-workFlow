## 循环和可迭代对象

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

正如你从之前的章节中所了解到的，Kotlin 中使用 `for` 循环来遍历范围、数组和各种类型的集合。此外，我们还了解到 Kotlin 中的集合有一种称为 `iterator` 特殊结构，它提供了遍历和处理集合的方法。迭代器不仅可以用于标准集合，还可以用于自定义类。在本章节中，我们将学习如何使用它。

## 迭代器作为接口

在 Java 和 Kotlin 等编程语言中，迭代器是一种非常有用的结构，它能帮助你逐个处理一系列元素：例如，打印每个值，甚至删除某些元素。为了使用迭代器，表示元素集合的类需要实现 `Iterable` 接口，该接口声明了 `iterator()` 函数。该函数会创建并返回一个 `Iterator` 对象，该对象会按顺序访问集合中的元素。

`Iterator` 有两个基本函数： `next()` 和 `hasNext()` 。\`hasNext `hasNext()` 用于检查迭代中是否存在后续元素。调用 `next()` 时，它会返回当前元素，并将迭代器的指针移动到下一个元素（如果存在）。以下是一个示例：

```kotlin
val alphabet = listOf('a', 'b', 'c', 'd', 'e')
val alphabetIterator = alphabet.iterator()
while (alphabetIterator.hasNext()) {
    print(alphabetIterator.next() + " ") // a b c d e
}
```

如果要在迭代序列的过程中修改元素，需要使用 `MutableIterator` 它是一种支持在迭代过程中删除元素的迭代器版本。添加和修改元素的功能仅由 `MutableListIterator` 支持，而 MutableListIterator 则与 `MutableList` 配合使用。

```kotlin
val colors = mutableListOf("red", "green", "blue", "white") 
val mutableIterator = colors.listIterator()

mutableIterator.next()
mutableIterator.remove()    
println("After : $colors") // After: [green, blue, white]
mutableIterator.add("black")
println("After : $colors") // After: [black, green, blue, white]
```

## 集合作为接口

在 Kotlin 中，有两个通用的接口用于处理元素序列 `Iterable` 和 `MutableIterable` 是一个表示通用元素集合 `Collection` `Collection` ，它继承自 `Iterable` 与 `Iterable` 区别在于它提供了诸如 `get()` 、 `find()` 、 `filter()` 、 `count()` 等方法。如下面的示意图所示， `List` 和 `Set` 都是 `Collection` 的继承者：

![interface diagram for working with a sequence of elements](https://ucarecdn.com/cb37aa43-2c3b-44f5-b6b5-ea6e909cdf04/)

正如您在之前的文章中可能已经了解到的， `Iterable` 不支持对集合进行修改：例如，您无法从继承自 `Collection` 集合中删除元素，也无法向其中添加新元素。如果您需要添加或删除元素， `MutableCollection` 您操作的集合必须实现 `MutableCollection` 接口。MutableCollection 提供了诸如 `add()` 、 `addAll()` 、 `remove()` 、 `removeAll()` 、 `drop()` 等方法。此接口分别由 `List` 和 `Set` 的可变版本 `MutableList` 和 `MutableSet` 实现。

如您所见，像 `List` 和 `Set` 的标准集合都继承自 `Iterable` ，因此您可以创建一个迭代器对象来处理这些集合。接下来，我们将看看如何实现我们自己的 `Iterable` 并为其创建一个迭代器。

## 创建你自己的迭代器

假设我们有一个简单的 `Message` ，它表示一条消息，包含一段简短的文本和一个指向下一条消息的指针：

```kotlin
class Message(var text: String, var next: Message? = null) { }
```

我们可能会有很多消息，并且希望将它们存储在例如 `MessageBox` 中。此外，最好能够逐条读取消息，因此我们需要能够遍历它们。

让我们创建 `MessageBox` 类，它将是我们自定义的消息序列实现。它有 `head` 和 `tail` 属性，分别指向 `MessageBox` 中的第一条消息和最后一条消息。如果我们想要遍历 `MessageBox` ，我们需要让它继承自 `Iterable<Message>` ，并重写其 `iterator()` 函数。该函数返回一个 `MessageBoxIterator` 对象，我们稍后会创建它。

```kotlin
class MessageBox(var head: Message, var tail: Message = head) : Iterable<Message> {

    init {
        if (tail != head) {
            head.next = tail
        }
    }

    fun add(newMessage: Message) {
        tail.next = newMessage // change 'next' pointer of the former last element to a new message
        tail = newMessage // new message becomes a new tail
    }

    override fun iterator(): Iterator<Message> {
        return MessageBoxIterator(this)
    }
}
```

此外，我们还声明了一个函数 `add()` ，用于向 `MessageBox` 添加新消息。

由于 `MessageBoxIterator` 实现了 `Iterator<Message>` ，我们需要重写 `hasNext()` 和 `next()` 方法，以便获取下一个元素。我们还声明了一个变量 `current` ，它指向 `MessageBoxIterator` 所指向的序列的当前对象。

```kotlin
class MessageBoxIterator(messageBox: MessageBox) : Iterator<Message> {

    private var current: Message = Message("EMPTY_PRE_HEAD", next = messageBox.head)

    override fun hasNext(): Boolean {
        return current.next != null
    }

    override fun next(): Message {
        if (current.next == null) throw NoSuchElementException()

        current = current.next!!
        return current
    }
}
```

如您所见，这里我们使用了 Kotlin 关键字 `private` 和 `lateinit` 。前者是一个 [可见性修饰符](https://kotlinlang.org/docs/visibility-modifiers.html#packages) 。该修饰符禁止在类外部修改布尔变量 \` `isAccessed` 的值。正如您在 [关于迭代器 (Iterator) 的主题](https://hyperskill.org/learn/step/20794) 中所了解的，当创建一个迭代器对象时，它指向集合中第一个元素 **之前的** 位置。如果我们已经调用了 \` `next()` 函数并且迭代器指向某个元素，则 `isAccessed` 的值为 \` `true` ；如果尚未访问集合，则其值为 `false` 。为了声明稍后初始化的非空类型，我们在变量声明中使用关键字 \` `lateinit` 。您可以 [阅读更多相关内容](https://hyperskill.org/learn/step/14661) 。

让我们试着运用我们已经取得的成果：

```kotlin
fun main() {
    var messageBox = MessageBox(Message("hello!"))
    messageBox.add(Message("I am from hyperskill"))
    messageBox.add(Message("which programming language do you study?"))

    val messageIterator = messageBox.iterator()
    while (messageIterator.hasNext()) {
        println(messageIterator.next().text)
    }

}
```

结果如下：

```kotlin
hello!
I am from hyperskill
which programming language do you study?
```

如果在遍历完 `MessageBox` 的所有元素后尝试调用 `next()` 函数，则会抛出 `NoSuchElementException` 异常。这意味着在遍历完整个序列后，迭代器已无法继续使用，需要创建一个新的 `Iterator` 对象。

## for 循环和迭代器

任何实现了 `Iterable` 接口的类都可以在增强型 `for` 循环中使用。如果我们创建自定义类，则需要实现 `Iterable` 接口并提供一个迭代器。

例如，接口 `List` 继承自 `Collection` ，而 Collection 又继承自 `Iterable` ，这就是为什么我们可以在 `for` 循环中访问 `List` 的每个元素。让我们来看下面的例子：

```kotlin
val languages = listOf("java", "kotlin", "python")
for (lang in languages) {
  println(lang) 
}
/*
 java
 kotlin
 python
*/
```

但是，如果我们尝试使用 `File` 类（例如）在增强型 `for` 循环中读取文件中的行，则会收到错误，因为 `File` 没有实现 `Iterable` 接口：

```kotlin
var file = File("kotlin.txt")
for(line in File){ // compile error
   ...
}
```

`for` 循环可以与 `Iterator` 一起使用，方法如下：

```kotlin
val letters = listOf("k", "o", "t", "l", "i", "n")
val iterator = letters.iterator()
for (letter in iterator) {
  print(letter) // kotlin
}
```

## 结论

在本主题中，您学习了 `Iterator` 和 `Collection` 作为接口的知识。我们了解了 `Iterable` 和 `MutableIterable` 之间的区别，并讨论了如何处理可变和不可变的元素序列。

此外，我们已经通过创建类并尝试使用它们实现了 `Iterable` 和 `Iterator` 。请记住，如果您想创建一个表示元素序列并对其进行迭代的类，您的类应该继承自 `Iterable` 并重写其 `iterator()` 方法。如果您需要创建自己的迭代器，可以通过实现 `Iterator` 来实现。

51 名学员喜欢这部分理论内容， 16 名学员不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
