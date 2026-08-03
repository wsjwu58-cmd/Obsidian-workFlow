## 概念

Vue是一款用于**构建用户界面**的**渐进式**的JavaScript框架

框架：一套完整的项目解决方案，用于快速构建项目

优点：大大提升前端项目的开发效率

缺点：需要记忆框架的使用规则

### 准备

引入Vue模块

创建Vue程序的应用实例，控制视图的元素

准备元素，被Vue控制

### 数据驱动视图

准备数据

通过插值表达式渲染页面

## Vue常用指令

指令：HTML标签上带有v-前缀的特殊属性，不同的指令具有不同的含义，可以实现不同的功能

### v-for

作用：列表渲染，遍历容器的元素或者对象的属性

语法：

```
<tr v-for="(item,index) in items":key="item.id">{{item}}</tr>
```

items:要遍历的数组

item:为遍历出来的元素

index:索引/下标，从0开始；

key:

作用：为元素添加唯一标识，便于vue进行列表项的正确排序复用，提升渲染性能

推荐使用id作为key(唯一)

### v-bind

作用：动态为HTML标签绑定属性值，如设置href,src,style样式等

语法：v-bind:属性名="属性值"

简化：：属性名=“属性值”

### v-if &v-show

作用：这两类指令，都是用来控制元素的显示与隐藏的

v-if

- 语法v-if="表达式"，表达式的值为true，显示：false，隐藏
- 原理：基于条件判断，来控制创建或移除元素节点
- 场景：要么显示，要么不显示， 不频繁切换的场景





v-show

- 语法：v-show="表达式",表达式的值为true，显示：false，隐藏
- 原理：基于CSS样式display来控制显示与隐藏
- 场景：频繁切换显示隐藏的场景

### v-on

作用：为html标签绑定事件（添加事件监听）

语法：

v-on：事件名=“方法名”

简写为 @事件名="..."

### v-model

- v-model指令可以在表单 input、textarea以及select元素上创建双向数据绑定；
- 它会根据控件类型自动选取正确的方法来更新元素；
- 尽管如此， v-model 本质上是语法糖，它负责监听用户的输入事件来更新数据，并在某种极端场景下进行一些特殊处理；

## Ajax

作用：

数据交换：通过Ajax可以给服务器发送请求，并获取服务器响应的数据

异步交互：可以在不重新加载整个页面的情况下，与服务器交换数据并更新部分网页的技术，如：搜索联想，用户名是否可用的校验等等

### 同步与异步

同步：客户端发起请求服务器，服务器处理，客户端等待，处理后返回客户端，客户端解除等待

异步：客户端发出请求后可以执行其他操作，服务器处理后返回

### Axios

对原生的Ajax进行了封装，简化书写，快速开发

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ajax</title>
</head>
<body>
    <input type="button" value="获取数据CET" id="btnGet">
    <input type="button" value="操作数据POST" id="btnPost">

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        //发送GET请求
        document.querySelector('#btnGet').addEventListener('click',()=>{
            //axios发布异步请求
            axios({
                url:'https://mock.apifox.cn/m1/3083103-0-default/emps/list',
                method:'GET'
            }).then((result)=>{//成功回调函数
                console.log(result);
            }).catch((err)=>{//失败回调函数
                console.log(err);
            })

        })
        //发送POST请求
        document.querySelector('#btnPost').addEventListener('click',()=>{
            axios({
                url:'https://mock.apifox.cn/m1/3083103-0-default/emps/upda',
                method:'POST',
                data:{id:1}//Post请求方式
            }).then((result)=>{//成功回调函数
                console.log(result);
            }).catch((err)=>{//失败回调函数
                console.log(err);
            })
        })
    </script>
</body>
</html>
```

## Maven

是一款用于管理和构建java的工具

### 作用

依赖管理：方便快捷的管理项目依赖的资源（jar包）

项目构建：标准化的跨平台的自动化项目构建方式

统一项目结构：提供标准、统一的项目结构，降低开发，构建，维护的成本

### 坐标

是资源（jar）的唯一标识，通过坐标可以唯一定位资源位置

使用坐标定义项目或引入项目中需要的依赖

#### 主要组成

groupid:定义当前Maven项目隶属组织名称

artifactId:定义当前Maven项目名称（模块名称）

version：定义当前项目版本号

SNAPSHOT:功能不稳定，尚处于开发中的版本

RELEASE：功能趋于稳定，可以用于发行的版本

### 依赖管理

依赖：项目在运行过程中需要的jar包，一个项目中可以引入多个依赖

配置：

在pom.xml中编写<dependencies>标签

在<dependencies>标签中用<dependency>引入坐标

定义坐标的groupId,artifactId,version

点击刷新按钮，引入最新加入的坐标

#### 排除依赖

指的是主动断开依赖的资源，被排除的资源无需指定版本

```
<dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>6.1.4</version>
            <exclusions>
                <exclusion>
                    <groupId>io.micrometer</groupId>
                    <artifactId>micrometer-observation</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
```

### 生命周期

- clean:清理工作
- default:核心工作，如：编译、测试、打包、安装、部署等
- site:生成报告、发布站点等

### 单元测试

测试：鉴定软件的完整性、安全性和质量的过程

阶段划分：单元测试、集成测试、系统测试、验收测试

测试方法：白盒测试、黑盒测试及灰盒测试

- 白盒：清楚知道代码内部结构、代码逻辑
- 黑盒：不清楚代码内部结构、用于验证软件的功能、兼容性等方面
- 灰盒：即关注软件内部表现也关注外部功能

使用junit单元测试框架

![image-20251016082137928](https://gitee.com/Wsj123789/wsj/raw/master/img/20251016082138045.png)

```
@DisplayName("用户信息测试类")
public class UserServiceTest {
    @Test
    public void testgetage(){
        UserService us=new UserService();
        Integer age=us.getAge("14010820060823001X");
        System.out.println(age);
    }
    @Test
    public void testGetgender(){
        UserService us=new UserService();
        String gender=us.getGender("14010820060823001X");
        System.out.println(gender);
    }
    @Test
    public void testGenderWithAssert(){
        UserService us=new UserService();
        String gender=us.getGender("14010820060823001X");
        Assertions.assertEquals("男",gender,"性别获取错误有问题");
    }

    @Test
    public void testGenderWithAssert2(){
        UserService us=new UserService();
        Assertions.assertThrows(IllegalArgumentException.class,()->{
            us.getGender(null);
        });
    }
    @DisplayName("测试用户性别"
    )
    @ParameterizedTest
    @ValueSource(strings={"14010820060823001X","140108200608230020"})
    public void testGetgender2(String idCard){
        UserService us=new UserService();
        String gender=us.getGender(idCard);
        //断言
        Assertions.assertThrows(IllegalArgumentException.class,()->{
            us.getGender(null);
        });
    }

}
```



#### 单元测试-企业开发规范

## Web基础

### Spring

#### SpringBoot

入门程序

基于SpringBoot开发一个Web应用，浏览器发送请求/Hello之后，浏览器返回一个“hello world”

```
@RestController//当前类是一个请求处理类
public class HelloControl {
    @RequestMapping("/hello")
    public String hello(String name){
        System.out.println("name:"+name);
        return "Hello"+name+"~";
    }
}
```

启动

```
@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

}
```

### HTTP协议

概念：规定了浏览器与服务器之间数据传输的规则

特点：

基于TCP协议：面向连接，安全

基于请求-响应模型的：一次请求对应以此响应

HTTP协议是无状态的协议：对于事物处理没有记忆能力，每次请求-响应都是独立的

- 缺点：多次请求间不能共享数据
- 优点：速度快

#### 请求数据格式

Host：请求的主机名

User-Agent:浏览器版本，例如Chrome浏览器的标识类似Mozilla/5.0....

Accept-Language:表示浏览器的偏好语言，服务器可以据此返回不同语言的网页

Accept-Encoding:表示浏览器可以支持的压缩类型，例如gzip,deflate等

Content-Type:请求主体的数据类型

Content-Length:请求主体的大小

请求行指的是请求数据格式的第一行，由三个部分组成：

- 请求方式
- 请求资源路径
- 协议及版本

请求头指的就是从第二行开始一直到后面的部分数据。请求头的格式是键值对形式，中间用冒号分隔。前面是请求头的名字，后面是对应的值。

请求体是 POST 请求特有的组成部分，用来存放请求参数。请求体和请求头之间有一个空行存在，通过一个空行将这两部分分离开来。

在 POST 请求里面，请求参数是携带在请求体这个位置。

Web服务器对HTTP协议请求进行了解析，并进行封装，在调用Controller方法的时候传递给了该方法

```
@RestController
public class Request {
    @RequestMapping("/request")
    public String request(HttpServletRequest request){
        //1.获取请求方式
        String method=request.getMethod();
        System.out.println("method:"+method);

        //2.获取请求url地址
        String url=request.getRequestURL().toString();
        System.out.println("url:"+url);

        //3.获取请求协议
        String protocol=request.getProtocol();
        System.out.println("protocol:"+protocol);

        //4.获取请求参数
        String queryString=request.getParameter("name");
        System.out.println("name:"+queryString);



        //5.获取请求头 --Accept
        String accept=request.getHeader("Accept");
        System.out.println("Accept:"+accept);

        return "请求成功";
    }

}
```

#### 响应数据格式

![image-20251019202239393](https://gitee.com/Wsj123789/wsj/raw/master/img/20251019202246174.png)

重定向：底层涉及到两次请求，浏览器请求服务器A响应数据，但是A服务器中没有它需要的数据，于是返回一个响应头（LocationB）,指向服务器B的地址，浏览器获取到地址后向服务器B响应数据，服务器返回数据

#### 响应数据设置

```
@RestController
public class ResponseController {
    @RequestMapping("/response")
    public void response(HttpServletResponse response) throws IOException {
        //设置响应状态码
        response.setStatus(401);
        //设置响应头
        response.setHeader("name","itheima");
        //设置响应体
        response.getWriter().write("<h1>hello response</h1>");

    }
    @RequestMapping("/response2")
    public ResponseEntity<String> response2(){
        //设置响应状态码
        return ResponseEntity.status(401).header("name","javaweb-ai").body("<h1>hello response</h1>");
    }

}
```

两种方式

#### Web案例

**服务端**

```
@RestController//@ResponseBody ->将controller返回值直接作为响应体的数据直接响应；返回值是对象/集合->json
public class UserController {
    @RequestMapping("/list")
    public List<User> list() throws FileNotFoundException {
        //读取user.txt文件获取用户数据
        InputStream in=this.getClass().getClassLoader().getResourceAsStream("user.txt");

        //读取文件封装到List集合中
        ArrayList<String> as=IoUtil.readLines(in, StandardCharsets.UTF_8,new ArrayList<>());


        //解析用户信息，封装为User对象->List集合
        List<User> userList=as.stream().map(line->{
            String[] parts=line.split(",");
            Integer id=Integer.parseInt(parts[0]);
            String username=parts[1];
            String password=parts[2];
            String name=parts[3];
            Integer age=Integer.parseInt(parts[4]);
            LocalDateTime ld=LocalDateTime.parse(parts[5], DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            return new User(id,username,password,name,age,ld);
        }).toList();


        //返回数据
        return userList;
    }
}
```

使用IO流获取字节输入流，再通过行读取数据封装到ArrayList数组当中

map函数可以将以逗号分隔开的用户信息封装到新对象User中，并封装到List数组当中

**前端**

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户列表数据</title>
    <style>
        /*定义css，美化表格*/
        table{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
            border: 1px solid #ccc;
            text-align: center;
            font-size: 14px;
        }
        tr {
            height: 40px;
        }
        th,td{
            border: 1px solid #ccc;
        }
        thead{
            background-color: #e8e8e8;
        }
        h1{
            text-align: center;
            font-family: 楷体;
        }
    </style>
</head>
<body>
    <div id="app">
        <h1>用户列表数据</h1>
        <!--定义一个表格,包括6列,分别是: ID, 用户名, 密码, 姓名, 年龄, 更新时间-->
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>用户名</th>
                    <th>密码</th>
                    <th>姓名</th>
                    <th>年龄</th>
                    <th>更新时间</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in userList">
                    <td>{{user.id}}</td>
                    <td>{{user.username}}</td>
                    <td>{{user.password}}</td>
                    <td>{{user.name}}</td>
                    <td>{{user.age}}</td>
                    <td>{{user.updateTime}}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!--引入axios-->
    <script src="js/axios.min.js"></script>
    <script type="module">
        import { createApp } from './js/vue.esm-browser.js'
        createApp({
            data() {
                return {
                    userList: []
                }
            },
            methods: {
                async search(){
                    const result = await axios.get('/list');
                    this.userList = result.data;
                }
            },
            mounted() {
                this.search();
            }
        }).mount('#app')
    </script>
</body>
</html>
```

### 分层解耦

#### 三层架构

Controller:控制层，接收前端发送的请求，对请求进行处理，并响应数据

```
@RestController//@ResponseBody ->将controller返回值直接作为响应体的数据直接响应；返回值是对象/集合->json
public class UserController {
    private UserService us=new UserServiceimpl();
    @RequestMapping("/list")
    public List<User> list() throws FileNotFoundException {
        //调用service获取数据
        List<User> userList=us.findAll();



        //返回数据
        return userList;
    }
}
```

service:业务逻辑层，处理具体的业务逻辑

```
public class UserServiceimpl implements UserService {
    private UserDao userDao=new UserDaoimpl();
    @Override
    public List<User> findAll() {
        List<String>as=userDao.findAll();
        //调用Dao
        //解析用户信息，封装为User对象->List集合
        List<User> userList=as.stream().map(line->{
            String[] parts=line.split(",");
            Integer id=Integer.parseInt(parts[0]);
            String username=parts[1];
            String password=parts[2];
            String name=parts[3];
            Integer age=Integer.parseInt(parts[4]);
            LocalDateTime ld=LocalDateTime.parse(parts[5], DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            return new User(id,username,password,name,age,ld);
        }).toList();
        return userList;
    }
}
```



dao:数据访问层（持久层），负责数据访问操作，包括数据的增删改查

```
public class UserDaoimpl implements UserDao {

    @Override
    public List<String> findAll() {
        //读取user.txt文件获取用户数据
        InputStream in=this.getClass().getClassLoader().getResourceAsStream("user.txt");

        //读取文件封装到List集合中
        ArrayList<String> as= IoUtil.readLines(in, StandardCharsets.UTF_8,new ArrayList<>());
        return as;
    }
}
```

可读性强，复用性强，方便维护



**耦合**：衡量软件中各个层/各个模块的依赖关联程度

**内聚**：软件中各个功能模块内部的联系

**软件设计原则**：高内聚低耦合

#### IOC与DI

控制反转：简称IOC，对象的创建控制权由自身转变为外部容器，需要使用时从容器中取出

依赖注入：简称DI，容器为应用程序提供运行时，所依赖的资源，称之为依赖注入

Bean对象：IOC容器中创建管理的对象



**步骤：**

将Dao和Service层的实现类交给IOC容器管理

在实现类上方添加**@Component**

为Controller及service注入运行时所依赖的对象

在创建对象时上方添加**@Autowired**



#### IOC详解

![image-20251021181053301](https://gitee.com/Wsj123789/wsj/raw/master/img/20251021181058252.png)

声明的注解，想要生效，需要被组件扫描注解@ComponentScan扫描，默认扫描范围是启动类所在的包及其子包

#### DI详解

```
//构造器注入
    private final UserService userService;
    @Autowired
   public UserController(UserService userService){
        this.userService=userService;
    }
```

优点：清晰看到类的依赖关系，提高了代码的安全性

缺点：代码繁琐，如果构造参数过多，可能会导致构造函数臃肿

setter注入

缺点：需要额外编写setter方法，增加了代码量



如果存在多个相同类型的bean，将会报错

@Primary:优先注入

@Qualifier():注入哪个bean

@Resource(name="")：注入bean的名称

## MyBatis

### JDBC

操作关系型数据库的一种API

操作数据库的步骤

```
public class JdbcTest {
    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {
        //注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");

        //获取数据库的链接
        String url="jdbc:mysql://localhost:3306/web01";
        String username="root";
        String password="qwer1234";
        Connection connection=DriverManager.getConnection(url,username,password);

        //获取SQL语句的执行对象
        Statement statement=connection.createStatement();

        //执行SQL
        int i=statement.executeUpdate("update user set age=25 where id = 1");
        System.out.println("sql语句执行完影响的记录数为："+i);

        //释放资源
        statement.close();
        connection.close();

    }
}
```

#### 执行DQL语句

```
@Test
    public void testSelect(){
        String URL = "jdbc:mysql://localhost:3306/web01";
        String USER = "root";
        String PASSWORD = "qwer1234";

        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null; //封装查询返回的结果

        try {
            // 1. 注册 JDBC 驱动
            Class.forName("com.mysql.cj.jdbc.Driver");

            // 2. 打开链接
            conn = DriverManager.getConnection(URL, USER, PASSWORD);

            // 3. 执行查询
            String sql = "SELECT id, username, password, name, age FROM user WHERE username = ? AND password = ?"; //预编译SQL
            stmt = conn.prepareStatement(sql);

            stmt.setString(1, "daqiao");
            stmt.setString(2, "123456");

            rs = stmt.executeQuery();

            // 4. 处理结果集
            while (rs.next()) {
                User user = new User(
                        rs.getInt("id"),
                        rs.getString("username"),
                        rs.getString("password"),
                        rs.getString("name"),
                        rs.getInt("age")
                );
                System.out.println(user); // 使用 Lombok 的 @Data 自动生成的 toString 方法
            }
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // 5. 关闭资源
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
    }
```

#### 预编译SQL

优势一：防止SQL注入，更安全

通过控制输入一些代码或字符传递到服务器，对服务器进行攻击

如果使用静态SQL，会被进行修改，改变判断条件

优势二：性能更高

如果缓存中有输入的SQL语句，则直接从缓存中拿出

### MyBatis

创建工程，引入依赖

```
spring.datasource.url=jdbc:mysql://localhost:3306/web01
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.username=root
spring.datasource.password=qwer1234
```

准备数据库表、实体类

application.properties中配置数据库连接信息

定义mapper接口，编写SQL

```
@Mapper //应用程序运行时，自动为接口创建一个实现类对象（代理对象），并且自动将实现类对象存入IOC容器
public interface UserMapper {
    @Select("select * from user")
    public List<User> findAll();

}
```

测试类运行

```
@SpringBootTest //单元测试的注解-当前测试类中的测试方法运行时，会启动SpringBoot项目
class SpringbootMybatisApplicationTests {
    @Autowired
    private UserMapper userMapper;
    @Test
    public  void testFindAll(){
        List<User> userList=userMapper.findAll();
        userList.forEach(System.out::println);
    }

}
```

#### 删除用户-delete

#{}:占位符，执行时替换为？，生成预编译SQL

```
@Delete("delete from user where id=#{id}")
public Integer delete(Integer id);
```

#### 添加用户

```
@Insert("insert into user(username,password,name,age) values(#{username},#{password},#{name},#{age})")
public void insert(User user);
```

#### 修改用户

```
@Update("update user set username=#{username},password=#{password},name=#{name},age=#{age} where id=#{id}")
public void update(User user);
```

#### 查询操作

```
@Select("select * from user where password=#{password} and username=#{username}")
public User findUsernameAndPassword(String username,String password);
```

### 数据库连接池

数据库连接池是个容器，负责分配、管理数据库连接

它允许应用程序重复使用一个现有的数据库连接，而不是在重新建立一个

避免因为没有释放连接而引起的数据库连接遗漏

### XML映射配置

默认规则：

- XML映射文件的名称与Mapper接口名称一致，并且将XML映射文件和Mapper接口放置在相同包下
- XML映射文件的namespace属性与Mapper接口全限定名一致
- XML映射文件中sql语句的id与Mapper接口中的方法名一致，并保持返回类型一致

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.example.springbootmybatis.mapper.UserMapper">
    <select id="findAll" resultType="org.example.springbootmybatis.pojo.User">
        select id,username,password,name,age from user
    </select>
</mapper>
```

```
#指定XML映射配置文件的位置
mybatis.mapper-locations=classpath:mapper/*.xml
```

## SpringBoot项目配置文件

### yml配置文件

格式：

数值前加空格

相同元素左侧对齐

```
#定义对象/Map集合
user:
  name: JACK
  age: 18
  gender: 男
#定义数组/List/Set集合
hobby:
  -Java
  -python
  -c
```

## Logback入门程序

通过配置文件控制程序是否输出日志

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
	<!-- 控制台输出 -->
	<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
		<encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
			<!--格式化输出：%d 表示日期，%thread 表示线程名，%-5level表示级别从左显示5个字符宽度，%logger显示日志记录器的名称， %msg表示日志消息，%n表示换行符 -->
			<pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50}-%msg%n</pattern>
		</encoder>
	</appender>

	<!-- 系统文件输出 -->
	<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
			<!-- 日志文件输出的文件名, %i表示序号 -->
			<FileNamePattern>D:/tlias-%d{yyyy-MM-dd}-%i.log</FileNamePattern>
			<!-- 最多保留的历史日志文件数量 -->
			<MaxHistory>30</MaxHistory>
			<!-- 最大文件大小，超过这个大小会触发滚动到新文件，默认为 10MB -->
			<maxFileSize>10MB</maxFileSize>
		</rollingPolicy>

		<encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
			<!--格式化输出：%d 表示日期，%thread 表示线程名，%-5level表示级别从左显示5个字符宽度，%msg表示日志消息，%n表示换行符 -->
			<pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50}-%msg%n</pattern>
		</encoder>
	</appender>

	<!-- 日志输出级别 -->
	<root level="ALL">
		<appender-ref ref="STDOUT" />
		<appender-ref ref="FILE" />
	</root>
</configuration>

```

常见日志级别

![image-20251025164818775](https://gitee.com/Wsj123789/wsj/raw/master/img/20251025164821423.png)


## 相关条目
- [[VUE]]
- [[案例]]
- [[苍穹]]
- [[Layui表格和表单]]
