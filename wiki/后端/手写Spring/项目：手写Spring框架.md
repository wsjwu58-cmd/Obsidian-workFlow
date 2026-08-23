# 项目：手写Spring框架
[实现AOP - 手写Spring - 廖雪峰的官方网站](https://liaoxuefeng.com/books/summerframework/aop/index.html)

## 实现IOC

## 实现ResourceResolver

Java的ClassLoader机制可以在指定的Classpath中根据类名加载指定的Class，但遗憾的是，给出一个包名，例如，`org.example`，它并不能获取到该包下的所有Class，也不能获取子包。要在Classpath中扫描指定包名下的所有Class，包括子包，实际上是在Classpath中搜索所有文件，找出文件名匹配的`.class`文件。例如，Classpath中搜索的文件`org/example/Hello.class`就符合包名`org.example`，我们需要根据文件路径把它变为`org.example.Hello`，就相当于获得了类名。因此，搜索Class变成了搜索文件。

提供一个`ResourceResolver`，定义`scan()`方法来获取扫描到的`Resource`：

```
public class ResourceResolver {
    String basePackage;

    public ResourceResolver(String basePackage) {
        this.basePackage = basePackage;
    }

    public <R> List<R> scan(Function<Resource, R> mapper) {
        ...
    }
}

```

过滤Class:

```
// 定义一个扫描器:
ResourceResolver rr = new ResourceResolver("org.example");
List<String> classList = rr.scan(res -> {
    String name = res.name(); // 资源名称"org/example/Hello.class"
    if (name.endsWith(".class")) { // 如果以.class结尾
        // 把"org/example/Hello.class"变为"org.example.Hello":
        return name.substring(0, name.length() - 6).replace("/", ".").replace("\\", ".");
    }
    // 否则返回null表示不是有效的Class Name:
    return null;
});

```

## 实现PropertyResolver

Spring框架中，注入分为@Autowired和@Value两种，第一种依赖bean注入，而第二中只是简单

的属性注入，所以，我们可以创建一个类。存放配置的属性，并提供方法来获取属性

Java中提供了按照key查询的Properties,我们可以将其传入

### PropertyResolver

```
public PropertyResolver(Properties props) {  
    //获取环境变量  
    this.properties.putAll(System.getenv());  
    Set<String> names = props.stringPropertyNames();  
    for (String name : names) {  
        this.properties.put(name, props.getProperty(name));  
    }  
    if (logger.isDebugEnabled()) {  
        List<String> keys = new ArrayList<>(this.properties.keySet());  
        Collections.sort(keys);  
        for (Iterator<String> it = keys.iterator(); it.hasNext();) {  
            String key = it.next();  
            logger.debug("PropertyResolver: {} = {}", key, this.properties.get(key));  
        }  
    }  
  
    converters.put(String.class, s -> s);  
    converters.put(boolean.class, s -> Boolean.parseBoolean(s));  
    converters.put(Boolean.class, s -> Boolean.valueOf(s));  
  
    converters.put(byte.class, s -> Byte.parseByte(s));  
    converters.put(Byte.class, s -> Byte.valueOf(s));  
  
    converters.put(short.class, s -> Short.parseShort(s));  
    converters.put(Short.class, s -> Short.valueOf(s));  
  
    converters.put(int.class, s -> Integer.parseInt(s));  
    converters.put(Integer.class, s -> Integer.valueOf(s));  
  
    converters.put(long.class, s -> Long.parseLong(s));  
    converters.put(Long.class, s -> Long.valueOf(s));  
  
    converters.put(float.class, s -> Float.parseFloat(s));  
    converters.put(Float.class, s -> Float.valueOf(s));  
  
    converters.put(double.class, s -> Double.parseDouble(s));  
    converters.put(Double.class, s -> Double.valueOf(s));  
  
    converters.put(LocalDate.class, s -> LocalDate.parse(s));  
    converters.put(LocalTime.class, s -> LocalTime.parse(s));  
    converters.put(LocalDateTime.class, s -> LocalDateTime.parse(s));  
    converters.put(ZonedDateTime.class, s -> ZonedDateTime.parse(s));  
    converters.put(Duration.class, s -> Duration.parse(s));  
    converters.put(ZoneId.class, s -> ZoneId.of(s));  
}
```

### 获取键值

解析${abc.xyz:defaultValue}这样的key，我们需要定义一个实体类，传入key和默认值，所以在获取键值（getProperty(String key)）的方法中，我们需要判断是否存在默认值（parsePropertyExpr(String key)），如果不存在默认值，则将属性defaultValue置为NULL

### 转换类型

方法

```
<T> T convert(Class<?> clazz, String value) {  
    Function<String, Object> fn = this.converters.get(clazz);  
    if (fn == null) {  
        throw new IllegalArgumentException("Unsupported value type: " + clazz.getName());  
    }  
    return (T) fn.apply(value);  
}
```

存储

```
Map<Class<?>, Function<String, Object>> converters = new HashMap<>();
```

```
键为要转化的对象,所以我们可以通过Function类型来实现注入类型的转换
```

### 传入key的思考

如果key所对应的值也存在占位符的使用，那么应该如何处理：

定义一个函数专门进行处理占位符，如果存在占位符，递归重新获取键值，没有则返回原值

### 函数调用总览

```
getProperty(String key)
├── parsePropertyExpr(key)
├── getRequiredProperty(key)
│   └── getProperty(key)
├── parseValue(value)
│   ├── parsePropertyExpr(value)
│   ├── getProperty(key, defaultValue)
│   └── getRequiredProperty(key)
└── 返回结果

getProperty(String key, String defaultValue)
├── getProperty(key)
└── parseValue(defaultValue)

getProperty(String key, Class<T> targetType)
├── getProperty(key)
└── convert(targetType, value)

getRequiredProperty(String key, Class<T> targetType)
├── getProperty(key, targetType)
└── Objects.requireNonNull()

```

核心：getProperty(String key) 调用后先判断是否是占位符格式，如果是，将其转换成指定的实体 类，再次进行判断：如果有默认值->获取默认值，没有则获取属性值

getProperty(String key, Class\<\> targetType)和getRequiredProperty(String key, Class\<\> targetType)是对注入的属性值进行类型转换

## 创建BeanDefinition

我们可以定义BeanDefinitiin这样一个类来管理Bean的信息，包括：名称，声明类型，构造器方法，工厂方法名称，工厂方法，声明类型，Bean的实例，Bean的顺序，对外提供工厂方法和构造器方法的有参构造

定义好类型以后，我们可以设置一个Map\<\>类型的变量，按照名字存储Bean信息

```

public class AnnotationConfigApplicationContext {
    Map<String, BeanDefinition> beans;
}
```

但是如果我们按照名字查找Bean的话，只能返回一个实例或者无实例，使用上存在一定的局限，但如果按照类查询的话，无法定义以class为键的Map类型，因为可能声明类型和实际类型不一定相符，如果不进行标注，可能返回多个实例

```
@Configuration
public class AppConfig {
    @Bean
    AtomicInteger counter() {
        return new AtomicInteger();
    }
    
    @Bean
    Number bigInt() {
        return new BigInteger("1000000000");
    }
}

```

所以我们需要定义一个方法，根据类型查找出所有满足条件的BeanDefinition，然后再定义一个方法，如果有唯一标识，则返回特定BeanDefinition

```
// 根据Type查找若干个BeanDefinition，返回0个或多个:
List<BeanDefinition> findBeanDefinitions(Class<?> type) {
    return this.beans.values().stream()
        // 按类型过滤:
        .filter(def -> type.isAssignableFrom(def.getBeanClass()))
        // 排序:
        .sorted().collect(Collectors.toList());
    }
}

```

```
// 根据Type查找某个BeanDefinition，如果不存在返回null，如果存在多个返回@Primary标注的一个:
@Nullable
public BeanDefinition findBeanDefinition(Class<?> type) {
    List<BeanDefinition> defs = findBeanDefinitions(type);
    if (defs.isEmpty()) { // 没有找到任何BeanDefinition
        return null;
    }
    if (defs.size() == 1) { // 找到唯一一个
        return defs.get(0);
    }
    // 多于一个时，查找@Primary:
    List<BeanDefinition> primaryDefs = defs.stream().filter(def -> def.isPrimary()).collect(Collectors.toList());
    if (primaryDefs.size() == 1) { // @Primary唯一
        return primaryDefs.get(0);
    }
    if (primaryDefs.isEmpty()) { // 不存在@Primary
        throw new NoUniqueBeanDefinitionException(String.format("Multiple bean with type '%s' found, but no @Primary specified.", type.getName()));
    } else { // @Primary不唯一
        throw new NoUniqueBeanDefinitionException(String.format("Multiple bean with type '%s' found, and multiple @Primary specified.", type.getName()));
    }
}

```

所以主要流程：

```
1. 构造函数调用
   ↓
2. 扫描配置类及其关联的 Bean 类名
   → 获取 @ComponentScan 指定的包（默认为 configClass 所在包）
   → 使用 ResourceResolver 扫描这些包下的所有 .class 文件 → 提取全限定类名
   → 同时收集 @Import 导入的配置类名
   ↓
3. 得到一组候选类名 Set<String> classNameSet
   ↓
4. 遍历每个类名，加载 Class 对象
   → Class.forName(className)
   ↓
5. 判断该 Class 是否是“组件”（即是否间接或直接标注了 @Component）
   → 通过 ClassUtils.findAnnotation(clazz, Component.class) 递归查找元注解
   ↓
6. 若是组件：
   → 提取 Bean 名称（默认为首字母小写的类名）
   → 获取合适的构造方法（用于后续实例化）
   → 查找 @Order、@Primary、@PostConstruct、@PreDestroy 等注解信息
   → 创建 BeanDefinition（类型为 clazz，无工厂方法）
   → 注册到 Map<String, BeanDefinition> beans
   ↓
7. 若该组件同时是 @Configuration（即工厂类）：
   → 遍历其所有方法
   → 查找带有 @Bean 注解的方法
      → 提取 Bean 名称（默认为方法名）
      → 声明类型 = 方法返回类型（注意：不一定是实际运行时类型！）
      → 工厂方法 = 该 Method 对象
      → 工厂 Bean 名 = 配置类的 Bean 名（用于后续调用实例方法）
      → 读取 @Bean(initMethod="...", destroyMethod="...")
      → 创建 BeanDefinition（带 factoryName + factoryMethod）
      → 注册到 beans Map
   ↓
8. 最终得到完整的 Map<String, BeanDefinition> beans
   ↓
9. （后续步骤，虽未实现但隐含）：
   → 按依赖顺序实例化 Bean（先实例化 @Configuration 工厂类）
   → 调用构造方法 或 工厂方法 创建 instance
   → 注入依赖（字段/方法/setter）
   → 调用初始化方法（@PostConstruct / init-method）
```

## 创建Bean实例

Spring提供了四种注入方法：构造方法注入，工厂方法注入，Setter注入，字段注入

前两种方法Bean的创建和注入是不可分离的，后两种可以先创建，后注入

因为创建和注入是不可分离的，所以如果遇到循环注入就只能抛出异常

检测循环依赖

```
if (!this.creatingBeanNames.add(def.getName())) {  
    throw new UnsatisfiedDependencyException(String.format("Circular dependency detected when create bean '%s'", def.getName()));  
}
```

尝试将当前创建的Bean姓名进行存放，如果已经创建，说明存在循环依赖，抛出异常

逻辑：

createBeanAsSingleton 有三种入口

1. 创建@Configuration类型的Bean

2. 创建普通的Bean

1.  递归执行

第一种方式必然不会循环依赖

第二种方式在执行前会检查instance是否已赋值，所以不会让creatingBeanNames重复

只有第三者情况，即在递归执行createBeanAsSingleton时，才可能存在重复；如果遇到重复的Bean，说明之前的Bean还没创建完成，也就说明有了循环依赖

创建时先创建配置类，再创建普通Bean

核心逻辑：通过递归循环调用依赖创建进行注入，如果构造函数或者工厂方法的参数又进行了依赖

注入，可以再次调用方法创建实例返回，通过反射获取构造函数及其参数，创建实例，完成依赖注

入

```
private Object createBeanAsEarlySingleton(BeanDefinition def) {  
        log.debug("Try create bean '{}' as early singleton: {}", def.getName(), def.getBeanClass().getName());  
        //检测循环依赖  
        if (!this.creatingBeanNames.add(def.getName())) {  
            throw new UnsatisfiedDependencyException(String.format("Circular dependency detected when create bean '%s'", def.getName()));  
        }  
        //创建方式：构造函数或工厂方法  
        //Executable:统一处理构造函数和工厂方法  
        Executable  createFn=null;  
        if (def.getFactoryName()== null){  
            createFn=def.getConstructor();  
        }else {  
            createFn=def.getFactoryMethod();  
        }  
        // 创建参数:  
        final Parameter[] parameters = createFn.getParameters();  
        final Annotation[][] parametersAnnos = createFn.getParameterAnnotations();  
        Object[] args = new Object[parameters.length];  
        for (int i = 0; i < parameters.length; i++) {  
            final Parameter param = parameters[i];  
            final Annotation[] paramAnnos = parametersAnnos[i];  
            final Value value = ClassUtils.getAnnotation(paramAnnos, Value.class);  
            final Autowired autowired = ClassUtils.getAnnotation(paramAnnos, Autowired.class);  
  
            // @Configuration类型的Bean是工厂，不允许使用@Autowired创建:  
            final boolean isConfiguration = isConfigurationDefinition(def);  
            if (isConfiguration && autowired != null) {  
                throw new BeanCreationException(  
                        String.format("Cannot specify @Autowired when create @Configuration bean '%s': %s.", def.getName(), def.getBeanClass().getName()));  
            }  
  
            // 参数需要@Value或@Autowired两者之一:  
            if (value != null && autowired != null) {  
                throw new BeanCreationException(  
                        String.format("Cannot specify both @Autowired and @Value when create bean '%s': %s.", def.getName(), def.getBeanClass().getName()));  
            }  
            if (value == null && autowired == null) {  
                throw new BeanCreationException(  
                        String.format("Must specify @Autowired or @Value when create bean '%s': %s.", def.getName(), def.getBeanClass().getName()));  
            }  
            // 参数类型:  
            final Class<?> type = param.getType();  
            if (value != null) {  
                // 参数是@Value:  
                args[i] = this.propertyResolver.getRequiredProperty(value.value(), type);  
            } else {  
                // 参数是@Autowired:  
                String name = autowired.name();  
                boolean required = autowired.value();  
                // 依赖的BeanDefinition:  
                BeanDefinition dependsOnDef = name.isEmpty() ? findBeanDefinition(type) : findBeanDefinition(name, type);  
                // 检测required==true?  
                if (required && dependsOnDef == null) {  
                    throw new BeanCreationException(String.format("Missing autowired bean with type '%s' when create bean '%s': %s.", type.getName(),  
                            def.getName(), def.getBeanClass().getName()));  
                }  
                if (dependsOnDef != null) {  
                    // 获取依赖Bean:  
                    Object autowiredBeanInstance = dependsOnDef.getInstance();  
                    if (autowiredBeanInstance == null && !isConfiguration) {  
                        // 当前依赖Bean尚未初始化，递归调用初始化该依赖Bean:  
                        autowiredBeanInstance = createBeanAsEarlySingleton(dependsOnDef);  
                    }  
                    args[i] = autowiredBeanInstance;  
                } else {  
                    args[i] = null;  
                }  
            }  
        }  
  
        //创建Bean实例  
        Object instance=null;  
        //构造函数创建  
        if(def.getFactoryName()== null){  
            try {  
                //注入过程：创建Bean实例  
                instance = def.getConstructor().newInstance(args);  
            }catch (Exception e){  
                throw new BeanCreationException(e);  
            }  
        }else {  
//            获取配置类实例：通过 getBean(def.getFactoryName()) 获取定义了 @Bean 方法的配置类实例  
//            调用工厂方法：使用 def.getFactoryMethod().invoke(configInstance, args) 调用 @Bean 注解的方法来创建 Bean 实例  
//            异常处理：如果调用过程中发生异常，包装成 BeanCreationException 抛出  
//            设置实例：通过 def.setInstance(instance) 将创建好的实例设置到 BeanDefinition 中  
//            返回实例：最终返回创建的 Bean 实例  
            // 用@Bean方法创建:  
            Object configInstance = getBean(def.getFactoryName());  
            try {  
                instance = def.getFactoryMethod().invoke(configInstance, args);  
            } catch (Exception e) {  
                throw new BeanCreationException(String.format("Exception when create bean '%s': %s", def.getName(), def.getBeanClass().getName()), e);  
            }  
        }  
        //设置实例  
        def.setInstance(instance);  
        return def.getInstance();  
  
    }
```

## 初始化Bean

在创建Bean过程中，我们实现了强依赖注入，接下来实现字段和Setter注入

使用Setter方法和字段注入时，要注意一点，就是不仅要在当前类查找，还要在父类查找，因为有些`@Autowired`写在父类，所有子类都可使用，这样更方便。注入弱依赖代码如下：

```
// 在当前类及父类进行字段和方法注入:
void injectProperties(BeanDefinition def, Class<?> clazz, Object bean) {
    // 在当前类查找Field和Method并注入:
    for (Field f : clazz.getDeclaredFields()) {
        tryInjectProperties(def, clazz, bean, f);
    }
    for (Method m : clazz.getDeclaredMethods()) {
        tryInjectProperties(def, clazz, bean, m);
    }
    // 在父类查找Field和Method并注入:
    Class<?> superClazz = clazz.getSuperclass();
    if (superClazz != null) {
        // 递归调用:
        injectProperties(def, superClazz, bean);
    }
}

// 注入单个属性
void tryInjectProperties(BeanDefinition def, Class<?> clazz, Object bean, AccessibleObject acc) {
    ...
}

```

注入完依赖之后，在对BeanDifinition进行遍历，执行init方法

## 实现BeanPostProcessor

`BeanPostProcessor`的出现改变了这一切。Spring允许用户自定义一种特殊的Bean，即实现了`BeanPostProcessor`接口，它有什么用呢？其实就是替换Bean。

例子：

```
@Configuration
@ComponentScan
public class AppConfig {

    public static void main(String[] args) {
        var ctx = new AnnotationConfigApplicationContext(AppConfig.class);
        // 可以获取到ZonedDateTime:
        ZonedDateTime dt = ctx.getBean(ZonedDateTime.class);
        System.out.println(dt);
        // 错误:NoSuchBeanDefinitionException:
        System.out.println(ctx.getBean(LocalDateTime.class));
    }

    // 创建LocalDateTime实例
    @Bean
    public LocalDateTime localDateTime() {
        return LocalDateTime.now();
    }

    // 实现一个BeanPostProcessor
    @Bean
    BeanPostProcessor replaceLocalDateTime() {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
                // 将LocalDateTime类型实例替换为ZonedDateTime类型实例:
                if (bean instanceof LocalDateTime) {
                    return ZonedDateTime.now();
                }
                return bean;
            }
        };
    }
}

```

定义一个代理类继承原始Bean，通过BeanPostProcessor的postProcessBeforeInitialization（）

方法将原始Bean替换为代理类，并将BeanDenifition中对应的实现类进行替换

但是由此引发了一个问题，当我们想对这个Bean注入依赖的时候，是注入到原始Bean还是代理Bean上呢，举个例子

```
@Configuration
@ComponentScan
public class AppConfig {

    public static void main(String[] args) {
        var ctx = new AnnotationConfigApplicationContext(AppConfig.class);
        UserService u = ctx.getBean(UserService.class);
        System.out.println(u.getClass().getSimpleName()); // UserServiceProxy
        u.register("bob@example.com", "bob12345");
    }

    @Bean
    BeanPostProcessor createProxy() {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
                // 实现事务功能:
                if (bean instanceof UserService u) {
                    return new UserServiceProxy(u);
                }
                return bean;
            }
        };
    }
}

@Component
class UserService {
    public void register(String email, String password) {
        System.out.println("INSERT INTO ...");
    }
}

// 代理类:
class UserServiceProxy extends UserService {
    UserService target;

    public UserServiceProxy(UserService target) {
        this.target = target;
    }

    @Override
    public void register(String email, String password) {
        System.out.println("begin tx");
        target.register(email, password);
        System.out.println("commit tx");
    }
}

```

我们创建的代理类实现了事务功能，但是方法还是调用的原始Bean，也就是说必须对原始Bean进行

注入，否则在调用原始方法时会进行报错

两条原则：

1.  一个Bean如果被Proxy替换，则依赖它的Bean应注入Proxy，即上图的`MvcController`应注入`UserServiceProxy`；
2.  一个Bean如果被Proxy替换，如果要注入依赖，则应该注入到原始对象，即上图的`JdbcTemplate`应注入到原始的`UserService`。

基于这个原则，要满足条件1是很容易的，因为只要创建Bean完成后，立刻调用`BeanPostProcessor`就实现了替换，后续其他Bean引用的肯定就是Proxy了。先改造创建Bean的流程，在创建`@Configuration`后，接着创建`BeanPostProcessor`，再创建其他普通Bean：

```

 // 创建BeanPostProcessor类型的Bean:
    List<BeanPostProcessor> processors = this.beans.values().stream()
            // 过滤出BeanPostProcessor:
            .filter(this::isBeanPostProcessorDefinition)
            // 排序:
            .sorted()
            // 创建BeanPostProcessor实例:
            .map(def -> {
                return (BeanPostProcessor) createBeanAsEarlySingleton(def);
            }).collect(Collectors.toList());
    this.beanPostProcessors.addAll(processors);

```

替换实例

```
public Object createBeanAsEarlySingleton(BeanDefinition def) {
    ...

    // 创建Bean实例:
    Object instance = ...;
    def.setInstance(instance);

    // 调用BeanPostProcessor处理Bean:
    for (BeanPostProcessor processor : beanPostProcessors) {
        Object processed = processor.postProcessBeforeInitialization(def.getInstance(), def.getName());
        // 如果一个BeanPostProcessor替换了原始Bean，则更新Bean的引用:
        if (def.getInstance() != processed) {
            def.setInstance(processed);
        }
    }
    return def.getInstance();
}

```

这时，对这个Bean进行依赖注入会有问题，因为注入的是Proxy而不是原始Bean，怎么办？

这时我们要思考原始Bean去哪了？原始Bean实际上是被`BeanPostProcessor`给丢了！如果`BeanPostProcessor`能保存原始Bean，那么，注入前先找到原始Bean，就可以把依赖正确地注入给原始Bean。我们给`BeanPostProcessor`加一个`postProcessOnSetProperty()`方法，让它返回原始Bean：

我们可以重写BeanPostProcessor中的 postProcessOnSetProperty（）方法，定义一个Map集合保留原始Bean,并返回原始Bean

例如：

```
// 在AroundProxyBeanPostProcessor中的实现：
public class AroundProxyBeanPostProcessor implements BeanPostProcessor {
    Map<String, Object> originBeans = new HashMap<>();  // 保存了原始Bean的引用
    
    @Override
    public Object postProcessOnSetProperty(Object bean, String beanName) {
        Object origin = this.originBeans.get(beanName);  // 查找原始Bean
        return origin != null ? origin : bean;  // 返回原始Bean或保持当前Bean
    }
}
```

## 实现AOP

## 相关知识

拦截器的invoke方法

Object invoke(Object proxy, Method method, Object\[\] args) throws Throwable

### 参数说明

*   `Object proxy`：**代理对象本身**（动态生成的子类实例）
*   `Method method`：**被调用的方法**（如 `hello()`, `morning()`）
*   `Object[] args`：**方法参数**（调用时传入的参数）

思路：通过注解的方式实现AOP，客户端自定义一个拦截器，例如Around拦截器，处理增强方法的逻辑，定义一个ProxyResolver传入原始Bean和自定义的拦截器进行代理类的创建；然后实现完整的AOP，定义一个AroundProxyBeanPostProcessor类实现BeanPostProcessor接口，在其中识别指定的注解并创建代理类，最后通过配置类将其放在IOC容器当中

## 实现ProxyResolver

在IoC容器中，实现动态代理需要用户提供两个Bean：

1.  原始Bean，即需要被代理的Bean；
2.  拦截器，即拦截了目标Bean的方法后，会自动调用拦截器实现代理功能。

拦截器需要定义接口，这里我们直接用Java标准库的`InvocationHandler`，免去了自定义接口。

假定我们已经从IoC容器中获取了原始Bean与实现了`InvocationHandler`的拦截器Bean，那么就可以编写一个`ProxyResolver`来实现AOP代理。

从[ByteBuddy的官网](https://bytebuddy.net/)上搜索很容易找到相关代码，我们整理为`createProxy()`方法：

```
public class ProxyResolver {
    // ByteBuddy实例:
    ByteBuddy byteBuddy = new ByteBuddy();

    // 传入原始Bean、拦截器，返回代理后的实例:
    public <T> T createProxy(T bean, InvocationHandler handler) {
        // 目标Bean的Class类型:
        Class<?> targetClass = bean.getClass();
        // 动态创建Proxy的Class:
        Class<?> proxyClass = this.byteBuddy
                // 子类用默认无参数构造方法:
                .subclass(targetClass, ConstructorStrategy.Default.DEFAULT_CONSTRUCTOR)
                // 拦截所有public方法:
                .method(ElementMatchers.isPublic()).intercept(InvocationHandlerAdapter.of(
                        // 新的拦截器实例:
                        //这个拦截器的作用是将所有public方法调用转发给外部的handler处理，同时传递原始bean实例、方法信息和参数，实现了AOP的切面功能
                        new InvocationHandler() {
                            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                                // 将方法调用代理至原始Bean:
                                return handler.invoke(bean, method, args);
                            }
                        }))
                // 生成字节码:
                .make()
                // 加载字节码:
                .load(targetClass.getClassLoader()).getLoaded();
        // 创建Proxy实例:
        Object proxy;
        try {
            proxy = proxyClass.getConstructor().newInstance();
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return (T) proxy;
    }
}

```

## 实现Around

`AroundProxyBeanPostProcessor`的机制非常简单：检测每个Bean实例是否带有`@Around`注解，如果有，就根据注解的值查找Bean作为`InvocationHandler`，最后创建Proxy，返回前保存了原始Bean的引用，因为IoC容器在后续的注入阶段要把相关依赖和值注入到原始Bean。

### 实现before和after

只需要实现拦截器接口，再实现类中定义before或after方法,后续定义拦截器的时候再实现这个抽象

类就可以了

```
public abstract class BeforeInvocationHandlerAdapter implements InvocationHandler {

    public abstract void before(Object proxy, Method method, Object[] args);

    @Override
    public final Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        before(proxy, method, args);
        return method.invoke(proxy, args);
    }
}

```

## 关键组件说明

### 1. **核心处理器**

*   `AroundProxyBeanPostProcessor`: AOP入口，处理@Around注解
*   `AnnotationProxyBeanPostProcessor`: 抽象基类，支持自定义注解

### 2. **拦截器类型**

*   **Around**: 完全控制方法调用
*   **Before**: 方法执行前拦截 (`BeforeInvocationHandlerAdapter`)
*   **After**: 方法执行后拦截 (`AfterInvocationHandlerAdapter`)

### 3. **执行流程特点**

**初始化阶段:**

*   BeanPostProcessor优先创建
*   检测@Around注解创建代理
*   属性注入到原始Bean

**运行时阶段:**

*   方法调用被代理对象拦截
*   根据拦截器类型执行相应逻辑
*   最终调用原始Bean方法

### 扩展Annotation

假设我们后续编写了一个事务模块，提供注解`@Transactional`，那么，要启动AOP，就必须仿照`AroundProxyBeanPostProcessor`，提供一个`TransactionProxyBeanPostProcessor`，不过复制代码太麻烦了，我们可以改造一下`AroundProxyBeanPostProcessor`，用泛型代码处理Annotation，先抽象出一个`AnnotationProxyBeanPostProcessor`：

```
public abstract class AnnotationProxyBeanPostProcessor<A extends Annotation> implements BeanPostProcessor {

    Map<String, Object> originBeans = new HashMap<>();
    Class<A> annotationClass;

    public AnnotationProxyBeanPostProcessor() {
        this.annotationClass = getParameterizedType();
    }
    ...
}

```

实现`AroundProxyBeanPostProcessor`就一行定义：

```jsp
public class AroundProxyBeanPostProcessor extends AnnotationProxyBeanPostProcessor<Around> {
}
```

后续如果我们想实现`@Transactional`注解，只需定义：

```jsp
public class TransactionalProxyBeanPostProcessor extends AnnotationProxyBeanPostProcessor<Transactional> {
}
```

就能自动根据`@Transactional`启动AOP。

## 实现JdbcTemplate

### 配置DataSource

使用JdbcTemplate之前，我们需要配置JDBC数据源。Spring本身只提供了基础的`DriverManagerDataSource`，但Spring Boot有一个默认配置的数据源，并采用HikariCP作为连接池。

实现一个HikariCP支持的`DataSource`，用配置类 JdbcConfiguration管理

```
@Configuration
public class JdbcConfiguration {

    @Bean(destroyMethod = "close")
    DataSource dataSource(
            // properties:
            @Value("${summer.datasource.url}") String url,
            @Value("${summer.datasource.username}") String username,
            @Value("${summer.datasource.password}") String password,
            @Value("${summer.datasource.driver-class-name:}") String driver,
            @Value("${summer.datasource.maximum-pool-size:20}") int maximumPoolSize,
            @Value("${summer.datasource.minimum-pool-size:1}") int minimumPoolSize,
            @Value("${summer.datasource.connection-timeout:30000}") int connTimeout
    ) {
        var config = new HikariConfig();
        config.setAutoCommit(false);
        config.setJdbcUrl(url);
        config.setUsername(username);
        config.setPassword(password);
        if (driver != null) {
            config.setDriverClassName(driver);
        }
        config.setMaximumPoolSize(maximumPoolSize);
        config.setMinimumIdle(minimumPoolSize);
        config.setConnectionTimeout(connTimeout);
        return new HikariDataSource(config);
    }
}
```

然后我们需要封装一个JdbcTemplate类，注入依赖DataSource,实现对数据库的一些操作 底层实现如下：

```
1. queryForObject(sql, rowMapper, 123)
   ↓
2. execute(psc, pscAction)          // 中间层execute
   ↓  
3. execute(connectionCallback)      // 底层execute
   ↓
4. dataSource.getConnection()       // 获取连接
   ↓
5. conn.setAutoCommit(true)         // 临时启用自动提交
   ↓
6. psc.createPreparedStatement(conn)
   │   ↓
   │   7. conn.prepareStatement("SELECT...")
   │   8. bindArgs(ps, 123) → ps.setObject(1, 123)
   │
   ↓
7. pscAction.doInPreparedStatement(ps)
   │   ↓
   │   10. ps.executeQuery() → ResultSet
   │   11. rs.next() → 遍历结果集
   │   12. rowMapper.mapRow(rs, rowNum) → User对象
   │
   ↓
8. 自动关闭ResultSet (try-with-resources)
9. 自动关闭PreparedStatement (try-with-resources)
10. conn.setAutoCommit(false)       // 恢复原始设置
11. 自动关闭Connection (try-with-resources)
```

最后把JdbcTemplate类写到配置类即可

## 实现声明式事务

Spring提供的声明式事务管理能极大地降低应用程序的事务代码。如果使用基于Annotation配置的声明式事务，则一个与数据库操作相关的类只需加上`@Transactional`注解，就实现了事务支持，非常方便

定义`@Transactional`注解时，需要指定默认的拦截器名称，默认值`platformTransactionManager`（接口）表示用名字为`platformTransactionManager`的Bean来管理事务

我们现在要做的就是实现该接口以及 InvocationHandler接口进行事务拦截器的开发

```
public class DataSourceTransactionManager implements
        PlatformTransactionManager, InvocationHandler
{
    static final ThreadLocal<TransactionStatus> transactionStatus = new ThreadLocal<>();
    final DataSource dataSource;

    public DataSourceTransactionManager(DataSource dataSource) {
        this.dataSource = dataSource;
    }
}

```

在invoke函数内部编写事务开启，事务进行以及事务关闭的逻辑

```
@Override
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    TransactionStatus ts = transactionStatus.get();
    if (ts == null) {
        // 当前无事务,开启新事务:
        try (Connection connection = dataSource.getConnection()) {
            final boolean autoCommit = connection.getAutoCommit();
            if (autoCommit) {
                connection.setAutoCommit(false);
            }
            try {
                // 设置ThreadLocal状态:
                transactionStatus.set(new TransactionStatus(connection));
                // 调用业务方法:
                Object r = method.invoke(proxy, args);
                // 提交事务:
                connection.commit();
                // 方法返回:
                return r;
            } catch (InvocationTargetException e) {
                // 回滚事务:
                TransactionException te = new TransactionException(e.getCause());
                try {
                    connection.rollback();
                } catch (SQLException sqle) {
                    te.addSuppressed(sqle);
                }
                throw te;
            } finally {
                // 删除ThreadLocal状态:
                transactionStatus.remove();
                if (autoCommit) {
                    connection.setAutoCommit(true);
                }
            }
        }
    } else {
        // 当前已有事务,加入当前事务执行:
        return method.invoke(proxy, args);
    }
}

```

但是开启事务以后，如何让其他在当前事务的方法加入进来呢？

我们需要编写一个有关事务的工具类，获取当前事务的连接

```
public class TransactionalUtils {
    @Nullable
    public static Connection getCurrentConnection() {
        TransactionStatus ts = DataSourceTransactionManager.transactionStatus.get();
        return ts == null ? null : ts.connection;
    }
}

```

改造当前Template加入事务的逻辑

```
public class JdbcTemplate {
    public <T> T execute(ConnectionCallback<T> action) throws DataAccessException {
        // 尝试获取当前事务连接:
        Connection current = TransactionalUtils.getCurrentConnection();
        if (current != null) {
            try {
                return action.doInConnection(current);
            } catch (SQLException e) {
                throw new DataAccessException(e);
            }
        }
        // 无事务,从DataSource获取新连接:
        try (Connection newConn = dataSource.getConnection()) {
            return action.doInConnection(newConn);
        } catch (SQLException e) {
            throw new DataAccessException(e);
        }
    }
    ...
}

```

最后把拦截器， TransactionalBeanPostProcessor，Template加入到配置类中，即可开启AOP管理

## 实现WebMVC

对于一个Web应用程序来说，启动时，应用程序本身只是一个`war`包，并没有`main()`方法，因此，启动时执行的是Server的`main()`方法。以Tomcat服务器为例：

1.  启动服务器，即执行Tomcat的`main()`方法；
2.  Tomcat根据配置或自动检测到一个`xyz.war`包后，为这个`xyz.war`应用程序创建Servlet容器；
3.  Tomcat继续查找`xyz.war`定义的Servlet、Filter和Listener组件，按顺序实例化每个组件（Listener最先被实例化，然后是Filter，最后是Servlet）；
4.  用户发送HTTP请求，Tomcat收到请求后，转发给Servlet容器，容器根据应用程序定义的映射，把请求发送个若干Filter和一个Servlet处理；
5.  处理期间产生的事件则由Servlet容器自动调用Listener。

详细流程：Tomcat启动，创建ServletContext，解析web.xml文件，找到ServletContextListener，调用里面的方法

```
public interface ServletContextListener {
    // Tomcat会在Web应用启动时自动调用
    void contextInitialized(ServletContextEvent sce);
    
    // Tomcat会在Web应用关闭时自动调用
    void contextDestroyed(ServletContextEvent sce);
}
```

在contextInitialized(ServletContextEvent sce);中向WebMvcConfiguration中注入servletContext，创建ApplicationContext（创建PropertyResolver）,创建IOC容器，并注册拦截器和前端控制器（通过WebUtils实现具体逻辑）

```
public class ContextLoaderListener implements ServletContextListener {  
  
    final Logger logger = LoggerFactory.getLogger(getClass());  
  
    @Override  
    public void contextInitialized(ServletContextEvent sce) {  
        logger.info("init {}.", getClass().getName());  
        var servletContext = sce.getServletContext();  
        WebMvcConfiguration.setServletContext(servletContext);  
  
        var propertyResolver = WebUtils.createPropertyResolver();  
        String encoding = propertyResolver.getProperty("${summer.web.character-encoding:UTF-8}");  
        servletContext.setRequestCharacterEncoding(encoding);  
        servletContext.setResponseCharacterEncoding(encoding);  
  
        //扫描配置类，创建ApplicationContext，创建IOC容器  
        var applicationContext = createApplicationContext(servletContext.getInitParameter("configuration"), propertyResolver);  
        // register filters:  
        WebUtils.registerFilters(servletContext);  
        // register DispatcherServlet:  
        WebUtils.registerDispatcherServlet(servletContext, propertyResolver);  
  
        servletContext.setAttribute("applicationContext", applicationContext);  
    }  
  
    //创建 ApplicationContext    ApplicationContext createApplicationContext(String configClassName, PropertyResolver propertyResolver) {  
        logger.info("init ApplicationContext by configuration: {}", configClassName);  
        if (configClassName == null || configClassName.isEmpty()) {  
            throw new NestedRuntimeException("Cannot init ApplicationContext for missing init param name: configuration");  
        }  
        Class<?> configClass;  
        try {  
            configClass = Class.forName(configClassName);  
        } catch (ClassNotFoundException e) {  
            throw new NestedRuntimeException("Could not load class from init param 'configuration': " + configClassName);  
        }  
        return new AnnotationConfigApplicationContext(configClass, propertyResolver);  
    }  
}
```

## 前端控制器详细方法调用链

### 阶段1: **框架初始化** (`init()` 方法调用链)

text

1.  DispatcherServlet.init() ↓
2.  applicationContext.findBeanDefinitions(Object.class) ↓
3.  遍历每个Bean定义: ↓
4.  beanClass.getAnnotation(Controller.class) / RestController.class ↓
5.  addController(false/true, beanName, beanInstance) ↓
6.  addMethods(isRest, name, instance, instance.getClass()) ↓
7.  遍历类的所有方法: ↓
8.  method.getAnnotation(GetMapping.class) / PostMapping.class ↓
9.  checkMethod(method) ↓
10.  new Dispatcher("GET/POST", isRest, instance, method, urlPattern) ↓
11.  Dispatcher构造函数:
    *   设置isRest, isResponseBody, isVoid
    *   PathUtils.compile(urlPattern) - 编译URL正则
    *   解析方法参数: new Param\[...\] ↓
12.  Param构造函数:
    *   解析参数注解: @PathVariable, @RequestParam, @RequestBody
    *   确定ParamType和参数名称

```
@Override  
public void init() throws ServletException {  
    logger.info("init {}.", getClass().getName());  
    // scan @Controller and @RestController:  
    for (var def : ((ConfigurableApplicationContext) this.applicationContext).findBeanDefinitions(Object.class)) {  
        Class<?> beanClass = def.getBeanClass();  
        Object bean = def.getRequiredInstance();  
        Controller controller = beanClass.getAnnotation(Controller.class);  
        RestController restController = beanClass.getAnnotation(RestController.class);  
        if (controller != null && restController != null) {  
            throw new ServletException("Found @Controller and @RestController on class: " + beanClass.getName());  
        }  
        if (controller != null) {  
            addController(false, def.getName(), bean);  
        }  
        if (restController != null) {  
            addController(true, def.getName(), bean);  
        }  
    }  
}
```

### 阶段2: **请求处理** (`doGet()` 方法调用链)

text

1.  DispatcherServlet.doGet(HttpServletRequest, HttpServletResponse) ↓
2.  获取请求URL: req.getRequestURI() ↓
3.  判断请求类型:
    *   如果是静态资源: doResource(url, req, resp)
    *   如果是动态请求: doService(req, resp, getDispatchers) ↓
4.  doService(req, resp, dispatchers):
    *   异常处理包装
    *   调用doService(url, req, resp, dispatchers) ↓
5.  doService(url, req, resp, dispatchers): ↓
6.  遍历dispatchers列表: for (Dispatcher dispatcher : dispatchers) { ↓
7.  dispatcher.process(url, req, resp) ↓
8.  URL正则匹配: urlPattern.matcher(url).matches() ↓
9.  如果匹配成功: ↓
10.  构建参数数组 arguments\[methodParameters.length\] ↓
11.  遍历每个参数: for (int i = 0; i < arguments.length; i++) { Param param = methodParameters\[i\]; ↓
12.  ```
        switch (param.paramType):
            ↓
    ```
13.  ```
        case PATH_VARIABLE:
            - matcher.group(param.name) 从URL提取值
            - convertToType() 类型转换
            ↓
    ```
14.  ```
        case REQUEST_PARAM:
            - request.getParameter(param.name) 获取参数
            - getOrDefault() 处理默认值
            - convertToType() 类型转换
            ↓
    ```
15.  ```
        case REQUEST_BODY:
            - request.getReader() 获取输入流
            - JsonUtils.readJson() JSON反序列化
            ↓
    ```
16.  ```
        case SERVLET_VARIABLE:
            - 根据类型返回HttpServletRequest/Response等
    }
    ↓
    ```
17.  反射调用: handlerMethod.invoke(controller, arguments) ↓
18.  控制器方法执行业务逻辑 ↓
19.  返回Result(true, result) } ↓
20.  结果处理: if (dispatcher.isRest) { // REST处理逻辑 } else { // MVC处理逻辑 }

## 具体场景分析

### 场景1: **REST API 请求**

```
请求: GET /api/users/123

执行流程:
1. DispatcherServlet.doGet()
2. doService() -> 遍历getDispatchers
3. 找到匹配的Dispatcher (URL: /api/users/{id})
4. Dispatcher.process():
   - URL正则匹配: /api/users/123 匹配 /api/users/{id}
   - 构建参数: 
     * @PathVariable("id") Long id → convertToType(Long.class, "123") → 123L
5. 调用: userController.getUser(123L)
6. 返回: User对象
7. 结果处理 (isRest = true):
   - resp.setContentType("application/json")
   - JsonUtils.writeJson(pw, userObject)
8. 响应: {"id":123, "name":"John"}
```

### 场景2: **MVC 页面请求**

```

请求: GET /user/profile

执行流程:
1. DispatcherServlet.doGet()
2. doService() -> 遍历getDispatchers  
3. 找到匹配的Dispatcher (URL: /user/profile)
4. Dispatcher.process():
   - 无参数，直接调用userController.profile()
5. 返回: ModelAndView("profile", model)
6. 结果处理 (isRest = false):
   - resp.setContentType("text/html")
   - viewResolver.render("profile", model, req, resp)
7. 响应: 渲染profile.ftl模板生成的HTML
```

### 场景3: **表单提交请求**

```
请求: POST /user/update

执行流程:
1. DispatcherServlet.doPost()
2. doService() -> 遍历postDispatchers
3. 找到匹配的Dispatcher (URL: /user/update)
4. Dispatcher.process():
   - 构建参数: @RequestBody User user
   - JsonUtils.readJson(reader, User.class) → User对象
5. 调用: userController.update(user)
6. 返回: "redirect:/user/list"
7. 结果处理:
   - resp.sendRedirect("/user/list")
```

使用框架时:可以自定义过滤器，编写逻辑

## 相关知识

## Record类型

Record 是 Java 14 引入、Java 16 正式化的特性，用于创建**不可变的数据载体类**。

### **Record会自动生成：**

1.  **私有final字段**（与组件名称相同）
2.  **规范构造函数**（canonical constructor）
3.  **访问器方法**（`name()`、`age()`，不是getXxx）
4.  **equals()、hashCode()、toString()**

## Function函数式编程

`Function<T, R>` 是Java函数式编程的核心接口，表示**接收一个参数T，返回结果R**的函数。

### 创建

```
import java.util.function.Function;

// 1. Lambda表达式（最常用）
Function<String, Integer> stringToInt1 = s -> Integer.parseInt(s);

// 2. 方法引用
Function<String, Integer> stringToInt2 = Integer::parseInt;
Function<String, String> toUpperCase = String::toUpperCase;
Function<String, Integer> getLength = String::length;

// 3. 匿名内部类（传统方式）
Function<String, Integer> stringToInt3 = new Function<String, Integer>() {
    @Override
    public Integer apply(String s) {
        return Integer.parseInt(s);
    }
};

// 4. 已有方法赋值
Function<String, Integer> myMethod = this::parseStringToInt;
private Integer parseStringToInt(String s) {
    return Integer.parseInt(s);
}
```

### 使用apply()方法

```
// 创建Function
Function<String, Integer> stringToInt = s -> Integer.parseInt(s);

// 使用apply()调用
Integer number = stringToInt.apply("123");
System.out.println(number);  // 123

// 更多例子
Function<Integer, String> intToString = i -> "Number: " + i;
String result = intToString.apply(456);  // "Number: 456"

Function<String, String> process = s -> s.trim().toUpperCase();
String processed = process.apply("  hello  ");  // "HELLO"
```