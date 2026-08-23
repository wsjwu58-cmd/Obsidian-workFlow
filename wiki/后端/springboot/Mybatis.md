# Mybatis
[MyBatis 3 | 入门 – mybatis](https://mybatis.org/mybatis-3/zh_CN/getting-started.html)

## 映射文件

两个一致：

方法名和sql语句中的id一致

映射文件名字和Mapper接口名字一致

1. **加载 MyBatis 配置文件**

InputStream is = Resources.getResourceAsStream("mybatis-config.xml");

*   `Resources.getResourceAsStream()`: MyBatis 提供的工具方法
*   从 classpath 根目录加载 `mybatis-config.xml` 配置文件
*   返回配置文件的输入流

2. **创建 SqlSessionFactoryBuilder**

SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();

*   创建工厂构建器，用于构建 `SqlSessionFactory`

3. **构建 SqlSessionFactory**

SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(is);

*   根据配置文件构建 `SqlSessionFactory`（数据库会话工厂）
*   这是**重量级对象**，通常应用生命周期内只创建一次
*   负责解析配置、创建数据库连接等

4. **获取 SqlSession**

SqlSession sqlSession = sqlSessionFactory.openSession();

*   创建 `SqlSession`（数据库会话）
*   这是**轻量级对象**，每次数据库操作都应该创建新的
*   默认情况下**不会自动提交事务**，需要则在openSession中设置true

5. **获取 Mapper 接口代理对象**

UserMapper u = sqlSession.getMapper(UserMapper.class);

*   通过动态代理技术创建 `UserMapper` 接口的实现类
*   MyBatis 会自动将接口方法与对应的 SQL 映射关联

6. **执行数据库操作**

int result = u.insertUser(); System.out.println(result);

*   调用 Mapper 方法执行 SQL
*   `insertUser()` 对应 XML 或注解中的 SQL 语句
*   返回受影响的行数

## resulttype和resultmap

resulttype主要用于定义java类型，数据库字段和实体类属性名一致

resultmap主要用于映射配置，若数据库字段和实体类属性名不一致，定义映射，使得实体类中的

属性可以接收数据库的数据

## MyBatis获取参数值的两种方式

${}：字符串拼接 #{}：占位符赋值

当mapper接口的参数为多个时，Mybatis会将这些参数放在map集合当中

以ang0,arg1...为键

以param1,param2....为键

或者直接定义一个map集合，手动将数据放到map中，根据键值访问数据

```
@Test  
public void test3() throws IOException {  
    SqlSession s =SqlSessionUtils.getSqlSession();  
    UserMapper userMapper=s.getMapper(UserMapper.class);  
    Map<String,Object> map=new HashMap<>();  
    map.put("param1","wss");  
    map.put("param2","1234");  
  
    User user=userMapper.checkLogin(map);  
    log.info("user:{}",user);  
}
```

```
<select id="checkLogin" resultType="User">  
    select * from user where username=#{param1} and password=#{param2}  
</select>
```

使用@Param注解命名参数，Mybatis将这些参数放在一个Map集合中，以两种方式存储 利用#{}的方式访问键中的值

## Mybatis查询功能

查询数据只有一条： 可以用实体类接收 可以用List数组接收 可以用map集合接收

查询数据多条： 不能使用实体类接收

### @MapKey注解

如果在查询多条数据时，想要用Map类型的数据返回，需要在Mapper接口处加上@MapKey注解，指明返回数据的键值，键值与返回数据的字段名相关

### 模糊查询

使用${}进行查询

```
select * from user where username like '%${username}%'
```

使用concat字符串连接

```
select * from user where username like concat(‘%’,#{username},'%')
```

### 批量删除

```
delete from user where id in (${ids})
```

### 添加功能获取自定义主键

```
<insert id="addUser" useGeneratedKeys="true" keyProperty="id">  
    insert into user values(null,#{username},#{password},#{age},#{sex},#{email})  
</insert>
```

## 成员变量和属性详细对比

| 方面 | 成员变量 (Field) | 属性 (Property) |
| --- | --- | --- |
| **本质** | 变量声明 | 方法（getter/setter） |
| **语法** | `private String name;` | `getName()`, `setName()` |
| **访问控制** | 直接通过访问修饰符控制 | 通过方法的公开性控制 |
| **封装性** | 直接暴露实现细节 | 隐藏实现，提供接口 |
| **计算能力** | 只是存储数据 | 可以在方法中添加逻辑 |
| **命名规范** | 无特殊要求 | getter/setter遵循JavaBean规范 |

1.  **所有属性都对应着方法，但不一定有对应的成员变量**
2.  **有成员变量不一定有对应的属性**（如果是private且没有getter/setter）
3.  **属性是面向外部的接口，成员变量是内部实现**
4.  **良好的设计应该：成员变量私有，通过属性方法对外提供访问**

## 思考：为什么数据库列名要与实体类属性名进行映射，而参数不用

传递参数时，参数已经在方法调用栈中，可以直接通过参数名或者参数位置进行访问

```
// MyBatis内部简化逻辑（参数解析器）
public class ParamNameResolver {
    public Object getNamedParams(Object[] args) {
        // 参数直接存储在args数组中
        // 创建Map: {username=value1, age=value2, param1=value1, param2=value2}
        Map<String, Object> param = new HashMap<>();
        param.put("username", args[0]);    // 通过参数名访问
        param.put("age", args[1]);         // 通过参数名访问
        param.put("param1", args[0]);      // 通过位置访问
        param.put("param2", args[1]);      // 通过位置访问
        return param;
    }
}
```

实体类传递时，由于成员变量是私有属性，Mybatis通过反射进行访问，获取指定的get方法，如果没有进行映射的话，Mybatis无法找到对应的get方法，也就无法进行值的传递

```
// 这些写法必须严格匹配属性名
<select id="findUser" resultType="User">
    select * from user 
    where username = #{username}      <!-- 正确：对应getUsername() -->
    <!-- where username = #{user} -->     <!-- 错误：没有getUser()方法 -->
    <!-- where username = #{name} -->     <!-- 错误：没有getName()方法 -->
</select>
```

## ResultMap使用

基础语法

```
<resultMap id="唯一标识" type="映射的Java类型">
    <!-- 主键映射 -->
    <id column="数据库列名" property="Java属性名"/>
    <!-- 普通字段映射 -->
    <result column="数据库列名" property="Java属性名"/>
    <!-- 关联对象映射 -->
    <association property="Java属性名" javaType="关联对象类型"/>
    <!-- 集合映射 -->
    <collection property="Java属性名" ofType="集合元素类型"/>
</resultMap>

<select id="selectUserById" resultMap="BaseUserMap">
    select user_id, user_name, age, email, create_time
    from user 
    where user_id = #{userId}
</select>
```

### 处理映射关系

#### 多对一：

级联属性赋值 一次性获取所有属性，建立映射

```
<resultMap id="EmployeeAndDeptMap" type="Employee">
    <id column="id" property="id"/>
    <result column="last_name" property="lastName"/>
    <result column="email" property="email"/>
    
    <!-- 级联属性赋值 -->
    <result column="dept_id" property="dept.id"/>
    <result column="department_name" property="dept.departmentName"/>
</resultMap>

<select id="getEmployeeAndDeptById" resultMap="EmployeeAndDeptMap">
    select 
        e.id, e.last_name, e.email, e.dept_id,
        d.id as dept_id, d.department_name
    from employee e
    left join department d on e.dept_id = d.id
    where e.id = #{id}
</select>
```

association

```
<!-- 方式1：嵌套结果映射 -->
<resultMap id="EmployeeWithDeptMap" type="Employee">
    <id column="id" property="id"/>
    <result column="last_name" property="lastName"/>
    <result column="email" property="email"/>
    
    <!-- association 关联映射 -->
    <association property="dept" javaType="Department">
        <id column="dept_id" property="id"/>
        <result column="department_name" property="departmentName"/>
    </association>
</resultMap>

<select id="getEmployeeWithDept" resultMap="EmployeeWithDeptMap">
    select 
        e.id, e.last_name, e.email,
        d.id as dept_id, d.department_name
    from employee e
    left join department d on e.dept_id = d.id
    where e.id = #{id}
</select>
```

分布查询 Mapper接口

```
// EmployeeMapper.java
public interface EmployeeMapper {
    // 级联属性方式
    Employee getEmployeeAndDeptById(Integer id);
    
    // association方式
    Employee getEmployeeWithDept(Integer id);
    
    // 分步查询方式
    Employee getEmployeeByIdStep(Integer id);
}

// DepartmentMapper.java
public interface DepartmentMapper {
    Department getDeptById(Integer id);
}
```

SQL映射文件

```
<!-- EmployeeMapper.xml -->
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.EmployeeMapper">

    <!-- 1. 级联属性方式 -->
    <resultMap id="EmployeeAndDeptMap" type="Employee">
        <id column="id" property="id"/>
        <result column="last_name" property="lastName"/>
        <result column="email" property="email"/>
        <result column="dept_id" property="dept.id"/>
        <result column="department_name" property="dept.departmentName"/>
    </resultMap>

    <!-- 2. association方式 -->
    <resultMap id="EmployeeWithDeptMap" type="Employee">
        <id column="id" property="id"/>
        <result column="last_name" property="lastName"/>
        <result column="email" property="email"/>
        <association property="dept" javaType="Department">
            <id column="dept_id" property="id"/>
            <result column="department_name" property="departmentName"/>
        </association>
    </resultMap>

    <!-- 3. 分步查询方式 -->
    <resultMap id="EmployeeStepMap" type="Employee">
        <id column="id" property="id"/>
        <result column="last_name" property="lastName"/>
        <result column="email" property="email"/>
        <result column="dept_id" property="deptId"/>
        <association property="dept" 
                     select="com.example.mapper.DepartmentMapper.getDeptById"
                     column="dept_id"
                     fetchType="lazy"/>
    </resultMap>

    <!-- 查询方法 -->
    <select id="getEmployeeAndDeptById" resultMap="EmployeeAndDeptMap">
        select e.id, e.last_name, e.email, e.dept_id,
               d.id as dept_id, d.department_name
        from employee e
        left join department d on e.dept_id = d.id
        where e.id = #{id}
    </select>

    <select id="getEmployeeWithDept" resultMap="EmployeeWithDeptMap">
        select e.id, e.last_name, e.email,
               d.id as dept_id, d.department_name
        from employee e
        left join department d on e.dept_id = d.id
        where e.id = #{id}
    </select>

    <select id="getEmployeeByIdStep" resultMap="EmployeeStepMap">
        select id, last_name, email, dept_id
        from employee 
        where id = #{id}
    </select>

</mapper>

<!-- DepartmentMapper.xml -->
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.DepartmentMapper">

    <select id="getDeptById" resultType="Department">
        select id, department_name
        from department 
        where id = #{id}
    </select>

</mapper>
```

| 特性 | 级联属性 | association | 分步查询 |
| --- | --- | --- | --- |
| **SQL次数** | 1次 | 1次 | 2次 |
| **性能** | 好 | 好 | 可能更好（懒加载） |
| **配置复杂度** | 简单 | 中等 | 复杂 |
| **灵活性** | 低 | 高 | 最高 |
| **懒加载** | 不支持 | 不支持 | 支持 |
| **适用场景** | 简单关联 | 复杂关联 | 大型对象、性能敏感 |

#### 一对多

collection:处理一对多的关系

ofType:该属性集合中的类型

```
<resultMap id="empResultMap" type="org.example.pojo.Emp">  
    <id column="id" property="id"/>  
    <result column="username" property="username"/>  
    <result column="password" property="password"/>  
    <result column="name" property="name"/>  
    <result column="gender" property="gender"/>  
    <result column="phone" property="phone"/>  
    <result column="job" property="job"/>  
    <result column="salary" property="salary" />  
    <result column="image" property="image"/>  
    <result column="entry_date" property="entryDate"/>  
    <result column="dept_id" property="deptId"/>  
    <result column="create_time" property="createTime"/>  
    <result column="update_time" property="updateTime"/>  
  
    <collection property="exprList" ofType="org.example.pojo.EmpExpr">  
        <id column="ee_id" property="id"/>  
        <result column="ee_empid" property="empId"/>  
        <result column="ee_begin" property="begin"/>  
        <result column="ee_end" property="end"/>  
        <result column="ee_company" property="company"/>  
        <result column="ee_job" property="job"/>  
    </collection></resultMap>
```

## 动态SQL

### if where 标签

```
select emp.*,dept.name deptName from emp left join  dept on emp.dept_id = dept.id  
<where>  
    <if test="name !=null and name !=''">  
        emp.name like concat('%',#{name},'%')  
    </if>  
  <if test="gender !=null">  
      and emp.gender=#{gender}  
  </if>  
  <if test="begin !=null and end !=null">  
      and emp.entry_date between #{begin} and #{end}  
  </if>  
</where>
```

### trim标签

prefix：在trim标签内sql语句加上前缀 suffix：在trim标签内sql语句加上后缀 prefixOverrides：指定去除多余的前缀内容，如：prefixOverrides=“AND | OR”，去除trim标签内sql语句多余的前缀"and"或者"or"。 suffixOverrides：指定去除多余的后缀内容。

### foreach标签

```
<!-- in查询所有，不分页 -->
<select id="selectIn" resultMap="BaseResultMap">
    select name,hobby from student where id in
    <foreach item="item" index="index" collection="list" open="(" separator="," close=")">
        #{item}
    </foreach>
</select>

```

collection：collection 属性的值有三个分别是 list、array、map 三种，分别对应的参数类型为：List、数组、map 集合。（如果传入单个参数，可以直接写参数名） item ：表示在迭代过程中每一个元素的别名 index ：表示在迭代过程中每次迭代到的位置（下标） open ：前缀 close ：后缀 separator ：分隔符，表示迭代时每个元素之间以什么分隔

## Mybatis缓存

### Mybatis的一级缓存

级别：SqlSession

同一个SqlSession查询的数据被缓存，下一次查询时会从缓存中拿取数据

### 二级缓存

需要手动开启（默认开启）

在xml文件中设置标签开启二级缓存

在SqlSession关闭或提交后有效

查询的数据转化的实体类必须实现序列化的接口

### 查询顺序

先查询二级缓存，二级缓存中有其他程序查询出的数据

再查询一级缓存

数据库

SqlSession关闭，一级缓存中的数据会写入二级缓存

## 第三方缓存EHCaChe

引入依赖

```
<dependency>  
    <groupId>org.mybatis.caches</groupId>  
    <artifactId>mybatis-ehcache</artifactId>  
    <version>1.2.1</version>  
</dependency>
<dependency>  
    <groupId>ch.qos.logback</groupId>  
    <artifactId>logback-classic</artifactId>  
    <version>1.4.14</version>  
</dependency>
```

配置文件

```
<?xml version="1.0" encoding="UTF-8"?>  
<ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://ehcache.org/ehcache.xsd">  
    <diskStore path="java.io.tmpdir"/>  
    <!-- defaultCache -->  
    <defaultCache  
            maxElementsInMemory="10000"  
            eternal="false"  
            timeToIdleSeconds="120"  
            timeToLiveSeconds="120"  
            maxElementsOnDisk="10000000"  
            diskExpiryThreadIntervalSeconds="120"  
            memoryStoreEvictionPolicy="LRU">  
        <persistence strategy="localTempSwap"/>  
    </defaultCache>    <!-- userEntityCache(有效期5min) -->  
    <cache name="userEntityCache" maxElementsInMemory="10" eternal="false"  
           timeToIdleSeconds="60"  
           timeToLiveSeconds="300"  
           overflowToDisk="true"  
           memoryStoreEvictionPolicy="LRU"/>  
</ehcache>
```

## 逆向工程

根据数据库表生成实体类，mapper接口，xml映射文件

配置文件

```
<build>  
  
    <!-- 构建过程中用到的插件 -->  
    <plugins>  
  
        <!-- 具体插件，逆向工程的操作是以构建过程中插件形式出现的 -->  
        <plugin>  
            <groupId>org.mybatis.generator</groupId>  
            <artifactId>mybatis-generator-maven-plugin</artifactId>  
            <version>1.3.0</version>  
  
            <!-- 插件的依赖 -->  
            <dependencies>  
  
                <!-- 逆向工程的核心依赖 -->  
                <dependency>  
                    <groupId>org.mybatis.generator</groupId>  
                    <artifactId>mybatis-generator-core</artifactId>  
                    <version>1.3.0</version>  
                </dependency>                <!--数据库连接池-->  
                <dependency>  
                    <groupId>com.mchange</groupId>  
                    <artifactId>c3p0</artifactId>  
                    <version>0.9.2</version>  
                </dependency>                <dependency>                    <groupId>org.mybatis</groupId>  
                    <artifactId>mybatis</artifactId>  
                    <version>3.5.7</version>  
                </dependency>  
  
  
                <!-- MySQL驱动 -->  
                <dependency>  
                    <groupId>mysql</groupId>  
                    <artifactId>mysql-connector-java</artifactId>  
                    <version>8.0.17</version>  
                </dependency>            </dependencies>        </plugin>    </plugins></build>
```

```
<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE generatorConfiguration  
        PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"  
        "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">  
<generatorConfiguration>  
    <!--  
            targetRuntime: 执行生成的逆向工程的版本  
                    MyBatis3Simple: 生成基本的CRUD（清新简洁版）  
                    MyBatis3: 生成带条件的CRUD（奢华尊享版）  
     -->  
    <context id="DB2Tables" targetRuntime="MyBatis3">  
        <!-- 数据库的连接信息 -->  
        <jdbcConnection driverClass="com.mysql.cj.jdbc.Driver"  
                        connectionURL="jdbc:mysql://localhost:3306/mybatis?serverTimezone=Asia/Shanghai"  
                        userId="root"  
                        password="qwer1234">  
            <property name="nullCatalogMeansCurrent" value="true"/>  
        </jdbcConnection>        <!-- javaBean的生成策略-->  
        <javaModelGenerator targetPackage="com.wsj.mybatis.pojo" targetProject=".\src\main\java">  
            <property name="enableSubPackages" value="true" />  
            <property name="trimStrings" value="true" />  
        </javaModelGenerator>        <!-- SQL映射文件的生成策略 -->  
        <sqlMapGenerator targetPackage="com.wsj.mybatis.mapper"  targetProject=".\src\main\resources">  
            <property name="enableSubPackages" value="true" />  
        </sqlMapGenerator>        <!-- Mapper接口的生成策略 -->  
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.wsj.mybatis.mapper"  targetProject=".\src\main\java">  
            <property name="enableSubPackages" value="true" />  
        </javaClientGenerator>        <!-- 逆向分析的表 -->  
        <!-- tableName设置为*号，可以对应所有表，此时不写domainObjectName -->  
        <!-- domainObjectName属性指定生成出来的实体类的类名 -->  
        <table tableName="user" domainObjectName="User"/>  
  
  
    </context></generatorConfiguration>
```