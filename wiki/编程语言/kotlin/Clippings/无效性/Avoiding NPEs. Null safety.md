## 避免 NPE。零安全性

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

是 Kotlin 设计中的一个关键特性，它解决了臭名昭著的“十亿美元错误”——在编程中使用空引用。Kotlin 的旨在消除空引用，因为空引用通常会导致软件开发中的错误和崩溃。让我们来学习如何使用可空类型。

## 安全通话

假设你有一个可为空的字符串，并且想要获取它的长度。在 Kotlin 中，你无法直接用简单的方法获取它的长度：

```kotlin
val name: String? = "Kotlin"
val length = name.length // Compilation error
```

如果您需要访问可空对象的属性或调用其方法，则必须先检查它是否 `null` 。您可以这样做：

```kotlin
val name: String? = "Kotlin"
val length = if (name != null) name.length else null
```

但是这个表达式太长了！使用安全调用运算符 `?.` 可以得到相同的结果，它允许你访问可空变量的属性或调用其方法，而不会冒着抛出 `NullPointerException` 风险：

```kotlin
val name: String? = "Kotlin"
val length = name?.length // length is null if name is null
```

就是这样！只需在每次可空引用后面加上一个问号（ `?` 。 `?.` 会将它的值与 `null` 进行比较，如果该引用为 `null` ，则返回 `null` 。这对于链式调用来说更加方便。以下是两个连续的示例：

```kotlin
val street = city?.address?.street // the same as the next expression

val street = if (city != null && city.address != null) 
    city.address.street else null
```

## 猫王操作员

Kotlin 还有另一种处理可空变量的有趣方法。让我们来看一下这段代码：

```kotlin
var name: String? = "Kotlin"
val length: Int? = name?.length
print(if (length != null) length else 0)
```

如您所见，当 `name` 变量为 `null` 时， `length` 变量也将为 `null` 。但如果我们想在 `length` 为 `null` 时打印 `0` ，则需要添加额外的检查。这有点笨拙。不过，我们可以使用 **Elvis 运算符** 简化代码：

```kotlin
var name: String? = "Kotlin"
val length: Int? = name?.length
print(length ?: 0)
```

Elvis 运算符的工作原理如下：如果表达式（ `name?.length` ）的左侧不为 `null` ，则返回左侧；否则，返回右侧（0）。你也可以在右侧使用 `return` 和 `throw` 表达式：

```kotlin
val length: Int = name?.length ?: throw Exception("The name is null")
```

你可能会问，为什么叫猫王？看：他就在那儿！

![](https://ucarecdn.com/70a56aca-5d34-4852-ae94-eeadf39527c7/)

## 非空断言运算符

有一种简单的方法可以触发空指针异常 (NPE)：使用非空断言运算符 `!!` 。只有当你 100% 确定变量不为 `null` ，代码才不会崩溃。

```kotlin
var name: String? = "Kotlin"
print(name!!.length)
```

上面的代码看起来像是在尖叫，试图吓唬编译器。上面的代码片段几乎等同于下面的代码：

```kotlin
var name: String? = "Kotlin"
val length: Int = name?.length ?: throw NullPointerException()
print(length)
```

此运算符用于在遇到 `null` 时停止程序。\` `!!` 运算符断言该值非空，如果该值确实为空，则会立即抛出 \` `NullPointerException` 异常。这违背了 Kotlin 的空安全理念，应谨慎使用。为什么过度使用 `!!` 会带来问题：

1. **破坏空值安全** ：Kotlin 的类型系统旨在优雅地处理空值。过度使用 `!!` 会绕过这些安全措施。
2. **代码异味** ：频繁使用通常表明忽视了正确的空值检查，并可能导致代码稳定性降低，维护难度增加。
3. **意外崩溃** ：如果在使用 `!!` 之前没有进行适当的空值检查，可能会导致应用程序意外崩溃。

## Kotlin 中空值安全的最佳实践

Kotlin 的类型系统旨在消除代码中空引用的风险，也就是所谓的“价值十亿美元的错误”。以下是一些确保空安全的最佳实践：

1. **谨慎使用可空类型** ：仅当变量确实可以为 `null` 使用可空类型（ `Type?` ）。如果变量不应该为 `null` ，请使用。
2. **安全调用（**`?.` ）：访问可空对象的属性或方法时，请使用安全调用运算符。如果对象为 `null` ，则此运算符将返回 `null` 而不是抛出 `NullPointerException` 。
	```kotlin
	val length = nullableString?.length
	```
3. **Elvis 运算符（**`?:`:）：Elvis 运算符允许您在表达式计算结果为 `null` 时提供一个替代值。
	```kotlin
	val length = nullableString?.length ?: 0
	```
4. **非空断言（** `!!` ）：仅当您确定值不 `null` 时才使用此运算符。如果值为 `null` ，则会抛出 `NullPointerException` 异常。
	```kotlin
	val length = nullableString!!.length
	```

遵循这些实践并利用 Kotlin 的函数，您可以编写更健壮、更安全的空指针异常代码。请记住，避免 `NullPointerException` 关键在于编写能够明确声明空指针状态并优雅地处理空指针异常的代码。

## 结论

Kotlin 的空安全特性旨在降低与空引用相关的风险。通过默认类型不可为空并提供显式的可空类型，Kotlin 强制开发者以可控的方式处理空值。使用安全调用和 Elvis 运算符可以安全地处理可空类型，并防止 `NullPointerException` 。

424 名学习者喜欢这篇理论文章， 15 名学习者不喜欢。 **你觉得呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
