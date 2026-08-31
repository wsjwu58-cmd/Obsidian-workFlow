提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

如您所知， 允许您将代码作为数据，并将其作为函数的参数传递。另一种方法是使用 **函数引用** 。函数引用通常比相应的 lambda 表达式更易读。此外，还能迫使开发人员将程序分解成一组职责清晰的短函数。

## 使用函数引用使代码更清晰

简单回顾一下： **函数引用** 是一种特殊的链接，它通过函数名指向特定的函数，我们可以随时调用它。让我们来看一个例子：

```kotlin
fun isOdd(x: Int) = x % 2 != 0

fun isEven(x: Int) = x % 2 == 0

fun printNumbers(numbers: MutableList<Int>, filter: (Int) -> Boolean) {
    for (number in numbers) {
        if (filter(number))
            print("$number ")
    }
}

fun main() {
    val numbers = mutableListOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val oddFunction = ::isOdd
    print("Odd numbers: ")
    printNumbers(numbers, oddFunction)
    print("\nEven numbers: ")
    printNumbers(numbers, ::isEven)
}
```

如您所见，我们可以直接调用 `isOdd()` 和 `isEven()` 函数，也可以通过使用 `::` 传递它们的值。

该计划的结果将是：

```
Odd numbers: 1 3 5 7 9 
Even numbers: 2 4 6 8 10
```

将函数传递给另一个方法是常见的做法。当然，你可以使用 lambda 表达式来实现这一点，但如果你已经有了函数，为什么不使用链接来避免代码重复呢？在本主题中，你将学习如何创建对各种函数的引用。

## 按类引用

此外，您还可以引用属于某个类的函数。在这种情况下，基本如下所示：

```kotlin
objectOrClass::functionName
```

这里， `objectOrClass` 可以是，也可以是类的 **特定** 。

让我们来看一个使用 `Person` 类的例子：

```kotlin
class Person(val name: String, val lastname: String) {

    fun printFullName(): String {
        return("full name: $name $lastname")
    }
}
```

这里，我们创建一个函数引用：

```kotlin
val person: Person = Person("Sara", "Rogers")
val personFun: () -> String = person::printFullName
```

现在，我们使用特殊的函数 `invoke` 来调用该函数：

```kotlin
print(personFun.invoke())
```

实际上，你也可以不调用函数 `invoke` 来调用该函数：

```kotlin
print(personFun())
```

结果如下：

```
full name: Sara Rogers
```

现在您明白如何通过使用引用轻松地将函数转换为对象了吧。  
这是一项非常有用的编程技能，当你开始从事严肃的项目时，它将帮助你解决许多问题。

我们来看看函数引用的其他可能性。

## 标准类和函数参考

函数引用也适用于 Kotlin 标准类中的函数。我们来看一个例子。

我们创建了对 `Int` 类的标准函数 `dec` 的引用。dec `dec` 将数字减 1（递减）。

```kotlin
val dec: (Int) -> Int = Int::dec
```

这里， `Int::dec` 是对一个函数的引用。

这段代码之所以能运行，是因为函数 `operator fun dec(): Int` 的定义符合类型 `(Int) -> Int` ：它们都表示接受一个整数参数并返回一个整数值。

现在我们有了可以作为函数使用的 `dec` 对象。让我们调用它吧！

```kotlin
print(dec(4)) // 3
```

因此，一旦分配给一个对象，函数引用就与 lambda 表达式的工作方式相同。

以下是使用 lambda 表达式创建相同对象的另一种方法：

```kotlin
val dec: (Int) -> Int = {x -> x.dec()}
```

如果只需要调用一个标准函数而不需要执行其他操作，建议使用函数引用而不是 lambda 表达式。这样代码会更简洁、更易读、更易于测试。

请注意，我们可以使用函数引用来引用标准函数和自定义函数。

## 函数引用的类型

一般来说，函数引用有四种类型：

1. 函数引用；
2. 按类别引用；
3. 按对象引用；
4. 引用构造函数。

**1\. 对函数的引用**

该引用包含以下声明：

```
::functionName
```

让我们来看一个使用对 `multiply` 和 `add` 函数的引用的例子：

```kotlin
fun multiply(x: Int, y: Int) = x * y

fun add(x: Int, y: Int) = x + y

fun main() {
    val operatorMultiply: (Int, Int) -> Int = ::multiply
    val operatorAdd: (Int, Int) -> Int = ::add
}
```

现在我们可以对一对值调用 `operatorMultiply` 和 `operatorAdd` 函数，并查看结果：

```kotlin
operatorMultiply(10, 5) // 50
operatorAdd(5, 4) // 9
```

`operatorMultiply` 和 `operatorAdd` 函数也可以使用以下 lambda 表达式编写：

```kotlin
val operatorMultiply: (Int, Int) -> Int = {x: Int, y: Int -> x * y}
val operatorAdd: (Int, Int) -> Int = {x: Int, y: Int -> x + y}
```

**2\. 按班级参考**

一般形式如下：

```kotlin
ClassName::functionName
```

让我们来看一下 `Int` 类的函数，它允许我们对两个二进制数进行逻辑 `and` 运算：

以下是该函数的工作原理示例：

```kotlin
val a = 5 and 4 // 101 & 100 = 100 (4)
```

此外，我们 `and` 可以用另一种方式调用该函数：

```kotlin
val b = 9.and(3) // 1001 & 0011 = 0001 (1)
```

所以， `and` 是 `Int` 类的函数，我们可以获取到它的引用：

```kotlin
val and: (Int, Int) -> Int = Int::and
```

现在我们可以使用两个值来调用 `and` 函数，例如 1 和 3：

```kotlin
and(1, 3) // the result is 1
```

也可以使用以下 lambda 表达式来编写 `and` 函数：

```kotlin
val and: (Int, Int) -> Int = {a: Int, b: Int -> a.and(b)}
```

**3\. 通过对象引用**

一般形式如下：

```kotlin
objectName::functionName
```

我们来看一个从特定字符串中引用 `indexOf` 函数的例子；该函数查找文本中元素首次出现的索引。此函数接受三个参数：要查找的字符串、搜索起始索引以及一个布尔值，该布尔值决定匹配字符时是否忽略大小写（默认值为 **false** ）。

```kotlin
val whatsGoingOnText: String = "What's going on here?"
val indexWithinWhatsGoingOnText: (String, Int, Boolean) -> Int = whatsGoingOnText::indexOf
```

以下是将其应用于不同论证的结果：

```kotlin
println(indexWithinWhatsGoingOnText("going", 0, true)) // 7
println(indexWithinWhatsGoingOnText("Hi", 0, true))  // -1
println(indexWithinWhatsGoingOnText("what's", 0, false))  // -1
println(indexWithinWhatsGoingOnText("what's", 0, true))  // 0
```

如您所见，我们实际上始终使用从上下文中捕获的 `whatsGoingOnText` 对象。

以下 lambda 表达式示例与上述参考资料完全等效，可以帮助您更好地理解相关情况：

```kotlin
val indexWithinWhatsGoingOnText: (String, Int, Boolean) -> Int =
        { string: String, startIndex: Int, ignoreCase: Boolean ->
            whatsGoingOnText.indexOf(string, startIndex, ignoreCase)
        }
```

**4\. 对构造函数的引用**

该引用包含以下声明：

```kotlin
::ClassName
```

例如，我们考虑一下我们自定义的 `Person` ，它只有一个字段 `name` 。

```kotlin
class Person (val name: String){
}
```

以下是该类构造函数的参考信息：

```kotlin
val personGenerator: (String) -> Person = ::Person
```

该函数根据名称生成新的 `Person` 对象。

```kotlin
val johnFoster: Person = personGenerator("John Foster")
```

以下是实现相同功能的对应 lambda 表达式：

```kotlin
val personGenerator: (String) -> Person = {string -> Person(string)}
```

此外，我们将结合使用 lambda 表达式和函数引用。

让我们总结一下新学到的知识：

| **类型** | **函数参考** |
| --- | --- |
| 函数引用 | ::函数名 |
| 按班级参考 | 类::函数名 |
| 对象引用 | 对象::函数名 |
| 构造函数的引用 | ：：班级 |

后续章节将探讨更多实际示例。目前，只需掌握函数引用的基本概念和语法即可。

## 结论

你已经学习了一种使用函数引用创建函数对象的新方法。它与 lambda 表达式有很多相似之处，但可以编写更易读、更易分解的代码。学习完本主题后，你应该记住所有四种类型的函数引用，以便在需要将一段代码传递给某个函数时，能够在程序中使用它们。

173 名学习者喜欢这篇理论文章， 13 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
