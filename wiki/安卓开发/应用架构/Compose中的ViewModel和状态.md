## [了解应用架构](https://developer.android.com/codelabs/basic-android-kotlin-compose-viewmodel-and-state?authuser=77&hl=zh-cn&continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-compose-unit-4-pathway-1%3Fauthuser%3D77%26hl%3Dzh-cn%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-compose-viewmodel-and-state#3)

应用架构提供了在应用中的类之间分配责任时应遵循的准则。精心设计的应用架构可以帮助您扩缩应用，以及用更多功能对应用进行扩展。架构还可以简化团队协作。

最常用的[架构原则](https://developer.android.com/jetpack/guide?authuser=77&hl=zh-cn#common-principles)包括：**分离关注点**和**通过模型驱动界面**。

**分离关注点**

分离关注点设计原则指出，应将应用分为函数类，每个类都有各自的责任。

**通过模型驱动界面**

通过模型驱动界面原则指出，应该通过模型驱动界面，最好是通过持久性模型。模型是负责处理应用数据的组件。它们独立于应用中的界面元素和应用组件，因此不受应用的生命周期以及相关的关注点的影响。

### 推荐的应用架构

基于上一部分提到的常用架构原则，每个应用应至少有两个层：

- **界面层：**在屏幕上显示应用数据但独立于数据的层。
- **数据层：**用于存储、检索和提供应用数据的层。

您可以另外添加一个名为“网域层”的架构层，以简化和重复使用界面层与数据层之间的交互。该层是可选的，不在本课程的范围之内。

![a4da6fa5c1c9fed5.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260920204246090.png)

**注意**：本指南示意图中的箭头表示各个类之间的依赖关系。例如，网域层依赖于数据层类。

### 界面层

界面层（或表示层）的作用是在屏幕上显示应用数据。每当数据因用户互动（例如按了某个按钮）而发生变化时，界面都应随之更新，以反映这些变化。

界面层由以下组件组成：

- **界面元素：**用于在屏幕上呈现数据的组件。您将使用 [Jetpack Compose](https://developer.android.com/jetpack/compose?authuser=77&hl=zh-cn) 构建这些元素。
- **状态容器：**用于保存数据、向界面提供数据以及处理应用逻辑的组件。状态容器的一个示例为 [ViewModel](https://developer.android.com/topic/libraries/architecture/viewmodel?authuser=77&hl=zh-cn)。

![6eaee5b38ec247ae.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260920204249946.png)

### ViewModel

`ViewModel` 组件用于存储和公开界面所使用的状态。界面状态是经过 `ViewModel` 转换的应用数据。`ViewModel` 可让您的应用遵循通过模型驱动界面的架构原则。

`ViewModel` 会存储应用相关的数据，这些数据不会在 Android 框架销毁并重新创建 activity 时销毁。与 activity 实例不同，`ViewModel` 对象不会被销毁。应用会在配置更改期间自动保留 `ViewModel` 对象，以便它们存储的数据在重组后立即可用。

如需在应用中实现 `ViewModel`，请扩展架构组件库中提供的 `ViewModel` 类，并将应用数据存储在该类中。

### 界面状态

界面是相对用户而言的，而界面状态是相对应用而言的。界面是界面状态的直观呈现。对界面状态所做的任何更改都会立即反映在界面中。

![9cfedef1750ddd2c.png](https://gitee.com/Wsj123789/wsj/raw/master/img/20260920204253093.png)

*界面是将屏幕上的界面元素与界面状态绑定在一起的结果。*

```
// Example of UI state definition, do not copy over

data class NewsItemUiState(
    val title: String,
    val body: String,
    val bookmarked: Boolean = false,
    ...
)
```