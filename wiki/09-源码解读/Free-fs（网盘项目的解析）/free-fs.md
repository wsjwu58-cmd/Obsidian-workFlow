# free-fs
## 存储系统模块

### SPI详解

#### 是什么

是java提供的一种服务发现机制，用于实现接口与实现解耦

```
┌─────────────────────────────────────────────────────────────────┐
│                        SPI 加载流程                              │
│                                                                 │
│  1. 定义接口                                                     │
│     IStorageOperationService.java                               │
│                                                                 │
│  2. 实现接口                                                      │
│     AliyunOssStorageServiceImpl.java                            │
│     LocalStorageOperationService.java                           │
│                                                                 │
│  3. 配置 SPI                                                     │
│     META-INF/services/com.xddcodec...IStorageOperationService   │
│     内容：com.xddcodec...AliyunOssStorageServiceImpl            │
│                                                                 │
│  4. 运行时加载                                                    │
│     ServiceLoader.load(IStorageOperationService.class)          │
│     → 自动发现并加载所有实现类                                    │
└─────────────────────────────────────────────────────────────────┘
```

SPI通常在spring启动时自动加载

```
┌─────────────────────────────────────────────────────────────────┐
│                    Spring 启动流程                               │
│                                                                 │
│  1. 扫描 @Component 注解的类                                     │
│           │                                                     │
│           ▼                                                     │
│  2. 创建 StoragePluginRegistry Bean                             │
│           │                                                     │
│           ▼                                                     │
│  3. 执行 @PostConstruct 方法 ──▶ loadPlugins() 自动执行          │
│           │                                                     │
│           ▼                                                     │
│  4. SPI 加载所有插件，注册到缓存                                  │
│           │                                                     │
│           ▼                                                     │
│  5. 应用启动完成，等待请求                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

相关源码

```
// java.util.ServiceLoader 源码简化版
public final class ServiceLoader<S> implements Iterable<S> {
    
    // ⭐ 配置文件路径前缀
    private static final String PREFIX = "META-INF/services/";
    
    // 加载服务
    public static <S> ServiceLoader<S> load(Class<S> service) {
        // 获取当前线程的类加载器
        ClassLoader loader = Thread.currentThread().getContextClassLoader();
        return new ServiceLoader<>(service, loader);
    }
    
    // 懒加载迭代器
    private Iterator<S> lazyIterator;
    
    // 核心方法：读取配置文件，加载实现类
    private Iterator<S> lookupIterator() {
        return new LazyIterator();
    }
    
    private class LazyIterator implements Iterator<S> {
        
        public boolean hasNext() {
            if (!loaded) {
                // ⭐ 读取配置文件
                String fullName = PREFIX + service.getName();
                // 文件路径：META-INF/services/com.xddcodec...IStorageOperationService
                
                Enumeration<URL> configs = loader.getResources(fullName);
                
                // 解析文件内容，获取实现类全限定名
                while (configs.hasMoreElements()) {
                    URL url = configs.nextElement();
                    parse(url);  // 解析文件，读取类名
                }
                loaded = true;
            }
            return nextName != null;
        }
        
        public S next() {
            String cn = nextName;  // 实现类全限定名
            // ⭐ 反射创建实例
            Class<?> c = Class.forName(cn, false, loader);
            S p = service.cast(c.newInstance());
            return p;
        }
    }
}
```

### 用户根据存储平台配置操作框架

spring容器启动时扫描到StoragePluginRegistry类进行初始化插件 /\*\*

初始化：通过 SPI 加载插件

**只有同时满足以下条件的类才被认为是有效的存储插件：**

*   实现 IStorageOperationService 接口
*   在 META-INF/services 中注册（SPI）
*   标注 @StoragePlugin 注解

满足以上条件才能被初始化，元数据和实现类分别用两个map集合存储，键值都是平台标识符，同时StoragePlatformAutoRegister类会同步插件配置到数据库

如果用户要上传文件等操作，会先获取相关文件的fileinfo中的存储配置id，通过查询数据库封装成StorageConfig实体类，然后调用StorageServiceFacade类中的getStorageService方法，在方法内部判断是本地配置存储还是自定义配置存储（阿里云等），调用StoragePluginManager类的getOrCreateInstance方法，因为该方法为函数式编程，第二个参数使用lambda表达式通过StorageInstanceFactory类的createInstance方法调用StoragePluginRegistry类的getPrototype方法获取插件原型实例，如果当前实例在缓存中，则直接返回，如果不在缓存中，则调用这个方法进行实例化，这样就返回了相应的存储实例，可以对其进行操作

#### 两个Map的具体定义

```
// StoragePluginRegistry.java
public class StoragePluginRegistry {
    
    // 原型实例缓存
    private final Map<String, IStorageOperationService> prototypes = new ConcurrentHashMap<>();
    
    // 插件元数据缓存
    private final Map<String, StoragePluginMetadata> metadataMap = new ConcurrentHashMap<>();
}
```

#### Lambda延迟加载的好处

```
// StorageServiceFacade.java
public IStorageOperationService getStorageService(String configId) {
    return pluginManager.getOrCreateInstance(
        configId,
        () -> loadConfigFromDatabase(configId)  // ⭐ Lambda 延迟加载
    );
}
```

只有在未命中的时候才会去查询数据库

#### 缓存键的生成规则

```
// StorageUtils.java
public static String generateCacheKey(String platformIdentifier, String configId) {
    if (isLocalConfig(configId)) {
        return "local:system";  // 本地存储固定键
    }
    return configId + ":" + platformIdentifier;  // 如：b7e96d25:AliyunOSS
}
```

#### 具体流程图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           完整流程总结                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    阶段一：启动初始化                                   │ │
│  │                                                                       │ │
│  │   Spring 容器启动                                                     │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   扫描到 StoragePluginRegistry                                        │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   @PostConstruct → loadPlugins()                                      │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   SPI 扫描 META-INF/services/...                                      │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   ┌─────────────────────────────────────────┐                         │ │
│  │   │ 验证条件：                               │                         │ │
│  │   │ 1. 实现 IStorageOperationService 接口   │                         │ │
│  │   │ 2. 在 META-INF/services 中注册          │                         │ │
│  │   │ 3. 标注 @StoragePlugin 注解             │                         │ │
│  │   └─────────────────────────────────────────┘                         │ │
│  │        │                                                              │ │
│  │        ├── 满足 → 创建原型实例，存入两个 Map                            │ │
│  │        │         prototypes.put(identifier, prototype)                │ │
│  │        │         metadataMap.put(identifier, metadata)                │ │
│  │        └── 不满足 → 跳过                                               │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    阶段二：运行时使用                                   │ │
│  │                                                                       │ │
│  │   用户上传文件                                                         │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   获取 FileInfo.storagePlatformSettingId（配置ID）                    │ │
│  │        │                                                              │ │
│  │        ▼                                                              │ │
│  │   StorageServiceFacade.getStorageService(configId)                    │ │
│  │        │                                                              │ │
│  │        ├── configId == null 或 "Local" → 返回本地存储实例              │ │
│  │        │                                                              │ │
│  │        └── 其他 configId → 继续下面流程                                │ │
│  │               │                                                       │ │
│  │               ▼                                                       │ │
│  │   StoragePluginManager.getOrCreateInstance(configId, () -> ...)       │ │
│  │               │                                                       │ │
│  │               ▼                                                       │ │
│  │   ┌─────────────────────────────────────────┐                         │ │
│  │   │ 检查缓存：instanceCache.get(cacheKey)   │                         │ │
│  │   └─────────────────────────────────────────┘                         │ │
│  │               │                                                       │ │
│  │               ├── 命中 → 直接返回实例                                   │ │
│  │               │                                                       │ │
│  │               └── 未命中 → 执行 Lambda 加载配置                         │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               loadConfigFromDatabase(configId)                        │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               构建 StorageConfig 对象                                  │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               StorageInstanceFactory.createInstance(config)           │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               pluginRegistry.getPrototype(identifier)                 │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               prototype.createConfiguredInstance(config)              │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               反射调用有参构造 → 创建配置化实例                         │ │
│  │                      │                                                │ │
│  │                      ▼                                                │ │
│  │               存入缓存 → 返回实例                                       │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 拦截器配置

由于在调用链中通常都会有userId,configId的传递，所以我们需要一个基于线程的获取上下文的类储存这些值，拦截器会拦截请求头中的信息放到这个类中

#### TransmittableThreadLocal 是什么？

```
┌─────────────────────────────────────────────────────────────────┐
│                 ThreadLocal 对比                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ThreadLocal                                                    │
│  ├── 每个线程独立存储                                            │
│  └── 线程池中子线程无法继承父线程的值                             │
│                                                                 │
│  InheritableThreadLocal                                         │
│  ├── 子线程可以继承父线程的值                                     │
│  └── 但线程池复用时会出问题                                       │
│                                                                 │
│  TransmittableThreadLocal（阿里开源）                            │
│  ├── 子线程可以继承父线程的值                                     │
│  ├── 线程池复用时也能正确传递                                     │
│  └── 适合异步任务场景                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 工作流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        工作流程                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  HTTP 请求到达                                                               │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 拦截器：设置上下文                                                   │   │
│  │                                                                      │   │
│  │    StoragePlatformContext context = new StoragePlatformContext(     │   │
│  │        userId, configId                                              │   │
│  │    );                                                               │   │
│  │    StoragePlatformContextHolder.setContext(context);                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Controller/Service：获取上下文                                       │   │
│  │                                                                      │   │
│  │    String userId = StoragePlatformContextHolder.getUserId();        │   │
│  │    String configId = StoragePlatformContextHolder.getConfigId();    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 异步任务：自动继承上下文（TransmittableThreadLocal 的优势）          │   │
│  │                                                                      │   │
│  │    @Async                                                           │   │
│  │    public void asyncUpload() {                                      │   │
│  │        // 子线程也能获取到 userId、configId                          │   │
│  │        String userId = StoragePlatformContextHolder.getUserId();    │   │
│  │    }                                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 拦截器：清除上下文（请求结束）                                        │   │
│  │                                                                      │   │
│  │    StoragePlatformContextHolder.clear();                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 本地存储实现（分片上传）

#### FileChannel

FileChannel 是 Java NIO 中用于文件读写的通道类，提供高效的文件操作能力

```
┌─────────────────────────────────────────────────────────────────┐
│                    FileChannel 优势                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 零拷贝：数据直接在内核层面传输，不经过用户空间               │
│                                                                 │
│  2. 高性能：比传统 IO 快 50% 以上                               │
│                                                                 │
│  3. 自动追加：outChannel 会自动追加到文件末尾                   │
│                                                                 │
│  4. 简洁代码：一行代码完成文件复制                              │
│                                                                 │
│  传统 IO 写法：                                                 │
│  byte[] buffer = new byte[8192];                                │
│  int bytesRead;                                                 │
│  while ((bytesRead = fis.read(buffer)) != -1) {                 │
│      fos.write(buffer, 0, bytesRead);                           │
│  }                                                              │
│                                                                 │
│  FileChannel 写法：                                             │
│  inChannel.transferTo(0, inChannel.size(), outChannel);         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 相关方法

*   initiateMultipartUpload() → 初始化分片上传，返回 uploadId
*   ​
*   uploadPart() → 上传单个分片，返回 eTag
*   listParts() → 列出已上传的分片
*   completeMultipartUpload() → 合并所有分片为完整文件
*   abortMultipartUpload() → 取消上传，清理临时文件

#### initiateMultipartUpload

![image-20260310111716183](https://gitee.com/Wsj123789/wsj/raw/master/img/20260310111717727.png)

初始化分片上传，创建临时目录，生成唯一的上传ID

```
D:/storage/
└── temp/
    └── a1b2c3d4e5f6/     ← uploadId 作为目录名
        ├── 0             ← 第 0 个分片
        ├── 1             ← 第 1 个分片
        └── 2             ← 第 2 个分片
```

#### uploadPart

![image-20260310111743618](https://gitee.com/Wsj123789/wsj/raw/master/img/20260310111744628.png)

构建分片文件路径，确保临时目录存在

写入分片文件（字节流读取字节数组进行写入）

生成分片标识：获取文件大小和最后修改时间

#### listParts

作用 ：

*   查询已上传的分片列表
*   用于断点续传时判断哪些分片已上传

#### completeMultipartUpload\`

![image-20260310111819121](https://gitee.com/Wsj123789/wsj/raw/master/img/20260310111849526.png)

作用 ：

*   按顺序合并所有分片为完整文件
*   使用 FileChannel.transferTo() 零拷贝高效合并
*   合并完成后删除临时目录

分片上传流程

```
// 合并分片文件
            String tempDir = getTempDir(uploadId);
            try (FileOutputStream fos = new FileOutputStream(targetFile);
                 FileChannel outChannel = fos.getChannel()) {

                // 按分片号排序
                partETags.sort((a, b) -> {
                    int partNumA = (int) a.get("partNumber");
                    int partNumB = (int) b.get("partNumber");
                    return Integer.compare(partNumA, partNumB);
                });
                // 依次读取并合并分片
                for (Map<String, Object> partInfo : partETags) {
                    int partNumber = (int) partInfo.get("partNumber");
                    String partFilePath = tempDir + partNumber; // 使用分片号作为文件名
                    File partFile = new File(partFilePath);
                    if (!partFile.exists()) {
                        throw new StorageOperationException("分片文件不存在: " + partFilePath);
                    }
                    try (FileInputStream fis = new FileInputStream(partFile);
                         FileChannel inChannel = fis.getChannel()) {
                        inChannel.transferTo(0, inChannel.size(), outChannel);
                    }
                }
            }
```

```
临时目录：
temp/{uploadId}/
├── 0  (1MB)
├── 1  (1MB)
├── 2  (1MB)
└── 3  (0.5MB)

        │
        │ 按顺序合并
        ▼

最终文件：
D:/storage/free-fs/user/xxx/test.pdf (3.5MB)
```

## 文件管理模块

### 一、上传流程

#### 1\. 前端操作

1.  选择文件 ：用户在前端选择要上传的文件
2.  获取文件信息 ：前端获取文件大小、文件名、MIME类型等信息
3.  计算文件MD5 ：前端计算文件的MD5值（用于秒传校验）
4.  计算分片数 ：根据文件大小和预设的分片大小计算总分片数

#### 2.后端调用顺序

**2.1 初始化上传任务**

```
前端 → FileTransferTaskServiceImpl.initUpload
(InitUploadCmd)
```

*   参数 ：包含文件名、文件大小、总分片数、分片大小、MIME类型、父目录ID
*   流程 ：
    
    1.  生成任务ID和临时文件名
    2.  生成唯一的objectKey
    3.  创建FileTransferTask对象并设置初始状态为 initialized
    4.  保存任务到数据库
    5.  缓存任务信息
    6.  推送初始化成功事件
    7.  返回任务ID给前端
        
        **2.2 检查上传（秒传校验）**

```
前端 → FileTransferTaskServiceImpl.checkUpload
(CheckUploadCmd)
```

*   参数 ：包含任务ID、文件MD5
*   流程 ：
    
    1.  获取任务信息
    2.  更新任务状态为 checking
    3.  推送检查中状态事件
    4.  查询是否存在相同MD5的文件
    5.  如果存在且文件真实存在，执行秒传（调用 handleQuickUpload ）
    6.  否则，调用存储服务初始化分片上传，获取uploadId
    7.  更新任务状态为 uploading
    8.  推送可以开始上传的状态事件
    9.  返回检查结果给前端
        
        **2.3 上传分片**

```
前端 → FileTransferTaskServiceImpl.uploadChunk(byte[] 
fileBytes, UploadChunkCmd)
```

*   参数 ：分片文件字节数组、任务ID、分片索引
*   流程 ：
    
    1.  异步执行 doUploadChunk 方法
    2.  doUploadChunk ：
        
        *   获取任务信息
        *   检查任务状态是否为上传中
        *   检查分片是否已上传
        *   调用存储服务上传分片
        *   缓存已上传分片信息和传输字节数
        *   推送进度事件
    3.  检查是否所有分片都已上传（调用 checkAndAutoMerge ）
    4.  如果所有分片上传完成，异步执行 doMergeChunks
        
        **2.4 合并分片**

```
FileTransferTaskServiceImpl.doMergeChunks(String 
taskId)
```

*   流程 ：
    1.  获取任务信息
    2.  验证分片是否全部上传
    3.  更新任务状态为 merging
    4.  推送合并中状态事件
    5.  调用存储服务完成分片合并
    6.  创建文件记录（FileInfo）
    7.  更新任务状态为 completed
    8.  清理缓存
    9.  推送完成事件
    10.  返回文件信息

#### 3\. 前端操作

1.  接收任务ID ：从 initUpload 获取任务ID
2.  接收检查结果 ：从 checkUpload 获取是否秒传
3.  上传分片 ：循环调用 uploadChunk 上传所有分片
4.  接收进度 ：通过SSE接收上传进度
5.  接收完成事件 ：接收上传完成事件，获取文件ID

### 二、下载流程

#### 1\. 前端操作

1.  选择文件 ：用户在前端选择要下载的文件
2.  请求下载 ：发起下载请求

#### 2\. 后端调用顺序

**2.1 初始化下载任务**

```
前端 → FileTransferTaskServiceImpl.initDownload
(InitDownloadCmd)
```

*   参数 ：包含文件ID、分片大小
*   流程 ：
    
    1.  检查并发下载任务数限制
    2.  获取文件信息
    3.  验证文件存在性和权限
    4.  计算分片总数
    5.  创建下载任务，状态为 initialized
    6.  保存任务到数据库
    7.  缓存任务信息
    8.  推送初始化成功事件
    9.  返回任务信息给前端
        
        **2.2 下载分片**

```
前端 → FileTransferTaskServiceImpl.downloadChunk
(String taskId, Integer chunkIndex)
```

*   参数 ：任务ID、分片索引
*   流程 ：
    1.  获取任务信息
    2.  验证任务类型和分片索引
    3.  计算分片的字节范围
    4.  调用存储服务下载分片
    5.  返回分片数据流给前端

#### 3\. 前端操作

1.  接收任务信息 ：从 initDownload 获取任务ID、总分片数等信息
2.  下载分片 ：循环调用 downloadChunk 下载所有分片
3.  组装文件 ：将所有分片组装成完整文件

### 三、任务管理流程

#### 1\. 暂停任务

```
前端 → FileTransferTaskServiceImpl.pauseTransfer
(String taskId)
```

*   流程 ：
    1.  获取任务信息
    2.  验证状态是否支持暂停
    3.  验证状态转换合法性
    4.  更新任务状态为 paused
    5.  推送暂停状态事件

#### 2\. 恢复任务

```
前端 → FileTransferTaskServiceImpl.resumeTransfer
(String taskId)
```

*   流程 ：
    1.  获取任务信息
    2.  验证状态是否支持恢复
    3.  根据任务类型确定目标状态（上传中/下载中）
    4.  验证状态转换合法性
    5.  更新任务状态
    6.  推送恢复状态事件

#### 3\. 取消任务

```
前端 → FileTransferTaskServiceImpl.cancelTransfer
(String taskId)
```

*   流程 ：
    1.  获取任务信息
    2.  检查任务状态是否可以取消
    3.  验证状态转换合法性
    4.  推送取消中状态事件
    5.  更新任务状态为 canceled
    6.  中止分片上传（如果是上传任务）
    7.  删除任务记录
    8.  清理缓存
    9.  推送已取消状态事件

#### 4\. 清除已完成任务

```
前端 → FileTransferTaskServiceImpl.clearTransfers()
```

*   流程 ：
    1.  查询已完成的任务
    2.  删除任务记录
    3.  清理缓存

### 四、关键状态转换流程

#### 上传任务状态转换

```
initialized → checking → uploading → merging → 
completed
              ↓          ↓          ↓
              failed     paused     failed
              ↓          ↓
              canceled   canceled
```

#### 下载任务状态转换

```
initialized → downloading → completed
              ↓
              paused
              ↓
              canceled
```

### 五、完整交互时序图

#### 上传流程时序图

1.  前端 ：选择文件，计算MD5和分片数
2.  前端 → 后端 ：调用 initUpload
3.  后端 ：创建上传任务，返回任务ID
4.  前端 → 后端 ：调用 checkUpload
5.  后端 ：检查秒传，返回检查结果
6.  前端 ：如果不是秒传，循环调用 uploadChunk 上传分片
7.  后端 ：异步处理分片上传，推送进度
8.  后端 ：所有分片上传完成，自动调用 doMergeChunks
9.  后端 ：合并分片，创建文件记录，推送完成事件
10.  前端 ：接收完成事件，显示上传成功

#### 下载流程时序图

1.  前端 ：选择文件，发起下载请求
2.  前端 → 后端 ：调用 initDownload
3.  后端 ：创建下载任务，返回任务信息
4.  前端 ：循环调用 downloadChunk 下载分片
5.  后端 ：返回分片数据流
6.  前端 ：接收分片，组装成完整文件

### 删除文件（ Spring 框架的 **事务同步机制** ）

**确保“删除物理文件”这个操作，只有在数据库事务成功提交（Commit）之后才会执行。**

```
TransactionSynchronizationManager.registerSynchronization(
        new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                for (FileInfo file : physicalFilesToDelete) {
                    try {
                        deletePhysicalFile(file);
                    } catch (Exception e) {
                        log.error("删除物理文件失败: {}", file.getObjectKey(), e);
                    }
                }
            }
        }
);
```

如果不进行这个操作的话，在删除物理文件之后，有异常出现（更新用户统计等），事务进行回滚，数据库回滚成删除前的状态，但是这时物理文件已经被删除了，造成数据不一致的问题

#### 代码工作原理

`TransactionSynchronizationManager.registerSynchronization(...)` 注册了一个回调监听器：

1.  **注册阶段**：当前代码执行时，只是把这个“删除任务”登记在册，**并不会立即执行**。
2.  **等待阶段**：主业务逻辑继续执行，直到整个数据库事务结束。
3.  触发阶段：
    *   **如果事务成功提交 (`afterCommit`)**：Spring 调用 `afterCommit()` 方法。此时，数据库变更已永久生效，代码开始遍历 `physicalFilesToDelete` 列表，真正去删除云存储上的文件。这是**安全**的。
    *   **如果事务回滚 (`afterRollback`)**：Spring **不会**调用 `afterCommit()`。那个删除物理文件的代码永远不会执行。数据库记录恢复了，物理文件也还在，数据保持一致。

## 相关条目
- [[09-源码解读/Free-fs/free-fs]]
- [[面向对象]]
