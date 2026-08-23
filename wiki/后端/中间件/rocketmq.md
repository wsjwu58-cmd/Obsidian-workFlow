## RocketMq

[为什么选择RocketMQ | RocketMQ](https://rocketmq.apache.org/zh/docs/4.x/)

### 概念

我们平时使用一些体育新闻软件，会订阅自己喜欢的一些球队板块，当有作者发表文章到相关的板块，我们就能收到相关的新闻推送。

发布-订阅（Pub/Sub）是一种消息范式，消息的发送者（称为发布者、生产者、Producer）会将消息直接发送给特定的接收者（称为订阅者、消费者、Consumer）。而RocketMQ的基础消息模型就是一个简单的Pub/Sub模型。

- 相同的ConsumerGroup下的消费者主要有两种负载均衡模式，即**广播模式**，和**集群模式**（图中是最常用的集群模式）。
- 在集群模式下，同一个 ConsumerGroup 中的 Consumer 实例是负载均衡消费，如图中 ConsumerGroupA 订阅 TopicA，TopicA 对应 3个队列，则 GroupA 中的 Consumer1 消费的是 MessageQueue 0和 MessageQueue 1的消息，Consumer2是消费的是MessageQueue2的消息。
- 在广播模式下，同一个 ConsumerGroup 中的每个 Consumer 实例都处理全部的队列。需要注意的是，广播模式下因为每个 Consumer 实例都需要处理全部的消息，因此这种模式仅推荐在通知推送、配置同步类小流量场景使用。



![image-20251223155708049](https://gitee.com/Wsj123789/wsj/raw/master/img/20251223155710069.png)

### 生产者 Producer

发布消息的角色。Producer通过 MQ 的负载均衡模块选择相应的 Broker 集群队列进行消息投递，投递的过程支持快速失败和重试。

### **消费者 Consumer**

消息消费的角色。

- 支持以推（push），拉（pull）两种模式对消息进行消费。
- 同时也支持**集群方式**和广播方式的消费。
- 提供实时消息订阅机制，可以满足大多数用户的需求。

### 名字服务器 **NameServer**

NameServer是一个简单的 Topic 路由注册中心，支持 Topic、Broker 的动态注册与发现。

主要包括两个功能：

- **Broker管理**，NameServer接受Broker集群的注册信息并且保存下来作为路由信息的基本数据。然后提供心跳检测机制，检查Broker是否还存活；
- **路由信息管理**，每个NameServer将保存关于 Broker 集群的整个路由信息和用于客户端查询的队列信息。Producer和Consumer通过NameServer就可以知道整个Broker集群的路由信息，从而进行消息的投递和消费。

NameServer通常会有多个实例部署，各实例间相互不进行信息通讯。Broker是向每一台NameServer注册自己的路由信息，所以每一个NameServer实例上面都保存一份完整的路由信息。当某个NameServer因某种原因下线了，客户端仍然可以向其它NameServer获取路由信息。

### 代理服务器 Broker

Broker主要负责消息的存储、投递和查询以及服务高可用保证。

NameServer几乎无状态节点，因此可集群部署，节点之间无任何信息同步。Broker部署相对复杂。

在 Master-Slave 架构中，Broker 分为 Master 与 Slave。一个Master可以对应多个Slave，但是一个Slave只能对应一个Master。Master 与 Slave 的对应关系通过指定相同的BrokerName，不同的BrokerId 来定义，BrokerId为0表示Master，非0表示Slave。Master也可以部署多个。

```
每个 Broker 与 NameServer 集群中的所有节点建立长连接，定时注册 Topic 信息到所有 NameServer。

Producer 与 NameServer 集群中的其中一个节点建立长连接，定期从 NameServer 获取Topic路由信息，并向提供 Topic 服务的 Master 建立长连接，且定时向 Master 发送心跳。Producer 完全无状态。

Consumer 与 NameServer 集群中的其中一个节点建立长连接，定期从 NameServer 获取 Topic 路由信息，并向提供 Topic 服务的 Master、Slave 建立长连接，且定时向 Master、Slave发送心跳。Consumer 既可以从 Master 订阅消息，也可以从Slave订阅消息。
```

### RocketMQ集群工作流程

### 1. 启动NameServer

启动NameServer。NameServer启动后监听端口，等待Broker、Producer、Consumer连接，相当于一个路由控制中心。

### 2. 启动 Broker

启动 Broker。与所有 NameServer 保持长连接，定时发送心跳包。心跳包中包含当前 Broker 信息以及存储所有 Topic 信息。注册成功后，NameServer 集群中就有 Topic跟Broker 的映射关系。

### 3. 创建 Topic

创建 Topic 时需要指定该 Topic 要存储在哪些 Broker 上，也可以在发送消息时自动创建Topic。

### 4. 生产者发送消息

生产者发送消息。启动时先跟 NameServer 集群中的其中一台建立长连接，并从 NameServer 中获取当前发送的 Topic存在于哪些 Broker 上，轮询从队列列表中选择一个队列，然后与队列所在的 Broker建立长连接从而向 Broker发消息。

### 5. 消费者接受消息

消费者接受消息。跟其中一台NameServer建立长连接，获取当前订阅Topic存在哪些Broker上，然后直接跟Broker建立连接通道，然后开始消费消息。

## 实际操作

### 发送普通消息



```java
@Test
    public void produce() throws MQClientException, MQBrokerException, RemotingException, InterruptedException {
        //设置producer
        DefaultMQProducer producer=new DefaultMQProducer("group1");
        //设置nameServer地址
        producer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        //启动producer
        producer.start();
        //创建消息
        Message message=new Message("topic2","hello-mq".getBytes());
        //发送消息
       SendResult result= producer.send(message);
        System.out.println( result);
        //关闭producer
        producer.shutdown();
    }
```



### 异步消息

```java
//异步发送消息
public class AsyncProducerTest {
    @Test
    public void produce() throws MQClientException, InterruptedException {
        // 初始化一个producer并设置Producer group name
        DefaultMQProducer producer = new DefaultMQProducer("please_rename_unique_group_name");
        // 设置NameServer地址
        producer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        // 启动producer
        producer.start();
        producer.setRetryTimesWhenSendAsyncFailed(0);
        int messageCount = 100;
        final CountDownLatch countDownLatch = new CountDownLatch(messageCount);
        for (int i = 0; i < messageCount; i++) {
            try {
                final int index = i;
                // 创建一条消息，并指定topic、tag、body等信息，tag可以理解成标签，对消息进行再归类，RocketMQ可以在消费端对tag进行过滤
                Message msg = new Message("topic2",
                        "TagA",
                        "Hello world".getBytes(RemotingHelper.DEFAULT_CHARSET));
                // 异步发送消息, 发送结果通过callback返回给客户端
                producer.send(msg, new SendCallback() {
                    @Override
                    public void onSuccess(SendResult sendResult) {
                        System.out.printf("%-10d OK %s %n", index,
                                sendResult.getMsgId());
                        countDownLatch.countDown();
                    }
                    @Override
                    public void onException(Throwable e) {
                        System.out.printf("%-10d Exception %s %n", index, e);
                        e.printStackTrace();
                        countDownLatch.countDown();
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
                countDownLatch.countDown();
            }
        }
        //异步发送，如果要求可靠传输，必须要等回调接口返回明确结果后才能结束逻辑，否则立即关闭Producer可能导致部分消息尚未传输成功
        countDownLatch.await(5, TimeUnit.SECONDS);
        // 一旦producer不再使用，关闭producer
        producer.shutdown();
    }
    }
```

### 批量消息

```java
//批量发送消息
public class BatchTest {
    @Test
    public void produce() throws Exception {
        DefaultMQProducer producer=new DefaultMQProducer("group3");
        producer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        producer.start();
        List<Message> list=new ArrayList<>();
        list.add(new Message("batchtopic","tagA","hello".getBytes()));
        list.add(new Message("batchtopic","tagB","hello1".getBytes()));
        list.add(new Message("batchtopic","tagB","hello2".getBytes()));
        producer.send(list);
        producer.shutdown();
    }
}
```

### 单项消息

```
//日志单项发送
public class MessageTest {
    @Test
    public void produce() throws MQBrokerException, RemotingException, InterruptedException, MQClientException {
        DefaultMQProducer defaultMQProducer=new DefaultMQProducer("group2");
        defaultMQProducer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        try {
            defaultMQProducer.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
        Message message=new Message("topic2","tag2","message".getBytes());
        defaultMQProducer.send(message);
        defaultMQProducer.shutdown();
    }
}
```

### 延时消息发送

```
//延时消息发送
public class timeoutTest {
    @Test
    public void produce() throws MQBrokerException, RemotingException, InterruptedException, MQClientException {
        DefaultMQProducer defaultMQProducer=new DefaultMQProducer("group2");
        defaultMQProducer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        try {
            defaultMQProducer.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
        Message message=new Message("topic1","tag1","key1","hello delay".getBytes());
        message.setDelayTimeLevel(3);
        defaultMQProducer.send( message);
        defaultMQProducer.shutdown();
    }
    @Test
    public  void consume() throws MQClientException, IOException {
        DefaultMQPushConsumer consumer=new DefaultMQPushConsumer("consume1");
        //设置nameServe地址
        consumer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        //订阅一个或多个topic
        consumer.subscribe("topic1","*");
        consumer.registerMessageListener(new MessageListenerConcurrently() {
            @Override
            public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> list, ConsumeConcurrentlyContext consumeConcurrentlyContext) {
                System.out.println(Thread.currentThread().getName()+":"+new String(list.get(0).getBody()));
                //返回消费状态
                return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
            }
        });
        consumer.start();
        //挂起线程，让程序不退出
        System.in.read();
        System.out.println("consumer started");
    }
}
```

### MQ的顺序消息

在实际开发中我们往往遇到这样的情况：用户在下单时会经过一系列有顺序的过程：获取订单状态，修改订单，这些顺序是不能颠倒的，但是消息在发送时会随机向一个主题的多个队列中填充，不能保证消息的顺序，而且消费者在消费时默认是多线程，消费的顺序也不一样



这时我们有的解决方案分为两方面：

将消费者模式改为单线程（一个队列一个线程）

将同一订单的消息按顺序放在一个队列中，顺序消息发送时将ShardingKey相同（同一订单号）的消息序路由到一个逻辑队列中。

这样可以保证消息被顺利按顺序消费

```
//顺序
public class orderTest {
    private List<Model> msgModels= Arrays.asList(
            new Model("qwer",1,"下单"),
            new Model("qwer",1,"短信"),
            new Model("qwer",1,"物流"),
            new Model("zxcv",1,"下单"),
            new Model("zxcv",1,"短信"),
            new Model("zxcv",1,"物流")
    );
    @Test
    public void produce() throws Exception {
        DefaultMQProducer producer=new DefaultMQProducer("order-group");
        producer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        producer.start();
        msgModels.forEach(model -> {
            try {
                Message message=new Message("order-topic",model.toString().getBytes());
                producer.send(message, new MessageQueueSelector() {
                    @Override
                    public MessageQueue select(List<MessageQueue> list, Message message, Object o) {
                        int hashCode=o.toString().hashCode();
                        int i=hashCode%list.size();
                        return list.get(i);
                    }
                },model.getOrderSn());
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        producer.shutdown();
        System.out.println("produce over");
    }

    @Test
    public void consume() throws Exception {
        DefaultMQPushConsumer consumer=new DefaultMQPushConsumer("order-consumer");
        consumer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        consumer.subscribe("order-topic","*");
        consumer.registerMessageListener(new MessageListenerOrderly() {
            @Override
            public ConsumeOrderlyStatus consumeMessage(List<MessageExt> list, ConsumeOrderlyContext consumeOrderlyContext) {
                System.out.println(Thread.currentThread().getId()+":"+new String(list.get(0).getBody()));
                return  ConsumeOrderlyStatus.SUCCESS;
            }
        });
        consumer.start();
        System.in.read();
    }
}
```

## RocketMq去重操作

幂等性

多次操作产生的影响均和第一次操作产生的影响相同

新增操作没有幂等性（除非给特定字段加唯一索引）

删除操作，更新操作都符合幂等性



我们可以通过添加唯一索引，通过对数据库的新增来判断是否消息重复发送，在进行逻辑处理，

如果逻辑处理不正确抛出异常，需要删除新增再数据库的数据并进行重试，否则在重试时会因为数据库中的唯一索引被判断为重复消息，直接返回

```
@SpringBootTest
class DemoApplicationTests {
    @Autowired
    JdbcTemplate jdbcTemplate;

    @Test
    void repeatConsume() throws MQClientException, MQBrokerException, RemotingException, InterruptedException {
        DefaultMQProducer producer = new DefaultMQProducer("repeat");
        producer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        producer.start();
        String key= UUID.randomUUID().toString();
        System.out.println( key);
        Message message=new Message("repeatTopic",null,key,"扣减库存-1".getBytes());
        Message repeatMessage=new Message("repeatTopic",null,key,"扣减库存-1".getBytes());
        producer.send(message);
        producer.send(repeatMessage);
        System.out.println("发送完成");
        producer.shutdown();
    }

    @Test
    void repeatConsume2() throws MQClientException, MQBrokerException, RemotingException, InterruptedException, IOException {
        DefaultMQPushConsumer consumer=new DefaultMQPushConsumer("repeat-a");
        consumer.setNamesrvAddr(Mqconstant.NAME_SERVER);
        consumer.subscribe("repeatTopic","*");
        consumer.registerMessageListener(new MessageListenerConcurrently() {
            @Override
            public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> list, ConsumeConcurrentlyContext consumeConcurrentlyContext) {
                MessageExt messageExt=list.get(0);
                String key=messageExt.getKeys();
                //插入数据库
                jdbcTemplate.update("insert into table_name (type, user, order_sn) VALUES (2,'ww',?)",key);
                System.out.println(new String(messageExt.getBody()));
                return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
            }
        });
        consumer.start();
        System.in.read();
        System.out.println("消费者启动");

    }

}
```

## 死信队列

消息在重试超过最大次数时会被放入死信队列

- 重试超过 `maxReconsumeTimes` 后，消息自动进入 **%DLQ%my-group** 主题。

- 你需要**单独监听 DLQ**，进行人工处理或告警

  ```
  // 监听死信队列（用于告警/人工干预）
  @RocketMQMessageListener(
      topic = "%DLQ%my-group",
      consumerGroup = "dlq-monitor-group"
  )
  public class DlqListener implements RocketMQListener<MessageExt> {
      @Override
      public void onMessage(MessageExt msg) {
          log.error("Dead letter message: {}", new String(msg.getBody()));
          // 发送企业微信/钉钉告警
          alertService.sendAlert("MQ 消费失败，请人工处理");
      }
  }
  ```

  消费死信队列时不再编写业务逻辑，只是提醒人工处理错误

## SpringBoot集成

```
<dependency>
    <groupId>org.apache.rocketmq</groupId>
    <artifactId>rocketmq-spring-boot-starter</artifactId>
    <version>2.3.0</version>
</dependency>
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>2.0.25</version>
</dependency>
```

各种消息的发送

```
@SpringBootTest
class RocketProducerApplicationTests {
    @Autowired
    private RocketMQTemplate rocketMQTemplate;

    @Test
    void contextLoads() {
//        rocketMQTemplate.syncSend("boot-test-topic","我是boot的一个消息");
//
//        //异步
//        rocketMQTemplate.asyncSend("boot-async-group", "我是异步消息", new SendCallback() {
//            @Override
//            public void onSuccess(SendResult sendResult) {
//                System.out.println("成功发送：");
//            }
//
//            @Override
//            public void onException(Throwable throwable) {
//                System.out.println("发送失败"+throwable.getMessage());
//            }
//        });
//
//        //单项消息
//        rocketMQTemplate.sendOneWay("boot-oneway-group", "我是单向消息");
//        //延迟消息
//        Message<String> build = MessageBuilder.withPayload("我是一个延迟消息").build();
//        rocketMQTemplate.syncSend("boot-timeout",build,3000,3);
        //顺序消息
        List<Model> msgModels= Arrays.asList(
                new Model("qwer",1,"下单"),
                new Model("qwer",1,"短信"),
                new Model("qwer",1,"物流"),
                new Model("zxcv",1,"下单"),
                new Model("zxcv",1,"短信"),
                new Model("zxcv",1,"物流")
        );
        msgModels.forEach(model->{
            rocketMQTemplate.syncSendOrderly("boot-orderly", JSON.toJSON( model),model.getOrderSn());
        });
    }

    @Test
    void testTagKey(){
        rocketMQTemplate.syncSend("Tag-test:Tag1","我是一个boot带tag的信息");
        Message<String> build = MessageBuilder.withPayload("我是一个带Key的消息").setHeader(RocketMQHeaders.KEYS, "key")
                .build();
        rocketMQTemplate.syncSend("Key-topic",build);
    }

}
```

接收格式

```
//顺序监听
@Component
@RocketMQMessageListener(topic = "boot-orderly", consumerGroup = "boot-order-group",
                          consumeMode = ConsumeMode.ORDERLY,
                          maxReconsumeTimes = 5)//最大重试次数
public class OrderListener implements RocketMQListener<MessageExt> {
    @Override
    public void onMessage(MessageExt messageExt) {
        Model model= JSON.parseObject(new String(messageExt.getBody()),Model.class);
        System.out.println(model);
    }
}
```

```
@Component
@RocketMQMessageListener(topic = "Tag-test",
consumerGroup = "Tag-group",
selectorType = SelectorType.TAG,
selectorExpression = "Tag1||Tag2")
public class TagTest implements RocketMQListener<MessageExt> {

    @Override
    public void onMessage(MessageExt messageExt) {
        System.out.println(new String(messageExt.getBody()));
    }
}
```

## 秒杀

短时间内处理大量的请求（高并发）

并行：多核CPU上多个任务在同一时刻执行

并发：多个任务在同一个时间段内执行

QBS：每秒钟处理请求的数量

tomcat:QBS:

域名：域名下对应很多IP

通过DNS轮询的方式对域名进行解析。每个IP对应一个Tomcat服务器的集群



如何优化接口的响应时间？

- 能异步就异步
- 减少IO（统一查，统一写）
- 尽早return
- 加锁粒度尽量减少
- 事务控制粒度尽可能小

例如：验证码滑块进行分流

发送异步消息

```
public class SeckillController {
    @Autowired
    private StringRedisTemplate redisTemplate;

    @Resource
    private RocketMQTemplate rocketMQTemplate;

//    CAS java无锁的   原子性 安全的
    AtomicInteger userIdAt = new AtomicInteger(0);

    /**
     * 1.用户去重
     * 2.库存的预扣减
     * 3.消息放入mq
     * 秒杀不是一个单独的系统
     * 都是大项目的某一个小的功能模块
     *
     * @param goodsId
     * @return
     */
    @GetMapping("seckill")
    public String doSecKill(Integer goodsId  /*Integer userId*/) {
        // log 2023-4-24 16:58:11
        // log 2023-4-24 16:58:11
        Integer userId = userIdAt.incrementAndGet();
        // uk uniqueKey = [yyyyMMdd] +  userId + goodsId
        String uk = userId + "-" + goodsId;
        // setIfAbsent = setnx
        Boolean flag = redisTemplate.opsForValue().setIfAbsent("uk:" + uk, "");
        if (Boolean.FALSE.equals(flag)) {
            return "您已经参与过该商品的抢购，请参与其他商品O(∩_∩)O~";
        }
        // 记住 先查再改 再更新  不安全的操作

        Long count = redisTemplate.opsForValue().decrement("goodsId:" + goodsId);
        if (count < 0) {
            // 保证我的redis的库存 最小值是0
            redisTemplate.opsForValue().increment("goodsId:" + goodsId);
            return "该商品已经被抢完,下次早点来(●ˇ∀ˇ●)";
        }
        // 方mq 异步处理
        rocketMQTemplate.asyncSend("seckillTopic3", uk, new SendCallback() {
            @Override
            public void onSuccess(SendResult sendResult) {
                System.out.println("发送成功");
            }

            @Override
            public void onException(Throwable throwable) {
                System.out.println("发送失败:" + throwable.getMessage());
                System.out.println("用户的id:" + userId + "商品id" + goodsId);
            }
        });
        return "正在拼命抢购中,请稍后去订单中心查看";
    }


    /**
     * 抢一个付费的商品
     * 1.先扣减库存  再付费  | 如果不付费 库存需要回滚
     * 2.先付费  再扣减库存  | 如果库存不足  则退费
     */


}
```

在初始化之前将库存更新到redis中

```
@Component
public class DataSync {
    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private StringRedisTemplate redisTemplate;

//    @Scheduled(cron = "0 0 10 0 0 ?")
//    public void initData(){
//    }

    /**
     * 我希望这个方法再项目启动以后
     * 并且再这个类的属性注入完毕以后执行
     * bean生命周期了
     * 实例化 new
     * 属性赋值
     * 初始化  (前PostConstruct/中InitializingBean/后BeanPostProcessor)
     * 使用
     * 销毁
     * ----------
     * 定位不一样
     */
    @PostConstruct
    public void initData() {
        List<Goods> goodsList = goodsMapper.selectSeckillGoods();
        if (CollectionUtils.isEmpty(goodsList)) {
            return;
        }
        goodsList.forEach(goods -> {
            redisTemplate.opsForValue().set("goodsId:" + goods.getGoodsId(), goods.getTotalStocks().toString());
        });
    }



}
```

### 在事务外添加锁

如果在事务内添加锁，事务开启时，两个线程会获取到一样的数据，在锁释放后，事务提交，这会导致其他线程在事务没有提交之前而在锁释放之后进行操作，造成数据的不一致问题

```
//    @Override
//    public void onMessage(MessageExt messageExt) {
//        String uk=new String(messageExt.getBody());
//        Integer userId=Integer.parseInt(uk.split("-")[0]);
//        Integer goodsId=Integer.parseInt(uk.split("-")[1]);
//        synchronized (this) {
//            goodsService.realSeckill(userId, goodsId);
//        }
//    }
```

### Mysql设置行锁进行分布式隔离

```
   @Override
    @Transactional(rollbackFor = Exception.class)
    public void realSeckill(Integer userId, Integer goodsId) {
        // update goods set total_stocks = total_stocks - 1 where goods_id = goodsId and total_stocks - 1 >= 0;
        // 通过mysql来控制锁
//        Goods goods=goodsMapper.selectByPrimaryKey(goodsId);
//        int total=goods.getTotalStocks()-1;
//        if(total<0){
//            throw new RuntimeException("该商品"+goodsId+"库存不足,用户ID："+userId);
//        }
//        goods.setTotalStocks(total);
//        goods.setUpdateTime(new Date());
       
        int i=goodsMapper.updateStock(goodsId);
        if(i>0){
            Order order=new Order();
            order.setGoodsid(goodsId);
            order.setUserid(userId);
            order.setCreatetime(new Date());
            orderMapper.insert(order);
        }

    }
```

### Redis分布式锁

在Redis中设置锁，key为lock

```
redisTemplate.opsForValue().setIfAbsent("lock:" + goodsId, "",Duration.ofSeconds(30))
```

这个方法作用是：如果key不存在，手动设置key,如果key存在，返回false，这就说明，如果一个线程设置了锁以后，其他线程无法干扰这个线程的业务代码执行，必须等到锁释放完毕之后才能进行

```
while (currentTime < ZX_TIME) {
   if (Boolean.TRUE.equals(flag)) {
        try {
            goodsService.realSeckill(userId, goodsId);
            return;
        } finally {
            redisTemplate.delete("lock:" + goodsId);
        }

    } else {
        currentTime += 200;
        try {
            Thread.sleep(200L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

在逻辑执行完之后，删除锁，让别的线程执行，因为执行业务代码需要一些时间，所以可以让其他线程等待一些时间

注意：一定要设置过期时间

#### **没有设置过期时间（TTL）**

- 线程 A 获取锁成功，但执行过程中**崩溃或长时间阻塞**（如 Full GC、断电）。
- 锁永远不会释放。
- 管理员手动删除锁，或系统重启后，线程 B 立即获取到锁。
- 此时若线程 A 恢复（比如只是假死），**A 和 B 同时认为自己持有锁**。


## 相关条目
- [[mq]]
- [[redis]]
