提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

使用集合时，根据要解决的问题调整其功能至关重要。许多集合都实现了便于操作的行为。 [队列集合](https://en.wikipedia.org/wiki/Queue_\(abstract_data_type\)) 和 [栈集合](https://en.wikipedia.org/wiki/Stack_\(abstract_data_type\)) 就很好地体现了两种常用的行为。

在本主题中，我们将学习如何借助 ArrayDeque 来处理栈和队列等集合。

## 栈和队列

在你的任务中，你会经常用到两种具有特定行为的集合：队列和栈。

- 队列：它遵循先进先出（FIFO）原则。在这种集合中，数据总是从末尾添加，从开头移除。你去超市排队结账时就能看到这种模式：第一个到达的人总是第一个被服务。队列的基本方法是 **入队** （将数据添加到末尾）和 **出队** （从开头移除）。
- 栈：它采用后进先出（LIFO）原则。根据这一原则，最后添加的元素将最先被移除，也就是说，元素是堆叠的。你可以想象一下把书放进盒子里：你把它们一本叠放在一起，从盒子里取出时，你会先拿最上面的那本。栈的基本方法有 `push` （在顶部添加元素）、 `pop` （从顶部移除元素）和 `peek` （返回顶部元素）。

我们可以利用 Kotlin 的 MutableList 实现队列行为，其工作原理如下：使用 `add()` 方法将元素加入队列，即将其添加到列表末尾； `removeFirst()` 移除列表的第一个元素。关键在于，这两个操作分别作用于集合的头部和尾部。

```kotlin
fun main() {
    val queue = mutableListOf<Int>()

    queue.add(1)
    queue.add(2)
    queue.add(3)
    queue.add(4)
    println(queue) // [1, 2, 3, 4]

    queue.removeFirst()
    queue.removeFirst()
    println(queue) // [3, 4]
}
```

此外，我们可以使用 MutableList 来模拟栈的行为，通过 `add()` 在末尾添加元素，通过 `removeLast()` 方法移除最后一个元素。诀窍在于这两个操作都作用于集合的同一侧：在本例中，即尾部或末尾。

```kotlin
fun main() {
    val stack = mutableListOf<Int>()

    stack.add(1)
    stack.add(2)
    stack.add(3)
    stack.add(4)
    println(stack) // [1, 2, 3, 4]

    stack.removeLast()
    stack.removeLast()
    println(stack) // [1, 2]
}
```

## 数组队列

ArrayDeque 是一种同时实现了 `Queue` （先进先出）和双 `Deque` （先进先出，后进先出）原则的集合；它也被称为数组双端队列或数组双端队列。它允许你从集合的两端添加和删除元素：该集合提供了方便访问两端的方法。它还实现了 MutableList 接口，并支持通过索引进行高效的 get/set 操作。因此，你也可以使用所有熟悉的 MutableList 方法。

那么，既然我们可以用 MutableList 完成类似的任务，为什么还需要 ArrayDeque 呢？当你需要“双端队列”、队列或栈的功能时，就应该使用 ArrayDeque：它的方法在语义上已经过调整，能够满足这类任务的需求。

让我们来看一个这类收藏的例子。

```kotlin
fun main() {
    val deque = ArrayDeque<Int>()

    // as a queue, FIFO on both sides
    deque.addLast(1)
    deque.addLast(2)
    deque.addLast(3)
    println(deque) // [1, 2, 3]
    deque.removeFirst()
    deque.removeFirst()
    println(deque) // [3]

    // as a stack, LIFO on one side, i.e., the end
    deque.addLast(1)
    deque.addLast(2)
    println(deque) // [3, 1, 2]
    deque.removeLast()
    deque.removeLast()
    println(deque) // [3]
    // or LIFO on the other side, i.e., the start
    deque.addFirst(1)
    deque.addFirst(2)
    println(deque) // [2, 1, 3]
    deque.removeFirst()
    deque.removeFirst()
    println(deque) // [3]

}
```

## 添加元素

假设你想向一个集合中添加元素。你可以从集合的开头添加，也可以从结尾添加。记住，如果你想要一个队列，就必须从末尾添加元素（例如超市里的排队队伍）；如果你想要一个堆叠，就可以从开头添加元素（例如一摞脏盘子）。以下是一些执行这些任务的方法：

- `add()` 方法：将指定的元素添加到列表末尾并返回 true。您可以传递索引作为参数，以将元素添加到特定位置。索引必须为正数。此操作返回 true 是因为列表总是会因此而发生变化。
- `addAll()` ：将所有元素（集合）添加到末尾；如果指定了索引，则添加到指定的索引位置。此操作返回 true，因为列表总是会因此而改变。
- `addFirst()` ：将指定的元素添加到集合的开头。这意味着将其添加到集合的开头。它返回 Unit 值。
- `addLast()` ：将指定的元素添加到双端队列的末尾。它返回 Unit 值。
```kotlin
fun main() {
    val deque = ArrayDeque<Int>()

    deque.add(1)
    deque.add(2)
    deque.add(3)
    println(deque) // [1, 2, 3]
    deque.add(1, 4)
    println(deque) // [1, 4, 2, 3]
    deque.addAll(listOf(5, 6, 7))
    println(deque) // [1, 4, 2, 3, 5, 6, 7]
    deque.addFirst(8)
    println(deque) // [8, 1, 4, 2, 3, 5, 6, 7]
    deque.addLast(9)
    println(deque) // [8, 1, 4, 2, 3, 5, 6, 7, 9]
}
```

## 移除元素

下一步是移除集合中的元素：您可以“为超市排队的顾客服务”（处理第一个商品），或者“优先清洗脏盘子队列中最上面的盘子”。以下是一些执行这些任务的方法：

- `remove()` ：如果集合中存在指定的元素，则将其从集合中移除。如果元素已成功移除，则返回 true；如果元素不存在于集合中，则返回 false。
- `removeAll()` ：移除指定集合中包含的所有元素。如果指定集合中的任何元素被移除，则返回 true；如果集合未被修改，则返回 false。
- `removeAt()` ：从列表中移除指定索引处的元素。它将返回已移除的元素，如果元素的索引超出范围，则抛出 `IndexOutOfBoundsException` 。
- `removeFirst()` ：从双端队列中移除第一个元素，并返回移除的元素；如果双端队列为空，则抛出 `NoSuchElementException` 。
- `removeFirstOrNull()` ：从双端队列中移除第一个元素，并返回移除的元素；如果双端队列为空，则返回 null。
- `removeLast()` ：从双端队列中移除最后一个元素，并返回移除的元素；如果双端队列为空，则抛出 `NoSuchElementException` 。
- `removeLastOrNull()` ：从双端队列中移除最后一个元素，并返回移除的元素；如果双端队列为空，则返回 null。
```kotlin
fun main() {
    val deque = ArrayDeque<Int>()

    deque.addAll(listOf(1, 2, 3, 4, 5, 6, 7, 8, 9))
    println(deque) // [1, 2, 3, 4, 5, 6, 7, 8, 9]
    deque.remove(5)
    println(deque) // [1, 2, 3, 4, 6, 7, 8, 9]
    deque.removeAll(listOf(1, 2))
    println(deque) // [3, 4, 6, 7, 8, 9]
    deque.removeAt(2)
    println(deque) // [3, 4, 7, 8, 9]
    deque.removeFirst()
    println(deque) // [4, 7, 8, 9]
    deque.removeLast()
    println(deque) // [4, 7, 8]
    deque.clear()
    deque.removeFirstOrNull()
    println(deque) // []
    deque.removeLastOrNull()
    println(deque) // []
}
```

## 获取元素

想象一下，你想知道超市里谁在排队，或者一堆脏盘子里第一个或最后一个是什么，而无需进行任何处理。你可以使用以下方法获取集合中的元素：

- `get()` ：返回列表中指定索引处的元素（也可以使用 `[]` ），如果元素的索引超出范围，则抛出 `IndexOutOfBoundsException` 。
- `first()` ：返回第一个元素，如果双端队列为空，则抛出 `NoSuchElementException` 。
- `firstOrNull()` ：返回第一个元素，如果双端队列为空则返回 `null` 。
- `last()` ：返回最后一个元素，如果双端队列为空，则抛出 `NoSuchElementException` 。
- `lastOrNull()` ：返回最后一个元素，如果双端队列为空则返回 null。
```kotlin
fun main() {
    val deque = ArrayDeque<Int>()

    deque.addAll(listOf(1, 2, 3, 4, 5, 6, 7, 8, 9))
    println(deque) // [1, 2, 3, 4, 5, 6, 7, 8, 9]
    println(deque[2]) // 3
    println(deque.first()) // 1
    println(deque.last()) // 9
    deque.clear()
    println(deque.firstOrNull()) // null
    println(deque.lastOrNull()) // null
    println(deque[50]) // exception java.lang.IndexOutOfBoundsException: Index: 50, Size: 9
}
```

## ArrayDeque 和 MutableList，你应该选择哪一个？

`ArrayDeque` 和 `MutableList` 在不同操作中具有不同的性能特征。让我们来看看它们的主要区别：

1. **开头添加/删除元素** ：
	- **ArrayDeque** ：从队列开头添加或删除元素通常以常数时间 O(1) 完成。这是由于 `ArrayDeque` 的双向结构所致。
		- **MutableList** ：从列表开头添加或删除元素需要移动所有后续元素，使得这些操作与列表的大小成正比——O(n)。
2. **在末尾添加/删除元素** ：
	- **ArrayDeque** ：就像开头一样，从队列末尾添加或删除元素通常以常数时间 O(1) 进行。
		- **可变列表** ：向列表末尾添加元素通常需要 O(1) 的时间复杂度，除非需要调整数组大小。从列表末尾删除元素也需要 O(1) 的时间复杂度。
3. **访问元素** ：
	- **ArrayDeque** ：由于 `ArrayDeque` 的内部表示形式是循环缓冲区，因此通过索引访问任意元素可能比在 `MutableList` 中花费的时间更长。
		- **MutableList** ：通过索引访问元素的时间复杂度为 O(1)。

实际上， `ArrayDeque` 和 `MutableList` 之间的选择取决于应用程序中哪些操作最频繁且最关键。如果您经常需要从集合的开头添加或删除元素， `ArrayDeque` 是更佳选择。但是，如果主要操作是通过索引访问元素，那么 `MutableList` 可能更合适。

## 结论

在本主题中，我们学习了如何使用 ArrayDeque 来管理集合，它模拟了数组双端队列或数组栈，从而能够使用栈和队列来解决我们的问题。重要的是要理解，指定行为有时可以帮助我们为每个任务找到最合适的集合。请记住，ArrayDeque 提供了您已经了解的所有 MutableList 方法，以及针对所选行为的特定方法。它是一种您在未来的项目中会经常用到的重要集合类型。

现在是时候做一些任务来检验你所学的知识了。准备好了吗？

52 名学员喜欢这篇理论文章， 3 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
