## 可变映射和可变集合作为接口

提供方： [JetBrains 学院](https://hyperskill.org/providers/2)

在 Kotlin 中， `MutableMap` 和 `MutableSet` 是扩展其不可变对应对象 `Map` 和 `Set` 接口。它们提供了修改集合的额外功能。

`MutableMap` 是一个键值对集合，其中每个键都是唯一的。它允许你添加、删除或更新条目。以下是一个示例：

```kotlin
val mutableMap = mutableMapOf("one" to 1, "two" to 2)
mutableMap["three"] = 3  // Add a new entry
mutableMap.remove("one") // Remove an entry
```

`MutableSet` 是一个包含唯一元素的集合，允许您添加、删除或更新元素。以下是一个示例：

```kotlin
val mutableSet = mutableSetOf(1, 2, 3)
mutableSet.add(4)    // Add a new element
mutableSet.remove(1) // Remove an element
```

可变集合和的主要区别在于后者是只读的；创建后就无法修改。例如，如果尝试向不可变集合中添加元素，则会收到编译错误：

```kotlin
val immutableSet = setOf(1, 2, 3)
immutableSet.add(4) // Compilation error
```

总之， `MutableMap` 和 `MutableSet` 比不可变的对应类型更灵活，但代价是额外的内存开销。当需要在创建集合后对其进行修改时，请使用它们。

## 理解 Kotlin 中的 Mutable Map

Kotlin 中的 `MutableMap` 接口是 Kotlin 集合框架的一部分。它继承自 `Map` 接口，并且允许修改映射条目，这与不可变的 `Map` 不同。

## MutableMap 的属性和方法

`MutableMap` 有两个主要属性： `keys` 和 `values` `keys` 返回一个包含映射中所有键的 `MutableSet` ，而 `values` 返回一个包含所有值的 `MutableCollection` 。

```kotlin
val mutableMap = mutableMapOf("one" to 1, "two" to 2)
println(mutableMap.keys) // prints: [one, two]
println(mutableMap.values) // prints: [1, 2]
```

`MutableMap` 接口提供了几个修改映射的方法，例如 `put()` 、 `putAll()` 、 `remove()` 和 `clear()` 。

```kotlin
mutableMap.put("three", 3) // adds a new key-value pair
mutableMap.remove("one") // removes the key-value pair with key "one"
mutableMap.clear() // removes all entries
```

## 何时以及为何使用 MutableMap

`Map` 是只读的，创建后无法修改，而 `MutableMap` 则允许修改。当您需要动态添加、删除或更新条目时，MutableMap 非常有用。

```kotlin
val map = mapOf("one" to 1, "two" to 2)
map["three"] = 3 // Error: Val cannot be reassigned

val mutableMap = mutableMapOf("one" to 1, "two" to 2)
mutableMap["three"] = 3 // OK
```

但是，您应该谨慎使用 `MutableMap` 。像 `Map` 这样的不可变对象本质上是线程安全的，不需要同步。如果您的映射在创建后不需要更改，为了获得更好的性能和安全性，请优先使用 `Map` 。

## 理解 Kotlin 中的可变集

Kotlin 中的 `MutableSet` 是一个扩展了 `Set` 接口的接口。与不可变的 `Set` 不同，它允许修改集合中的元素。

```kotlin
val mutableSet: MutableSet<Int> = mutableSetOf(1, 2, 3)
```

## MutableSet 的属性和方法

`MutableSet` 接口继承了 `Collection` 接口中的 `size` 和 `isEmpty` 等属性，并提供了额外的修改方法：

- `add(element: E)`: 将指定的元素添加到集合中。
- `remove(element: E)`: 从集合中删除指定元素的单个实例。
- `addAll(elements: Collection<E>)`: 将指定集合中的所有元素添加到集合中。
- `removeAll(elements: Collection<E>)`: 从此集合中删除所有也包含在指定集合中的元素。
```kotlin
mutableSet.add(4) // mutableSet now contains 1, 2, 3, 4
mutableSet.remove(1) // mutableSet now contains 2, 3, 4
```

## 何时以及为何使用 MutableSet

`Set` 确保了集合的不可变性，而当需要在创建集合后对其进行修改时，则需要使用 `MutableSet` 。它非常适合管理需要动态添加或删除唯一项的集合。

```kotlin
val names: MutableSet<String> = mutableSetOf("John", "Jane")
names.add("Joe") // names now contains John, Jane, Joe
```

请记住，虽然 `MutableSet` 提供了灵活性，但它牺牲了线程安全性。如果多个线程同时访问和修改 `MutableSet` ，则必须对其进行外部同步。

总之，在 Kotlin 中， `MutableSet` 是创建动态、独特集合的绝佳选择。不过，在 `Set` 和 `MutableSet` 之间做出选择之前，务必权衡自身需求以及它们的优缺点。

## Kotlin 中可变映射和可变集合的实际应用

MutableMap 和 MutableSet 是功能强大的 Kotlin 接口，允许您修改它们的元素。以下是一些实际应用案例：

**数据缓存** ：使用 MutableMap 缓存数据。它存储键值对，其中每个键都是唯一的。这种方法可以加快数据检索速度。

```kotlin
val cache: MutableMap<String, Any> = mutableMapOf()
cache["user"] = User("John", "Doe")
val user = cache["user"] as User
```

**统计出现次数** ：使用 MutableMap 统计集合中元素出现的次数。

```kotlin
val words = listOf("a", "b", "a", "c", "b", "a")
val frequencyMap: MutableMap<String, Int> = mutableMapOf()

for (word in words) {
    val count = frequencyMap[word] ?: 0
    frequencyMap[word] = count + 1
}
```

**数据分组** ：使用 MutableMap 根据特定条件对数据进行分组。

```kotlin
val people = listOf(Person("John", 20), Person("Jane", 30), Person("John", 30))
val peopleGroupedByAge: MutableMap<Int, MutableList<Person>> = mutableMapOf()

for (person in people) {
    peopleGroupedByAge.getOrPut(person.age) { mutableListOf() }.add(person)
}
```

**删除重复项** ：使用 MutableSet 从集合中消除重复元素，因为它只允许唯一元素。

```kotlin
val numbers = listOf(1, 2, 2, 3, 4, 4, 5)
val uniqueNumbers: MutableSet<Int> = mutableSetOf()

for (number in numbers) {
    uniqueNumbers.add(number)
}
```

以上仅列举几个例子。您可以根据具体需求定制 MutableMap 和 MutableSet 的应用场景。

## Kotlin 中使用 Mutable Map 和 Mutable Set 的最佳实践

在 Kotlin 中使用 Mutable Map 和 Mutable Set 时，以下是一些最佳实践：

1. **使用** `mutableMapOf()` **和** `mutableSetOf()` **函数** ：这些函数是创建和集合的最直接方法。
2. **避免不必要的变更** ：虽然变更代码是可行的，但最好避免不必要的变更。不必要的变更会导致错误，并使代码更难理解。
3. **使用** `put()` **方法向可变映射中添加元素** ：此方法会向映射中添加一个新的键值对。如果映射中已存在该键，则会覆盖其关联的值。
4. **使用** `add()` **方法向** 添加元素：此方法会将新元素添加到集合中。如果集合中已存在该元素，则不会再次添加。
5. **使用** `remove()` **方法删除元素** ：此方法从可变映射或集合中删除指定的元素。
6. **使用** `clear()` **方法删除所有元素** ：此方法从可变映射或集合中删除所有元素。

请记住，虽然可变集合功能强大，但应谨慎使用，以保持代码的可读性和可靠性。

## 结论

在 Kotlin 中， `MutableMap` 和 `MutableSet` 是强大的接口 `MutableMap` 它们扩展了不可变的 `Map` 和 `Set` ，允许你在创建集合后对其进行修改。MutableMap 是一个包含唯一键值对的集合，而 `MutableSet` 包含唯一的元素。它们都提供了添加、删除或更新元素的方法。

当您需要动态修改集合时，例如、统计出现次数、数据分组或删除重复项， MutableMap 和 MutableSet 就非常有用。但是，由于它们会带来额外的内存开销和潜在的线程安全问题，因此必须谨慎使用。

18 位学员喜欢这部分理论内容， 4 位学员不喜欢。 **你呢？**

报告拼写错误

## 相关条目
- [[Kotlin基础语法梳理]]
