## Redis启动



```
redis-server.exe  redis.windows.conf
```



```
redis-cli
```



设置开机自启

```
redis-server.exe --service-install redis.windows.conf --loglevel verbose
```



卸载

```
redis-server --service-uninstall
```





## 常见数据类型

存储Key-value类型的数据

- **string（字符串）:** 基本的数据存储单元，可以存储字符串、整数或者浮点数。
- **hash（哈希）:**一个键值对集合，可以存储多个字段。
- **list（列表）:**一个简单的列表，可以存储一系列的字符串元素。
- **set（集合）:**一个无序集合，可以存储不重复的字符串元素。
- **zset(sorted set：有序集合):** 类似于集合，但是每个元素都有一个分数（score）与之关联。
- **位图（Bitmaps）：**基于字符串类型，可以对每个位进行操作。
- **超日志（HyperLogLogs）：**用于基数统计，可以估算集合中的唯一元素数量。
- **地理空间（Geospatial）：**用于存储地理位置信息。
- **发布/订阅（Pub/Sub）：**一种消息通信模式，允许客户端订阅消息通道，并接收发布到该通道的消息。
- **流（Streams）：**用于消息队列和日志存储，支持消息的持久化和时间排序。
- **模块（Modules）：**Redis 支持动态加载模块，可以扩展 Redis 的功能。

### 常用命令

#### 字符串命令

![image-20251205133106054](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209212116257.png)

#### 哈希命令

![image-20251205133501101](https://gitee.com/Wsj123789/wsj/raw/master/img/20260202102054489.png)

#### 列表命令

Redis列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）

![image-20251205182707279](https://gitee.com/Wsj123789/wsj/raw/master/img/20251205182712003.png)

#### 集合命令

Redis 的 Set 是 String 类型的无序集合。集合成员是唯一的，这就意味着集合中不能出现重复的数据

![image-20251205182804498](https://gitee.com/Wsj123789/wsj/raw/master/img/20251205182806070.png)

#### 有序集合

Redis 有序集合和集合一样也是 string 类型元素的集合,且不允许重复的成员。

不同的是每个元素都会关联一个 double 类型的分数。redis 正是通过分数来为集合中的成员进行从小到大的排序。

有序集合的成员是唯一的,但分数(score)却可以重复。

![image-20251205182901482](https://gitee.com/Wsj123789/wsj/raw/master/img/20251205182912038.png)

## java中配置

导入Maven坐标

```
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
```

配置Redis数据源

```
  redis:
    host: ${sky.redis.host}
    port:  ${sky.redis.port}
    password: ${sky.redis.password} 
    database: ${sky.redis.database} 
```

创建配置类

```
 @Bean
    public RedisTemplate redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        log.info("开始创建redisTemplate对象....");
        RedisTemplate redisTemplate=new RedisTemplate();
        //配置连接工厂
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        //设置redis,key序列化器
        redisTemplate.setKeySerializer(new StringRedisSerializer());
        return redisTemplate;
        }
```

## Java客户端RedisTemplate

如果使用SpringDate中的RedisTemplate,设置键值的时候会将其序列化为16进制的格式，不方便我们阅读和查看

```
\xac\xed\x00\x05t\x00\x04name
```

所以我们可以自行配置RedisTemplate的序列化方式，使之序列化为JSON格式字符串

```
@Configuration
public class redisconfig {
    @Bean
    public RedisTemplate<String,Object> redisTemplate(RedisConnectionFactory connectionFactory){
        //创建RedisTemplate对象
        RedisTemplate<String,Object> redisTemplate = new RedisTemplate<>();
        //设置连接工厂
        redisTemplate.setConnectionFactory(connectionFactory);
        //创建JSON序列化工具
        GenericJackson2JsonRedisSerializer jsonRedisSerializer=new GenericJackson2JsonRedisSerializer();
        //设置KEY的序列化
        redisTemplate.setKeySerializer(RedisSerializer.string());
        redisTemplate.setHashKeySerializer(RedisSerializer.string());
        //设置VALUE的序列化
        redisTemplate.setValueSerializer(jsonRedisSerializer);
        redisTemplate.setHashValueSerializer(jsonRedisSerializer);
        //返回
        return redisTemplate;
    }
}
```

### StringRedisTemplate

由于自行配置的RedisTemplate会将实体类型也写入Redis中，会占用额外的内存，所以我们最好使用StringRedisTemplate

但是我们需要进行手动序列化

```
private static final ObjectMapper mapper=new ObjectMapper();
    @Test
    void test1() throws JsonProcessingException {
        User user=new User("name",18);
        //手动序列化
        String json=mapper.writeValueAsString(user);
        stringRedisTemplate.opsForValue().set("user:29",json);
        //获取数据
        String json1=stringRedisTemplate.opsForValue().get("user:29");
        User user1=mapper.readValue(json1,User.class);
        System.out.println(user1);
    }
```

## Redis实现共享session登录

### 集群的session的共享问题

多台Tomcat服务器并不共享session的数据，会造成数据丢失的问题

session代替方案：

- 数据共享
- 内存存储
- key,value的结构

### 使用redis存储登录数据

流程：用户输入手机号，发起请求发送验证码，输入验证码登陆，发起登录请求，数据库查询手机号，如果查询到就保存用户到redis，随机生成token作为key，如果没有查询到就在数据库中插入新用户，并将新用户保存到redis中，key为token，随后返回token，以后访问时都i会携带token，拦截器拦截到token以后查询redis设置ThreadLocal

注意：返回的token不能使用手机号，是因为token会作为请求头的一部分，传递中会有泄露的风险



在存储用户数据的时候，应该使用hash存储（占用内存小），但如果直接将数据转换为map集合会出现问题，由于StringRedisTemplate只允许键值类型都为String，如果实体类中有属性不为String，会执行错误，所以我们需要对Map集合中的值进行处理

```
//根据手机号查新用户
        User user=userMapper.selectByPhone(loginForm.getPhone());

        if(user==null){
            user=createUserWithPhone(loginForm.getPhone());
        }
        //随机生成令牌
        String token = UUID.randomUUID().toString();
        //转为DTO,map
        UserDTO newUser=BeanUtil.copyProperties(user, UserDTO.class);
        Map<String, Object> userMap = BeanUtil.beanToMap(newUser,new HashMap<>(),
                CopyOptions.create().setIgnoreNullValue(true).setFieldValueEditor((fieldName,filedValue)->filedValue.toString()));
        //存储
        redisTemplate.opsForHash().putAll(RedisConstants.LOGIN_USER_KEY+token,userMap);
        //设置token有效期
        redisTemplate.expire(RedisConstants.LOGIN_USER_KEY+token,30,TimeUnit.MINUTES);
        return Result.ok(token);
```

存储完之后通过拦截器进行token拦截，并重新设置token时间（切换页面时重置token时间）

但是该拦截器只拦截了特定请求，一些与登录无关的功能页面的请求无法延长token时间

解决：

再设置一个拦截器比原来拦截器先执行，用来刷新时间，原来的拦截器只需判断线程中是否存在用户信息

## 缓存更新策略

### 主动更新操作

删除缓存：先删除缓存再操作数据库，查询时再更新数据库

线程安全问题：更新数据库的逻辑比较复杂，如果不设置锁，其他线程进行查询数据库时查到了未更新的数据并写入缓存，导致数据库和缓存不一致问题

先操作数据库，再删除缓存

线程安全问题：线程一查询缓存未命中，查询数据库，在这时线程二进行数据库更新操作，更新之后线程一插入旧数据缓存（发生几率较小，可以为缓存设置过期时间解决）

## 缓存穿透

客户端请求的数据在redis和数据库中都不存在，这些请求都会打到数据库。

解决方案：

缓存空对象：

将空对象ID设置为key，value设置为空放到redis中

```
优点：实现简单，维护方便
缺点：可能造成短期的不一致（缓存后向数据库插入了数据）
```

布隆过滤器

优点：内存占用小，没有多余key

缺点：实现复杂，存在误判可能（判断存在时不一定真的存在）

增加ID复杂度

做好数据的基础格式校验

加强用户权限校验

做好热点参数的限流

```
//判断是否是空值
        if(shopJason!=null){
            return Result.fail("店铺信息不存在");
        }
        Shop shop=shopMapper.selectById(id);
        //存在，写入redis
        //不存在，通过id查询数据库
        if(shop==null){
            stringRedisTemplate.opsForValue().set(key,"",RedisConstants.CACHE_NULL_TTL,TimeUnit.MINUTES);
            return Result.fail("店铺不存在");
        }
```

## 缓存雪崩

同一时段大量的key同时失效或者Redis服务宕机，导致大量的请求到达数据库，导致巨大压力

解决方案：

给不同的key设置随机TTL

利用Redis集群提高服务的可用性

给业务增加多级缓存

给缓存业务添加降级限流策略

## 缓存击穿

用户高并发地对某个已经失效的 Redis key 进行请求，从而导致 MySQL 的压力剧增而系统宕机的情况。

### 加互斥锁

在线程1查询缓存判断是否存在，存在则直接返回，再判断是否是空值，如果不是（空字符串）则返回null

如果缓存中不存在，加互斥锁，查询数据库数据并写入缓存，解开互斥锁

其他线程没有拿到互斥锁会进行休眠，然后重新查询缓存，拿互斥锁

```
优点：保持一致性
没有额外内存消耗
缺点：线程需要等待。性能被影响
可能由死锁风险
```



### 逻辑删除

给缓存设置永不过期，增加一个过期字段（当前时间加过期时间）

如果缓存不存在，直接返回null

在线程1查询缓存发现逻辑时间过期时，会获取互斥锁，开启一个新线程，对数据库进行查询并写入缓存，重置逻辑时间，释放锁

线程1返回旧数据，其他线程发现互斥锁被占用后也会返回旧数据

```
优点：线程无需等待，性能好
缺点：不保证一致性；
     内存额外消耗
     实现复杂
```

### 思考

在进行缓存更新操作时，会删除掉缓存，而如果这时使用逻辑删除的方法查询更新后的数据，那么就会因为缓存为空而返回null

所以逻辑删除一般用于热点key的查询，一般不会对数据库进行更新，所以更新时直接操作数据库就行

### 工具类

```
@Slf4j
@Component
public class CacheClient {
    private final StringRedisTemplate stringRedisTemplate;

    public CacheClient(StringRedisTemplate stringRedisTemplate){
        this.stringRedisTemplate=stringRedisTemplate;
    }
    public void set(String key, Object value, Long time, TimeUnit unit){
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(value),time,unit);
    }
    public void setWithLogicalExpire(String key, Object value, Long time, TimeUnit unit){
        RedisData redisData=new RedisData();
        redisData.setData(value);
        redisData.setExpireTime(LocalDateTime.now().plusSeconds(unit.toSeconds(time)));
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(redisData));
    }
    public <R,ID> R queryWithThrough(String keyPrefix, ID id, Class<R> type, Function<ID,R> dbFailback,Long time, TimeUnit unit){
        String key=keyPrefix + id;
        //从redis查询缓存
        String shopJason = stringRedisTemplate.opsForValue().get(key);
        //判断是否存在
        if(StrUtil.isNotBlank(shopJason)){

            //存在直接返回
           return JSONUtil.toBean(shopJason,type);
        }
        //判断是否是空值
        if(shopJason!=null){
            return null;
        }
        R r=dbFailback.apply(id);
        //不存在，通过id查询数据库
        if(r==null){
            stringRedisTemplate.opsForValue().set(key,"",RedisConstants.CACHE_NULL_TTL,TimeUnit.MINUTES);
            return null;
        }
        //存在，写入redis
        this.set(key,r,time,unit);
        return r;
    }
    //逻辑删除
    public <R,ID> R queryWithLogicalExpire(String keyPrefix,ID id,Class<R> type, Function<ID,R> dbFailback,Long time, TimeUnit unit){
        String key=keyPrefix + id;
        //从redis查询缓存
        String shopJason = stringRedisTemplate.opsForValue().get(key);
        //判断是否存在
        if(StrUtil.isBlank(shopJason)){
            //不存在直接返回
            return null;
        }
        //命中，需要把json反序列化为对象
        RedisData redisData=JSONUtil.toBean(shopJason,RedisData.class);
        R r=JSONUtil.toBean((JSONObject) redisData.getData(),type);
        LocalDateTime expireTime=redisData.getExpireTime();
        //判断是否过期
        if(expireTime.isAfter(LocalDateTime.now())){
            //没过期直接返回数据
            return r;
        }
        //已过期，需要缓存重建
        //获取互斥锁
        String lockKey=RedisConstants.LOCK_SHOP_KEY+id;
        //判断是否获取锁成功
        if(tryLock(lockKey)){
            //成功。建立线程实现缓存重建
            CACHE_REBUILD_EXECUTOR.submit(()->{
                try {
                    R newr=dbFailback.apply(id);
                    this.setWithLogicalExpire(key,newr,time,unit);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }finally {
                    //释放锁
                    deleteLock(lockKey);
                }
            });
        }
        return r;
    }

    private  static  final ExecutorService CACHE_REBUILD_EXECUTOR= Executors.newFixedThreadPool(10);

    private boolean tryLock(String key){
        Boolean flag=stringRedisTemplate.opsForValue().setIfAbsent(key,"1",RedisConstants.LOCK_SHOP_TTL,TimeUnit.SECONDS);
        return BooleanUtil.isTrue(flag);
    }

    private void deleteLock(String key){
        stringRedisTemplate.delete(key);
    }
}
```

## 全局ID生成器

订单要求ID唯一

```
//开始时间戳
    private static final  long BEGIN_TIMESTAMP=1640995200L;
    private static final  long COUNT_BYTE=32;
    private  StringRedisTemplate stringRedisTemplate;

    public RedisIdWorker(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    public long nextId(String keyPrefix){
        //生成时间戳
        LocalDateTime now=LocalDateTime.now();
        long nowSecond=now.toEpochSecond(ZoneOffset.UTC);
        long timestamp=nowSecond-BEGIN_TIMESTAMP;

        //生成序列号
        //获取当前日期
        String data=now.format(DateTimeFormatter.ofPattern("yyyy:MM:dd"));
        //自增长
        long count=stringRedisTemplate.opsForValue().increment("icr:"+keyPrefix+":"+data);
        //保存返回
        return timestamp<<COUNT_BYTE|count;
    }
```

## 库存超卖问题分析

### 悲观锁

线程安全问题一定会发生，在操作数据之前获取锁，确保线程串行进行

### 乐观锁

认为线程安全问题不一定会发生，因此不加锁，只在更新数据的时候判断是否被其他线程修改

查询库存时只要库存大于0就进行自减

## 一人一单

每个人只能抢一张购物券

我们可以根据购物券ID和用户ID查询订单的数量，如果数量大于0，那么就返回

但是这样会出现并发问题：在第一次抢购时如果多个线程都查询到订单数为0，那么就会执行多次抢购和创建订单的操作，违反了一人一单

所以这时我们应该将具体的库存减少和创建订单的逻辑封装成一个函数，进行加锁，加锁时应该为用户ID加锁，这样就不会阻塞其他用户ID的抢购

但是这样的话有出现的了一个新的问题，该方法开启了事务，所以在锁释放的时候事务并没有进行提交，如果这时另一个线程进来查询订单数据仍是未插入的状态，又会导致并发问题

所以我们应该在方法外部加锁，由于Spring的代理机制，其他方法在调用该方法时为原始方法，所以我们应该调用代理的方法

```
<dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
        </dependency>
```

```
@EnableAspectJAutoProxy(exposeProxy = true)
```

```
@Override
    public Result seckillVoucher(Long voucherId) {
        //查询优惠券
        SeckillVoucher seckillVoucher=seckillVoucherMapper.selectById(voucherId);
        //判断秒杀是否开始
        if(seckillVoucher.getBeginTime().isAfter(LocalDateTime.now())){
            return Result.fail("秒杀还未开始");
        }
        //判断秒杀是否结束
        if(seckillVoucher.getEndTime().isBefore(LocalDateTime.now())){
            return Result.fail("秒杀已经结束");
        }
        //判断库存
        if(seckillVoucher.getStock()<1){
            return Result.fail("库存不足");
        }
        //返回订单id
        Long userId=UserHolder.getUser().getId();
        synchronized (userId.toString().intern()) {
            //获取代理对象
           IVoucherOrderService proxy= (IVoucherOrderService)AopContext.currentProxy();
            return proxy.createVoucherOrder(voucherId);
        }

    }
    @Transactional
    @Override
    public Result createVoucherOrder(Long voucherId){
        //一人一单
        Long userId= UserHolder.getUser().getId();
            int count = voucherOrderMapper.selectCountOrder(userId, voucherId);
            if (count > 0) {
                return Result.fail("您已经购买了一次");
            }
            //扣减库存
            boolean success = seckillVoucherService.update()
                    .setSql("stock= stock -1")
                    .eq("voucher_id", voucherId).gt("stock", 0).update();
            if (!success) {
                return Result.fail("库存不足");
            }
            //创建订单
            VoucherOrder voucherOrder = new VoucherOrder();
            long orderId = redisIdWorker.nextId("order");
            voucherOrder.setId(orderId);


            voucherOrder.setUserId(userId);

            voucherOrder.setVoucherId(voucherId);
            voucherOrderMapper.insert(voucherOrder);


            //返回订单id
            return Result.ok(orderId);

    }
```

这样就解决了一人一单的高并发问题

### 并发安全问题

集群模式下，会造成线程安全问腿

### 分布式锁

多进程可见

互斥

高性能

高可用

安全性

通过在redis中setnx，使得其他线程不能在key存在的情况下获取锁，实现分布式，业务逻辑执行完后对锁进行释放

```
 //创建对象
        SimpleRedisLock lock=new SimpleRedisLock("order:"+userId,stringRedisTemplate);
        boolean isLock= lock.tryLock(1200L);
        if(!isLock){
            return Result.fail("不允许重复下单");
        }
        try {
            //获取代理对象
            IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
            return proxy.createVoucherOrder(voucherId);
        }finally {
            lock.unlock();
        }
        
```

### 线程安全问题

如果线程A枷锁后遇到了阻塞，锁自动过期，这时其他线程进入，加锁执行业务逻辑，这时线程A恢复，也执行业务逻辑，最后把线程B的锁释放，这时其他线程会涌入，导致并发问题

解决：在A释放锁的时候判断是不是自己的锁，但是这样的话还是无法避免创建两个订单的情况，毕竟还是两个线程一起执行业务逻辑，所以最好的解决就是避免这种情况发生



以下是断点调试，模拟锁过期，可以发现两个线程都获取锁执行业务逻辑

![](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209211958371.png)

![image-20260114101907286](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209212003298.png)

在执行业务逻辑时，都查询到了订单数为0，导致订单重复插入

![image-20260114102016354](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209212006956.png)

![image-20260114102027622](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209212009763.png)

这里通过比较确定了不是自己的锁

![image-20260114102138793](https://gitee.com/Wsj123789/wsj/raw/master/img/20260209212011890.png)

### Lua脚本

#### 引入原因

在释放锁的过程中，判断和释放是分开进行的，如果在判断之后线程在释放锁的时候宕机，锁过期释放，这时其他线程进入，重新设置锁，线程苏醒后继续执行释放锁的操作，这样就会误删其他线程的锁，造成并发问题

#### 解决

将判断和释放锁的逻辑写入lua脚本中，通过API调用lua脚本执行

```
if(redis.call('get',KEYS[1])==ARGV[1]) then
    return redis.call('del',KEYS[1])
end
return 0
```

获取脚本

```
private static  final DefaultRedisScript<Long> UNLOCK_SCRIPT;
    static {
        UNLOCK_SCRIPT=new DefaultRedisScript<>();
        UNLOCK_SCRIPT.setLocation(new ClassPathResource("unlock.lua"));
        //返回值类型
        UNLOCK_SCRIPT.setResultType(Long.class);
    }
```

API调用

```
@Override
    public void unlock() {
        //调用lua脚本
        //代码变为一行，判断和删除在脚本中执行，满足原子性
        stringRedisTemplate.execute(UNLOCK_SCRIPT, Collections.singletonList(KEY_PREFIX+name),
                ID_PREFIX+Thread.currentThread().getId());
        }
```

## Redis秒杀优化

### 阻塞队列实现异步秒杀

原先逻辑：查询优惠券信息，判断是否过期，库存是否充足，通过redissonClient对象指定锁名并设置锁，获取创建订单，库存删减的代理对象，执行方法

所有逻辑同步进行，导致性能较差

**解决**

- 在新增优惠券时，将优惠券的库存加入到redis中，以后在redis的基础上进行库存操作
- 将用户ID加入到Redis中，使用一个LIst数据存储，每次抢购时先判断ID是否在redis中，如果不在则加入到redis中
- 前两步涉及到redis的多步操作，会涉及并发问题，需要用lua脚本编写
- 设置一个阻塞队列，单开一个线程进行对数据库的读写操作，主线程传递优惠券信息，创建订单

这样主线程只在redis基础上操作，性能得到大量的提高

```
//加载lua脚本
    static {
        SECKILL_SCRIPT=new DefaultRedisScript<>();
        SECKILL_SCRIPT.setLocation(new ClassPathResource("seckill.lua"));
        //返回值类型
        SECKILL_SCRIPT.setResultType(Long.class);
    }
    //阻塞队列
    private BlockingQueue<VoucherOrder> orderTasks=new ArrayBlockingQueue<>(1024*1024);
    private static final ExecutorService SECKILL_ORDER_EXECUTOR= Executors.newSingleThreadExecutor();
    @PostConstruct
    private void init(){
        SECKILL_ORDER_EXECUTOR.submit(new VoucherOrderHandler());
    }
    private class VoucherOrderHandler implements Runnable{

        @Override
        public void run() {
            while (true) {
                try {
                    //获取数据
                    VoucherOrder voucherOrder = orderTasks.take();
                    //创建订单
                    handleVoucherOrder(voucherOrder);
                } catch (Exception e) {
                    log.error("订单处理异常:", e);
                }
            }
        }
    }

    private void handleVoucherOrder(VoucherOrder voucherOrder) {
        Long userId=voucherOrder.getUserId();

        RLock rLock=redissonClient.getLock("lock:order:"+userId);
        boolean isLock= rLock.tryLock();
        if(!isLock){
            log.error("不允许重复下单");
            return;
        }
        try {
            //获取代理对象
            proxy.createVoucherOrder(voucherOrder);
        }finally {
            rLock.unlock();
        }
    }

    @Override
    public Result seckillVoucher(Long voucherId) {
                //查询优惠券
        SeckillVoucher seckillVoucher=seckillVoucherMapper.selectById(voucherId);
//        获取用户ID
        Long userId=UserHolder.getUser().getId();
        //判断秒杀是否开始
        if(seckillVoucher.getBeginTime().isAfter(LocalDateTime.now())){
            return Result.fail("秒杀还未开始");
        }
        //判断秒杀是否结束
        if(seckillVoucher.getEndTime().isBefore(LocalDateTime.now())){
            return Result.fail("秒杀已经结束");
        }
        //执行lua脚本，判断有没有购买资格
        Long result = stringRedisTemplate.execute(SECKILL_SCRIPT, Collections.emptyList(), voucherId.toString(), userId.toString());
        //判断结果是不是0，如果不为0，没有购买资格
        int r=result.intValue();
        if(r!=0){
            //不为0
            return Result.fail(r==1?"库存不足":"不能重复下单");
        }
        long orderId=redisIdWorker.nextId("order");

        VoucherOrder voucherOrder = new VoucherOrder();
        voucherOrder.setId(orderId);

        voucherOrder.setUserId(userId);

        voucherOrder.setVoucherId(voucherId);
        //为0.将下单信息保存到阻塞队列
        orderTasks.add(voucherOrder);
        //获取代理对象
        proxy = (IVoucherOrderService) AopContext.currentProxy();
        //返回订单ID
        return Result.ok(orderId);

    }
```

```
@Transactional
    @Override
    public void createVoucherOrder(VoucherOrder voucherOrder){
        //一人一单
        Long userId= voucherOrder.getUserId();
            int count = voucherOrderMapper.selectCountOrder(userId, voucherOrder.getVoucherId());
            if (count > 0) {
                log.error("您已经购买了一次");
                return ;
            }
            //扣减库存
            boolean success = seckillVoucherService.update()
                    .setSql("stock= stock -1")
                    .eq("voucher_id", voucherOrder.getVoucherId()).gt("stock", 0).update();
            if (!success) {
                log.error("库存不足");
                return;
            }
            //创建订单
            voucherOrderMapper.insert(voucherOrder);


    }
```



## 相关条目
- [[redis分布式缓存]]
- [[mq]]
- [[rocketmq]]
- [[苍穹]]
