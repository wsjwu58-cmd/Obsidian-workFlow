提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您可以通过在变量名后添加等号，后跟一个值来声明变量：

```kotlin
var a = "I love Hyperskill!"
```

像这样创建一个 `String` 对象对编译器来说并不消耗太多资源或时间。但是，创建更复杂类的实例则可能代价高昂。在本主题中，您将学习如何通过使用来解决这个问题，延迟创建对象直到需要它们时才创建。

## 工作原理

延迟初始化允许我们在第一次引用对象时才创建该对象。

这意味着我们不需要浪费时间，立即使用程序的资源为一开始并不需要的对象分配内存。

如果我们允许在需要时初始化对象，就可以通过在程序的生命周期内重新分配资源来节省大量时间。

## 执行

在不同的语言和框架中，可以通过不同的方式实现这一目标。

例如， [Spring 后端框架](https://spring.io/projects/spring-framework) 有一个特殊的属性 `spring.main.lazy-initialization=true` 。这可以通过在启动时创建更少的组件来缩短应用程序的启动时间。然而，在 Spring 的上下文中，这个特性也存在一些缺点，这些缺点超出了我们讨论的范围。

我们来看看如何在不使用框架的情况下使用延迟初始化。

Kotlin 有一个特殊的 `lazy()` 函数，它接受一个 [lambda](https://hyperskill.org/learn/step/6154) 表达式。第一次调用该函数会执行这个 lambda 表达式并记住结果。后续调用则直接返回这个值。

下面你可以看到一个简单的例子：

```kotlin
fun main() {
    val a: String by lazy {
        print("Variable a is initialized. ")
        "I love Hyperskill!"
    }

    println("Initializing a! ") // Initializing a!
    println(a) // Variable a is initialized. I love Hyperskill!
    println(a) // I love Hyperskill!
}
```

那么，为什么会得到这样的输出呢？在 `a` 的值变成 `"I love Hyperskill!"` 之前，lambda 函数体被调用了 `print()` 。这一切都发生在第一次调用 `println(a)` 函数的时候——不多不少。当我们再次打印 `a` ，并没有进行任何计算，所以只显示了 `a` 的值。

> [!primary] Primary
> 在 Kotlin 中使用延迟初始化时，必须使用 `val` 声明变量，因为值只能一次。

## 同步问题

如果你的程序利用了多线程，你需要了解 `lazy()` 函数的 mode 参数。

- `LazyThreadSafetyMode.SYNCHRONIZED` 表示该值仅在一个线程中计算，所有线程都将获得相同的值。这是默认选项，因此您可以根据需要省略它：
	```kotlin
	val a: String by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
	```
- `LazyThreadSafetyMode.PUBLICATION` 指定 lambda 表达式可以被多次调用，每次调用都使用未初始化的惰性对象值，但会使用第一次返回的值：
	```kotlin
	val a: String by lazy(LazyThreadSafetyMode.PUBLICATION) {
	```
- `LazyThreadSafetyMode.NONE` 表示完全不进行同步，因此如果我们从不同的线程调用变量，则无法唯一确定其值。如果您的程序允许从多个线程首次调用惰性对象，则不建议使用此选项。
	```kotlin
	val a: String by lazy(LazyThreadSafetyMode.NONE) {
	```

你可能想知道为什么 `by` 关键字要放在 `lazy` 前面？这与 **委托** 有关。委托的作用是将相应属性的实现委托给一个 lambda 表达式。关于委托的详细解释，请参阅委托主题。

## lateinit

[Kotlin 中另一个值得一提的延迟初始化特性](https://kotlinlang.org/docs/properties.html#late-initialized-properties-and-variables) 是 `lateinit` 。这是一个关键字，而不是像 `lazy()` 那样的函数。

通常情况下，如果的值不为空，我们应该立即初始化该属性，或者在构造函数中初始化。但很多时候，在创建类实例时，我们无法初始化该属性，而且我们也不希望将其设置为可为空。

我们不能使用以下方法，因为必须初始化该字段的默认值：

```kotlin
var a: String
```

我们可以创建 `a` 可空值，但我们不想让它可空！

```kotlin
var a: String? = null
```

幸运的是，可以使用 `lateinit` 来解决这个问题：

```kotlin
lateinit var a: String

fun initA(a: String) {
    this.a = a
}
```

这种方法允许我们在对象创建后的合适时机，在 `initA()` 函数中设置 `a` 的值。

请注意， `lateinit` 变量必须使用 `var` 声明，这与使用 `lazy()` 声明的变量不同。

我们还可以检查属性是否已被初始化。为了了解其工作原理，让我们向类中添加一个函数。如下所示，可以通过 `this::a` 调用当前对象的 `isInitialized` 函数，该函数返回 \`true\` 或 \`false\`：

```kotlin
lateinit var a: String

fun initA(a: String) {
    this.a = a
}

fun doSmth() {
    if (::a.isInitialized)
        println("a is Initialized")
    else
        println("a isn't Initialized")
}
```

> [!warning] Warning
> 如果在属性初始化之前尝试访问它，将会抛出错误：
> 
> 原因：kotlin.UninitializedPropertyAccessException：lateinit 属性 a 尚未初始化

## 结论

现在你已经熟悉了延迟初始化。你理解了延迟初始化的必要性以及如何应用它。虽然 `lazy()` 和 `lateinit` 的用法非常相似，但你也了解它们之间的区别。你还了解 `lazy()` 模式。

134 名学习者喜欢这篇理论文章， 8 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
