## 认识Stream流

Stream流大量结合了Lambda的语法风格来编程，功能强大，性能高效，可读性好

简化集合，数组操作的API

### 使用步骤

1. 获取Stream流
2. 调用流水线的各种方法
3. 获取处理的结果

<img src="https://gitee.com/Wsj123789/wsj/raw/master/img/20250927150927861.png" alt="image-20250927150927807" style="zoom:80%;" />

### 获取Stream流

```
Collection<String> list=new ArrayList<>();
        Stream<String> s1=list.stream();
        
        //map集合拿Stream流
        Map<String,Integer> map=new HashMap<>();
        Stream<String> s2=map.keySet().stream();
        Stream<Integer> s3=map.values().stream();
        Stream<Map.Entry<String,Integer>> s4=map.entrySet().stream();
        
        //获取数组的流
        String[] names={"2","3"};
        Stream<String> s5= Arrays.stream(names);
        System.out.println(s5.count());
        Stream<String> s6=Stream.of(names);
```

### 中间方法

![image-20250927152747949](https://gitee.com/Wsj123789/wsj/raw/master/img/20250927152748020.png)

```
List<String> ls=new ArrayList<>();
        ls.add("ww");
        ls.add("fw");
        ls.add("dw");
        ls.add("sw");
        ls.add("aw");

        //过滤方法

        List<String> newlist=ls.stream().filter(s->s.startsWith("w")).filter(s->s.length()==2).collect(Collectors.toList());

        //排序
        List<Double> scores=new ArrayList<>();
        scores.add(53.2);
        scores.add(73.2);
        scores.add(345.2);
        scores.add(63.2);
        scores.add(33.2);
        scores.stream().sorted().forEach(System.out::println);
        scores.stream().sorted((o1,o2)->Double.compare(o2,o1)).skip(2).forEach(System.out::println);

        //映射/加工方法，将原来的数据拿出来变成新数据再放上去
        ls.stream().map(s->(s+10)).forEach(System.out::println);
```

### 方法中可变参数

在形参列表中只能出现一个

```
public static void main(String[] args) {
        sum();
        sum(10,20,30);
        sum(new int[]{2,3});
    }
    public static void sum(int...nums){
        System.out.println(nums.length);
        System.out.println(Arrays.toString(nums));
        System.out.println(nums);
    }
```

### Collections工具类

![image-20250927164500522](https://gitee.com/Wsj123789/wsj/raw/master/img/20250927164500575.png)

## File

```
File f1=new File("D:\\note\\1.txt");
        System.out.println(f1.length());
        System.out.println(f1.getName());

        File f2=new File("D:\\note\\2.txt");
        System.out.println(f2.exists());

        //创建多级文件夹
        File f3=new File("D:\\note\\aaa\\bbb");
        System.out.println(f3.mkdirs());

        File f4=new File("D:\\note");
        File[] f5=f4.listFiles();
//        for(File file:f5){
//            System.out.println(file.getAbsoluteFile());
//        }
        System.out.println(Arrays.toString(f5));
```

## IO流

读文本内容用字符流，转移数据用字节流，如复制文件

### 字节流

**文件字节输入流**

```
public static void main(String[] args) throws Exception{
        InputStream is=new FileInputStream("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\1.txt");
        int b;
        // 每次读取一个字节的问题，性能较差，读取汉字会乱码
//        while((b=is.read())!=-1){
//            System.out.println((char) b);
//        }

        //每次读取多个字节
        byte[] buffer=new byte[3];
        //定义一个变量，记录读取了多少字节
         int len;
         while((len=is.read(buffer))!=-1){
             String str=new String(buffer,0,len);
             System.out.print(str);
         }
    }
```

读取小文件可以一次性读取文件中的所有字节

**文件字节输出流**

```
public static void main(String[] args) throws Exception{
        //使用文件字节输出流
//        FileOutputStream fs=new FileOutputStream("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\2.txt");
        //追加
        FileOutputStream fs=new FileOutputStream("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\2.txt",true);
        fs.write(97);

        fs.write('b');

        //写一个字节数组出去
        byte[] bytes="66".getBytes(StandardCharsets.UTF_8);
        fs.write(bytes);

        fs.write(bytes,0,1);
        fs.close();
    }
```

**复制文件**

```
public static void main(String[] args) {
        // 使用字节流完成文件的复制
        try {
            func("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\2.txt", "D:\\note\\1.txt");
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void func(String first, String end) {

        try (
            FileInputStream fis = new FileInputStream(first);
            FileOutputStream fos = new FileOutputStream(end);
        )
                //关闭文件
        {
            byte[] bytes = new byte[1024];
            int len;
            while ((len = fis.read(bytes)) != -1) {
                fos.write(bytes, 0, len);
            }
            System.out.println("复制完成");
        } catch(Exception e){
            e.printStackTrace();
        }

    }
```

### 字符流

**文件字符输入流**

```
public static void main(String[] args) throws Exception {
        try (Reader fr = new FileReader("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\1.txt"))
        {
            char[] c=new char[3];
            int len;
            while((len=fr.read(c))!=-1){
                String str=new String(c);
                System.out.println(str);
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
```

**文件字符输出流**

和文件字节输出流一致

### 缓冲流

**BufferedInputStream缓冲字节输入流**

作用：提高字节输入流读取字符的效率

提供大小为8K的缓冲池，读取数据时可以通过缓冲池将数据放到内存中

将数据写到文件中时同样可以通过缓冲池提高效率

```
try {
            func("D:\\idea code\\FileDemo\\src\\com\\wsj\\file\\2.txt", "D:\\note\\1.txt");
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void func(String first, String end) {

        try (
                FileInputStream fis = new FileInputStream(first);
                InputStream bis=new BufferedInputStream(fis);
                FileOutputStream fos = new FileOutputStream(end);
                OutputStream bos=new BufferedOutputStream(fos);
        )
        //关闭文件
        {
            byte[] bytes = new byte[1024];
            int len;
            while ((len = bis.read(bytes)) != -1) {
                fos.write(bytes, 0, len);
            }
            System.out.println("复制完成");
        } catch(Exception e){
            e.printStackTrace();
        }

    }
```

**输出流**

```
try (
                FileInputStream fis = new FileInputStream(first);
                InputStream bis=new BufferedInputStream(fis);
                FileOutputStream fos = new FileOutputStream(end);
                OutputStream bos=new BufferedOutputStream(fos);
        )
        //关闭文件
        {
            byte[] bytes = new byte[1024];
            int len;
            while ((len = bis.read(bytes)) != -1) {
                fos.write(bytes, 0, len);
            }
            System.out.println("复制完成");
        } catch(Exception e){
            e.printStackTrace();
        }
```

### 其他流

字符输入转换流

### IO框架

![image-20250928213428973](https://gitee.com/Wsj123789/wsj/raw/master/img/20250928213429050.png)

## 多线程

线程是一个程序内部的一条执行流程

多线程指从软硬件上实现的多条执行流程的技术（多条线程由CPU负责调度执行）

###  创建方式一：继承Thread类

1. 定义子类继承Thread类，重写run()方法

2. 创建对象

3. 使用start启用

   ```
   public class demo1 {
       //main方法本身有一条主线程负责推动执行
       public static void main(String[] args) {
           // 创建线程的方式1，继承thread实现
           //创建线程类的对象
           Thread s1=new MyThread();
           s1.start();
           for (int i = 0; i < 5; i++) {
               System.out.println("主线程输出："+i);
           }
       }
   }
   class MyThread extends Thread{
       @Override
       public void run(){
           for (int i = 0; i < 5; i++) {
               System.out.println("子线程输出："+i);
           }
       }
   }
   ```

   

**注意事项**

启动线程必须调用start方法，如果调用run方法还是相当于单线程执行

只有调用start方法才是启动一个线程的执行

### 创建方式二：实现Runnable接口

优点：任务类只是实现类接口，可以继续继承其他类，实现其他接口，扩展性强

缺点：需要多一个任务类对象

```
public class demo2 {
    public static void main(String[] args) {
        //实现Runnable接口实现
        // 创建一个线程任务类的对象
//        Runnable r=new MyRunnable();
        Thread t1=new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 5; i++) {
                    System.out.println("子线程输出："+i);
                }
            }
        });
        t1.start();
        for (int i = 0; i < 5; i++) {
            System.out.println("主线程输出："+i);
        }
    }
}
//class MyRunnable implements Runnable{
//
//    @Override
//    public void run() {
//        for (int i = 0; i < 5; i++) {
//            System.out.println("子线程输出："+i);
//        }
//    }
//}

```

### 创建方式三：实现Callable接口

优点：可以返回线程完毕后的结果

1. 创建任务对象
2. 定义一个类实现Callable接口，重写call方法，封装要做的事情，和要返回的数据
3. 把Callable类型的对象封装成FutureTask（线程任务对象）
4. 把线程任务对象交给Thread对象
5. 调用start
6. 执行完毕后，通过FutureTask对象的get获取任务执行的结果

```
public static void main(String[] args) {
        Callable<String> cs=new Mycallable(100);
        //封装成线程任务对象
        FutureTask<String> FS=new FutureTask<>(cs);
        // 传给Thread线程对象
        Thread t1=new Thread(FS);
        t1.start();

        Callable<String> c1=new Mycallable(50);
        //封装成线程任务对象
        FutureTask<String> F1=new FutureTask<>(c1);
        // 传给Thread线程对象
        Thread t2=new Thread(F1);
        t2.start();

        try{
            //如果主线程发现第一个线程没有执行完毕，会让出CPU，等第一个线程执行完毕后，才会往下执行
            System.out.println(FS.get());
        }catch (Exception e){
            e.printStackTrace();
        }

        try{
            System.out.println(F1.get());
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
class Mycallable implements Callable<String>{
private int n;
public Mycallable(int n){
    this.n=n;
}
    @Override
    public String call() throws Exception {

        int sum=0;
        for(int i=0;i<=n;i++){
            System.out.println(i);
            sum+=i;
        }
        return "子线程计算的"+"1-"+n+"结果："+sum;
    }
}
```

### 常用方法

方法名称

说明

String getName()

返回此线程的名称

int getId()

返回此线程的ID

void setName(String name)

设置线程的名字(构造方法也可以设置名字)

static Thread currentThread( )

获取当前线程的对象

static void sleep(long time)

让线程休眠指定的时间，单位为毫秒

setPriority(int newPriority)

设置线程的优先级

final int getPriority( )

获取线程的优先级

final void setDaemon(boolean on)

设置为守护线程

public static void yield( )

出让线程/礼让线程

public static void join( )

插入线程/插队线程

### 线程安全问题

- 存在多个线程同时进行

- 同时访问共享资源

- 存在修改共享资源

  ```
  public class DrawThread extends Thread{
      private Account acc;
      public DrawThread(String name,Account acc){
          super(name);
          this.acc=acc;
      }
      @Override
      public void run() {
          acc.drawmoney(100000);
      }
  }
  ```

  ```
  public static void main(String[] args) {
          // 设计一个账户类
          Account acc=new Account(100000,"x");
          Thread t1=new DrawThread("小明",acc);
          t1.start();
          new DrawThread("小红",acc).start();
      }
  ```

  

### 线程同步

核心思想：让多个线程先后一次访问共享资源，这样就可以避免出现线程安全问题

加锁：每次只允许一个线程加锁，加锁后才能访问，访问完毕后自动解锁，然后其他线程才能加锁进来

**方式一：同步代码块**

作用：把访问共享资源的核心代码上锁，以此保证线程安全

```
synchronize(同步锁){
  访问公共资源的核心代码
}
```

使用规范：建议使用共享资源作为锁对象，对于实例方法建议使用this作为锁对象

对于静态方法建议 使用字节码对象作为锁对象

**方式二：同步方法**

作用：把访问共享资源的核心方法上锁，以此保证线程安全

```
public synchronized void drawmoney(double money){
        String name=Thread.currentThread().getName();
        //判断余额是否足够
            if(this.money>=money){
                System.out.println(name+"取钱成功，取了"+money);
                this.money-=money;
                System.out.println(name+"取钱成功，剩余"+this.money);
            }
            else{
                System.out.println(name+"取钱失败");
            }
        
    }
```

**方式三：lock锁**

```
public  void drawmoney(double money){
        String name=Thread.currentThread().getName();
        //判断余额是否足够
        lk.lock();
        try {
            if(this.money>=money){
                System.out.println(name+"取钱成功，取了"+money);
                this.money-=money;
                System.out.println(name+"取钱成功，剩余"+this.money);
            }
            else{
                System.out.println(name+"取钱失败");
            }
        } finally {
            lk.unlock();

        }

    }
```

### 线程池

一个可以复用线程的技术

创建线程池

ExecutorService-->ThreadPoolExecutor

**方式一 通过ThreadPoolExecytor创建线程池**

（1）corePoolSize：核心线程数，线程池中始终存活的线程数。

（2）maximumPoolSize: 最大线程数，线程池中允许的最大线程数。

（3）keepAliveTime: 存活时间，线程没有任务执行时最多保持多久时间会终止。

（4）unit: 单位，参数keepAliveTime的时间单位，7种可选。
（5）workQueue: 一个阻塞队列，用来存储等待执行的任务，均为线程安全，7种可选。

（6）threadFactory: 线程工厂，主要用来创建线程，默及正常优先级、非守护线程。

（7）handler：拒绝策略，拒绝处理任务时的策略，4种可选，默认为AbortPolicy。

**注意事项**

新任务提交时发现核心线程在忙，任务队列也满了，并且可以创建临时线程，此时才能创建临时线程

核心线程和临时线程都在忙，任务队列也满了，拒绝

```
public static void main(String[] args) {
        //创建线程池对象
        ExecutorService pool=new ThreadPoolExecutor(3,5,10, TimeUnit.SECONDS,new ArrayBlockingQueue<>(3),
                Executors.defaultThreadFactory(),new ThreadPoolExecutor.AbortPolicy());
        Runnable target=new MyRunnable();
        Runnable target1=new MyRunnable();
        Runnable target2=new MyRunnable();
        Runnable target3=new MyRunnable();
        Runnable target4=new MyRunnable();
        Runnable target5=new MyRunnable();
        pool.execute(target);
        pool.execute(target1);
        pool.execute(target2);
        pool.execute(target3);
        pool.execute(target4);
        pool.execute(target5);
        pool.execute(target);

        //关闭线程池，一般不关闭线程池
        pool.shutdown();//所有任务执行完毕后关闭线程池
```

**方式二：Executors工具类**

```
 ExecutorService pool=Executors.newFixedThreadPool(3);
```

### 并发/并行

进程：正在进行的程序就是一个独立的进程

线程是属于进程的

## 网络编程

### IP地址

设备在网络中的地址，是设备在网络中的唯一标识

**DNS域名解析**

将域名转化为对应IP地址的分布式命名系统，将容易记的域名转化为数字化的IP地址

**内网IP**

局域网IP，专门为组织机构内部使用

**公网IP**

是可以连接到互联网的IP地址

### InetAddress

获取本机IP对象和对方IP对象

### 端口

应用程序在程序中的唯一标识

被规定一个16位的二进制，范围是0-65535

**端口分类**

周知端口：0-1023

注册端口：1024-49151

动态端口：49152-65535

自己开发的程序一般使用注册端口，同一个设备中不能出现两个相同的端口

### 协议

**通信协议**

网络上的通信设备，实现预定的连接规则，以及传递数据的规则被称为网络通信协议

**开发式网络互联标准：**

TCP/IP网络模型：事实上的国际标准

![image-20251006154603169](https://gitee.com/Wsj123789/wsj/raw/master/img/20251006154603282.png)

**传输层的两个通信协议**

UDP：用户数据报协议

特点：通信效率高，无连接，不可靠的协议，发送端把数据封装成一个64KB的包



TCP：传输控制协议

面向连接，可靠通信

保证在不可靠的信道上实现可靠的数据传输



三次握手建立可靠连接

- 客户端发出连接请求
- 服务端返回响应
- 客户端再次发出确认信息，连接建立



四次挥手断开连接

- 客户端发出消息断开连接请求
- 服务端返回一个响应：稍等
- 返回一个响应：消息处理完毕，确认断开
- 客户端发出确认断开消息，连接断开

客户端发送数据

```
public class TCPdemo1 {
    public static void main(String[] args) throws IOException {
        //tcp通信下一发一收，客户端开发
        //创建客户端管道对象，请求与服务端连接
        Socket socket=new Socket("127.0.0.1",9999);

        //从Socket管道中得到一个字节输出流
        OutputStream os=socket.getOutputStream();

        DataOutputStream dos=new DataOutputStream(os);
        dos.writeInt(1);
        dos.writeUTF("哈哈");
        socket.close();
    }
}
```

服务端接收数据

```
public class TCPdemo2 {
    public static void main(String[] args) throws IOException {
        ServerSocket ss=new ServerSocket(9999);

        //一旦有客户端连接返回一个Socket对象
        Socket s=ss.accept();
        //获取输入流
        InputStream is=s.getInputStream();
        //字节输入流包装成特殊数据输入流
        DataInputStream ds=new DataInputStream(is);

        int id=ds.readInt();
        String msg=ds.readUTF();
        System.out.println(id+msg);
        System.out.println("客户端的ip"+s.getInetAddress().getHostAddress());
        System.out.println("客户端的端口"+s.getPort());


    }
}
```







UDP通信

客户端发送数据

```
System.out.println("客户端启动");
        //完成UDP通信一发一收，客户端开发
        //发送对象
        DatagramSocket socket=new DatagramSocket();//随机端口
        // 创建数据包对象
        byte[] bytes="我是客户端".getBytes();
        //发送数据，发送长度，目的地的IP地址,目的地端口
        DatagramPacket packet=new DatagramPacket(bytes,bytes.length, InetAddress.getLocalHost(),8080);

        socket.send(packet);
```

服务端接收数据

```
System.out.println("服务端启动了");
        //接数据的对象
        DatagramSocket socket=new DatagramSocket(8080);
        //创建数据包接取数据
        byte[] buf=new byte[1024*64];
        DatagramPacket packet=new DatagramPacket(buf,buf.length);

        //接受数据
        socket.receive(packet);
        //获取数据长度
        int len=packet.getLength();
        String data=new String(buf,0,len);
        System.out.println(data);

        //获取对方的IP对象和程序端口
        String ip=packet.getAddress().getHostAddress();
        int port=packet.getPort();
        System.out.println("ip地址"+ip+"端口"+port);
```

### TCP通信-支持多个客户端通信

服务端

```
public class TCPdemo2 {
    public static void main(String[] args) throws IOException {
        ServerSocket ss=new ServerSocket(9999);

        //一旦有客户端连接返回一个Socket对象
        while (true) {
            Socket s=ss.accept();
            System.out.println("一个客户端上线了"+s.getInetAddress().getHostAddress());

            new SeverReader(s).start();

        }


    }
}
```

线程

```
public class SeverReader extends Thread{
    private Socket socket;
    public SeverReader(Socket socket){
        this.socket=socket;
    }
    @Override
    public void run() {
        //获取输入流
        try {
            InputStream is= socket.getInputStream();
            //字节输入流包装成特殊数据输入流
            DataInputStream ds=new DataInputStream(is);


            while (true) {
                String msg=ds.readUTF();
                System.out.println(msg);
                System.out.println("客户端的ip"+socket.getInetAddress().getHostAddress());
                System.out.println("客户端的端口"+socket.getPort());
                System.out.println("------------------------");
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("客户端下线了");
        }
    }
}
```

### B/S架构的原理

服务器必须给浏览器响应HTTP协议规定的数据格式，否则浏览器不识别返回的数据

![image-20251009171618644](https://gitee.com/Wsj123789/wsj/raw/master/img/20251009171618777.png)

```
public class SeverReader extends Thread{
    private Socket socket;
    public SeverReader(Socket socket){
        this.socket=socket;
    }
    @Override
    public void run() {
        //获取输入流
        try {
            //给浏览器响应一个网页回去
            OutputStream os=socket.getOutputStream();
            //把字节输出流包装成打印流
            PrintStream ps=new PrintStream(os);
            ps.println("HTTP/1,1 200 OK");
            ps.println("Content-Type:text/html;charset=utf-8");
            ps.println();
            ps.println("<html>");
            ps.println("<head>");
            ps.println("<meta charset='utf-8'>");
            ps.println("<title>");
            ps.println("wsj的网页");
            ps.println("</title>");
            ps.println("</head>");
            ps.println("<body>");
            ps.println("<h1>wsj</h1>");
            ps.println("</body>");
            ps.println("</html>");
            ps.close();
            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("客户端下线了");
        }
    }
}
```



## 相关条目
- [[03-后端/java/集合]]
- [[面向对象]]
- [[java高级技术]]
