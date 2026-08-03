## 单元测试

针对最小的功能单元：方法，编写测试代码对其进行正确性测试

### Junit单元测试框架

可以对方法进行测试，它是第三方公司开源出来的

![](https://gitee.com/Wsj123789/wsj/raw/master/img/20251012161631803.png)

**优点**

可以灵活的编写测试代码，可以针对某个方法执行测试，也支持一键完成对全部方法的自动化测试，且各自独立

不需要程序员去分析测试的结果，会自动生成测试报告出来

```
package com.wsj.junit;

import org.junit.Assert;
import org.junit.Test;

//junit单元测试框架，对业务类中的业务方法进行正确性测试
public class StringUtilTest {
    //测试方法：必须是公开public:无参，无返回值
    //测试方法必须加@Test注解（核心步骤）
    @Test
    public void testPrintNumber(){
        StringUtil.printNumber("张三abc");//5
        //测试用例
        StringUtil.printNumber("");
        StringUtil.printNumber(null);

    }
    @Test
    public void testetMaxIndex(){
        int index=StringUtil.getMaxIndex("acdswe");
        int index2=StringUtil.getMaxIndex(null);
        int index3=StringUtil.getMaxIndex("");
        System.out.println(index);
        System.out.println(index2);
        System.out.println(index3);
        //做断言，断言结果是否与预期结果一致
        Assert.assertEquals("本轮测试失败，请检查",5,index);

    }
}
```

## 反射

### 认识反射

加载类，并允许以编程的方式解剖类中的各种成分（成员变量、方法、构造器等）

1. 加载类，获取类的字节码：class对象
2. 获取类的构造器：Constructor对象
3. 获取类的成员变量：Field对象
4. 获取类的成员方法：Method对象

```
@Test
    public void GetClassInfo() throws NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        //获取类本身
        Class c1= Student.class;

        System.out.println(c1);
        System.out.println(c1.getName());
        System.out.println(c1.getSimpleName());
        //获取单个构造器
        Constructor con=c1.getDeclaredConstructor();
        con.setAccessible(true);
        Student s1=(Student) con.newInstance();
        System.out.println(s1);

        Constructor con1=c1.getDeclaredConstructor(String.class,int.class);
        con1.setAccessible(true);
        Student s2=(Student) con1.newInstance("小猫",3);
        System.out.println(s2);
        
        //获取成员变量
        
    }
```

### 反射的基本作用

- 基本作用:可以得到一个类的全部成分然后操作
- 可以破环封装性
- 可以绕过泛型的约束

主流框架都会基于反射设计出一些通用的功能

## 注解

java代码里的特殊标记，比如：@Override,@Test.作用是：让其他程序根据注解信息来决定怎么执行该程序

注意：注解可以在类上，构造器上，方法上，成员变量上，参数上，等位置处

### 自定义注解



```
public @interface 注解名称{
        public 属性类别 属性名（）default 默认值;
}
```

如果只有一个value，可以省略不写

注解本质上是一个接口，java中所有注解都是继承了Annotation接口的

@注解（...）其实就是一个实现类对象，实现了该注解以及Annotation接口

### 元注解

注解注解的注解

@Target注解

Target注解的作用是：描述注解的使用范围(即被修饰的注解可以用在什么地方).

Target注解用来说明那些被它所注解的注解类可修饰的对象范围：注解可以用于修饰 packages、types(类、接口、枚举、注解类)、类成员(方法、构造方法、成员变量、枚举值)、方法参数和本地变量(如循环变量、catch参数)，在定义注解类时使用了@Target 能够更加清晰的知道它能够被用来修饰哪些对象，它的取值范围定义在ElementType 枚举中.

@Retention

Reteniton注解的作用是：描述注解保留的时间范围(即：被描述的注解在它所修饰的类中可以被保留到何时).

Reteniton注解用来限定那些被它所注解的注解类在注解到其他类上以后，可被保留到何时，一共有三种策略，定义在RetentionPolicy枚举中.

### 注解的解析

指导思想：要解析谁上面的注解，就应该先拿到谁

![image-20251012154549880](https://gitee.com/Wsj123789/wsj/raw/master/img/20251012154549935.png)

```
public class DemoTest {
    @Test
    public void parseClss(){
        Class c1=Demo.class;
        if(c1.isAnnotationPresent(MyTest.class)){
            //获取注解对象
            MyTest myTest=(MyTest) c1.getDeclaredAnnotation(MyTest.class);

            String name=myTest.value();
            double height=myTest.price();
            String[] address=myTest.address();

            System.out.println(Arrays.toString(address));
            System.out.println(name);
            System.out.println(height);
        }
    }
    @Test
    public void parseMethod() throws NoSuchMethodException {
        Class c1=Demo.class;
        Method method=c1.getMethod("go");
        if(method.isAnnotationPresent(MyTest.class)){
            MyTest mytest=(MyTest) method.getDeclaredAnnotation(MyTest.class);
            String[] address=mytest.address();
            String name=mytest.value();
            double height=mytest.price();
            System.out.println(Arrays.toString(address));
            System.out.println(name);
            System.out.println(height);

        }
    }
}

```

```
package demo1reflect;
@MyTest(value = "赵四",address = {"北京，上海"})
public class Demo {
    @MyTest(value = "事务所",address = {"上海","山西"})
    public void go(){

    }
}
```

### 应用场景

```
public class Annotationdemo1 {
    public static void main(String[] args) throws InvocationTargetException, IllegalAccessException {
        //获取类对象
        //获取所有方法
        //遍历所有方法，如果有注解就执行
        Annotationdemo1 ad=new Annotationdemo1();
        Class c=Annotationdemo1.class;
        Method[] md=c.getMethods();
        for(Method ed:md){
            if(ed.isAnnotationPresent(MyTest2.class)){
                //执行这个方法
                ed.invoke(ad);
            }
        }
    }

        @MyTest2
        public  void test1(){
            System.out.println("test1方法执行");
    }
    public void test2(){
        System.out.println("test2方法执行");
    }
    public void test3(){
        System.out.println("test3方法执行");
    }
    public void test4(){
        System.out.println("test4方法执行");
    }


}
```

## 动态代理

```
//中介公司，创建对象并返回
public class ProxyUtil {
    public static StarService createProxy(Star s){
        //类型一：用于执行用那个类加载器生成的代理类
        //参数二：代理类需要实现的接口
        //参数三：制定代理类如何去代理
        StarService proxy=(StarService) Proxy.newProxyInstance(s.getClass().getClassLoader(), s.getClass().getInterfaces(), new InvocationHandler() {
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                //参数一：proxy接收代理对象本身
                //参数二：method表示正在被代理的方法的参数
                //参数三：args代表正在被代理的方法的参数
                String methodname=method.getName();
                if("sing".equals(methodname)){
                    System.out.println("准备话筒，收费20万");
                }else if("dance".equals(methodname)){
                    System.out.println("准备场地，收费100万");
                }
                //把真正的明星找来干活
                Object result=method.invoke(s,args);
                return result;
            }
        });
        return proxy;
    }
}
```



## 相关条目
- [[面向对象]]
- [[Stream]]
