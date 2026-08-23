# SpringBoot
## 配置

优先级：命令行优先级>java系统>properties>yml>yaml

## Bean管理

默认单例的bean是启动时候创建的

@Lazy 延迟初始化，知道第一次使用再来创建bean

@Scope("prototype") 多例创建

## Bean作用域

### 有状态 Bean (Stateful)

**特点**：拥有可变的成员变量，状态会随着调用而改变

内部会保存状态信息，多个线程同时操作Bean时，保持数据的一致性，维护线程安全

### 无状态 Bean (Stateless)

**特点**：没有可变的成员变量，每次调用都是独立的

不会保存任何的数据，只会存在一个实例对象，线程安全

| 作用域 | 英文 | 实例数量 | 生命周期 | 适用场景 |
| --- | --- | --- | --- | --- |
| **单例** | singleton | 1个 | 容器启动到关闭 | 无状态服务、工具类、配置类 |
| **原型** | prototype | 多个 | 每次获取创建，GC回收 | 有状态对象、线程不安全类 |
| **请求** | request | 每个请求1个 | HTTP请求开始到结束 | 请求参数封装、临时数据 |
| **会话** | session | 每个会话1个 | Session创建到超时 | 用户登录信息、购物车 |
| **应用** | application | 1个 | 应用启动到关闭 | 全局配置、缓存管理 |

## 第三方Bean

第三方依赖里面的类不能被Spring扫描，不能直接声明为Bean，那么怎样让他们进入IOC容器当中

呢？

我们可以创建一个配置类，声明@Configuration注解，

配置类是一个用 `@Configuration` 注解标注的 Java 类，它的主要作用是**替代传统的 XML 配置文件**，通过 Java 代码的方式来定义和配置 Spring 容器中的 Bean。

`**@Bean**` **是一个方法级别的注解**，它告诉Spring："**这个方法会返回一个对象，这个对象应该被注册到Spring的IOC容器中，成为一个Bean**"。

```
@Configuration
public class ThirdPartyConfig {
    
    /**
     * 将第三方服务注册为Spring Bean
     * 方法名就是Bean的名称
     */
    @Bean
    public ThirdPartyService thirdPartyService() {
        return new ThirdPartyService();
    }
    
    /**
     * 可以自定义Bean名称
     */
    @Bean("externalConfig")
    public ExternalConfig externalConfig() {
        ExternalConfig config = new ExternalConfig();
        config.setApiKey("your-api-key-123");
        config.setEndpoint("https://api.example.com");
        return config;
    }
    
    /**
     * 带初始化的复杂Bean
     */
    @Bean(initMethod = "init", destroyMethod = "cleanup")
    public ComplexService complexService() {
        ComplexService service = new ComplexService();
        service.setTimeout(5000);
        return service;
    }
}
```

## 自动配置

第三方依赖使用注解声明Bean不生效是因为需要被spring组件扫描到，而Spring默认扫描范围是

该类所在的包及其所有子包

方案一：

如果第三方依赖中有Bean注解，需要在启动类中表明引入IOC容器的包名，否则无法引入依赖

```
@ComponentScan(basePackages = {"com.example","com.itheima"})
```

缺点：繁琐，性能低

方案二：

@Import: 导入普通类和配置类

或者导入ImportSelector的实现类

![](/attachments/Pasted%20image%2020251101195206.png)

但是如果这样会很繁琐，必须指定类

方案三：封装import注解

@EnableHeaderConfig注解进行对import注解的封装，开发者不需要知道导入那些类

### 源码跟踪

启动类相当于一个配置类

核心注解：@SpringBootApplication

底层封装了 @EnableAutoConfiguration

![](/attachments/Pasted%20image%2020251102102325.png)

底层又封装了@Import注解，传递了ImportSelector 接口的实现类，会把里面封装的所有类返回

并根据条件判定是否创建Bean

@ConditionalOnClass :判断当前环境是否有对应的字节码文件，才注册bean到IOC容器

@ConditionalOnMissingBean : 判断环境当中是否有对应的bean，有才注册Bean到IOC，没有

就创建bean

@ConditionalOnProperty : 判断配置文件中有对应属性和值，有才注册Bean

### Starter

在引入依赖时，配置文件中总会有一些starter字段，封装一些依赖的公共组件

**Starter** 是一个依赖描述符，它**聚合了一组相关的依赖项**，并提供了自动配置功能，让你能够"开箱即用"地使用某个功能。

通过自定义 Starter，你**不需要在每个项目中手动编写工具类并注入到 IOC 容器**，Starter 会自动完成这些工作。

以封装aliyun工具类为例

创建autoconfigure模块，导入工具类以及pom文件

创建配置类，将工具类注册Bean到IOC容器当中，不能使用@Component注解，因为启动类只会

扫描当前包及其子类包

```
@Configuration  
@EnableConfigurationProperties(AliyunOSSProperities.class)  
public class AliyunOSSAutoConfiguration {  
    @Bean  
    @ConditionalOnMissingBean    public AliyunOSSOperator aliyunOSSOperator(AliyunOSSProperities aliyunOSSProperities){  
        return new AliyunOSSOperator(aliyunOSSProperities);  
    }  
}
```