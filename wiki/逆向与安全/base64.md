# base64

具体转换步骤

    第一步，将待转换的字符串每三个字节分为一组，每个字节占8bit，那么共有24个二进制位。
    第二步，将上面的24个二进制位每6个一组，共分为4组。
    第三步，在每组前面添加两个0，每组由6个变为8个二进制位，总共32个二进制位，即四个字节。
    第四步，根据Base64编码对照表（见下图）获得对应的值。
码表

```
0　A　　17　R　　　34　i　　　51　z

1　B　　18　S　　　35　j　　　52　0

2　C　　19　T　　　36　k　　　53　1

3　D　　20　U　　　37　l　　　54　2

4　E　　21　V　　　38　m　　　55　3

5　F　　22　W　　　39　n　　　56　4

6　G　　23　X　　　40　o　　　57　5

7　H　　24　Y　　　41　p　　　58　6

8　I　　25　Z　　　42　q　　　59　7

9　J　　26　a　　　43　r　　　60　8

10　K　　27　b　　　44　s　　　61　9

11　L　　28　c　　　45　t　　　62　+

12　M　　29　d　　　46　u　　　63　/

13　N　　30　e　　　47　v

14　O　　31　f　　　48　w　　　

15　P　　32　g　　　49　x

16　Q　　33　h　　　50　y

```

实例：

![image-20250628102639503](https://gitee.com/Wsj123789/wsj/raw/master/img/20251026221004560.png)

位数不足情况

![image-20250628102804420](https://gitee.com/Wsj123789/wsj/raw/master/img/20250628102804459.png)

后面补0，没有位数的字节补=

## Python脚本解码

```
import base64
encodestr = base64.b64encode('abcr34r344r'.encode('utf-8'))
print(encodestr)
```

```
>>>
import base64
bs = 'bXMwODA2Nw== '
bbs = str(base64 .b64decode(bs)
print(bbs)
```

## 黑盒处理

特性：识别到密文的base64特征，但是不知道加密表

方法：置换法

解密：用魔改表解密标准base64码表

加密：用标准表加密密文，得到中间表

解密：再用中间表解密标准base64

加密：用标准表加密密文，结果为魔改base64表

# gcc

-pie（Position-Independent Executable）

    功能：-pie 选项是链接选项，用于生成位置无关的可执行文件（PIE）。它告诉链接器将使用 -fPIE 或 -fPIC 编译生成的目标文件链接成一个位置无关的可执行文件。
    用途：用于构建可以在任意内存地址加载和执行的可执行文件。PIE 是现代操作系统中安全机制（如 ASLR）的一部分，用于防止攻击者预测程序在内存中的布局。
    特点：
        要求：所有用于生成 PIE 的目标文件必须是用 -fPIE 或 -fPIC 编译的。
        安全性：生成的 PIE 文件可以显著提高程序的安全性，因为它们可以在每次运行时加载到不同的内存地址。



基址固定，gdb可以下断点

# tea

te[a算法](https://so.csdn.net/so/search?q=a算法&spm=1001.2101.3001.7020)的主要特征表现在sum和delta变量，以及3行核心加密中出现的右移4左移5，两行各有3个小括号互相异或

加密使用的数据为2个32位无符号整数，密钥为4个32位无符号整数即密钥长度为128位

```
#include <stdio.h>
#define uint32_t unsigned int//ubuntu下不兼容 宏替换 
//加密函数
void encrypt (uint32_t* v, uint32_t* k) {
        uint32_t v0=v[0], v1=v[1], sum=0, i; /* set up */
        uint32_t delta=0x9e3779b9; /* a key schedule constant */
        uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */
        for (i=0; i < 32; i++) { /* basic cycle start */
                sum += delta;
                v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
                v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        } /* end cycle */
        v[0]=v0; v[1]=v1;
}
//解密函数
void decrypt (uint32_t* v, uint32_t* k) {
        uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i; /* set up */
        uint32_t delta=0x9e3779b9; /* a key schedule constant */
        uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */
        for (i=0; i<32; i++) { /* basic cycle start */
                v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
                v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
                sum -= delta;
        } /* end cycle */
        v[0]=v0; v[1]=v1;
}

int main()
{
        uint32_t v[2]={1,2},k[4]={2,2,3,4};
        // v为要加密的数据是两个32位无符号整数
        // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
        printf("加密前原始数据：%u %u\n",v[0],v[1]);
        encrypt(v, k);
        printf("加密后的数据：%u %u\n",v[0],v[1]);
        decrypt(v, k);
        printf("解密后的数据：%u %u\n",v[0],v[1]);
                                                                                            }
```

# xtea

增加了更多的密钥表，移位和异或操作等等

```
#include <stdio.h>
#include <stdint.h>
#define uint32_t unsigned int//ubuntu变量类型替换


/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] - key[3] */

void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
        unsigned int i;
        uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
        for (i=0; i < num_rounds; i++) {
                v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
                sum += delta;
                v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        }
        v[0]=v0; v[1]=v1;
}

void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
        unsigned int i;
        uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;
        for (i=0; i < num_rounds; i++) {
                v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
                sum -= delta;
                v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        }
        v[0]=v0; v[1]=v1;
}

int main()
{
        uint32_t v[2]={1,2};
        uint32_t const k[4]={2,2,3,4};
        unsigned int r=32;//num_rounds建议取值为32
        // v为要加密的数据是两个32位无符号整数
        // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
        printf("加密前原始数据：%u %u\n",v[0],v[1]);
        encipher(r, v, k);
        printf("加密后的数据：%u %u\n",v[0],v[1]);
        decipher(r, v, k);
        printf("解密后的数据：%u %u\n",v[0],v[1]);
        return 0;
}

```

# xxtea

```
#include <stdio.h>
#include <stdint.h>
#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))
#define uint32_t unsigned int

void btea(uint32_t *v, int n, uint32_t const key[4])
{
        uint32_t y, z, sum;
        unsigned p, rounds, e;
        if (n > 1)            /* Coding Part */
        {
                rounds = 6 + 52/n;
                sum = 0;
                z = v[n-1];
                do
                {
                        sum += DELTA;
                        e = (sum >> 2) & 3;
                        for (p=0; p<n-1; p++)
                        {
                                y = v[p+1];
                                z = v[p] += MX;
                        }
                        y = v[0];
                        z = v[n-1] += MX;
                }
                while (--rounds);
        }
        else if (n < -1)      /* Decoding Part */
        {
                n = -n;
                rounds = 6 + 52/n;
                sum = rounds*DELTA;
                y = v[0];
                do
                {
                        e = (sum >> 2) & 3;
                        for (p=n-1; p>0; p--)
                        {
                                z = v[p-1];
                                y = v[p] -= MX;
                        }
                        z = v[n-1];
                        y = v[0] -= MX;
                        sum -= DELTA;
                }
                while (--rounds);
        }
}


int main()
{
        uint32_t v[2]= {1,2};
        uint32_t const k[4]= {2,2,3,4};
        int n= 2; //n的绝对值表示v的长度，取正表示加密，取负表示解密
        // v为要加密的数据是两个32位无符号整数
        // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
        printf("加密前原始数据：%u %u\n",v[0],v[1]);
        btea(v, n, k);
        printf("加密后的数据：%u %u\n",v[0],v[1]);
        btea(v, -n, k);
        printf("解密后的数据：%u %u\n",v[0],v[1]);
        return 0;
}                                                                    

```

# ELF文件

        ELF文件（Executable and Linking Format）是用在Linux系统下的一种目标文件（object file）存储格式。典型的目标文件有如下3类：
    
    可重定向文件（relocatable file）可重定向文件里面包含了代码和数据，用于和其他可重定向文件一起链接形成一个可执行文件或者动态库。符号为ET_REL。就是gcc加-c参数而生成的只编译不链接文件。后期还需要ld来完成重定位过程。平时很少直接用到。
    可执行文件（executable file） 可执行文件里面包含了可以运行的程序代码。符号为ET_EXEC。
    动态库文件（shared object file） 动态库文件里面也包含了可用于链接的代码和程序。符号为ET_DYN。它用于2个过程，首先链接器把它和其他可重定向文件、动态库一起链接形成一个可执行文件。然后程序运行时，动态链接器负责在需要时动态加载动态库文件。

(1) ELF是容器：装载了代码、数据和各种元数据

(2) 分层结构：ELF 头、程序头表、节区、节区头表

(3) 两种视角：

执行视角：段（Segments）- 加载器关心
链接视角：节（Sections）- 链接器关心
(4) 生命周期：从源代码到目标文件，再到可执行文件，最后变成进程

1. ELF头（ELF Header）

ELF 头是整个文件的"门面"，包含了文件的基本信息和指向其他部分的指针。用readelf -h命令可以查看：

Entry point address：程序执行的入口点地址
Start of program headers：程序头表的位置
Start of section headers：节区头表的位置
2. 程序头表（Program Header Table）

程序头表告诉操作系统如何创建进程映像，用readelf -l命令查看：

3. 节区头表（Section Header Table）

节区头表描述了文件中各个节区的信息，用readelf -S查看：

# VA，IMAGEBase，RVA，FA初步了解

ImageBase:表示基准地址，表示PE文件（DLL文件为主）加载到进程的虚拟内存时的特定位置

VA，虚拟地址，也就是程序被加载到内存中的地址

RVA，以虚拟地址前边加上个“相对的”，也就是说它还是按虚拟地址来换算，只不过不是从0开始，而是把一个模块的基址作为参考点。

VA与RVA满足下面的换算关系:

RVA + ImageBase = VA

PE（Portable Executable）头部信息大多以RVA形式存在。原因在于，PE文件（主要是DLL（DLL，Dynamic Linked Library））加载到进程虚拟内存的特定位置时，该位置可能已经加载了其它PE文件（DLL）。此时必须通过重定位（Relocation）将其加载到其它空白的位置，若PE头信息使用的是VA，则无法正常访问。因此，使用RVA来定位信息，即使发生了重定位，只要相对于基准位置的相对地址没有变化，就能正常访问到指定信息，不会出现任何问题。

FA（File Address，文件地址）：指的是可执行文件在存储设备（如硬盘）上的地址。它是文件在存储介质中的偏移量，用于标识文件中的特定位置。在分析可执行文件的结构或者进行文件操作时，需要使用 FA 来定位文件中的数据。与虚拟地址不同，FA 是基于文件系统的地址，而虚拟地址是在程序运行时操作系统为程序分配的内存地址。



## 相关条目
- [[题目总结]]
