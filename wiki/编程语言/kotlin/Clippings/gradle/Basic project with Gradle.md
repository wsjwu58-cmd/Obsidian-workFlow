## 使用 Gradle 的基本项目

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在本主题中，您将学习如何创建一个简单的 Gradle 项目以及 Gradle 如何管理它。我们假设您已经在计算机上安装了 Gradle。如果没有，请按照 [安装说明](https://gradle.org/install/) 进行操作。要验证安装是否成功，请运行 \` `gradle -v` 命令。如果出现错误，请在网上搜索具体错误信息、阅读文档或给我们留言描述问题。

## Gradle 的关键概念

让我们从介绍 Gradle 中的关键概念开始： **项目** 和 **任务** 。

- **项目** 可以代表待 **构建的内容** （例如 JAR 文件或 ZIP 压缩包），也可以代表 **待执行的操作** （例如部署应用程序）。每个 Gradle 构建都包含一个或多个项目。
- **任务** 是指构建过程中执行的单个工作单元。这可能包括编译类、运行测试、生成文档等等。每个项目本质上都是一个或多个任务的集合。

下图展示了这些概念之间的关系：

![gradle project tasks](https://ucarecdn.com/2ad089d5-37be-4d25-af1e-b26138a4af76/)

在简单的情况下，一个构建版本通常只包含一个项目和几个任务。这在你的学习过程中会很常见。如果这些概念看起来有点抽象，也不用担心。我们很快会学习一个更具体的例子。

## 初始化由 Gradle 管理的基本项目

让我们使用操作系统中的终端，通过 Gradle 初始化一个新项目。

> [!primary] Primary
> 未来，您很可能无需手动执行此操作，因为现代集成开发环境 (IDE) 可以自动为您完成此操作。

1\. 创建一个新目录来存储项目文件，然后进入该目录。

```java
mkdir gradle-demo
cd gradle-demo
```

2\. 运行 `gradle init` 命令生成一个简单的项目。新版本的 Gradle 会要求您在对话框中填写几个参数。为了熟悉这个过程，只需选择 `basic` 作为项目类型，并 `Groovy` 作为构建脚本 DSL 即可。

该命令将产生以下输出：

```
> Task :init

BUILD SUCCESSFUL in 10s
2 actionable tasks: 2 executed
```

Gradle 为您执行了一些任务，现在有一个结构最基本的简单项目：

```
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle
```

以下是所有生成文件的简要信息：

- `build.gradle` 文件是一个主要文件，它指定了 Gradle 项目，包括其任务和外部库。在这里，它位于 `gradle-demo` 文件夹中，可以在执行 `gradle init` 命令后创建。目前，该文件不包含任何有用的信息，但在实际项目中，它通常会被更新以添加新的信息。
- 文件 `gradle-wrapper.jar` 、 `gradle-wrapper.properties` 、 `gradlew` 和 `gradlew.bat` 属于 Gradle Wrapper，它允许您在不手动安装的情况下运行 Gradle。
- `settings.gradle` 文件指定要包含在构建中的项目。对于只有一个项目的构建，此文件是可选的；但对于多项目构建，此文件是必需的。

让我们从 `build.gradle` 所在的同一目录运行 `gradle build` 命令来构建项目。它将产生类似这样的输出：

```
> Task :buildEnvironment

------------------------------------------------------------
Root project
------------------------------------------------------------

...

BUILD SUCCESSFUL in 725ms
1 actionable task: 1 executed
```

因此，该项目已成功构建，并执行了一个任务。

> [!primary] Primary
> 您还可以调用 `build` 以及其他命令，例如在类 Unix 系统中使用 `./gradlew build` ，在 Windows 系统中使用 `gradlew.bat build` 。它会自动下载 Gradle 并运行指定的命令。使用封装器可以让开发者无需手动安装即可开始使用基于 Gradle 的项目。

## 通过 IntelliJ IDEA 创建一个基本项目

您也可以通过 IntelliJ IDEA 创建一个新的 Gradle 项目。为此，请在启动屏幕上选择“新建项目”选项，或在主菜单中单击 **“文件”>“新建”>“项目...”按钮** 。

![intellij idea welcome screen](https://ucarecdn.com/84f88453-1583-4a9f-9724-716ad3ba5f55/)

在“新建项目”窗口中，选择 **“新建项目”** 选项，然后选择所需的语言（Java 或 Kotlin）和构建系统（Gradle）。

![intellij idea new project window](https://ucarecdn.com/be3e28c1-bca9-4ee6-b671-dec5f8707f4b/)

在这里，您还可以选择项目名称和位置，并指定一些其他选项，例如 JDK 版本或 Gradle DSL 语言等。完成后，单击 **“创建”** 按钮。

片刻之后，一个新的由 Gradle 管理的项目将被创建并构建：

![intellij idea gradle project structure](https://ucarecdn.com/03ccd134-c726-4995-8029-b95f620e5eff/)

它的结构与使用终端命令构建的结构相同。

## 修改构建文件

让我们使用 Groovy DSL 向 `build.gradle` 文件添加一些属性和一个任务，使我们的构建过程更有趣。

```java
description = "A basic Gradle project"

task helloGradle {
    doLast {
        println 'Hello, Gradle!'
    }
}
```

在这里，我们设置了 `description` 属性，并定义了一个简单的任务，该任务会打印一条“hello”消息。使用 `gradle -q helloGradle` 命令执行该任务后，会输出以下内容：

```
> Task :buildEnvironment

------------------------------------------------------------
Root project - A basic Gradle project
------------------------------------------------------------

...

> Task :helloGradle
Hello, Gradle!

BUILD SUCCESSFUL in 831ms
2 actionable tasks: 2 executed
```

本次构建共执行了两个任务。我们的新任务打印了“ `Hello, Gradle!` 消息。此外，我们还修改了构建中的项目描述。 `-q` 参数用于简化命令输出。

> [!primary] Primary
> 你也可以在构建文件中使用 Kotlin 作为 DSL。要启用此功能，需要在创建项目时指定 Kotlin 作为 DSL。在这种情况下，文件名将是 `build.gradle.kts` 。

## 所有任务列表

如果您想查看所有可以执行的 Gradle 任务，只需运行 \` `gradle tasks --all` 命令即可。列表中也会包含我们的任务：

```
> Task :tasks

------------------------------------------------------------
Tasks runnable from root project - A basic Gradle project
------------------------------------------------------------

Build Setup tasks
-----------------
init - Initializes a new Gradle build.
wrapper - Generates Gradle wrapper files.

Help tasks
----------
buildEnvironment - Displays all buildscript dependencies declared in root project 'gradle-demo'.
...

Other tasks
-----------
helloGradle
```

在实际项目中，任务列表会更大，因为除了标准任务外，它还会包含来自各种插件（如 Java 或 Kotlin 插件）的大量任务。

我们已经将生成的简单项目中所有与 Gradle 相关的文件与任何源代码文件隔离开来。

## 结论

你已经学习了 Gradle 项目的关键概念，并且独立于任何源代码文件，研究了一个简单的生成项目中的所有文件。现在是时候将 Gradle 与你最喜欢的编程语言结合起来了！

696 名学习者喜欢这篇理论文章， 113 名学习者不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
