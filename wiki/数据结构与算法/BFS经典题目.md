# BFS经典题目

## 题目描述

呵呵，有一天我做了一个梦，梦见了一种很奇怪的电梯。大楼的每一层楼都可以停电梯，而且第 i*i* 层楼（1≤i≤N1≤*i*≤*N*）上有一个数字 Ki*K**i*（0≤Ki≤N0≤*K**i*≤*N*）。电梯只有四个按钮：开，关，上，下。上下的层数等于当前楼层上的那个数字。当然，如果不能满足要求，相应的按钮就会失灵。例如： 3,3,1,2,53,3,1,2,5 代表了 Ki*K**i*（K1=3*K*1=3，K2=3*K*2=3，……），从 11 楼开始。在 11 楼，按“上”可以到 44 楼，按“下”是不起作用的，因为没有 −2−2 楼。那么，从 A*A* 楼到 B*B* 楼至少要按几次按钮呢？

## 输入格式

共二行。

第一行为三个用空格隔开的正整数，表示 N,A,B*N*,*A*,*B*（1≤N≤2001≤*N*≤200，1≤A,B≤N1≤*A*,*B*≤*N*）。

第二行为 N*N* 个用空格隔开的非负整数，表示 Ki*K**i*。

## 输出格式

一行，即最少按键次数，若无法到达，则输出 `-1`。

## 思路

从楼层的A开始，有两种选择，上升或下降，上升或下降的数字取决于所处楼层的数字，求最短到达B层的次数。

我们可以用cur记录当前所在层数,visited数组记录按按钮的次数，nx表示下一个所能到达的楼层，使用队列来存储nx，每次用cur取出队头，在K[]数组(就是题目中的Ki)中找到当前层数对应的数字，然后加减该楼层，反复遍历，直到达到层数B,退出循环，如果到不了，输出-1。

源代码:

```
#include<bits/stdc++.h>
using namespace std;
int main(){
	int N,A,B,K[100001],visited[100001],a[2]={1,-1};
	cin>>N>>A>>B;
	for(int i=1;i<=N;i++)
	cin>>K[i];
	queue <int>que;
	que.push(A);
	visited[A]=1;
	while(!que.empty()){
		int cur=que.front();
		for(int i=0;i<=1;i++){
			int nx=K[cur]*a[i]+cur;
			if(nx>=1&&nx<=N&&visited[nx]==0){
				visited[nx]=visited[cur]+1;
				if(nx==B){
					cout<<visited[nx]-1;
					goto end_loop;
				}
				que.push(nx);
			}
		}
		que.pop();
	}
	cout<<-1;
	end_loop:
	return 0;
}
```

but：如果只是这样的话，会有一种情况被排除在外--->A=B,所以，还应加上这一段代码：

```
	if (A == B) {  
        cout << 0 << endl;
        return 0;
    }
```

这样就大功告成了

AC测评

![image-20250526170035069](https://gitee.com/Wsj123789/wsj/raw/master/img/20250526170035139.png)

## 相关条目
- [[DP动态规划]]
- [[图结构的应用]]
- [[题目总结]]
