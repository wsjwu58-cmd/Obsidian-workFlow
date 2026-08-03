# 一、逻辑存储结构

![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250826102421582.png)

表空间（ibd文件），一个mysql实例可以对应多个表空间，用于存储记录、索引等数据。
段，分为数据段（Leaf node segment）、索引段（Non-leaf node segment）、回滚段（Rollback segment），InnoDB是索引组织表，数据段就是B+树的叶子节点， 索引段即为B+树的非叶子节点。段用来管理多个Extent（区）。
区，表空间的单元结构，每个区的大小为1M。 默认情况下， InnoDB存储引擎页大小为16K， 即一个区中一共有64个连续的页。
页，是InnoDB 存储引擎磁盘管理的最小单元，每个页的大小默认为 16KB。为了保证页的连续性，InnoDB 存储引擎每次从磁盘申请 4-5 个区。
行，InnoDB 存储引擎数据是按行进行存放的。
Trx_id：每次对某条记录进行改动时，都会把对应的事务id赋值给trx_id隐藏列。
Roll_pointer：每次对某条引记录进行改动时，都会把旧的版本写入到undo日志中，然后这个隐藏列就相当于一个指针，可以通过它来找到该记录修改前的信息。

# 二、架构

MySQL5.5 版本开始，默认使用InnoDB存储引擎，它擅长事务处理，具有崩溃恢复特性，在日常开发中使用非常广泛。下面是InnoDB架构图，左侧为内存结构，右侧为磁盘结构。
![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250826102459745.png)

### 1、内存架构

- **Buffer Pool**：缓冲池是主内存中的一个区域，里面可以缓存磁盘上经常操作的真实数据，在执行增删改查操作时，先操作缓冲池中的数据（若缓冲池没有数据，则从磁盘加载并缓存），然后再以一定频率刷新到磁盘，从而减少磁盘IO，加快处理速度。

![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250826102526023.png)

**缓冲池以Page页为单位，底层采用链表数据结构管理Page。**根据状态，将Page分为三种类型：
• free page：空闲page，未被使用。
• clean page：被使用page，数据没有被修改过。
• dirty page：脏页，被使用page，数据被修改过，也中数据与磁盘的数据产生了不一致。

Change Buffer：更改缓冲区（针对于非唯一二级索引页），在执行DML语句时，如果这些数据Page 没有在Buffer Pool中，不会直接操作磁盘，而会将数据变更存在更改缓冲区 Change Buffer 中，在未来数据被读取时，再将数据合并恢复到Buffer Pool中，再将合并后的数据刷新到磁盘中。
Change Buffer的意义是什么? 与聚集索引不同，二级索引通常是非唯一的，并且以相对随机的顺序插入二级索引。同样，删除和更新可能会影响索引树中不相邻的二级索引页，如果每一次都操作磁盘，会造成大量的磁盘IO。有了ChangeBuffer之后，我们可以在缓冲池中进行合并处理，减少磁盘IO。
Adaptive Hash Index：自适应hash索引，用于优化对Buffer Pool数据的查询。InnoDB存储引擎会监控对表上各索引页的查询，如果观察到hash索引可以提升速度，则建立hash索引，称之为自适应hash索引。
**Log Buffer**：日志缓冲区，用来保存要写入到磁盘中的log日志数据（redo log 、undo log），默认大小16MB，日志缓冲区的日志会定期刷新到磁盘中。如果需要更新、插入或删除许多行的事务，增加 日志缓冲区的大小可以节省磁盘 I/O。

### 2、磁盘架构

- **System Tablespace**：系统表空间是更改缓冲区(change buffer)的存储区域。如果表是在系统表空间而不是每个表文件或通用表空间中创建的，它也可能包含表和索引数据。(在MySQL5.x版本中还包含InnoDB数据字典、undolog等)

- **File-Per-Table Tablespaces**：每个表的文件表空间包含单个InnoDB表的数据和索引 ，并存储在文件系统上的单个数据文件中。

- **General Tablespaces**：通用表空间，需要通过 CREATE TABLESPACE 语法创建通用表空间，在创建表时，可以指定该表空间。(需要自己创建，自己指定)

```
#创建通用表空间
create tablespace ts_name datafile 'file_name.ibd' engine =engine_name;

#创建表时指定
create table table_name(...)tablespace ts_name;


```

- **Undo Tablespaces**：撤销表空间，MySQL实例在初始化时会自动创建两个默认的undo表空间（初始大小16M），用于存储undo log日志。

- **Temporary Tablespaces**：InnoDB 使用会话临时表空间和全局临时表空间。存储用户创建的临时表等数据。

- **Doublewrite Buffer Files**：双写缓冲区，innoDB引擎将数据页从Buffer Pool刷新到磁盘前，先将数据页写入双写缓冲区文件中，便于系统异常时恢复数据。

- **Redo Log：**重做日志，是用来实现事务的持久性。该日志文件由两部分组成：重做日志缓冲（redo log buffer）以及重做日志文件（redo log）,前者是在内存中，后者在磁盘中。当事务提交之后会把所有修改信息都会存到该日志中, 用于在刷新脏页到磁盘时,发生错误时, 进行数据恢复使用。

  

### 3、后台线程

![负责内存和磁盘的数据传输](https://gitee.com/Wsj123789/wsj/raw/master/img/20250826172930130.png)

```
#查看innodb引擎的状态信息
show engine innodb status;

```

Master Thread
核心后台线程，负责调度其他线程，还负责将缓冲池中的数据异步刷新到磁盘中, 保持数据的一致性，还包括脏页的刷新、合并插入缓存、undo页的回收 。

IO Thread
在InnoDB存储引擎中大量使用了AIO来处理IO请求, 这样可以极大地提高数据库的性能，而IO Thread主要负责这些IO请求的回调。
Purge Thread
主要用于回收事务已经提交了的undo log，在事务提交之后，undo log可能不用了，就用它来回收。

Page Cleaner Thread
协助 Master Thread 刷新脏页到磁盘的线程，它可以减轻 Master Thread 的工作压力，减少阻塞。

# 三、事务原理

事务 是一组操作的集合，它是一个不可分割的工作单位，事务会把所有的操作作为一个整体一起向系统提交或撤销操作请求，即这些操作要么同时成功，要么同时失败。

**特性ACID**
• 原子性（Atomicity）：事务是不可分割的最小操作单元，要么全部成功，要么全部失败。
• 一致性（Consistency）：事务完成时，必须使所有的数据都保持一致状态。
• 隔离性（Isolation）：数据库系统提供的隔离机制，保证事务在不受外部并发操作影响的独立环境下运行。
• 持久性（Durability）：事务一旦提交或回滚，它对数据库中的数据的改变就是永久的。

其中，原子性，一致性，持久性是由redo log文件与undo log文件保证的。
隔离性是由锁和MVCC保证的

**redo log** 重做日志，记录的是事务提交时数据页的物理修改，是用来实现事务的持久性。 该日志文件由两部分组成：重做日志缓冲（redo log buffer）以及重做日志文件（redo log file）,前者是在内存中，后者在磁盘中。当事务提交之后会把所有修改信息都存到该日志文件中, 用于在刷新脏页到磁盘,发生错误时, 进行数据恢复使用。

**undo log**保证事务的原子性 回滚日志，用于记录数据被修改前的信息 , 作用包含两个 : 提供回滚 和 MVCC(多版本并发控制)

undo log和redo log记录物理日志不一样，它是逻辑日志。可以认为当delete一条记录时，undo log中会记录一条对应的insert记录，反之亦然，当update一条记录时，它记录一条对应相反的update记录。当执行rollback时，就可以从undo log中的逻辑记录读取到相应的内容并进行回滚。

**Undo log销毁**：undo log在事务执行时产生，事务提交时，并不会立即删除undo log，因为这些日志可能还用MVCC。

**Undo log存储**：undo log采用段的方式进行管理和记录，存放在前面介绍的 rollback segment 回滚段中，内部包含1024个undo log segment。

# 四、MVCC

当前读：读取的是记录的最新版本，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁。对于我们日常的操作，如：select
… lock in share mode(共享锁)，select … for
update、update、insert、delete(排他锁)都是一种当前读。

快照读：简单的select（不加锁）就是快照读，快照读，读取的是记录数据的可见版本，有可能是历史数据，不加锁，是非阻塞读。

• Read Committed：每次select，都生成一个快照读。
• Repeatable Read：开启事务后第一个select语句才是快照读的地方。
• Serializable：快照读会退化为当前读。
MVCC：全称 Multi-Version Concurrency Control，多版本并发控制。指维护一个数据的多个版本，使得读写操作没有冲突，快照读为MySQL实现MVCC提供了一个非阻塞读功能。MVCC的具体实现，还需要依赖于数据库记录中的三个隐式字段、undo log日志、readView。
**三个隐式字段**

| 隐藏字段    | 含义                                                         |
| ----------- | ------------------------------------------------------------ |
| DB_TRX_ID   | 最近修改事务ID，记录插入这条记录或最后一次修改该记录的事务ID。 |
| DB_ROLL_PTR | 回滚指针，指向这条记录的上一个版本，用于配合undo log，指向上一个版本。 |
| DB_ROW_ID   | 隐藏主键，如果表结构没有指定主键，将会生成该隐藏字段。       |

undo log
回滚日志，在insert、update、delete的时候产生的便于数据回滚的日志。

```
当insert的时候，产生的undo log日志只在回滚时需要，在事务提交后，可被立即删除。
而update、delete的时候，产生的undo log日志不仅在回滚时需要，在快照读时也需要，不会立即被删除。
```

![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250827103152075.png)

**不同事务或相同事务对同一条记录进行修改，会导致该记录的undolog生成一条记录版本链表，链表的头部是最新的旧记录，链表尾部是最早的旧记录。**

readview
ReadView（读视图） 是 快照读 SQL执行时MVCC提取数据的依据，记录并维护系统当前活跃的事务（未提交的）id。ReadView中包含了四个核心字段：

| 字段           | 含义                                                 |
| -------------- | ---------------------------------------------------- |
| m_ids          | 当前活跃的事务ID集合                                 |
| min_trx_id     | 最小活跃事务ID                                       |
| max_trx_id     | 预分配事务ID，当前最大事务ID+1（因为事务ID是自增的） |
| creator_trx_id | ReadView创建者的事务ID                               |

**版本链数据访问规则**

不同的隔离级别，生成ReadView的时机不同：
➢ READ COMMITTED ：在事务中每一次执行快照读时生成ReadView。

![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250827103231091.png)

![在这里插入图片描述](https://gitee.com/Wsj123789/wsj/raw/master/img/20250827103339517.png)

REPEATABLE READ：仅在事务中第一次执行快照读时生成ReadView，后续复用该ReadView。

**决定快照读记录版本的方法**
按照undo log文件的记录，结合ReadView，判断是否满足版本链数据访问规则，如果符合其中一条规则，则代表快照读读的就是这个版本


## 相关条目
- [[进阶]]
- [[Mysql]]
