# Spring
## IOC容器

又称控制反转，承载java new 出来的对象，需要时再取出

工作原理，加载xml映射文件，告诉IOC容器要创建什么类型的对象，IOC内部通过BeanFactory以

及反射将对象创建出来，实例化，初始化，最后通过context.getBean（）进行对象的获取

### 依赖注入

spring 创建对象时，将对象依赖属性通过配置注入

两种方式：

set注入

```
<bean id="user" class="com.wsj.spring.User">  
    <property name="age" value="11"></property>  
    <property name="name" value="wsj"></property>  
</bean>
```

构造器注入

```
<bean id="user" class="com.wsj.spring.User">  
    <constructor-arg name="name" value="wsj"></constructor-arg>  
    <constructor-arg name="age" value="18"></constructor-arg>  
</bean>
```

Bean管理：bean对象的创建和赋值

为对象类属性赋值

引入外部bean

```
<bean id="dept" class="com.wsj.spring.Dept">  
  
        <property name="name" value="开发部"></property>  
    </bean>  
    <bean id="emp" class="com.wsj.spring.Emp">  
        <property name="ename" value="wsj"></property>  
        <property name="age" value="22"></property>  
  
<!--        对象属性注入-->  
        <property name="dept" ref="dept"></property>  
  
    </bean>
```

内部bean注入

```
<bean id="emp" class="com.wsj.spring.Emp">  
        <property name="ename" value="wsj"></property>  
        <property name="age" value="22"></property>  
  
<!--        对象属性注入-->  
        <property name="dept">  
            <bean id="dept1" class="com.wsj.spring.Dept">  
  
                <property name="name" value="开发部"></property>  
            </bean>        </property>  
    </bean>
```

数组类型注入

```
<property name="loves" >  
    <array>        <value>java</value>  
        <value>python</value>  
        <value>c++</value>  
    </array></property>
```

List属性注入

```
<property name="emps">  
    <list>        <ref bean="emp1"></ref>  
        <ref bean="emp2"></ref>  
    </list></property>
```

map属性注入

```
<entry>
     <key>
     <value> </value>
     </key>
     <ref bean=""></ref>

</entry>
```

引入外部配置文件

```
<?xml version="1.0" encoding="UTF-8"?>  
<beans xmlns="http://www.springframework.org/schema/beans"  
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
       xmlns:context="http://www.springframework.org/schema/context"  
       xsi:schemaLocation="  
        http://www.springframework.org/schema/beans        http://www.springframework.org/schema/beans/spring-beans.xsd        http://www.springframework.org/schema/context        http://www.springframework.org/schema/context/spring-context.xsd">  
  
    <!-- 启用属性文件占位符 -->  
    <context:property-placeholder location="classpath:jdbc.properties"/>  
  
    <!-- 其他bean配置 -->  
    <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">  
        <property name="url" value="${jdbc.url}"/>  
        <property name="username" value="${jdbc.username}"/>  
        <property name="password" value="${jdbc.password}"/>  
        <property name="driverClassName" value="${jdbc.driver}"/>  
    </bean>  
</beans>
```

```
public void test2(){  
    ApplicationContext context=new ClassPathXmlApplicationContext("bean-jdbc.xml");  
    DruidDataSource dataSource=(DruidDataSource)context.getBean("dataSource");  
    System.out.println(dataSource.getUrl());  
}
```

### Bean作用域

singleton(默认)：单实例创建，在IOC容器初始化时进行创建

propertype：bean在容器中有多个实例，在获取bean时创建

### 生命周期

#### 1. 什么是Bean的生命周期

（1）Spring其实就是一个管理Bean对象的工厂，它负责对象的创建，对象的销毁等。

（2）所谓的生命周期就是：对象从创建开始到最终销毁的整个过程。

（3）为什么要知道Bean的生命周期？

生命周期的本质是：在哪个时间节点上调用了哪个类的哪个方法？我们需要充分的了解在这个生命线上，都有哪些特殊的时间节点！只有我们知道了特殊的时间节点都在哪，到时我们才可以确定代码写到哪。我们可能需要在某个特殊的时间点上执行一段特定的代码，这段代码就可以放到这个节点上；当生命线走到这里的时候，自然会被调用。 xml配置

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
 
    <bean id="user" class="com.bjpowernode.spring.bean.User"
          init-method="initBean" destroy-method="destroyBean">
          <!--给属性赋值-->
         <property name="username" value="张三"/>
    </bean>
</beans>
```

如果你还想在**初始化前**和**初始化后**添加代码，\*_可以加入“Bean后处理器”_\*\*\*；**需要编写一个类**实现BeanPostproccessor接口，**并**重写里面的befor和after方法。

```
package com.bjpowernode.spring.test;
 
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
 
public class LogBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        System.out.println("Bean后处理器的before方法执行，即将开始初始化");
        return BeanPostProcessor.super.postProcessBeforeInitialization(bean, beanName);
    }
 
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        System.out.println("Bean后处理器的after方法执行，已完成初始化");
        return BeanPostProcessor.super.postProcessAfterInitialization(bean, beanName);
    }
}
```

### 获取Bean

通过id获取

通过类型获取

通过id和类型获取

```
//根据id获取  
User user=(User)context.getBean("user");  
log.info("通过id 获取bean,{}",user);  
  
//根据类型获取bean  
User user1=context.getBean(User.class);  
log.info("通过类型获取bean,{}",user1);  
  
//根据id和类型获取  
User user2=context.getBean("user",User.class);  
log.info("通过id和类型获取bean,{}",user2);
```

## 手写IOC

### 阶段一：包扫描与Bean注册

1.  **路径处理**
    *   将包名转换为文件路径格式
    *   获取包的绝对路径
2.  **递归扫描**
    *   遍历指定包及其所有子包
    *   查找所有`.class`文件
3.  **Bean识别与注册**
    *   通过反射加载类
    *   检查类是否被`@Bean`注解标记
    *   实例化Bean对象
    *   存入Map容器：`接口类型 → Bean实例` 或 `类类型 → Bean实例`

### 阶段二：依赖注入

1.  **遍历所有Bean实例**
2.  **反射检查字段**
    *   查找被`@Di`注解标记的字段
3.  **自动注入**
    *   从容器中获取对应类型的Bean
    *   通过反射设置字段值

```
public class ApplicationImpl implements ApplicationContext{  
    //创建Map集合存放Bean对象  
    private  Map<Class, Object> beanFactory=new HashMap<>();  
    private static String packagePath;  
    @Override  
    public Object getBean(Class clazz) {  
        return beanFactory.get(clazz);  
    }  
    //设置包扫描规则  
    //当前包及其子包  
    public     ApplicationImpl(String packageName){  
        try {  
            //包扫描  
            String path=packageName.replaceAll("\\.","\\\\");  
            //获取包的绝对路径  
            Enumeration<URL> urls=Thread.currentThread().getContextClassLoader().getResources(path);  
            while(urls.hasMoreElements()){  
                URL url=urls.nextElement();  
                String fileName=URLDecoder.decode(url.getFile(),"utf-8");  
                //获取包前面的部分  
                 packagePath=fileName.substring(0,fileName.length()-path.length());  
                //包扫描  
                loadBean(new File(fileName));  
            }  
        } catch (Exception e) {  
            throw new RuntimeException(e);  
        }  
        //属性注入  
        loadDi();  
    }  
  
    private void loadDi() {  
        //遍历map集合  
        Set<Map.Entry<Class, Object>> entrySet=beanFactory.entrySet();  
        for(Map.Entry<Class, Object> entry:entrySet){  
            Object bean=entry.getValue();  
            Class<?> clazz=bean.getClass();  
            //获取每个对象属性  
            Field[] declaredFields=clazz.getDeclaredFields();  
            for(Field field:declaredFields){  
                Di annotation=field.getAnnotation(Di.class);  
                if(annotation!=null){  
                    field.setAccessible(true);  
                    try {  
                        field.set(bean,beanFactory.get(field.getType()));  
                    } catch (IllegalAccessException e) {  
                        throw new RuntimeException(e);  
                    }  
                }  
            }  
        }  
  
    }  
  
    private  void loadBean(File file) throws Exception {  
        //判断是文件还是文件夹  
        if(file.isDirectory()){  
            File[] files=file.listFiles();  
  
            if(files==null||files.length==0){  
                return;  
            }  
            for(File f:files){  
                if(f.isDirectory()){  
                    loadBean(f);  
                }else{  
                    //截取包路径和类名称部分  
                    String pathWithClass = f.getAbsolutePath().substring(packagePath.length() - 1);  
                    if(pathWithClass.contains(".class")){  
                        String className=pathWithClass.replaceAll("\\\\",".").replaceAll(".class","");  
                        //获取类的class对象  
                        Class<?> clazz=Class.forName(className);  
                        if(!clazz.isInterface()){  
                            //判断上面有没有注解  
                            Bean annotation=clazz.getAnnotation(Bean.class);  
                            if(annotation!=null){  
                                //实例化  
                                Object instance=clazz.getConstructor().newInstance();  
                                if(clazz.getInterfaces().length>0){  
                                    beanFactory.put(clazz.getInterfaces()[0],instance);  
                                }else{  
                                    beanFactory.put(clazz,instance);  
                                }  
                            }  
                        }  
                    }  
                }  
            }  
        }  
  
  
    }
```

## 事务管理

事务是一组操作的集合，是一个不可分割的工作单位，这组操作要么全部成功，要么全部失败

```
开启事务：start transaction/begin
```

提交事务

```
commit;
```

回滚事务

```
rollback
```

### 控制事务

注解：@Transactional（默认运行时出现异常才会回滚）

作用：方法执行前开启事务，成功执行，提交事务；出现异常，回滚事务

位置：业务层的方法上，类上，接口上（主要是方法上）

### 属性

readOnly=true 只读操作，不能进行修该和删除

timeout=-1（无限制） 如果事务在执行过程中因为某些问题卡住，导致数据库资源被占用，会抛出异常，进行回滚

传播行为

```
@Service
public class TransactionalService {
    
    @Transactional(propagation = Propagation.REQUIRED)
    public void requiredExample() {
        // 默认值：如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void requiresNewExample() {
        // 创建一个新的事务，如果当前存在事务，则把当前事务挂起
        // 独立的事务，不受外部事务影响
    }
    
    @Transactional(propagation = Propagation.SUPPORTS)
    public void supportsExample() {
        // 如果当前存在事务，则加入该事务；如果当前没有事务，则以非事务的方式执行
    }
    
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void notSupportedExample() {
        // 以非事务方式执行操作，如果当前存在事务，则把当前事务挂起
    }
    
    @Transactional(propagation = Propagation.MANDATORY)
    public void mandatoryExample() {
        // 必须在一个已有的事务中执行，否则抛出异常
    }
    
    @Transactional(propagation = Propagation.NEVER)
    public void neverExample() {
        // 必须不在一个事务中执行，否则抛出异常
    }
    
    @Transactional(propagation = Propagation.NESTED)
    public void nestedExample() {
        // 如果当前存在事务，则在嵌套事务内执行；如果当前没有事务，则执行与PROPAGATION_REQUIRED类似的操作
        // 嵌套事务可以独立回滚，但外部事务回滚会导致嵌套事务回滚
    }
}
```

隔离级别

```
@Service
public class IsolationService {
    
    @Transactional(isolation = Isolation.DEFAULT)
    public void defaultIsolation() {
        // 使用底层数据库的默认隔离级别
        // MySQL: REPEATABLE_READ, Oracle: READ_COMMITTED
    }
    
    @Transactional(isolation = Isolation.READ_UNCOMMITTED)
    public void readUncommitted() {
        // 读未提交：最低的隔离级别，允许读取尚未提交的数据变更
        // 可能导致脏读、不可重复读和幻读
    }
    
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public void readCommitted() {
        // 读已提交：允许读取并发事务已经提交的数据
        // 可以阻止脏读，但是不可重复读和幻读仍可能发生
    }
    
    @Transactional(isolation = Isolation.REPEATABLE_READ)
    public void repeatableRead() {
        // 可重复读：对同一字段的多次读取结果都是一致的
        // 可以阻止脏读和不可重复读，但幻读仍可能发生
    }
    
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void serializable() {
        // 最高的隔离级别，完全服从ACID的隔离级别
        // 所有的事务依次逐个执行，事务之间完全不可能产生干扰
    }
}
```

### 事务进阶--RollbackFor

无论任何类型异常都回滚

```
@Transactional(rollbackFor = {Exception.class})
```

### 事务进阶-propagation

![](/attachments/Pasted%20image%2020251027174602.png)

在业务层是日志接口实现类中加入注解，创建新事物，在其他业务层的类中用try-finally调用时会记录日志

### 四大特性

原子性：事务是不可分割的单元

一致性：事务完成时，事务完成时，必须所有数据保持一致状态

隔离性：数据库系统提供的隔离机制，保证事务在不受外界并发操作影响，独立执行

持久性：事务一旦提交或回滚，它对数据库中的数据改变是永久的

## SpringAop

```
<dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-aop</artifactId>  
    <version>6.2.12</version>  
</dependency>  
<dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-aspects</artifactId>  
    <version>6.2.12</version>  
</dependency>
```

AOP（面向切面编程）是Spring框架的核心模块之一，它提供了一种强大的方式来横向切割关注点，将跨越应用程序多个模块的功能进行模块化。

例如统计一个方法的执行时间，如果没有Aop，我们必须在每个方法执行前后记录时间，最后相减，这样不仅工程量巨大，而且可 维护性差

Aop就完美解决了这个问题

@Aspect注解标识Aop类

@Around注解：环绕通知

*   **切入点表达式**：`execution(* com.itheima.service.impl.*.*(..))`
    *   `execution`：匹配方法执行连接点
    *   第一个`*`：任意返回类型
    *   `com.itheima.service.impl`：包名
    *   第二个`*`：包下的任意类
    *   第三个`*`：类中的任意方法
    *   `(..)`：任意参数

```
//执行原始方法  
Object result=pjp.proceed();
```

切面(Aspect) ↓ 包含 通知(Advice) + 切入点(Pointcut) ↓ 作用于 连接点(Join Point) ↓ 存在于 目标对象(Target Object) ↓ 通过 织入(Weaving) ↓ 创建 AOP代理(AOP Proxy)

Aop的执行流程：定义增强逻辑（如统计方法执行所用时间）以及目标类，Spring在执行过程中扫

描到Aop类以及目标类，创建动态代理，IOC容器中放入代理类，程序运行过程中，控制层中会注

入代理类的依赖，目标类执行完后，继续返回Aop类中执行下一步操作

### 通知类型

| 通知类型 | 主要应用场景 |
| --- | --- |
| **@Before** | 参数验证、权限检查、日志记录、缓存检查 |
| **@After** | 资源清理、状态重置、审计日志 |
| **@AfterReturning** | 结果处理、缓存更新、成功日志、数据转换 |
| **@AfterThrowing** | 异常处理、错误日志、事务回滚、告警通知 |
| **@Around** | 性能监控、事务管理、缓存、重试机制、超时控制 |

@Before :在目标方法执行前执行

@After：在目标方法执行后执行

@AfterReturnibg：目标方法执行成功后执行

@AfterThrowing : 目标方法出现异常时执行

@Around:目标方法执行前后都执行

@Pointcut 注解：定义命名切入点

```
@Pointcut("execution(* com.itheima.service.impl.*.*(..))")  
private void pt(){}
```

### 切入点表达式

**execution**

基本语法

```
execution(修饰符? 返回类型 声明类型? 方法名(参数) 异常?)
```

**@annotation - 匹配注解**

```
// 匹配带有特定注解的方法
@annotation(com.example.Log)

// 匹配带有Transactional注解的方法
@annotation(org.springframework.transaction.annotation.Transactional)
```

在需要匹配的方法上加上特定注解，即可进行匹配

```
@Target(ElementType.METHOD)  
@Retention(RetentionPolicy.RUNTIME)  
public @interface LogOperation {  
}
```

### JoinPoint 连接点

```
@Autowired  
private OperateLogMapper operateLogMapper;  
  
@Around("@annotation(org.example.anno.LogOperation)")  
public Object logOperation(ProceedingJoinPoint joinPoint) throws Throwable {  
    long startTime = System.currentTimeMillis();  
    // 执行目标方法  
    Object result = joinPoint.proceed();  
    // 计算耗时  
    long endTime = System.currentTimeMillis();  
    long costTime = endTime - startTime;  
  
    // 构建日志实体  
    OperateLog olog = new OperateLog();  
    olog.setOperateEmpId(getCurrentUserId()); // 这里需要你根据实际情况获取当前用户ID  
    olog.setOperateTime(LocalDateTime.now());  
    olog.setClassName(joinPoint.getTarget().getClass().getName());  
    olog.setMethodName(joinPoint.getSignature().getName());  
    olog.setMethodParams(Arrays.toString(joinPoint.getArgs()));  
    olog.setReturnValue(result != null ? result.toString() : "void");  
    olog.setCostTime(costTime);  
      
    // 保存日志  
    log.info("记录操作日志: {}", olog);  
    operateLogMapper.insert(olog);  
  
    return result;  
}
```

通过提供的方法执行目标方法，获取方法名，类名

### ThreadLocal

是Thread的局部变量，线程本地变量

它为**每个使用该变量的线程都提供一个独立的变量副本**，实现了线程间的数据隔离。

**核心思想**

*   **数据隔离**：每个线程只能看到和修改自己的数据副本
*   **线程安全**：天然线程安全，因为不存在共享资源
*   **空间换时间**：通过为每个线程创建副本来避免同步开销

基本使用

```
public class ThreadLocalDemo {
    // 创建 ThreadLocal 实例
    private static final ThreadLocal<String> threadLocal = new ThreadLocal<>();
    
    public static void main(String[] args) {
        // 设置当前线程的值
        threadLocal.set("主线程的值");
        
        // 获取当前线程的值
        String value = threadLocal.get(); // "主线程的值"
        
        // 移除当前线程的值
        threadLocal.remove();
    }
}
```

执行流程：用户登陆后获取Token，存储用户的id和姓名，再次请求访问进行操作时，拦截器拦截

token检查是否出错，没有出错就把里面存储的id值传递给工具类中的ThreadLocal，当记录

操作日志时，获取线程本地变量中的empid，记录不同用户操作

## junit

`@SpringJUnitConfig(classes = AppConfig.class)` 的主要作用：

| 功能 | 说明 |
| --- | --- |
| **启动容器** | 创建Spring IOC容器 |
| **加载配置** | 加载指定的配置类(`AppConfig.class`) |
| **依赖注入** | 为测试类提供@Autowired等注入支持 |
| **Bean管理** | 创建和管理配置类中定义的Bean |
| **测试环境** | 提供完整的Spring测试环境 |

```
@SpringJUnitConfig(locations = "classpath:applicationContext.xml")
public class MyTest {
    // 测试代码
    
}
```

这样可以保证在测试类中可以使用注入后的bean

```
<dependency>  
    <groupId>org.junit.jupiter</groupId>  
    <artifactId>junit-jupiter-api</artifactId>  
    <version>5.11.4</version>  
</dependency>  
<dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-test</artifactId>  
    <version>6.2.12</version>  
</dependency>
```

## JdbcTemplate

JdbcTemplate提供了一系列基础的操作方法，包括查询、更新、批量操作等。这些操作方法都是通过JdbcTemplate类提供的API来实现的。下面是一些常用的基础操作方法：

配置：

```
<dependency>  
        <groupId>org.springframework</groupId>  
        <artifactId>spring-jdbc</artifactId>  
        <version>6.2.12</version>  
    </dependency>    <dependency>        <groupId>mysql</groupId>  
        <artifactId>mysql-connector-java</artifactId>  
        <version>8.0.17</version>  
    </dependency>    <dependency>        <groupId>com.alibaba</groupId>  
        <artifactId>druid</artifactId>  
        <version>1.2.21</version>  
    </dependency></dependencies>
```

```
<!-- 开启组件扫描 -->  
<context:component-scan base-package="com.wsj"/>  
  
<!-- 数据源配置 -->  
<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">  
    <property name="url" value="jdbc:mysql://localhost:3306/test"/>  
    <property name="username" value="root"/>  
    <property name="password" value="123456"/>  
    <property name="initialSize" value="5"/>  
    <property name="maxActive" value="20"/>  
</bean>  
<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">  
    <property name="dataSource" ref="dataSource"/>  
</bean>
```

## Spring八大设计模式

### 简单工厂模式

BeanFactory的getBean方法，典型的简单工厂模式（静态工厂模式）

### 工厂方法模式

FactoryBean是典型的工厂方法模式，配置文件中通过factory-method属性指定工厂方法，实例方法

### 单例模式

### 代理模式

AOP的动态代理

### 装饰器模式

根据每次请求的不同，将dataSource设置成不同的数据源

### 观察者模式

定义对象的一对多关系，当一个对象的状态发生改变时，所有依赖于它的对象自动更新

Spring中定义了一个ApplicationListener接口，监听Application事件，Application相当于ApplicationContext,，内置了几个事件

### 策略模式

比如一个接口有多个实现类，但是service 层中不需要关心，只需要面向接口进行调用，底层进行灵活的切换

### 模板方法模式

jdbcTemplate就是一个模板类