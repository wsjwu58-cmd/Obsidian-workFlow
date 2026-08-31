## 使用 Gradle 构建应用程序

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

希望您已经对 Gradle 的基本概念和使用方法有所了解。本主题将介绍如何使用此构建工具构建和运行小型应用程序。您在这里获得的知识可以应用于 Gradle 支持的任何基于 JVM 的编程语言（例如 Java 或 Kotlin）。

> [!warning] Warning
> 本文使用 **Gradle 9.0.0** 编写。其他 Gradle 版本可能存在差异。如果您在使用本文时遇到问题，可以阅读评论或参考 [Gradle 官方文档](https://docs.gradle.org/current/samples/sample_building_java_applications_multi_project.html) 。

## 初始化应用程序

我们假设您已经熟悉操作系统的终端，并将通过终端与 Gradle 进行交互。首先，创建一个新的空文件夹，名称随意（例如， `demo` ）。在该文件夹中，运行 `gradle init` 命令来初始化一个新的基于 Gradle 的项目。该命令会弹出一个对话框，供您设置所需的项目信息。

在此表单中，选择 `application` 作为项目类型，并选择 **Java** 或 **Kotlin** 作为实现语言。

```kotlin
Select type of build to generate:
  1: Application
  2: Library
  3: Gradle plugin
  4: Basic (build structure only)
Enter selection (default: Application) [1..4] 1

Select implementation language:
  1: Java
  2: Kotlin
  3: Groovy
  4: Scala
  5: C++
  6: Swift
Enter selection (default: Java) [1..6] 1

Enter target Java version (min: 7, default: 21): 21

Project name (default: demo): demo

Select application structure:
  1: Single application project
  2: Application and library project
Enter selection (default: Single application project) [1..2] 1

Select build script DSL:
  1: Kotlin
  2: Groovy
Enter selection (default: Kotlin) [1..2] 1

Select test framework:
  1: JUnit 4
  2: TestNG
  3: Spock
  4: JUnit Jupiter
Enter selection (default: JUnit Jupiter) [1..4] 4

Generate build using new APIs and behavior (some features may change in the next minor release)? (default: no) [yes, no] no
```

初始化完成后，项目结构如下：

```
.
├── app
│   ├── build.gradle.kts
│   └── src
│       ├── main
│       │   ├── java
│       │   │   └── org
│       │   │       └── example
│       │   │           └── App.java
│       │   └── resources
│       └── test
│           ├── java
│           │   └── org
│           │       └── example
│           │           └── AppTest.java
│           └── resources
├── gradle
│   ├── wrapper
│   │   ├── gradle-wrapper.jar
│   │   └── gradle-wrapper.properties
│   └── libs.version.toml
├── gradlew
├── gradlew.bat
├── gradle.properties
└── settings.gradle.kts
```

这个结构包含了很多你已经了解的文件（ `settings.gradle.kts` 、包装文件等等）。之所以存在一个名为 `app` 文件夹，是因为你将项目类型选择了 `application` ，这个文件夹代表了我们的应用程序。你将在下一节中更详细地了解 `build.gradle.kts` 文件。

`app` 下还有一个 `src` 目录，其中包含 `main` 和 `test` 两个子目录。这是使用 Gradle 时相当标准的项目结构。在本例中， `org.example` 包包含一些 Java 源代码（ `App.java` ）。如果您选择 Kotlin 作为实现语言，项目结构基本相同，只是源代码文件会使用 Kotlin 的 `.kt` 文件（而不是 `.java` ），并且会使用 `kotlin` 文件夹（而不是 `java` 文件夹）。

> [!primary] Primary
> 请注意，对于 Java 和 Kotlin 项目来说，将组织名称作为包名包含在源代码文件的路径中是一个好做法，例如 `org.hyperskill` 。

## 运行应用程序

如果您使用命令 `gradle tasks --all` 查看可用于管理项目的任务列表，您会发现该列表相当长。以下是其简化版本：

```java
Application tasks
-----------------
app:run - Runs this project as a JVM application

Build tasks
-----------
app:assemble - Assembles the outputs of this project.
app:build - Assembles and tests this project.
...
```

要启动应用程序，您可以使用 Gradle 的 `run` 命令。为此，请运行 `gradle run` 命令，或者您可以使用适用于您操作系统的 Gradle Wrapper 脚本。此命令将构建并运行应用程序。以下是一个输出示例：

```java
> Task :app:run
Hello World!

BUILD SUCCESSFUL in 3s
2 actionable tasks: 2 executed
```

如您所见，自动生成的应用程序已经可以显示欢迎字符串。如果您也得到类似的结果，则表示一切正常：您的应用程序运行良好，Gradle 可以管理它！

如果你再次查看项目结构，你会发现 `app/build/` 下新增了一些文件，包括带有字节码的文件（ `App.class` 和 `AppTest.class` ）。实际上，当我们执行 `run` 命令时，Gradle 构建并启动了 `App.class` 文件。

## 构建应用程序

如果要生成包含所有依赖项和启动应用程序脚本的应用程序包，请使用 `gradle build` 命令。

```java
BUILD SUCCESSFUL in 22s
7 actionable tasks: 7 executed
```

如果一切正常，Gradle 会为您生成两种格式的归档文件： `app/build/distributions/app.jar` 和 `app/build/distributions/app.zip` 。现在，您可以分发您的应用程序了！

## 结论

在本主题中，您学习了如何使用 Gradle 创建应用程序。您可以使用 Java 或 Kotlin 编写这些应用程序。您还学习了如何使用 `gradle run` 命令运行这些应用程序。此外，您还了解了 Gradle 生成的项目文件夹的基本结构。接下来，您将进一步学习如何配置该文件夹中的文件。

650 名学员喜欢这篇理论文章， 132 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
