# Mysql

## 一、SQL

### 1.SQL语言的分类

    DQL：数据查询语言：select、from、where
    DML：数据操作语言：insert、update、delete
    DDL：数据定义语言：create、alter、drop、truncate
    DCL：数据控制语言：grant、revoke
    TCL：事务控制语言：commit、rollback
### 2.DDL

#### 2.1数据库操作

**查询**

所有数据库

```
SHOW DATABASES
```

当前数据库

```
SELECT DATABASES
```

**创建**

```
CREATE DATABASE 【IF NOT EXISTS】 库名 【 CHARACTER SET 字符集名】;
```

**删除**

```
DROP DATABASE 【IF EXISTS】 库名;
```

**使用**

```
USE 数据库名
```

#### 2.2 表操作

**查询**

查询当前数据库所有表

```
SHOW TABLES
```

查询表结构

```
DESC 表名
```

查询指定表的建表语句

```
SHOW CREATE TABLE 表名
```

**创建**

```
CREATE TABLE 【IF NOT EXISTS】 表名 (
  字段名 字段类型 【约束】,
  字段名 字段类型 【约束】,
  ...
  字段名 字段类型 【约束】
) ;
```

**数据类型**

数值型

一、类型
类型	TINYINT	SMALLINT	MEDIUMINT	INT/INTEGER	BIGINT
字节	1	                    2	                      3	                   4	              8 

二、特点

    都可以设置无符号和有符号，默认有符号，通过unsigned设置无符号
    如果超出了范围，会报out or range异常，插入临界值（该类型的最大值或最小值即为临界值）
    长度可以不指定，默认会有一个长度，长度代表显示的最大宽度，如果不够则左边用0填充，但需要搭配zerofill，并且默认变为无符号整型
    如果对数据没有特殊要求，则优先考虑使用INT/INTEGER

5.3.2、浮点型

一、类型

    定点数
        DEC(M,D) ：M+2字节
        DECIMAL(M,D)：M+2字节
    浮点数
        FLOAT(M,D) ：4字节
        DOUBLE(M,D)：8字节

二、特点

    M代表整数部位+小数部位的个数，D代表小数部位
    如果超出范围，则报out or range异常，并且插入临界值（该类型的最大值或最小值即为临界值）
    M和D都可以省略，但对于定点数，M默认为10，D默认为0
    如果精度要求较高，则优先考虑使用定点数

5.3.3、字符型

一、类型
类型	CHAR	               VARCHAR	          BINARY	    VARBINARY	ENUM   SET	TEXT	BLOB
描述	固定长度字符	可变长度字符	二进制字符串	二进制字符串	枚举	集合	文本	二进制大型对象

二、特点

    char：固定长度的字符，写法为char(M)，最大长度不能超过M，其中M可以省略，默认为1
    varchar：可变长度的字符，写法为varchar(M)，最大长度不能超过M，其中M不可以省略
    如果对数据没有特殊要求，则优先考虑使用VARCHAR

5.3.4、日期型

一、类型

类型	YEAR	DATE	TIME	DATETIME	TIMESTAMP
描述	年份	日期	时间	日期+时间	日期+时间

二、特点

    TIMESTAMP比较容易受时区、语法模式、版本的影响，更能反映当前时区的真实时间，而DATETIME则只能反映出插入时的当地时区
    TIMESTAMP支持的时间范围较小，DATETIME的取值范围：1000-1-1 — 9999-12-31
    TIMESTAMP的属性受Mysql版本和SQLMode的影响很大
    如果对数据没有特殊要求，则优先考虑使用DATETIME
**修改**

添加字段

```
alter table 表名 add 字段名 数据类型（长度） 约束
```

修改数据类型

```
alter table 表名 modify 字段名 新数据类型（长度）
```

修改字段名和字段类型

```
alter table 表名 change 旧字段名 新字段名 新数据类型（长度）
```

删除字段

```
ALTER TABLE 表名 DROP 字段名；
```

修改表名

```sql
ALTER TABLE 表名 RENAME 【TO】 新表名;
```

表的删除

```
方式一：DROP TABLE 【IF EXISTS】 表名;

方式二：TRUNCATE TABLE 【IF EXISTS】 表名;
```

### 3.DML

添加数据

```
INSERT INTO 表名(字段名,...) VALUES(值,...);
全部字段
INSERT INTO 表名 VALUES(值,...);
批量添加
INSERT INTO 表名(字段名,...) VALUES(值,...)(值,...)(值,...);
```

字段顺序与值顺序一一对应

字符串和日期数据包含在引号中

修改数据

```
update 表名 set 字段名1=值1，字段名2=值2，...[where 条件]
```

删除数据

```
DELETE FROM 表名 [WHERE 条件]
```

### 4.DQL

#### 基本查询

查询多个字段

```
SELECT 字段1，字段2，字段3.。 FROM 表名;
```

```
select * from 表名;
```

设置别名

```
 SELECT 字段名 AS "别名" FROM 表名;
```

去重

```
SELECT DISTINCT 字段名 FROM 表名;
```

####  条件查询

**语法**

```
SELECT 查询列表 FROM 表名 WHERE 筛选条件;
```

**条件**

1.条件运算符：>、>=、<、<=、=、<=>、!=、<>

2.逻辑运算符：and、or、not

3.模糊运算符：   

- like：%任意多个字符、_任意单个字符，如果有特殊字符，需要使用escape转义
- between and   在某个范围内（包含最大最小值）
- not between and
- in      在in之后列表中多选一
- is null
- is not null

#### 聚合函数

将一列数据作为整体进行纵向计算

常见聚合函数：

count       统计数量

max        最大

min          最小

avg          平均值

sum          求和

#### 分组查询

语法

```
SELECT 
  查询列表 
FROM
  表 
【where 筛选条件】 
GROUP BY 分组的字段 
【having 分组后的筛选】
【order BY 排序的字段】 ;
```

查询每个工种有奖金的员工的最高工资>6000的最高工资和公众编号，按最高工资升序

```
SELECT 
  MAX(salary) m,
  job_id
FROM
  employees 
WHERE commission_pct IS NOT NULL 
GROUP BY job_id 
HAVING m > 6000 
ORDER BY m ;

```

查询每个工种每个部门的最低工资并按最低工资降序

```
SELECT 
  MIN(salary),
  job_id,
  department_id 
FROM
  employees 
GROUP BY job_id, department_id
ORDER BY MIN(salary) DESC ;
```

#### 排序查询

```
SELECT 字段列表 FROM 表名 ORDER BY 字段1 排序方式1 ，字段2 排序方式2 ；
```

#### 分页查询

语法

```
SELECT 字段列表 FROM 表名 LIMIT 起始索引， 查询记录数
```

起始索引从0开始，起始索引=（查询页码-1）*每页显示记录数



#### 执行顺序

FROM 

WHERE

GROUP BY

HAVING

SELECT

ORDER BY

LIMIT

### 5. DCL

#### 查询用户

```
USE mysql;
SELECT * FROM user;
```

#### 创建用户

```
CREATE USER '用户名'@'主机名' identified by '密码';
注意：'IP地址'可以设置为localhost(代表本机)或者'%'(代表允许所有IP地址登录)
```

#### 修改用户密码

```
alter user '用户名'@'%' identified with mysql_native_password by '新密码';
```

#### 删除用户

```
DROP USER 用户名@'IP地址';
注意：'IP地址'可以设置为localhost(代表本机)或者'%'(代表允许所有IP地址登录)
```

#### 权限控制

1.查询权限

```
SHOW GRANTS FOR 用户名@'IP地址';
注意：'IP地址'可以设置为localhost(代表本机)或者'%'(代表允许所有IP地址登录)

```

2.授予权限

```
GRANT 权限1,权限2,...... ON 数据库名.* TO 用户名@'IP地址' IDENTIFIED BY '密码';
注意：所有的数据库就用*.*，所有的权限就用all或者all privileges
```

3.删除权限

```
REVOKE 权限1,权限2,...... ON 数据库名.* FROM 用户名@'IP地址' IDENTIFIED BY '密码';
注意：所有的数据库就用*.*，所有的权限就用all或者all privileges
```

## 二.函数

### 字符串函数

![](https://gitee.com/Wsj123789/wsj/raw/master/img/20250815200033611.jpg)

### 数值函数

![image-20250815200316967](https://gitee.com/Wsj123789/wsj/raw/master/img/20250815200317053.png)

### 日期函数

```
select curdate();

select curtime();

select now();

select YEAR(now());

select MONTH(now());

select DAY(now());

select date_add(now(),INTERVAL 70 MONTH);

-- 相差天数
select datediff('2021-12-02','2021-11-01');
```

### 流程函数

实现条件筛选，提高语句效率

　**1、IF(expr,v1,v2)函数**

　　如果表达式expr成立，返回结果v1；否则，返回结果v2。

```
SELECT IF(1 > 0,'正确','错误')    
->正确
```

**2、IFNULL(v1,v2)函数**

```
SELECT IFNULL(null,'Hello Word')
->Hello Word
```

**3、CASE**

```
CASE 
　　WHEN e1
　　THEN v1
　　WHEN e2
　　THEN e2
　　...
　　ELSE vn
END
```

　CASE表示函数开始，END表示函数结束。如果e1成立，则返回v1,如果e2成立，则返回v2，当全部不成立则返回vn，而当有一个成立之后，后面的就不执行了。



```
CASE expr 
　　WHEN e1 THEN v1
　　WHEN e1 THEN v1
　　...
　　ELSE vn
END
```

如果表达式expr的值等于e1，返回v1；如果等于e2,则返回e2。否则返回vn。

## 三. 约束

### 1、主键约束

1. 创建表时，此列名后设置主键，语法：

   ```
   列名 数据类型 PRIMARY KEY [默认值]
   ```

    举例：定义一个学生表
   
    CREATE TABLE student_info(
        stu_id INT PRIMARY KEY, -- 学生编号 主键
        stu_name VARCHAR(20) NOT NULL,-- 学生姓名
        age INT NOT NULL,-- 年龄
        stu_birthday DATE NOT NULL,-- 出生日期
        cid INT
    );

sql

    创建表时，在所有列名后单独设置主键
    
    [CONSTRAINT 约束名 ]   PRIMARY KEY(列名) 
    
    举例：定义一个学生表
    
    create table stu(
        id int,
        stu_name varchar(10),
        primary key (id)
    )

sql

    在创建表后，通过alter修改表结构，设置表的主键
    
    ALTER TABLE 表名 ADD CONSTRAINT 主键名称 PRIMARY KEY (列名);
### 2、自动增长

每次添加新记录时，希望可以自动的生成主键值，在默认情况下，在 MySQL 中AUTO_INCREMENT 的初始值是 1，每次新添加一条数据，字段值都会自动加 1，规则如下：

    一个表里只能有一个自增字段
    
    必须做为主键的一个部分(只有主键可以设置)，不得单独使用
    
    字段的数据类型必须为整数类型

语法：

列名 数据类型 AUTO_INCREMENT PRIMARY KEY

举例：定义数据表 Grade，将主键 id 设置为自动增长，并设置初始值为1001

    CREATE TABLE Grade(
        id INT(11) AUTO_INCREMENT PRIMARY KEY, -- 年级编号 主键
        GradeName VARCHAR(20), -- 年级名称
        Major VARCHAR(50) -- 所属专业
    )ENGINE=INNODB AUTO_INCREMENT=1001;

### 3、非空约束

字段的值不能为空。如果用户在添加数据时没有指定值，数据库系统将会报错。

语法：

```
列名  数据类型  not null
```

### 4、默认约束

默认约束指定某列的默认值。比如性别默认男，设置默认值后插入数据时若未赋值则其数据就为“男”。语法：

列名  数据类型   default  默认值

注意：

    默认值不能用于AUTO_INCREMENT列，TIMESTAMP列。
    
    如果对一个已经有数据的表添加默认约束，原来的数据不能得到默认值。

### 5、唯一约束

唯一约束可以确保一列或者多列不出现重复值。比如身份证号、手机号、都是唯一的。要求该列的值唯一，允许为空，但是只能出现一个空值。

```
列名   数据类型   UNIQUE
```

### 6、外键约束

其作用是在多张表的数据之间建立关系，确保多个表之间数据的一致性、完整性。一个表中可以有零到任意个外键。外键属于引用完整性，一个表的外键可以为空值，若不为空值，则每一个外键值必须等于另一个表中主键的某个值。定义为外键后，不允许删除在另一个表中具有关联关系的数据行。

```
#在创建表时，直接添加外键
[CONSTRAINT外键名]  FOREIGN KEY  （当前表的字段） REFERENCES  主表名  （主键列）
​
#在创建表后，通过alter添加外键
alter table 表名 add constrant 外键名称 FOREIGN key(外键字段名) REFERENCES 主表名(主键列);
​
#查看创建表语句，
show create table employer;
#删除外键
alter table 表名 drop FOREIGN key 外键名;
```

RESTRICT： 受限制 (如果对应部门下有员工 不允许删除部门)

CASCADE： 级联操作 （删除部门的同时删除对应员工）

set null： 设置为空 (删除部门的同时，将员工中对应的部门id设置为null)

NO ACTION ：无影响

语法：添加外键语句后 on update 选项 on delete 选项

## 四. 多表查询

多表关系

在进行数据库表结构的设计时，会根据业务的需求和业务模块之间的关系，分析设计表结构，由于业务之间相互关联，所以各个表结构之间也存在各种联系
表与表之间的联系：

1.一对多(多对一)
2.多对多
3.一对一
一对多(多对一)

例如，一个员工对应一个部门，一个部门可以对应多个员工
![image-20250816202116402](https://gitee.com/Wsj123789/wsj/raw/master/img/20250816202116504.png)

**一般在多的一方创建外键，指向一的那一方**
 员工与部门，在员工表上设置外键，指向部门表

```
-- 添加外键约束（emp表的dept_id--->dept的主键id）
alter table emp add constraint fk_emp_dept_id foreign key (dept_id) references dept(id)
```

#### 多对多

例如，一个学生可以选修多门课程，一个课程可以被多名学生选修
 **一般会建立第三张表，至少包含两个外键，分别指向两张表的主键**

![image-20250816202159316](https://gitee.com/Wsj123789/wsj/raw/master/img/20250816202159399.png)

#### 一对一

例如，用户和自己的学历信息的关系，一个人只对应一条学历信息
 **可以在任意一方加入外键，关联另一方的主键，并且设置外键为唯一(unique)**

![image-20250816202214572](https://gitee.com/Wsj123789/wsj/raw/master/img/20250816202214653.png)

**注：可以放在一张表中，但是对其进行拆分，一张表放基础信息，另一张表放详情，可以提升操作效率**

### 多表查询

**概述：**
 从多张表中查询数据
 **笛卡尔积：**
 笛卡尔积为两个集合(两张表)中的每条数据进行两两组合的结果
 **在多表查询时会产生笛卡尔积，要通过添加条件消除笛卡尔积**

```
select * from emp, dept where emp.dept_id=dept.id;
```

### [内连接](https://so.csdn.net/so/search?q=内连接&spm=1001.2101.3001.7020)

语法：

```sql
# 隐式内连接
select 字段列表 from 表1,表2 where 条件;
# 显示内连接
select 字段列表 from 表1 [inner] join 表2 on 连接条件;
```

**内连接查询的是两张表交集的部分**

```sql
# 查询每一个员工的姓名及关联的部门的名称
select emp.name, dept.name from emp, dept where emp.dept_id=dept.id;
select emp.name, dept.name from emp inner join dept on emp.dept_id = dept.id;
```

### 外连接

语法：

```sql
# 左外连接
select 字段列表 from 表1 left [outer] join 表2 on 条件;
# 右外连接
select 字段列表 from 表1 right [outer] join 表2 on 条件;
sql
1234
```

左外连接相当于查询表1的所有数据包含表1和表2交集的部分数据
 右外连接相当于查询表2的所有数据包含表1和表2交集部分的数据

```sql
# 查询emp表的所有数据，和应于的部门信息(左)
select emp.*, dept.* from emp left outer join dept on emp.dept_id = dept.id;
# 查询dept表的所有数据，和对于的员工信息(右)
select dept.*, emp.* from emp right outer join dept on emp.dept_id = dept.id;

```

左外连接和右外连接可以进行相互转化

### 自连接

语法：

```sql
select 字段列表 from 表a 别名a join 表a 别名b on 条件;

```

自链接查询可以是内连接查询也可以是外连接查询

```sql
# 查询员工及其所属领导的名字
# 自连接可以看成两张一样的表进行连接查询
select a.name, b.name from emp a join emp b on a.managerid=b.id;
```

### 联合查询

**union、union all**
 对于联合查询就是把多次查询的结果合并起来，形成一个新的查询结果集
 语法：

```sql
select 字段列表 from 表a
union [all]
select 字段列表 from 表b

# 将薪资低于5000的员工和年龄大于50的员工查询出来
select * from emp where salary>5000
union all
select * from emp where age>50;

# 没有all重复满足条件的只出现一次
# 将薪资低于5000的员工和年龄大于50的员工查询出来
select * from emp where salary>5000
union
select * from emp where age>50;

```

对于联合查询的多张表的列数必须保持一致，字段类型也要保持一致
 union all会将全部的数据直接合并在一起，union会对合并之后的数据去重

### 子查询

#### 子查询

概念：SQL语句中嵌套select语句为嵌套查询，又称子查询
select * from 表1 where 字段=(select 字段 from 表2);
子查询外的语句可以是insert、update、delete、select中的一个
根据子查询的结构不同，分为：

标量子查询：子查询的结果为单个值
列子查询：子查询的结果为一列
行子查询：子查询的结果为一行
表子查询：子查询的结果为多行多列

根据子查询的位置，分为：

where之后
from之后
select之后

#### 标量子查询

子查询返回的结果是单个值(数字、字符串、日期等)，最简单的形式，这种子查询称为标量子查询
常用符号：=、<>、>、>=、<、<=

```
# 根据销售部门的id查询员工信息
# 先分开查询
# 查询销售部门的id
select id from dept where name='销售部'; #id为4
# 查询销售部门中员工的信息
select * from emp where dept_id=4;
# 合并为一个查询
select * from emp where dept_id=(select dept.id from dept where dept.name='销售部' );
```

#### 列子查询

子查询的结果为一列(可以是多行)的，这种子查询为列子查询
 常用操作符：

![image-20250817191811906](https://gitee.com/Wsj123789/wsj/raw/master/img/20250817191811993.png)

```
# 列子查询
# 查询销售部和市场部的所有员工信息
# 查询销售部和市场部的id
select id from dept where name='销售部' or name='市场部'; #id为2 4
# 查询两个部门的所有员工
select * from emp where dept_id in (2,4);
# 合并
select * from emp where dept_id in (select id from dept where name='销售部' or name='市场部');
```

#### 行子查询

子查询返回的结果是一行(可以是多列)，这种子查询为行子查询
 常用操作符：=、<>、in、not in

```
# 查询与张无忌的薪资及直属领导相同的员工信息
# 查询张无忌的薪资和直属领导
select salary, managerid from emp where name='张无忌';
# 查询与张无忌的薪资及直属领导相同的员工信息
select * from emp where (salary,managerid)=(select salary, managerid from emp where name='张无忌');
```

## 五.事务

 默认情况下，每一条SQL语句都是一个事务。这条SQL语句一旦执行完成，事务就会自动提交，也就是说，当执行完一条DML语句时，MySQL会立即隐式的提交事务。

        事务一旦提交，表格就会有对应的变化。
    
        如果有一件事，例如上面的转账操作，必须三个步骤同时完成才可以，此时就需要将几条SQL语句作为一个事务，保证它们同时成功或同时失败不影响原来的数据。
    
        所以此时我们就要对事务进行控制，将几条SQL语句组合为一个事务。如果成功，就统一提交，如果失败，则避免影响数据库的内容。
### 控制事务一

1、查看/设置事务提交方式

    -- 查看事务的提交方式
    
    select @@autocommit ;
    
    -- 如果赋值为1，就是自动提交事务；
    
    -- 如果赋值为0，就是手动提交事务；
    
    -- MySQL中默认自动提交事务，所以要设置为手动。
    
    set @@autocommit = 0 ;

2、提交事务

    -- 手动提交的情况下，要执行了commit，事务才会提交，数据库中内容才会发生改变。
    
    commit ;

3、回滚事务

    -- 执行过程中，如果发生了异常，就去执行rollback回滚，撤回该事务内已执行的操作。
    
    rollback ;

注意事项：

 ① 上述的这种方式，我们是修改了事务的自动提交行为，把默认的自动提交修改为了手动提

交，此时我们执行的DML语句都不会提交，需要手动的执行commit进行提交。

② 如果业务操作正常完成，事务需要提交，就执行commit指令；如果执行事务操作的过程中出现了异常，那就执行rollback指令回滚事务，保证数据库中数据的正确性与完整性。

> -- 手动开启事务，而不是修改事务的提交方式
>
> **start transaction ; 或** **begin ;**

### 事务的四大特性

1、原子性（Atomicity）

        事务是不可分割的最小操作单元，要么全部成功，要么全部失败。

2、一致性（Consistency）

        事务完成时，必须使所有的数据都保持一致状态。

3、隔离性（Isolation）

        数据库系统提供的隔离机制，保证事务在不受外部并发操作影响的独立环境下运行。
    
        就如下图的上半部分，事务AB并发执行，但是不会相互影响。事务A在操作的时候，不会影响并发的事务B的执行；事务B在操作的时候，也不会影响并发的事务A的执行；它们两个是在独立的环境下运行的。

4、持久性（Durability）

        事务一旦提交或回滚，它对数据库中的数据的改变就是永久的。
    
        就如下图的下半部分，因为数据库当中的数据最后是存储在了磁盘当中的，而存储在磁盘当中的数据，就可以永久地保留下来。
### **并发事务问题**

​    并发事务问题是事务A和事务B在**同时操作某一个数据库甚至一张表时，引发的问题。**

**1、赃读：**一个事务读到另外一个事务**还没有提交的数据**。

![image-20250818180511672](https://gitee.com/Wsj123789/wsj/raw/master/img/20250818180511741.png)

 比如，在事务A执行了 select 与 update 语句后，并未提交；但是在事务B中执行 select 语句后，却查询到了事务A未提交的数据。

2**、不可重复读：**一个事务先后读取同一条记录，**但两次读取的数据不同，称之为不可重复读**。

![image-20250818180546385](https://gitee.com/Wsj123789/wsj/raw/master/img/20250818180546447.png)

比如，在事务A两次读取同一条记录，却**因为期间事务B中 id=1 的数据被更新且提交**，**导致读取到的数据却是不一样的。**

**3、幻读：**一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了 "幻影"。

![image-20250818180621597](https://gitee.com/Wsj123789/wsj/raw/master/img/20250818180621657.png)

比如，在事务A中第一次查询，**没有查询到信息**；然后事务B中**插入并提交了id =1的数据**；此时在事务A中插入 id = 1 的数据**无法插入**，因为 id 是主键，id =1的数据在事务B中就已经插入；但是在事务A中再查询一次后，又无法查询得到。

### **事务隔离级别**

##### **1、事务隔离级别的介绍**    

​    为了**解决并发事务所引发的问题**，在数据库中引入了事务隔离级别。主要有以下几种：

![image-20250818183031889](https://gitee.com/Wsj123789/wsj/raw/master/img/20250818183031960.png)

   Repeatable Read是MySQL的默认事务隔离级别。

        事务隔离级别越高，数据越安全，但是性能越低；反之事务隔离级别越低，性能越高，但是数据越不安全。所以我们要权衡数据的安全性以及数据库的并发性能。
    
        其中，串行化指的是再进行并发事务操作的时候，一次只允许操作一个事务。
    
        事务A在操作的时候，只有当事务A提交完成之后，事务B才能来操作。
    
        就比如上面幻读的例子中，如果是在串行化的情况下，因为事务A是在事务B之前执行，所以事务A执行完成之前，事务B根本无法执行下去。
    
        事务B执行insert语句在执行后，光标会一直卡着，直到事务A执行完毕后，事务B才会执行，这样就可以避免幻读。
2、操作事务隔离级别的语法

（1）查看事务隔离级别

    select @@transaction_isolation

（2）设置事务隔离级别

    -- session与global二选一
    
    -- session 是指当前设置的事务隔离级别 仅对当前对话窗口有效
    
    -- global 是指当前设置的事务隔离级别 对所有对话窗口有效
    
    -- 后面的四个事务隔离级别四选一即可
    
    set { session | global } transaction isolation level { Read Uncommitted | Read committed | Repeatable Read | Serializable}


## 相关条目
- [[进阶]]
- [[InnoDB引擎]]
- [[管理数据库]]
- [[Mybatis-plus]]
- [[苍穹]]
