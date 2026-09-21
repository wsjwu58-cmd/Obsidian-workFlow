## 在 Compose 中使用状态

应用中的状态是指可以随时间变化的任何值。在该应用中，状态是指账单金额。

添加用于存储状态的变量：

1. 在 `EditNumberField()` 函数的开头，使用 `val` 关键字添加 `amountInput` 变量，并将它设为 `"0"` 值：

```
val amountInput = "0"
```

这是应用的账单金额状态。

1. 将 `value` 具名形参设置为 `amountInput` 值：

```
TextField(
   value = amountInput,
   onValueChange = {},
)
```

## 组合

“组合”是对 Compose 在执行可组合项时所构建界面的描述。Compose 应用调用可组合函数，以将数据转换为界面。如果发生状态更改，Compose 会使用新状态重新执行受影响的可组合函数，从而创建更新后的界面。这一过程称为“重组”。Compose 会为您安排重组。

在 Compose 中，您可以使用 [`State`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/State?authuser=77&hl=zh-cn) 和 [`MutableState`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/MutableState?authuser=77&hl=zh-cn) 类型让应用中的状态可被 Compose 观察或跟踪。`State` 类型不可变，因此您只能读取其中的值，而 [`MutableState`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/MutableState?authuser=77&hl=zh-cn) 类型是可变的。您可以使用 [`mutableStateOf()`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary?authuser=77&hl=zh-cn#mutableStateOf(kotlin.Any,androidx.compose.runtime.SnapshotMutationPolicy)) 函数来创建可观察的 `MutableState`。它接受初始值作为封装在 `State` 对象中的形参，这样便可使其 `value` 变为可观察。

`mutableStateOf()` 函数返回的值：

- 会保持状态，即账单金额。
- 可变，因此该值可以更改。
- 可观察，因此 Compose 会观察值的所有更改并触发重组以更新界面。

添加 cost-of-service 状态：

1. 在 `EditNumberField()` 函数中，将 `amountInput` 状态变量前面的 `val` 关键字更改为 `var` 关键字：

```
var amountInput = "0"
```

这会使 `amountInput` 可变。

1. 使用 `MutableState<String>` 类型（而非硬编码的 `String` 变量），以便 Compose 知道要跟踪 `amountInput` 状态，然后传入 `"0"` 字符串，该字符串是 `amountInput` 状态变量的初始默认值：

```
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateOf

var amountInput: MutableState<String> = mutableStateOf("0")
```

也可以使用类型推断编写 `amountInput` 初始化，如下所示：

```
var amountInput = mutableStateOf("0")
```

`mutableStateOf()` 函数接受初始值 `"0"` 作为实参，这样便可使其 `amountInput` 变为可观察。这会导致 Android Studio 中出现以下编译警告，但您很快就可以修复此问题：

```
Creating a state object during composition without using remember.
```

1. 在 `TextField` 可组合函数中，使用 `amountInput.value` 属性：

```
TextField(
   value = amountInput.value,
   onValueChange = {},
   modifier = modifier
)
```

Compose 会跟踪每个读取状态 `value` 属性的可组合项，并在其 `value` 更改时触发重组。

当文本框的输入更改时，系统会触发 `onValueChange` 回调。在 lambda 表达式中，`it` 变量包含新值。

1. 在 `onValueChange` 具名形参的 lambda 表达式中，将 `amountInput.value` 属性设置为 `it` 变量：

```
@Composable
fun EditNumberField(modifier: Modifier = Modifier) {
   var amountInput = mutableStateOf("0")
   TextField(
       value = amountInput.value,
       onValueChange = { amountInput.value = it },
       modifier = modifier
   )
}
```

当 `TextField` 通过 `onValueChange` 回调函数通知您文本发生更改时，您将更新 `TextField` 的状态（即 `amountInput` 变量）。

## [使用 remember 函数保存状态](https://developer.android.com/codelabs/basic-android-kotlin-compose-using-state?authuser=77&hl=zh-cn&continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-compose-unit-2-pathway-3%3Fauthuser%3D77%26hl%3Dzh-cn%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-compose-using-state#5)

可组合方法可能会因重组而被系统多次调用。如果不保存，可组合项就会在重组期间重置状态。

可组合函数可以使用 [`remember`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/remember.composable?authuser=77&hl=zh-cn#remember(kotlin.Function0)) 跨重组存储对象。初始组合期间，`remember` 函数计算的值会存储在组合中，而存储的值会在重组期间返回。`remember` 和 `mutableStateOf` 函数通常在可组合函数中一起使用，以使状态及其更新正确反映在界面中。

在 `EditNumberField()` 函数中使用 `remember` 函数：

1. 在 `EditNumberField()` 函数中，使用 `remember` 将对 [`mutableStateOf`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary?authuser=77&hl=zh-cn#mutableStateOf(kotlin.Any,androidx.compose.runtime.SnapshotMutationPolicy))`()` 的调用括起来，以便使用 `by` `remember` Kotlin 属性委托来初始化 `amountInput` 变量。
2. 在 [`mutableStateOf`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary?authuser=77&hl=zh-cn#mutableStateOf(kotlin.Any,androidx.compose.runtime.SnapshotMutationPolicy))`()` 函数中，传入一个空字符串（而非静态 `"0"` 字符串）：

```
var amountInput by remember { mutableStateOf("") }
```

现在，空字符串是 `amountInput` 变量的初始默认值。`by` 是 [Kotlin 属性委托](https://kotlinlang.org/docs/delegated-properties.html)。`amountInput` 属性的默认 getter 和 setter 函数分别委托给 `remember` 类的 getter 和 setter 函数。

1. 导入以下函数：

```
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
```

**警告：**此代码可能会抛出下图所示的关于 `getValue()` 扩展函数的错误：

![b651ccb43a6fd25.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260918154630238.png)

如果是这样，请将 `getValue` 和 `setValue` 导入内容手动添加到文件开头的 import 代码块中，如下图所示：

![bad619de4ecfefc.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260918154628471.png)

通过添加委托的 getter 和 setter 导入内容，您可以读取和设置 `amountInput`，而无需引用 `MutableState` 的 `value` 属性。

更新后的 `EditNumberField()` 函数应如下所示：

```
@Composable
fun EditNumberField(modifier: Modifier = Modifier) {
   var amountInput by remember { mutableStateOf("") }
   TextField(
       value = amountInput,
       onValueChange = { amountInput = it },
       modifier = modifier
   )
}
```

### remember 函数解析

`remember { mutableStateOf("") }` 这一段，核心是 **Kotlin 的高阶函数 + Lambda 表达式 + 尾随 Lambda 语法**。

你可以先把它展开成这样：

```
remember({
    mutableStateOf("")
})
```

这里的：

```
{
    mutableStateOf("")
}
```

不是普通的代码块，而是一个 **Lambda 表达式**。

大致可以理解成：

```
() -> MutableState<String>
```

也就是说，这是一个“没有参数，最后返回 `MutableState<String>` 的函数”。

`remember` 本身可以粗略理解成这样的函数：

```
fun <T> remember(calculation: () -> T): T
```

它接收一个函数：

```
calculation: () -> T
```

然后返回这个函数计算出来的结果：

```
T
```

所以：

```
remember {
    mutableStateOf("")
}
```

这里 Kotlin 会推导出：

```
T = MutableState<String>
```

整个过程相当于：

```
val lambda = {
    mutableStateOf("")
}

val state = remember(lambda)
```

## 修改外观

在上一部分中，您已经让文本字段正常运行了。在本部分中，您将改进界面。

### **向文本框添加标签**

每个文本框都应包含一个标签，以便用户了解可以输入哪些信息。在以下示例图片的第 1 部分中，标签文本位于文本字段的中间，并与输入行对齐。在以下示例图片的第 2 部分中，当用户点击文本框以输入文本时，该标签会移到文本框中靠上的位置。如需详细了解文本字段剖析，请参阅[剖析](https://material.io/components/text-fields#anatomy)。

![a2afd6c7fc547b06.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260918155542970.png)

修改 `EditNumberField()` 函数，以向文本字段添加标签：

1. 在 `EditNumberField()` 函数的 `TextField()` 可组合函数中，添加一个设置为空 lambda 表达式的 `label` 具名形参：

```
TextField(
//...
   label = { }
)
```

1. 在 lambda 表达式中，调用接受 `stringResource``(R.string.``bill_amount``)` 的 `Text()` 函数：

```
label = { Text(stringResource(R.string.bill_amount)) },
```

1. 在 `TextField()` 可组合函数中，添加设置为 `true` 值的 `singleLine` 具名形参：

```
TextField(
  // ...
   singleLine = true,
)
```

这样可以将文本框从多行压缩成可水平滚动的单行。

1. 添加设置为 `KeyboardOptions()` 的 `keyboardOptions` 形参：

```
import androidx.compose.foundation.text.KeyboardOptions

TextField(
  // ...
   keyboardOptions = KeyboardOptions(),
)
```

Android 提供了一个选项，用于配置屏幕上显示的键盘，以便输入数字、电子邮件地址、网址和密码等内容。如需详细了解其他键盘类型，请参阅 [KeyboardType](https://developer.android.com/reference/kotlin/androidx/compose/ui/text/input/KeyboardType?authuser=77&hl=zh-cn)。

1. 将键盘类型设置为数字键盘即可输入数字。向 `KeyboardOptions` 函数传递设置为 `KeyboardType.Number` 的 `keyboardType` 具名形参：

```
import androidx.compose.ui.text.input.KeyboardType

TextField(
  // ...
   keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
)
```

完成后的 `EditNumberField()` 函数应如以下代码段所示：

```
@Composable
fun EditNumberField(modifier: Modifier = Modifier) {
    var amountInput by remember { mutableStateOf("") }
    TextField(
        value = amountInput,
        onValueChange = { amountInput = it },
        singleLine = true,
        label = { Text(stringResource(R.string.bill_amount)) },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        modifier = modifier
    )
}
```

### Lambda表达式传递

Lambda 是外面的 `{ }`：

```
label = { Text("Bill Amount") }
        ↑                    ↑
        └──── Lambda ────────┘
```

而：

```
Text("Bill Amount")
```

只是 **Lambda 里面执行的一个函数调用**。

#### 先看普通 Kotlin

比如：

```
val action = {
    println("Hello")
}
```

这里：

```
{ println("Hello") }
```

整体才是 Lambda。

其中：

```
println("Hello")
```

只是 Lambda 里面调用了 `println()` 函数。

所以：

```
label = {
    Text("Bill Amount")
}
```

完全是同一个道理。

------

#### 那为什么 `label` 要写成 Lambda？

因为 `OutlinedTextField` 的 `label` 参数需要的类型类似：

```
label: @Composable (() -> Unit)?
```

重点看：

```
() -> Unit
```

这是 Kotlin 的**函数类型**，意思是：

> 一个没有参数、没有返回值的函数。

所以它不能接收：

```
label = Text("Bill Amount") // ❌
```

因为这代表**现在立刻调用 `Text()`**。

它需要的是：

> 「你给我一段代码，等我需要绘制 label 的时候，我再调用它。」

因此要传：

```
label = {
    Text("Bill Amount")
}
```

也就是把这个 Lambda 交给 `OutlinedTextField`。

可以类比成：

```
fun test(action: () -> Unit) {
    action()
}
```

调用：

```
test(
    action = {
        println("Hello")
    }
)
```

这里 `println()` 不是 Lambda：

```
{ println("Hello") }
└──────┬────────┘
     Lambda

  println("Hello")
  └──────┬──────┘
       函数调用
```

Compose 也是一样：

```
label = { Text("Bill Amount") }
        └─────────┬─────────┘
                Lambda
                  │
                  ↓
            Text("Bill Amount")
                  │
                  ↓
              函数调用
```

#### 为什么 Compose 特别喜欢这种写法？

因为这样 `OutlinedTextField` 可以自己决定**在哪里、什么时候、以什么上下文调用你的 UI**。

而且你传进去的不一定只能有一个 `Text`：

```
label = {
    Row {
        Icon(...)
        Text("Bill Amount")
    }
}
```

这时候就能看出 Lambda 的意义了：`label` 接收的是**一小块 UI 内容**，而不是一个字符串。

## [状态提升](https://developer.android.com/codelabs/basic-android-kotlin-compose-using-state?authuser=77&hl=zh-cn&continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-compose-unit-2-pathway-3%3Fauthuser%3D77%26hl%3Dzh-cn%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-compose-using-state#9)

在本部分中，您将了解如何决定在哪里定义状态，以便能够重复使用和共享可组合项。

在可组合函数中，您可以定义一些变量，用于保存要在界面中显示的状态。例如，您在 `EditNumberField()` 可组合项中将 `amountInput` 变量定义为状态。

当您的应用变得越来越复杂并且其他可组合项需要访问 `EditNumberField()` 可组合项中的状态时，您需要考虑将 `EditNumberField()` 可组合函数中的状态提升或提取出来。

### 了解有状态和无状态**可组合项**

当您需要执行以下操作时，应该提升状态：

- 与多个可组合函数共享状态。
- 创建可在应用中重复使用的无状态可组合项。

在您从可组合函数中提取状态后，生成的可组合函数称为无状态函数。也就是说，通过从可组合函数中提取状态，可以将其变为无状态。

无状态可组合项是指没有状态的可组合项，这意味着它不会保存、定义或修改新状态。相反，有状态可组合项是指具有可以随时间变化的状态的可组合项。

**注意**：在实际应用中，让可组合项完全无状态可能很难实现，具体取决于可组合项的职责。在设计可组合项时，您应该让可组合项拥有尽可能少的状态，并允许在提升状态有意义的情况下通过在可组合项的 API 中公开状态来实现状态提升。

状态提升是一种将状态移到其调用方以使组件变为无状态的模式。

当应用于可组合项时，这通常意味着向可组合项引入以下两个形参：

- `value: T` 形参，即要显示的当前值。
- `onValueChange: (T) -> Unit` - 回调 lambda，会在值更改时触发，以便可以在其他位置更新状态（例如，当用户在文本框中输入一些文本时）。

在 `EditNumberField()` 函数中提升状态：

1. 更新 `EditNumberField()` 函数定义，以通过添加 `value` 和 `onValueChange` 形参来提升状态：

```
@Composable
fun EditNumberField(
   value: String,
   onValueChange: (String) -> Unit,
   modifier: Modifier = Modifier
) {
//...
```

`value` 形参的类型为 `String`，`onValueChange` 形参的类型为 `(String) -> Unit`，因此它是一个接受 `String` 值作为输入且没有返回值的函数。`onValueChange` 形参用作传入 `TextField` 可组合项的 `onValueChange` 回调。

**注意**：最佳实践是为所有可组合函数提供默认的 [`Modifier`](https://developer.android.com/reference/kotlin/androidx/compose/ui/Modifier?authuser=77&hl=zh-cn) 形参，从而提高可重用性。您应在所有必需形参的后面添加它作为第一个可选形参。

1. 在 `EditNumberField()` 函数中，更新 `TextField()` 可组合函数以使用传入的形参：

```
TextField(
   value = value,
   onValueChange = onValueChange,
   // Rest of the code
)
```

1. 提升状态，将记住的状态从 `EditNumberField()` 函数移至 `TipTimeLayout()` 函数：

```
@Composable
fun TipTimeLayout() {
   var amountInput by remember { mutableStateOf("") }

   val amount = amountInput.toDoubleOrNull() ?: 0.0
   val tip = calculateTip(amount)
  
   Column(
       //...
   ) {
       //...
   }
}
```

1. 您已将状态提升到 `TipTimeLayout()`，现在将其传递到 `EditNumberField()`。在 `TipTimeLayout()` 函数中，更新 `EditNumberField``()` 函数调用以使用提升的状态：

```
EditNumberField(
   value = amountInput,
   onValueChange = { amountInput = it },
   modifier = Modifier
       .padding(bottom = 32.dp)
       .fillMaxWidth()
)
```

这会使 `EditNumberField` 变为无状态。您已将界面状态提升到其祖先实体 `TipTimeLayout()`。`TipTimeLayout()` 现在是状态(`amountInput`) 所有者。

### **位置格式设置**

通过位置格式设置，您可以使用字符串显示动态内容。例如，假设您希望 **Tip amount** 文本框显示一个 `xx.xx` 值，该值可以是在您的函数中计算并设置格式的任意金额。如需在 `strings.xml` 文件中完成此操作，您需要使用占位符实参定义字符串资源，如以下代码段所示：

```
// No need to copy.

// In the res/values/strings.xml file
<string name="tip_amount">Tip Amount: %s</string>
```

在 Compose 代码中，您可以拥有多个任意类型的占位符实参。`string` 占位符为 `%s`。

请注意 `TipTimeLayout()` 中的文本可组合项，您要将采用相应格式的小费金额作为实参传递到 `stringResource()` 函数。

```
// No need to copy
Text(
   text = stringResource(R.string.tip_amount, "$0.00"),
   style = MaterialTheme.typography.displaySmall
)
```

1. 在函数 `TipTimeLayout()` 中，使用 `tip` 属性显示小费金额。更新 `Text` 可组合项的 `text` 形参，以将 `tip` 变量用作形参。

```
Text(
     text = stringResource(R.string.tip_amount, tip),
     // ...
```

完成后的 `TipTimeLayout()` 和 `EditNumberField()` 函数应如以下代码段所示：

```
@Composable
fun TipTimeLayout() {
   var amountInput by remember { mutableStateOf("") }
   val amount = amountInput.toDoubleOrNull() ?: 0.0
   val tip = calculateTip(amount)

   Column(
       modifier = Modifier
            .statusBarsPadding()
            .padding(horizontal = 40.dp)
            .verticalScroll(rememberScrollState())
            .safeDrawingPadding(),
       horizontalAlignment = Alignment.CenterHorizontally,
       verticalArrangement = Arrangement.Center
   ) {
       Text(
           text = stringResource(R.string.calculate_tip),
           modifier = Modifier
               .padding(bottom = 16.dp, top = 40.dp)
               .align(alignment = Alignment.Start)
       )
       EditNumberField(
           value = amountInput,
           onValueChange = { amountInput = it },
           modifier = Modifier
               .padding(bottom = 32.dp)
               .fillMaxWidth()
       )
       Text(
           text = stringResource(R.string.tip_amount, tip),
           style = MaterialTheme.typography.displaySmall
       )
       Spacer(modifier = Modifier.height(150.dp))
   }
}

@Composable
fun EditNumberField(
   value: String,
   onValueChange: (String) -> Unit,
   modifier: Modifier = Modifier
) {
   TextField(
       value = value,
       onValueChange = onValueChange,
       singleLine = true,
       label = { Text(stringResource(R.string.bill_amount)) },
       keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
       modifier = modifier
   )
}
```

总而言之，您将 `amountInput` 状态从 `EditNumberField()` 提升到了 `TipTimeLayout()` 可组合项中。为了让文本框能够像以前一样工作，您必须向 `EditNumberField()` 可组合函数传入两个实参：`amountInput` 值，以及根据用户输入更新 `amountInput` 值的 lambda 回调。借助这些更改，您即可根据 `TipTimeLayout()` 中的 `amountInput` 属性计算并向用户显示小费金额。