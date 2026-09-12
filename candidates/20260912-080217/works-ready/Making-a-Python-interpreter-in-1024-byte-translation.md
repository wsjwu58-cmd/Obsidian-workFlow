---
created: 2026-09-12
updated: 2026-09-12
title: 用 1024 字节写一个 Python 解释器
sourceUrl: https://austinhenley.com/blog/python1024.html
sourceAuthor: Austin Z. Henley
translatedAt: 2026-09-12
sources: [references/articles.md 待处理队列]
tags: [C, Python, 解释器, 递归下降解析, 代码高尔夫, 编译器, type/翻译]
---

# 用 1024 字节写一个 Python 解释器

2026/9/6

![1024 字节高尔夫版 C 代码的截图。](https://austinhenley.com/blog/images/python1024.png)

_关于本文的讨论见 [Hacker News](https://news.ycombinator.com/item?id=49591876)、[r/programming](https://www.reddit.com/r/programming/comments/1w9c0an/making_a_python_interpreter_in_1024_bytes/) 和 [Lobste.rs](https://lobste.rs/s/n0zgj1/making_python_interpreter_1024_bytes)。_

为了保持「人味」，我会在周末**亲手**写代码。

我最近的一次挑战？用~~512~~1024 字节的「老派好 C 代码」写一个 Python 解释器。哦对，不许玩宏的骚操作，也不许耍库的鬼把戏。

```py
def buzz():
    for n in range(101):
        if n % 15 == 0:
            print("FizzBuzz")
        else:
            if n % 3 == 0:
                print("Fizz")
            else:
                if n % 5 == 0:
                    print("Buzz")
                else:
                    print(n)
buzz()
```

我大概没法把 Python 语言的_全部_塞进一个只有 1024 字节代码的解释器里。那么，我能塞进哪些东西，让它_看起来_像 Python 呢？

这段 fizzbuzz 程序看上去就很有 Python 味。它带着 _def_、冒号、缩进，_if_ 语句还不用括号。在我看来就是 Python！当然，除了只实现语法的一个子集之外，我还得再加上一些额外的限制。

不过我的第一次尝试很糟糕。

### 第一次尝试：512 字节根本不够！

我写过很多递归下降解析器，这能跟以前有多大差别？Python 的一个子集，应该和我实现过的其他语言（比如我的 [Teeny Tiny](https://austinhenley.com/blog/teenytinycompiler1.html) 编译器）差不多。

我从能想到的最基础的代码开始：**1 + 2**

然后我把它弄得更复杂一点：**x = 1 + 2 \* 3**

接着我甚至加上了语句：**if x > y: z = 3**

很好，我做了一个计算器……这可不是我这个挑战的本意！而且我已经超限了。就在那时，我退后一步，列出了一份「看起来像 Python」的元素清单，同时也意识到自己的代码高尔夫水平还达不到把它塞进 512 字节的程度。

也许我能在 1024 字节里做到？先让它跑起来，再让它变小。

### 解析器

真正的 [CPython](https://github.com/python/cpython) 实现会对 Python 源码做词法分析（tokenize），把它解析成抽象语法树，做一些分析与优化，生成字节码，然后解释执行字节码。

我这个解释器这些事基本都不做。

状态保存在寥寥几个全局变量里。它用一个定长数组（目前是 999）来存放原始 Python 代码。变量名和函数名则全都塞进同一个数组里。

```c
char src[999];       /* 去掉大部分空格后的整个程序。 */
int  vars[256];      /* 符号表。                     */
int  pos;            /* src 中的下一个字符。         */
int  ch;             /* src 中的当前字符。           */
int  line_start;     /* 当前行的起始位置。           */
```

表达式的处理和其他任何递归下降解析器一样，而且在解析的同时就被执行了。例如：

```c
int parse_sum(void) {
    int value = parse_term();
    while (ch == '+' || ch == '-') {
        if (ch == '+')
            value = value + parse_term();
        else
            value = value - parse_term();
    }
    return value;
}
```

到目前为止都很直白。

没有任何形式的错误处理！它对代码的正确性做了**大量**假设。比如，它假定所有关键字都拼写正确。

```c
    if (ch == 'w' || ch == 'i' || ch == 'f') {
        int keyword = ch;
        int loop_var = 0;

        if (keyword == 'f') {        /* "for K in range(N):" */
            pos += 2;                /* 跳过 "or"。          */
            loop_var = next();
            pos += 8;                /* 跳过 "inrange("。     */
            vars[loop_var] = 0;
        } else if (keyword == 'w')
            pos += 4;                /* 跳过 "hile"。        */
        else
            pos += 1;                /* 跳过 "if" 的 "f"。    */
```

它还假定 token 的边界都是正确的，并剥掉了大部分空白字符。它会保留缩进，以及字符串字面量内部的空格。

它只支持单个小写字符的变量名，这样就能直接做符号表查找：

```c
    if (ch > 96) {
        value = vars[ch];
        next();
    }
```

### 控制流的魔法

执行代码块的函数会一直执行，直到缩进变小为止。一旦发生这种情况，它就返回，由调用方来接管下一行。也就是说，它借助 C 程序自身的调用栈来处理递归。

```c
void run_block(int min_indent) {
    for (;;) {
        int indent = read_indent();

        if (ch == '\n')
            continue;

        if (indent < min_indent || ch == 0) {
            pos = line_start;
            return;
        }
```

那循环怎么办？！

由于什么都没有编译，循环是靠每次迭代都向后跳转、重新解析源码来实现的。_while_ 和 _for_ 循环都记着条件表达式所在的位置。循环体执行完后，就跳回那个位置继续解析。

函数的做法也一样。解析函数定义时，符号表会记下函数在源码中的位置。之后解析函数调用时，先保存调用点的位置，解析器跳到函数体，执行完函数体，在到达末尾时再恢复调用点的位置。

即便没有任何中间表示，我们能做到的事情也相当漂亮！而且这个解释器维护的状态也非常少。

### 压缩瘦身！

我没怎么玩过代码高尔夫。缩减变量名和空白字符是显而易见的，但那些大头字节要从哪里省呢？

有一个古老而被遗忘的网站叫 Stack Overflow，往昔的代码魔法师们曾在那里分享知识。我从 [《Tips for golfing in C》](https://codegolf.stackexchange.com/questions/2203/tips-for-golfing-in-c) 里学到了很多点子。

![Stack Overflow 上代码高尔夫技巧帖的截图。](https://austinhenley.com/blog/images/codegolfingtips.png)

既然规则只存在于你自己的想象里，我就不得不发挥点创造力。其中有些技巧依赖 GNU C89 特有的「特性」。这**不是**鬼把戏！这是老派的小打小闹。下面是我为了从可读版里抠掉字节所做的操作：

- 变量名和函数名都用单个字母
- 假定编译器会链接 libc
- 用全局变量充当临时变量
- 全局变量会被零初始化
- C89 允许变量声明隐式为 int，函数也被默认为返回 int
- 把函数参数当作保存在调用栈上的临时变量
- 用 ASCII 数值代替字符字面量
- 三元运算符与逗号运算符
- 用位运算代替逻辑运算

比如，我前面展示的 _parse\_sum(void)_ 函数，被高尔夫成了 _e(){for(z=t();c-43u<3;)y=44-c,z+=y\*t();return z;}_。它用 ASCII 数值抠掉了几个字节。

另一个例子是一个跳到行尾的辅助函数：

```c
void skip_to_eol(void) {
  if (ch != 0 && ch != '\n') {
    next();
    skip_to_eol();
  }
}
```

我把它压到了：_Y(){c&&c-10&&Y(G());}_。它检查是否为 0，减去 10 来判断换行，并用 _&&_ 代替 _if_。接着它用 _Y(G());_ 而不是 _G();Y();_，又省下了一个字节。真巧妙！再次感谢那篇 Stack Overflow 帖子。

一番折腾之后，高尔夫版正好是 **1024** 字节！

最终的可读版超过 4800 字节。我原本还加了好几个特性，但为了能塞进去，只能不停地砍。比较表达式本来是下一个要砍的对象，因为它占掉很多字节，而且没有它真值性依然能工作：_if n%15:_。

如果我只在乎让 fizzbuzz 跑起来，我觉得我能压到 800 字节以下！大概还有别的压缩技巧可用。

![终端里检查高尔夫版代码字节数、编译它并运行的截图。](https://austinhenley.com/blog/images/python1024running.png)

下面就是高尔夫版源码，请欣赏它的全貌：

```c
char s[999];v[256],p,c,x,y,z,w,u;G(){return c=s[p++];}I(){for(u=p;G()==32;);return p-u;}Y(){c&&c-10&&Y(G());}f(){x=0;if(G()>96)x=v[c],G();for(;c-48u<10;G())x=x*10+c-48;return x;}t(g,h){for(g=f();c==42|c==37;)h=c,g=h-42?g%f():g*f();return g;}e(){for(z=t();c-43u<3;)y=44-c,z+=y*t();return z;}E(a,q){a=e();if(c-60u>2)return a;w=c-61;q=G()==61;p-=!q;x=e();return w?(a-x)*w>-q:a==x;}S(i){for(;I()>i|c==10;)Y();p=u;}Q(){for(G();G()-34;)putchar(c);G();}B(i,q,j,k,a,m,n){for(;;){j=I();if(c==10)continue;if(j<i|!c){p=u;return;}if(c==119|c==105|c==102){k=c;k-102?p+=k/4-25:(p+=2,m=G(),p+=8,v[m]=0);q=p;for(;;){a=k-102?E():v[m]<E();p+=k==102;G();if(!a){S(j);break;}B(j+1);if(k==105)break;k-102||v[m]++;p=q;}I()-j|c-101?p=u:(p+=4,G(),a?S(j):B(j+1));}else if(c==100){p+=2;k=G();Y();v[k]=p;S(j);}else{if(c>96){k=c;while(G()>96);c==40?k-112?(G(),n=p,p=v[k],B(2),p=n,G()):(s[p]-34?printf("%d",E()):Q(),puts(""),G()):(v[k]=E());}Y();}}}main(q,m,h){for(h=m=q=0;~(c=getchar());){c=c-9?c:32;h^=c==34;s[q]=c;q+=c-32?1:!m|h;m=c>32|m&&c-10;}B(0);}
```

最终，我实现了这些特性：

- 整数变量（单个字母）与整数字面量
- 变量赋值
- 支持 + - \* % 与优先级（一元 + - 只能在表达式开头使用）
- 支持 < > <= >= == 比较（每个表达式只能有一个）
- 整数真值性
- _if_ 与 _else_
- _while_ 循环，包括 _else_ 块
- _for x in range(y)_ 循环，包括 _else_ 块
- 无参数的函数定义
- 函数调用，甚至支持递归
- 基于缩进的代码块（不带作用域）
- _print_ 单个字符串字面量或整数表达式
- 注释

我觉得近期我不会再碰任何代码高尔夫挑战了。这个过程相当枯燥：要在进行中的高尔夫版和原始版之间来回切换，只为搞明白自己两分钟前改了什么。两个版本都在 [GitHub](https://github.com/AZHenley/python1024) 上。

现在轮到你了。你的 1024 字节 Python 长什么样？
