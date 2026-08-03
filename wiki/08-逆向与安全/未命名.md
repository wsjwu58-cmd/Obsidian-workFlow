# Destination

在主函数处前下断点，步入，发现程序在0x418279 的 j__initterm 函数时会退出，所以推测该点存在反调试，直接在外部将该函数nop掉

![image-20250616195142191](https://gitee.com/Wsj123789/wsj/raw/master/img/20250616195142259.png)

![image-20250616195307353](https://gitee.com/Wsj123789/wsj/raw/master/img/20250616195307384.png)

动调跟随进入0x4140D7，可以发现这里代码有混淆。动调跟踪即可发现这里是将汇编每行拆开，然后跳转到下一个地方继续执行，发现大量花指令，一种是call,ret;另一种是永真跳转。

```
#include <idc.idc>
static main()
{
    auto last_eip;
    auto eip = 0x4140D7;
    auto offset;
    auto sum = 1;
    auto just_jump = 0;
    while(Byte(eip) != 0xC3) //遇到retn指令停止
    {
        if(Byte(eip) == 0xE8 && Byte(eip+1) == 0x00 && Byte(eip+1) == 0x00 && Byte(eip+1) == 0x00 && Byte(eip+1) == 0x00)
        {   //当遇到无效call花指令
            PatchByte(eip + 0, 0x90);
            PatchByte(eip + 1, 0x90);
            PatchByte(eip + 2, 0x90);
            PatchByte(eip + 3, 0x90);
            PatchByte(eip + 4, 0x90);
            PatchByte(eip + 5, 0x90);
            PatchByte(eip + 6, 0x90);
            PatchByte(eip + 7, 0x90);
            PatchByte(eip + 8, 0x90);
            PatchByte(eip + 9, 0x90);
            //去除call和retn组成的花指令
            eip = eip + 10;
            continue;
        }
        else if(Byte(eip) == 0xE9 && just_jump == 0)
        {   //当遇到长跳转jmp指令
            offset = Byte(eip+1);
            offset = Byte(eip+2) * 256 + offset;
            offset = Byte(eip+3) * 256 * 256 + offset;
            offset = Byte(eip+4) * 256 * 256 * 256 + offset;
            eip = eip + offset;
            eip = eip + 5;
            eip = eip & 0xffffffff;
            print(eip);
            //根据opcode计算跳转地址
            sum = sum + 1;
            just_jump = 1;
            continue;
        }
        else if(Byte(eip) == 0x0F && Byte(eip+1) == 0x84 && just_jump == 0)
        {   //当遇到永恒跳转花指令
            last_eip = eip;
            offset = Byte(eip+2);
            offset = Byte(eip+3) * 256 + offset;
            offset = Byte(eip+4) * 256 * 256 + offset;
            offset = Byte(eip+5) * 256 * 256 * 256 + offset;
            eip = eip + offset;
            eip = eip + 6;
            eip = eip & 0xffffffff;
            //根据opcode计算跳转地址
            print(eip);
            sum = sum + 1;
            just_jump = 1;
            PatchByte(last_eip, 0x90);
            PatchByte(last_eip+1, 0xE9);
            //将永恒跳转花指令替换为jmp
            continue;
        }
        else if(Byte(eip) == 0xEB && just_jump == 0)
        {   //当遇到短跳转jmp指令
            offset = Byte(eip+1);
            eip = eip + offset;
            eip = eip + 2;
            // //根据opcode计算跳转地址
            print(eip);
            sum = sum + 1;
            just_jump = 1;
            continue;
        }
        else if(Byte(eip) == 0x74 && just_jump == 0)
        {   //这里应该同理，但是翻了一下没找到这个对应花指令，去的差不多就行了
            last_eip = eip;
            offset = Byte(eip+1);
            eip = eip + offset;
            eip = eip + 2;
            print(eip);
            sum = sum + 1;
            just_jump = 1;
            PatchByte(last_eip, 0xEB);
            continue;
        }
        eip = eip + 1;
        just_jump = 0;
    }
    print(sum);
    return 0;
}
```

函数代码

```
void sub_4140D7()
{
  unsigned int v1; // [esp-10Ch] [ebp-110h]
  unsigned int v2; // [esp-10Ch] [ebp-110h]
  unsigned int sum; // [esp-44h] [ebp-48h]
  unsigned int v4; // [esp-38h] [ebp-3Ch]
  int e; // [esp-20h] [ebp-24h]
  unsigned int i; // [esp-14h] [ebp-18h]
  int rounds; // [esp-8h] [ebp-Ch]
 
  rounds = 50;
  sum = 0;
  v4 = flag[11];
  do
  {
    sum -= 0x5B4B9F9E;
    e = (sum >> 2) & 3;
    for ( i = 0; i < 11; ++i )
    {
      v2 = (((v4 ^ key[e ^ i & 3]) + (flag_1[i] ^ sum)) ^ (((16 * v4) ^ (flag_1[i] >> 3)) + ((4 * flag_1[i]) ^ (v4 >> 5))))
         + flag[i];
      flag[i] = v2;
      v4 = v2;
    }
    v1 = (((v4 ^ key[e ^ i & 3]) + (flag[0] ^ sum)) ^ (((16 * v4) ^ (flag[0] >> 3)) + ((4 * flag[0]) ^ (v4 >> 5))))
       + flag[11];
    flag[11] = v1;
    v4 = v1;
  }
  while ( --rounds );
}
```

这是XXTEA加密，，执行后面的 jmp far loc_4142A7 指令后，数据又被加密，这里运用了天堂之门的技术

## 天堂之门

在64位的操作系统上，32位的应用程序并不能直接在64位环境下运行。为了使32位程序可以正常运行，操作系统提供了一个称为 **WoW64**（Windows on Windows 64-bit）的子系统。WoW64 子系统相当于一个兼容层，专门为32位程序提供了类似32位的运行环境

天堂之门 (Heaven's Gate) 是一种在32位WoW64进程中执行64位代码，以及直接调用64位WIN32 API函数的技术。从安全角度看，天堂之门可以作为一种软件保护技术，用于防止静态分析以及跨进程的API Hook；从恶意代码角度看，该技术可以绕过沙盒对WIN32 API调用的检测。

WoW64是Windows x64提供的一种兼容机制，可以认为WoW64是64位Windows系统创建的一个32位的模拟环境，使得32位可执行程序能够在64位的操作系统上正常运行

**Windows判别位的方式，是根据`cs`段寄存器的，所以只要修改`cs`的值，就能实现切换，再使用`retf`指令回到xx位**

**WoW64（Windows-on-Windows 64-bit）是微软Windows操作系统的一个子系统，它使得32位应用程序能够在64位Windows操作系统上运行。WoW64实现了对32位应用程序的透明兼容，主要通过以下方式：**

**32位程序首先调用32位`ntdll.dll`中的32位函数**

**再由`ntdll.dll`调用`wow64cpu.dll`中的`X86SwitchTo64BitMode`，就是调用该函数后进程从32位模式切换到64位模式，`wow64.dll`将32位的系统调用转化为64位**

**再调用64位`ntdll.dll`中的64位函数**

![image-20211106105559585](https://gitee.com/Wsj123789/wsj/raw/master/img/20250623201129647.png)

![image-20250623201720143](https://gitee.com/Wsj123789/wsj/raw/master/img/20250623201720181.png)

在32dbg中发现跳转实际地址是00413F77，段寄存器为33

![image-20240324104449307](https://gitee.com/Wsj123789/wsj/raw/master/img/20250623202304730.webp)

第三次加密

## XXTEA

XXTEA 加密算法原理
核心思想

分组加密：将数据分成多个 32 位无符号整数（uint32_t）块进行处理。

多轮混淆：通过多轮（通常 6 + 52/n 轮，n 是块数量）的加法、异或和移位操作，使数据充分混淆。

依赖密钥和轮次：每轮的运算都依赖于密钥和当前轮次的 sum 值。
关键变量

v：待加密/解密的数据块（uint32_t 数组）。

n：数据块的长度（单位：uint32_t）。

key：128 位密钥（4 个 uint32_t）。

DELTA：魔数 0x9E3779B9（黄金比例的 32 位整数近似）。

rounds：加密轮数，通常取 6 + 52 / n。
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/qq_74349936/article/details/147188638

加密代码

```
#include <stdint.h>
 
#define DELTA 0x9E3779B9
#define MX (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z))
 
void xxtea_encrypt(uint32_t *v, int n, uint32_t const key[4]) {
    uint32_t y, z, sum;
    unsigned p, rounds, e;
 
    if (n < 1) return;  // 数据长度必须 >= 1
 
    rounds = 6 + 52 / n;  // 计算加密轮数
    sum = 0;
    z = v[n - 1];  // 初始化 z 为最后一个元素
 
    do {
        sum += DELTA;  // sum 每轮增加 DELTA
        e = (sum >> 2) & 3;  // 计算 e，用于密钥选择
 
        // 对每个块进行处理
        for (p = 0; p < n - 1; p++) {
            y = v[p + 1];
            z = v[p] += MX;  // MX 是核心混淆运算
        }
 
        // 处理最后一个块（因为它是环状依赖的）
        y = v[0];
        z = v[n - 1] += MX;
    } while (--rounds);
}
```

解密代码

```
void xxtea_decrypt(uint32_t *v, int n, uint32_t const key[4]) {
    uint32_t y, z, sum;
    unsigned p, rounds, e;
 
    if (n < 1) return;
 
    rounds = 6 + 52 / n;
    sum = rounds * DELTA;  // 初始 sum 是加密时的最终值
    y = v[0];  // 初始化 y
 
    do {
        e = (sum >> 2) & 3;  // 计算 e
        for (p = n - 1; p > 0; p--) {  // 逆向处理
            z = v[p - 1];
            y = v[p] -= MX;
        }
        z = v[n - 1];  // 处理第一个块
        y = v[0] -= MX;
        sum -= DELTA;  // sum 递减
    } while (--rounds
```

# picstore

![image-20250627095147235](https://gitee.com/Wsj123789/wsj/raw/master/img/20250627095147291.png)

魔改的luac文件和一个lua5.3打包的elf文件

查看luaU_undump源码

![image-20250627101936389](https://gitee.com/Wsj123789/wsj/raw/master/img/20250627101936444.png)

![image-20250627102320195](https://gitee.com/Wsj123789/wsj/raw/master/img/20250627102320233.png)

程序魔改了LoadByte函数

```
 if ( (unsigned __int8)(b - 1) <= 0xFDu )      // <=> b <= 0xfe
    return ~b;
```

修复picstore.bin代码块

- 程序load代码块的核心函数有且只有 一个函数 -- LoadBlock
- 程序dump代码块的核心函数有且只有 一个函数 --DumpBlock
- 这两个函数就像堆栈一样，Load代表 push ，Dump代表 pop

我们只需要记录 LoadBlock 和 DumpBlock 函数的执行次数和函数参数，就可以知道到哪些字节被改变了

gdb-python脚本

指令

source 文件地址

执行后会在当前目录下生成 log.log日志文件

```
import gdb
import time

startt = time.time()
fp = open(r"./log.log","w")
strr = ""
def pt(p):
    global strr
    strr += p + "\n"

Esp = 0
gdb.execute('b *0x55555559C078')    # LoadBlock 断点
gdb.execute('b *0x55555559C184')    # LoadByte
gdb.execute('b *0x55555559C1D1')    # LoadInt
gdb.execute('b *0x55555559C111')    # LoadNumber
gdb.execute('b *0x55555559C0A1')    # LoadInteger

gdb.execute('r')
while 1:

    
    frame = gdb.selected_frame()
    rip = frame.read_register("rip")
    
    if rip == 0x55555559C078 :
         
        rdx = frame.read_register("rdx")
        Esp += rdx
    
    elif rip == 0x55555559C184:
        pt(f"{hex(Esp).ljust(10,' ')} => 1")
    
    elif rip == 0x55555559C1D1:
        pt(f"{hex(Esp).ljust(10,' ')} => 4")

    elif rip == 0x55555559C111:
        pt(f"{hex(Esp).ljust(10,' ')} => 8")
    
    elif rip == 0x55555559C0A1:
        pt(f"{hex(Esp).ljust(10,' ')} => 8")
    
    if Esp == 0x19f0:
        fp.write(strr)
        fp.close()
        print("finish!!!")
        enddd = time.time()
        print(enddd - startt)
        break
        
    
    gdb.execute('c')      
```

修复

```
import struct
fp = open(r"C:\Users\Administrator\Desktop\RCTF\picstore\log.log","r")
fps = open(r"C:\Users\Administrator\Desktop\RCTF\picstore\picStore.bin","rb")
fix_bin = open(r"C:\Users\Administrator\Desktop\RCTF\picstore\fix_picStore.bin","wb")
data = fp.readlines()
data_bin = fps.read()
fix_data = b""


ans = 0
for i in range(len(data)):
    op_str = data[i]
    loa = int(op_str[2:6],16) + 1
    step = int(op_str[14:15],16)  

    for j in range(ans,loa):
        fix_data += struct.pack("B",data_bin[j])

    for j in range(loa,loa + step):
        if data_bin[j] != 0 and data_bin[j] != 0xff:
            t = data_bin[j] ^ 0xff
            fix_data += struct.pack("B",t)
        else:
            fix_data += struct.pack("B",data_bin[j])
    
    ans = loa + step
fix_bin.write(fix_data)
fix_bin.close()

```

进行反编译后通过z3进行解决

# LUA

Lua 是一种轻量小巧的脚本语言，它用标准C语言编写并以源代码形式开放。这意味着什么呢？这意味着Lua虚拟机可以**很方便的嵌入别的程序里**，从而为应用程序提供灵活的扩展和定制功能。而整个Lua虚拟机编译后仅仅一百余K，经过适当的裁剪还能做到更小，十分适合嵌入式的开发。

**LUA_VERSION_MAJOR** 代表了主版本号，**LUA_VERSION_MINOR** 代表了子版本号

比如，我们的lua版本号为5.3

那么 LUAC_VERSION 就等于5*16+3=83 <=> 0x53

那么luac文件开头的第4个字节应该为 0x53

#### 检查二进制文件的格式号

if (LoadByte(S) != LUAC_FORMAT)

lua5.3.3源码给出的LUAC_FORMAT的宏定义为

```
#define LUAC_FORMAT    0    /* this is the official format */
```

这个值应该一般都为0

检查地址在开头的第5字节

#### 检查LUAC_DATA

checkliteral(S, LUAC_DATA, "corrupted");

lua5.3.3源码给出的LUAC_DATA的宏定义为

```
#define LUAC_DATA    "\x19\x93\r\n\x1a\n"
```

这个值，不同版本应该也不怎么会变

检查地址在开头的第6 ~ 11 字节，检查长度为6字节


## 相关条目
- [[花指令]]
- [[题目总结]]
- [[标志寄存器]]
