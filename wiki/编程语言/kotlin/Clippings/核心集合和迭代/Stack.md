提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

当我们尝试使用集合来编写代码解决任务时，了解我们需要遵循的需求至关重要。许多集合都实现了相应的行为，这使得使用它们变得轻松便捷。两种常用的行为是先进先出（FIFO， [队列集合](https://en.wikipedia.org/wiki/Queue_\(abstract_data_type\)) ）和后进先出（LIFO， [栈集合](https://en.wikipedia.org/wiki/Stack_\(abstract_data_type\)) ）。

在本主题中，我们将学习如何使用栈（后进先出策略），并了解它们如何帮助我们改进代码和解决某些代码问题。

## 收集行为

有两种类型的集合，它们各自具有特定的行为，您在任务中会经常用到它们：先进先出 (FIFO) 和后进先出 (LIFO)。

- **先进先出** **（FIFO）** 原则是指数据总是从末尾添加到队列末尾，从队列开头移除。这种集合被称为 **队列** 。当你去超市排队结账时，就能看到这种模式：先到的人总是最先得到服务。队列的基本操作是 **入队** （将数据添加到队列末尾）和 **出队** （将数据从队列开头移除）。
- 后进先出 **（LIFO）** 行为——即 **后进先出** 原则。这种集合被称为 **栈。** 根据其原则，最后添加的元素将最先被移除：也就是说，元素是堆叠的。你可以想象一下把书放进盒子里：你把它们一本叠放在一起，从盒子里取出时，你会先拿最上面的那本。栈的基本方法有 `push` （添加到顶部）、 `pop` （从顶部移除）和 `peek` （返回顶部元素）。

## 堆

在 JVM 中， `Stack` 类使用 LIFO（后进先出）策略对 `Stack` 进行建模和实现。它是一个 Java 类，并非纯 Kotlin 集合，因此您必须导入它才能使用它（ `import java.util.Stack` ）。如果您需要基于 Kotlin 的集合，可以使用 `ArrayDeque` 。

向栈中添加元素时，将其放置在栈顶。从栈中移除元素时，总是移除栈顶元素。它扩展了 `Vector` 类，增加了五个操作，使向量可以像栈一样使用。其他现有方法均继承自 `Vector` 。

让我们来看看你可以在代码中使用的具体栈操作：

- `push()` ：此方法将元素放置在栈顶。
- `pop()` ：此方法移除栈顶的对象并返回该对象。如果栈为空，则会抛出 `EmptyStackException` 。
- `peek()` ：它会获取栈顶元素，但不会将其从栈中移除。如果栈为空，则会抛出 `EmptyStackException` 。
- `empty()` ：如果栈顶没有元素，则返回 true；否则返回 false。
- `search()` ：它返回元素从栈顶到栈顶的位置；否则，它将返回 -1。

让我们来看一个这类收藏的例子。

```kotlin
import java.util.*

fun main() {
    val stack = Stack<Int>()

    // push at top
    stack.push(1)
    stack.push(2)
    stack.push(3)

    println(stack) // [1, 2, 3]

    // pop from top
    stack.pop()

    println(stack) // [1, 2]

    // peek at top
    println(stack.peek()) // 2

    println(stack) // [1, 2]

    // search for element
    println(stack.search(1)) // 2
    println(stack.search(9)) // -1

    // is empty?
    println(stack.empty()) // false
    
}
```

此外，我们还可以将 `List` 转换为 `Stack` ，并使用 `pop()` 对其进行操作。以下示例使用后进先出 (LIFO) 策略打印姓名列表：

```kotlin
import java.util.*

fun main() {
    
    val listOfNames = listOf("John", "Jane", "Mary", "Peter", "Paul", "George")
    val stackOfNames = Stack<String>()

    stackOfNames.addAll(listOfNames)
    while (stackOfNames.isNotEmpty()) {
        print(stackOfNames.pop())
        print(" ")
    }
    // George Paul Peter Mary Jane John 
}
```

请记住：如果您需要 FIFO 和 LIFO 行为（无论两者兼备还是仅需其中之一），最好使用 `ArrayDeque` `Vector` 因为它比 Java 的 `Stack` 或 `List` 效率更高，而且是 100% 纯 Kotlin 集合。Java `Stack` 继承自 `Vector` 类。Vector 实现了一个可增长的对象数组；它与 `ArrayList` 非常相似，但 `Vector` 是 **同步的，** 这意味着在多线程环境中，它会将其他线程锁定在可运行或不可运行状态，直到当前线程释放对象的锁以执行操作。另一方面， `Vector` 类及其某些方法现已过时，已被 `ArrayDeque` 取代，ArrayDeque 更适合 FIFO/LIFO 策略，并且针对并发和多线程环境进行了优化。

## 结论

在本主题中，我们学习了如何使用 `Stack` 来管理集合，模拟后进先出（LIFO）行为：添加元素时，元素会被放置在栈顶；移除元素时，元素也会从栈顶移除。Java 的 `Stack` 类可以帮助你在项目中实现这些任务。

现在是时候做一些任务来检验你所学的知识了。准备好了吗？

44 名学员喜欢这部分理论， 5 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
