提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

如果你曾经在编程中使用过，那么你可能问过自己：“如何将多个常量存储在一个地方并同时处理它们？” Kotlin 对此问题给出了答案，我们称之为 **枚举（Enums）** 。简而言之， **枚举** 代表一组逻辑常量，它们使我们的代码更清晰、更易读。让我们来仔细了解一下枚举。

## 基本枚举

`enum` 是一个关键字，它允许我们仅从普通的类创建我们自己的枚举（ `enum` 所代表的单词）：

```kotlin
enum class Rainbow {
    RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET
}
```

如上例所示，这里列出了代表彩虹七种颜色的枚举类型。现在我们有了自己的存储空间来存放这些颜色。每种颜色都是一个独立的枚举实例。稍后您将看到如何进一步修改它。当然，您现在也可以创建自己的枚举类型，例如，用于表示订单状态：

```kotlin
enum class Status {
    OPEN, PENDING, IN_PROGRESS, RESOLVED, REJECTED, CLOSED
}
```

或者，主要建筑材料类型如下：

```kotlin
enum class Materials {
    GLASS, WOOD, FABRIC, METAL, PLASTIC, CERAMICS, CONCRETE, ROCK
}
```

根据 Kotlin 编码规范，您可以使用大写字母分隔的名称（例如 Kotlin 常量 `RED_COLOR` ），也可以使用以大写字母开头的驼峰式枚举名称（ `RedColor` ）。为了便于理解，我们的示例中将省略第二种选项，仅使用大写枚举，但请记住，两种选项都是可行的。

让我们回到第一个颜色示例。由于每种颜色都是 Rainbow 枚举的一个实例，因此您可以通过将这些颜色的名称传递给构造函数来初始化它们：

```kotlin
enum class Rainbow(val color: String) {
    RED("Red"),
    ORANGE("Orange"),
    YELLOW("Yellow"),
    GREEN("Green"),
    BLUE("Blue"),
    INDIGO("Indigo"),
    VIOLET("Violet")
}
```

现在我们可以像这样在任何地方使用颜色值：

```kotlin
val color = Rainbow.RED.color
```

看起来很有前景，但你可能会问“有什么好处呢？”问得好。稍后你就会明白，但现在让我们修改枚举，并为每个颜色添加一个参数：

```kotlin
enum class Rainbow(val color: String, val rgb: String) {
    RED("Red", "#FF0000"),
    ORANGE("Orange", "#FF7F00"),
    YELLOW("Yellow", "#FFFF00"),
    GREEN("Green", "#00FF00"),
    BLUE("Blue", "#0000FF"),
    INDIGO("Indigo", "#4B0082"),
    VIOLET("Violet", "#8B00FF")
}
```

太棒了！Rainbow 枚举不仅包含颜色名称，还包含其十六进制值。在 Web 开发中，将颜色值存储为蓝、红、绿三种颜色的十六进制数字形式是一种常用的方法。您可以 [在这里](https://en.wikipedia.org/wiki/Web_colors) 了解更多关于 Web 颜色的信息。现在，您可以像这样使用它们：

```kotlin
val rgb = Rainbow.RED.rgb
```

正如我们之前所说，Enum 仍然是一个自定义类，因此我们可以向其中添加我们自己的方法。让我们添加一个方法来打印 Rainbow 实例的完整信息：

```kotlin
enum class Rainbow(val color: String, val rgb: String) {
    RED("Red", "#FF0000"),
    ORANGE("Orange", "#FF7F00"),
    YELLOW("Yellow", "#FFFF00"),
    GREEN("Green", "#00FF00"),
    BLUE("Blue", "#0000FF"),
    INDIGO("Indigo", "#4B0082"),
    VIOLET("Violet", "#8B00FF");

    fun printFullInfo() {
        println("Color - $color, rgb - $rgb")
    }
}
```

现在，我们姑且称之为：

```kotlin
val rgb = Rainbow.RED
rgb.printFullInfo()
```

输出结果如下：

```kotlin
Color - Red, rgb - #FF0000
```

## 枚举内部

现在我们知道了枚举是什么以及如何创建它，但在大多数情况下，这还不够。是时候了解 Kotlin 中枚举提供了哪些开箱即用的 **方法** 和属性了：

1\. `name` 可以获取枚举实例的名称，例如：

```kotlin
val color: Rainbow = Rainbow.RED
println(color.name)
```

输出结果：

```kotlin
RED
```

2\. `ordinal` 包含枚举实例的位置，例如：

```kotlin
val color: Rainbow = Rainbow.GREEN
println(color.ordinal)
```

输出结果如下：

```kotlin
3
```

3\. `entries` 属性返回一个包含所有 Enum 实例的数组。如果您需要遍历 Enum 实例 `entries` 这将非常有用。现在我们可以检查某个特定颜色是否属于 Rainbow 数组。entries 属性是 synthetic `values()` 函数的现代高效替代方案，也是推荐的做法：

```kotlin
fun isRainbow(color: String) : Boolean {
    for (enum in Rainbow.entries) {
        if (color.toUpperCase() == enum.name) return true
    }
    return false
}
```

试着打电话：

```kotlin
println(isRainbow("black"))
```

输出结果如下：

```kotlin
false
```

4\. `valueOf()` 通过枚举名称返回一个字符串类型的 Enum 实例，区分大小写：

```kotlin
println(Rainbow.valueOf("RED"))
```

输出结果为：

```kotlin
RED
```

如果没有合适的枚举实例，则会抛出 `IllegalArgumentException` 异常。请注意，此方法区分大小写。

让我们来看一个包含 `entries` 的示例：

```kotlin
enum class Rainbow(val color: String, val rgb: String) {
    RED("Red", "#FF0000"),
    ORANGE("Orange", "#FF7F00"),
    YELLOW("Yellow", "#FFFF00"),
    GREEN("Green", "#00FF00"),
    BLUE("Blue", "#0000FF"),
    INDIGO("Indigo", "#4B0082"),
    VIOLET("Violet", "#8B00FF"),
    NULL("", "");

    fun printFullInfo() {
        println("Color - $color, rgb - $rgb")
    }
}

fun findByRgb(rgb: String): Rainbow {
    for (rainbow in Rainbow.entries) {
        if (rgb == rainbow.rgb) return rainbow
    }
    return Rainbow.NULL
}
```

你可以这样使用它：

```kotlin
println(findByRgb("#FF0001"))
```

输出结果为：

```kotlin
NULL
```

你猜到为什么结果是 `NULL` 了吗？你可能已经注意到了，我们添加了一个 NULL 常量，以便在找不到与 RGB 参数匹配的颜色时返回它。在我们的示例中，没有与 RGB 值“#FF0001”关联的颜色，因此输出为 NULL。

## 结论

让我们总结一下以上信息：简而言之，Kotlin 的枚举（Enum）是一个用于存储常量集合的容器。为了方便起见，它内置了一些属性和方法，可以让你获取常量的名称和顺序。你可以获取枚举的所有实例，也可以只获取其中一个，这应该会让你的工作更轻松。别忘了，你可以随时扩展你的枚举。现在你已经了解了它的用法，让我们开始练习吧！

472 名学习者喜欢这篇理论文章， 39 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
