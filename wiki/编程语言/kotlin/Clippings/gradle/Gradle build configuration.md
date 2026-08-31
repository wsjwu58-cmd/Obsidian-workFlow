## Gradle 构建配置

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

您已经学习了如何在 Gradle 中设置项目、运行项目以及构建应用程序。现在，我们来谈谈 `build.gradle(.kts)` 文件，它是 Gradle 项目的主要配置文件。这些知识可以应用于 Gradle 支持的任何编程语言，例如 Java 或 Kotlin。

> [!warning] Warning
> 请注意，本文基于 **Gradle 9.0.0** ，其他 Gradle 版本可能存在一些差异。

## 配置文件

让我们继续使用之前创建的用于创建应用程序的项目。

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

由于这是一个应用程序类型的项目，您可以在 app 目录中找到 `build.gradle.kts` 文件。该文件有两种版本：用于 Groovy DSL 的 `build.gradle` 和用于 Kotlin DSL 的 `build.gradle.kts` 。它定义了项目结构，并包含了各种任务和外部库。让我们来了解一下它的主要组成部分。

## 插件

`plugins` 部分用于添加插件以扩展项目的功能，例如添加新任务或属性。

```java
plugins {
    // Apply the application plugin to add support for building a CLI application in Java.
    application

    // Apply the plugin which adds support for Kotlin/JVM
    kotlin("jvm") version "2.2.0"

    // Apply code formatter plugin, using version catalog
    alias(libs.plugins.spotless)
}
```

这里， `alias` 是一个保留关键字，它允许你加载在版本目录文件（ `gradle/libs.versions.toml` ）中定义的插件。以下是如何在版本目录中定义插件的示例。

```java
[versions]
spotless = "7.2.1"

[plugins]
spotless = { id = "com.diffplug.spotless:spotless-plugin-gradle", version.ref = "spotless" }
```

Kotlin 和 Java 的插件能够理解如何构建、打包项目以及运行测试。 `application` 插件则有助于创建可执行的 JVM 应用程序。

项目中使用插件还有另一种方法。这是一种比较传统的方案，现在不太常用，但你可能会遇到：

```java
apply plugin: "application"   // for Groovy DSL
apply(plugin = "application") // for Kotlin DSL
```

[官方 Gradle 插件页面](https://plugins.gradle.org/) 上还有许多其他插件可供使用。大型项目可以使用数百个插件，因为 Gradle 对项目中可使用的插件数量没有限制。

## 存储库和依赖项

通常情况下，你不需要从头开始编写程序——你可以使用自己或其他开发者编写的现有代码。这时，依赖关系系统就派上用场了。

`repositories` 部分声明了 Gradle 将从中下载依赖项并将其添加到项目的位置。

```java
repositories {
    // Use Maven Central for resolving dependencies.
    mavenCentral()
}
```

有很多公共仓库： **JCenter** 、 **Maven Central** 、 **Google** 等。通常，依赖项的描述会指明它位于哪个仓库中。

`dependencies` 部分允许您向项目中添加外部库。Gradle 会自动从代码仓库下载这些库，并将其包含在应用程序归档文件中。您的 `dependencies` 项部分至少应包含一个测试库，例如 `JUnit` 或其他选项，具体取决于您在初始化项目时的选择。首先，您需要在版本目录中定义该库，然后在 `build.gradle.kts` 中使用它。

```java
[versions]
guava = "33.4.6-jre"
junit-jupiter = "5.12.1"

[libraries]
guava = { module = "com.google.guava:guava", version.ref = "guava" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit-jupiter" }
```
```java
dependencies {
    // Use JUnit Jupiter for testing.
    testImplementation(libs.junit.jupiter)

    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // This dependency is used by the application.
    implementation(libs.guava)
}
```

在接下来的主题中，您将学习更多关于存储库和依赖项的知识。

这是 Gradle 构建结构的一个标准组成部分。您可以在这里应用插件并指定项目的依赖项。所有 Gradle 管理的项目都采用相同的结构。

## 应用程序插件的配置

自动生成的 `build.gradle.kts` 文件包含一个配置 `application` 程序插件的部分，使您可以使用 `gradle run` 命令运行应用程序。

```java
application {
    // Defines the main class for the application
    mainClass = "org.example.App"
}
```

`mainClass` 属性指定包含应用程序入口点的类。通过此配置，您可以执行 `gradle run` 命令来运行应用程序。

## 生成并运行 Jar 归档

现在，让我们来探讨一下可以使用 `build.gradle.kts` 文件的另一个场景。

运行基于 JVM 的应用程序的标准方法是使用 `java -jar` 命令。您可以不使用 Gradle 运行此命令，但需要先准备好 JAR 文件。让我们为应用程序构建 JAR 文件：

```java
gradle jar

BUILD SUCCESSFUL in 748ms
2 actionable tasks: 2 executed
```

现在，JAR 文件位于 `app/build/libs` 目录中。如果您想清除项目文件夹中所有生成的工件，只需运行 `gradle clean` 命令即可。

但是，如果您尝试使用传统方法运行我们生成的应用程序，则会遇到问题：

```java
java -jar app/build/libs/app.jar
no main manifest attribute, in app/build/libs/app.jar
```

应用程序的 `MANIFEST.MF` 文件中缺少 `Main-Class` 属性。因此，JVM 找不到应用程序入口点的路径。

要解决此问题，您需要在生成应用程序归档文件时添加所需的属性。请将以下声明添加到 `build.gradle.kts` 文件中：

```java
// for Groovy DSL
jar {
    manifest {
        attributes("Main-Class": "org.hyperskill.gradleapp.App")
    }
}

// for Kotlin DSL
tasks.jar {
    manifest {
        attributes("Main-Class" to "org.hyperskill.gradleapp.AppKt")
    }
}
```

这段代码将 `Main-Class` 属性添加到 jar 任务的 manifest 属性中。可以将 manifest 视为属性映射，您可以在其中添加 `Main-Class -> Main` 。

现在，当你运行 `gradle jar` 然后运行 `java -jar app/build/libs/app.jar` 时，一切都会正常工作，你会看到输出行 `Hello world!` 。

> [!primary] Primary
> 请记住，即使没有 Gradle，您也可以运行 `java -jar` 命令。您只需要准备好 JAR 文件即可。

## 结论

在本主题中，您学习了 build.gradle（或.kts）文件的基本结构，并初步了解了插件、仓库、依赖项和版本目录。现在您知道如何将插件和仓库添加到 build.gradle（或.kts）配置文件中。您探索了应用程序插件配置，并学习了如何解决 JAR 文件创建问题。在接下来的主题中，您将深入学习这些概念，以扩展您的 Gradle 知识。

151 名学员喜欢这篇理论文章， 28 名学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
