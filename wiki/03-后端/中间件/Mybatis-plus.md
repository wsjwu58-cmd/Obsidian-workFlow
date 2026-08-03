[简介 | MyBatis-Plus](https://mybatis.plus/guide/)官方文档

[day01-MybatisPlus - 飞书云文档](https://ai.feishu.cn/wiki/PsyawI04ei2FQykqfcPcmd7Dnsc)

## 基本步骤

引入依赖

```
<dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.4.2</version>
        </dependency>
```



在mapper接口处继承BaseMapper并指定操作的实体类

```
public interface UserMapper extends BaseMapper<?>
```

## 常用注解

基本原理：Mybatis-plus通过反射获取实体类的字节码文件，获取相应的属性

约定：

类名驼峰转下划线为表名

属性名驼峰转下划线作为字段名

属性为id自动设置为主键



@TableName:指定表名和数据库的映射

@TableId:主键映射

@TableField:属性和字段名的映射

## 核心功能

### 条件构造器

- **AbstractWrapper**：这是一个抽象基类，提供了所有 Wrapper 类共有的方法和属性。它定义了条件构造的基本逻辑，包括字段（column）、值（value）、操作符（condition）等。所有的 QueryWrapper、UpdateWrapper、LambdaQueryWrapper 和 LambdaUpdateWrapper 都继承自 AbstractWrapper。
- **QueryWrapper**：专门用于构造查询条件，支持基本的等于、不等于、大于、小于等各种常见操作。它允许你以链式调用的方式添加多个查询条件，并且可以组合使用 `and` 和 `or` 逻辑。
- **UpdateWrapper**：用于构造更新条件，可以在更新数据时指定条件。与 QueryWrapper 类似，它也支持链式调用和逻辑组合。使用 UpdateWrapper 可以在不创建实体对象的情况下，直接设置更新字段和条件。
- **LambdaQueryWrapper**：这是一个基于 Lambda 表达式的查询条件构造器，它通过 Lambda 表达式来引用实体类的属性，从而避免了硬编码字段名。这种方式提高了代码的可读性和可维护性，尤其是在字段名可能发生变化的情况下。
- **LambdaUpdateWrapper**：类似于 LambdaQueryWrapper，LambdaUpdateWrapper 是基于 Lambda 表达式的更新条件构造器。它允许你使用 Lambda 表达式来指定更新字段和条件，同样避免了硬编码字段名的问题。

QueryWrapper

```
void UpdateUser(){
        User user = new User();
        user.setBalance(2000);
        QueryWrapper<User> queryWrapper = new QueryWrapper<User>().eq("username","jack");
        userMapper.update(user,queryWrapper);
    }
```

```
void LambdaUser(){
    LambdaQueryWrapper<User> lambdaQueryWrapper=new LambdaQueryWrapper<User>().select(User::getId,User::getBalance,User::getPassword).like(User::getUsername,"o").ge(User::getBalance,1000);
    List<User> list=userMapper.selectList(lambdaQueryWrapper);
    for (User user:list){
        System.out.println("user = " + user);
    }
}
```

### 链式调用与Lambda式调用

无需Warpper,直接进行sql操作并返回结果

```
// 普通链式调用
UpdateChainWrapper<T> update();
// Lambda式链式调用（不支持Kotlin）
LambdaUpdateChainWrapper<T> lambdaUpdate();

// 等价示例：
query().eq("id", value).one();
lambdaQuery().eq(Entity::getId, value).one();

// 等价示例：
update().eq("id", value).remove();
lambdaUpdate().eq(Entity::getId, value).remove();
```



### 自定义SQL

创建自定义方法

```
void updateBalance(@Param(Constants.WRAPPER) QueryWrapper<User> queryWrapper,@Param("amount") int amount);
```

在xml中使用自定义方法

```
<update id="updateBalance">
    UPDATE tb_user
    SET balance =balance-#{amount} ${ew.customSqlSegment}
</update>
```

编写具体逻辑

```
void Sqlcustom(){
    List<Long> ids= List.of(1L,3L,4L);
    int amount=2000;
    QueryWrapper<User> queryWrapper=new QueryWrapper<User>().in("id",ids);
    //调用自定义方法
    userMapper.updateBalance(queryWrapper,amount);
}
```

### Service 接口

接口继承 IService<T>

实现类实现该接口,并继承实现该接口的实现类ServiceImpl<（Mapper接口）,实体类>

## DTO/VO分离模式

DTO (Data Transfer Object): 数据传输对象，主要用于在不同层之间传输数据
VO (Value Object): 值对象，主要用于向前端展示数据
分离的好处
安全性
DTO可以包含敏感字段如password
VO过滤掉敏感信息，只暴露需要展示的数据
职责清晰
UserFormDTO专门处理表单输入数据
UserVO专门处理数据展示输出
灵活性
同一实体可以对应多个不同的DTO/VO
适应不同的业务场景和接口需求
维护性
修改一方不会影响另一方
降低代码耦合度

DTO

```
@Data
@ApiModel(description = "用户表单实体")
public class UserFormDTO {

    @ApiModelProperty("id")
    private Long id;

    @ApiModelProperty("用户名")
    private String username;

    @ApiModelProperty("密码")
    private String password;

    @ApiModelProperty("注册手机号")
    private String phone;

    @ApiModelProperty("详细信息，JSON风格")
    private String info;

    @ApiModelProperty("账户余额")
    private Integer balance;
}
```

VO

```
@Data
@ApiModel(description = "用户VO实体")
public class UserVO {

    @ApiModelProperty("用户id")
    private Long id;

    @ApiModelProperty("用户名")
    private String username;

    @ApiModelProperty("详细信息")
    private String info;

    @ApiModelProperty("使用状态（1正常 2冻结）")
    private Integer status;

    @ApiModelProperty("账户余额")
    private Integer balance;
}
```



## DB静态工具

提供了很多和service接口相似的方法，还包括链式调用

```
public UserVO AddressID(Long id) {
        //查询用户
        User user = getById(id);
        //判断异常
        if (user == null) {
            throw new RuntimeException("用户不存在");
        }
        //查询地址
        List<Address> address = Db.lambdaQuery(Address.class).
                eq(Address::getUserId, id).list();
        UserVO userVO = BeanUtil.copyProperties(user, UserVO.class);
        if (address != null) {
            userVO.setAddress(BeanUtil.copyToList((Collection<?>) address, AddressVO.class));
        }
        return userVO;
    }
```

## 逻辑删除

通过一个标记来记录是否删除数据，0为删除，1为保留

查询时只查询标记为1的数据

配置

```
global-config:
    db-config:
#      逻辑删除的字段名: deleted
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
```

## 枚举处理器





## 分页插件

在配置类中添加相应组件

```
@Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL)); // 如果配置多个插件, 切记分页最后添加
        // 如果有多数据源可以不配具体类型, 否则都建议配上具体的 DbType
        return interceptor;
    }
```

```
 @Test
    void testPageQuery() {
        //分页条件

        int pageNum = 1 , pageSize = 2;
        Page<User> userPage=Page.of(pageNum,pageSize);
        //排序条件
        userPage.addOrder( OrderItem.asc("balance"));
        userPage.addOrder( OrderItem.asc("id"));

        //分页查询
        Page<User> p=userService.page(userPage);

        long total=p.getTotal();
        System.out.println("总记录数："+total);
        List<User> records=p.getRecords();
        for (User record : records) {
            System.out.println(record);
        }
    }
```

分页功能实现

```
@Override
public PageDTO<UserVO> queryUsersPage(UserQuery userQuery) {
    String name=userQuery.getName();
    Integer status=userQuery.getStatus();

    //构建查询条件
    //分页条件
    Page<User> page=Page.of(userQuery.getPageNum(),userQuery.getPageSize());
    // 排序条件
    if(StrUtil.isNotEmpty(userQuery.getOrderBy())){
        page.addOrder(OrderItem.asc(userQuery.getOrderBy()));
    }else{
        page.addOrder(OrderItem.desc("update_time"));
    }
   Page<User> p=  lambdaQuery().like(name != null, User::getUsername, name).
            eq(status != null, User::getStatus, status).
            page(page);

    //封装结果
    PageDTO<UserVO> pageDTO=new PageDTO<>();
    pageDTO.setTotal(p.getTotal());
    pageDTO.setPages(p.getPages());

    List<User> list=p.getRecords();
    if(CollUtil.isEmpty(list)){
        pageDTO.setList(Collections.emptyList());
        return pageDTO;
    }
   List<UserVO> voList= BeanUtil.copyToList(list,UserVO.class);
    pageDTO.setList(voList);
    return pageDTO;
}
```

由于分页时在service层写的代码和业务关系不大，所有我们可以把他们封装的实体类中

在接收分页数据的实体类中

```
public <T> Page<T> ToPage(OrderItem ...  items){
    Page<T> page=Page.of(pageNum,pageSize);
    if(StrUtil.isNotEmpty(orderBy)){
        page.addOrder( order? OrderItem.asc(orderBy):OrderItem.desc(orderBy));
    }else if(items!=null){
        page.addOrder(items);
    }
    return page;

}
public <T> Page<T> ToPageDefaultSortByCreateTime(String defaultSortBy){
    return  ToPage(OrderItem.desc(defaultSortBy));
}
```

可变参数是Java中的一种语法特性，允许方法接收**不定数量**的同类型参数。

在封装数据的实体类中

```
public  static <PO,VO> PageDTO<VO> of(Page<PO> p,Class<VO> clazz){
   PageDTO<VO> pageDTO=new PageDTO<>();
    pageDTO.setTotal( p.getTotal());
    pageDTO.setPages(p.getPages());
    //当前页数据
    List<PO> list=p.getRecords();
    if(CollUtil.isEmpty( list)){
         pageDTO.setList(CollUtil.newArrayList());
         return pageDTO;
    }
    pageDTO.setList(BeanUtil.copyToList(list,clazz));
    return pageDTO;
}
public static <PO,VO> PageDTO<VO> of(Page<PO> p, Function <PO,VO> convert){
    PageDTO<VO> pageDTO=new PageDTO<>();
    pageDTO.setTotal( p.getTotal());
    pageDTO.setPages(p.getPages());
    //当前页数据
    List<PO> list=p.getRecords();
    if(CollUtil.isEmpty( list)){
        pageDTO.setList(CollUtil.newArrayList());
        return pageDTO;
    }
    List<VO> voList=list.stream().map(convert).toList();
    pageDTO.setList(voList);
    return pageDTO;
}
```

传入转化的类型，或者自己定义转化的类型


## 相关条目
- [[案例]]
- [[Mysql]]
