---

---

# C++模板和STL

## 1.模板

### 1.1 函数模板

建立一个通用函数，其函数返回值类型和形参类型可以不具体制定，用一个虚拟的类型来代表。

#### 语法

```
template<typename T>
函数声明或定义
```

template----声明创建模板

typename ---其后面的符号是一种数据类型，可以用class代替

1. ```c++
   #include<iostream>
   using namespace std;
   template<class T>
   void myswap(T&a,T&b){
       int temp=a;
       a=b;
       b=temp;
   }
   //必须推导出一致的数据类型T
   void text(){
       int a=10;
       int b=20;
       myswap(a,b);
       cout<<a<<b;
   }
   int main(){
       text();
       system("pause");
   }
   ```

#### 注意事项

函数模板不能直接进行隐式转换，如果一定要转换，在调用时表明数据类型。

```
template<class T>
T mysum(T a,T b){
    return a+b;
}
void text(){
    int a=10;
    int b=10;
    char c='a';
    cout<<mysum<int>(a,c)  <<endl;
}
```

#### 普通函数与函数模板调用规则

1.若两者都可以调用，优先调用普通函数；

2.可以通过空模板强制调用函数模板；

3.函数模板可以发生函数重载；

4.如果函数模板可以产生更好的匹配，优先调用函数模板。

### 1.2 类模板

#### 1.2.1语法

```
template<typename T>
类
```

template----声明创建模板

typename ---其后面的符号是一种数据类型，可以用class代替

T--通用的数据类型，名称可以替换，通常为大写字母

```
template<class NameType,class agetype>
class person {
public:
	person(NameType name, agetype age) {
		this->m_name = name;
		this->m_age = age;
	}
	void showperson() {
		cout << this->m_name << endl;
		cout << this->m_age << endl;
	}
	NameType m_name;
	agetype m_age;
};
void text01() {
	person<string, int>p1("张三", 666);
	p1.showperson();
}
```



#### 1.2.2类模板和函数模板的区别

1.类模板没有主动推导的使用方式

2.类模板在模板参数列表中可以有默认参数

```
template<class NameType,class agetype=int>
class person {
public:
	person(NameType name, agetype age) {
		this->m_name = name;
		this->m_age = age;
	}
	void showperson() {
		cout << this->m_name << endl;
		cout << this->m_age << endl;
	}
	NameType m_name;
	agetype m_age;
};
//类模板没有自动推导使用方式
void text01() {
	person<string,int> p("孙悟空", 22);//只能用显示制定类型
}
//类模板在模板参数列表中可以有默认参数
void text02() {
	person<string>p("孙悟空", 222);
}
```

#### 1.2.3 类模板中成员函数创建时机

普通类中的成员函数一开始就可以创建

类模板中的成员函数在调用时才创建

```
//类模板中成员函数的创建时机
class person1 {
public:
	void showperson1() {
		cout << "person11show" << endl;
	}
};
class person2 {
public:
	void showperson2() {
		cout << "person21show" << endl;
	}
};
template<class T>
class myclass {
public:
	T obj;
	//类模板中的成员函数
	void func1() {
		obj.showperson1();
	}
	void func2() {
		obj.showperson2();
	}
};
void text01() {
	myclass<person1>m;
	m.func1();
}
```

#### 1.2.4 类模板对象做函数参数

1.指定传入类型（最常用）

2.参数模板化

3.整个类模板化

```
template<class T1,class T2>
class person {
public:
	person(T1 name, T2 age) {
		this->m_name = name;
		this->m_age = age;
	}
	void showinfo() {
		cout << this->m_age << this->m_name << endl;;
	}
	T1 m_name;
	T2 m_age;
};
//1.指定传入类型
void printmm(person<string, int>& p) {
	p.showinfo();
}
//2.参数模板化
template<class T1, class T2>
void printperson2(person< T1, T2>&p) {
	p.showinfo();
	cout << "T1的类型" << typeid(T1).name() << endl;
	cout << "T2的类型" << typeid(T2).name() << endl;
}
//3.整个类模板化
template<class T>
void printperson3(T& p) {
	p.showinfo();
	cout << "T的数据类型" << typeid(T).name() << endl;
}
void text01() {
	person<string, int>p("孙悟空", 555);
	printmm(p);
}
void text02() {
	person<string, int>p1("猪八戒", 555);
	printperson2(p1);
}
void text03() {
	person<string, int>p1("唐僧", 555);
	printperson3(p1);
}
```

#### 1.2.5 类模板与继承

当类模板继承时，注意以下几点：

- 子类需提供T的类型
- 如果想灵活指定父类中T的类型，子类也需要变类模板

```
template<class T>
class base {
public:
	T m;
};

class Son :public base<int> {
public:
};
void text01() {
	Son a;

}
//如果想灵活指定父类中T的类型，子类也需要变类模板
template<class T1,class T2>
class Son2 :public base<T2> {
public:
	Son2(){
	cout << "T1的类型" << typeid(T1).name() << endl;
	cout << "T2的类型" << typeid(T2).name() << endl; }
	T1 obj;
};
void text02() {
	Son2<int, char>s2;//将char传给上面的T2，再传到父类的T中
}
```

#### 1.2.6 类模板成员函数的类外实现

```
template<class T1,class T2>
class person {
public:
	person(T1 name, T2 age);

	void showinfo();

	T1 m_name;
	T2 m_age;
};
//构造函数的类外实现
template<class T1, class T2>
person<T1,T2>::person(T1 name, T2 age) {
	this->m_name = name;
	this->m_age = age;
}
//成员函数的类外实现
template<class T1, class T2>
void person<T1, T2>::showinfo(){
	cout << "姓名：" << this->m_name
		<< "年龄：" << this->m_age;
}
void text01() {
	person<string, int>p1("张三",666);
	p1.showinfo();
}
```

#### 1.2.7 类模板分文件编写

由于类模板成员函数在调用时才会创建，所以编译.h头文件时会识别不了里面的成员函数

第一种解决方式：直接包含源文件
第二种解决方式，将.h和.cpp内容写到一起，将后缀名改成.hpp文件

```
#pragma once
#include<iostream>
using namespace std;
#include<string>
template<class T1, class T2>
class person {
public:
	person(T1 name, T2 age);

	void showinfo();

	T1 m_name;
	T2 m_age;
};
template<class T1, class T2>
person<T1, T2>::person(T1 name, T2 age) {
	this->m_name = name;
	this->m_age = age;
}
//成员函数的类外实现
template<class T1, class T2>
void person<T1, T2>::showinfo() {
	cout << "姓名：" << this->m_name
		<< "年龄：" << this->m_age;
}
```

#### 1.2.8 类模板和友元

```
//通过全局函数打印person 信息
//全局函数配合友元，类外实现-先做函数模板声明，在做函数模板定义，在做友元
template<class T1, class T2>
class person;
//类外实现
//定义时可以先声明，然后可以在后面定义
template<class T1, class T2>
void printperson2(person<T1, T2>& p);
template<class T1,class T2>
class person {
	//全局函数类内实现
	friend void printperson(person<T1,T2>p) {
		cout << p.m_name << p.m_age;
	}
	//空模板实现
	friend void printperson2<>(person<T1, T2>&p);
public:
	person(T1 name, T2 age) {
		this->m_name = name;
		this->m_age = age;
	}
private:
	T1 m_name;
	T2 m_age;
};
//1.全局函数类内实现
void text01() {
	person<string, int>p("nub", 22);
	printperson(p);
}
//2.全局函数类外实现
template<class T1, class T2>
void printperson2(person<T1, T2>& p) {
	cout << "类外实现" << p.m_name << p.m_age;
}
void text02() {
	person<string, int>p("tom", 33);
	printperson2(p);
}
```

#### 1.2.9 类模板案例

- 对内置数据类型以及自定义数据类型的数据进行存储

- 将数组中的数据存储到堆区

- 构造函数中可以传入数组的容量

- 提供相应的拷贝构造函数以及operator=防止浅拷贝问题

- 提供尾插法和尾删法对数组的数据进行增加和删除

- 可以通过下标的方式访问数组中的元素

- 可以获取数组中当前元素个数和数组的容量

  Myarray.hpp

  ```
  #pragma once
  #include<iostream>
  using namespace std;
  template<class T>
  class Myarray {
  public:
  	Myarray(int rong) {
  	/*	cout << "有参构造调用" << endl;*/
  		this->m_rong = rong;
  		this->m_size = 0;
  		this->paddress = new T[this->m_rong];
  	}
  	//拷贝构造
  	Myarray(const Myarray &arr) {
  		//cout << "拷贝构造调用" << endl;
  		this->m_rong = arr.m_rong;
  		this->m_size = arr.m_size;
  		//深拷贝
  		this->paddress = new T[arr.m_rong];
  		for (int i = 0; i < this->m_size; i++) {
  			this->paddress[i] = arr.paddress[i];
  		}
  	}
  	//operator 防止浅拷贝
  	Myarray& operator=(const Myarray& arr) {
  		/*cout << "operator=调用" << endl;*/
  		//先判断是否在堆区有数据，如果有，清零
  		if (this->paddress != NULL) {
  			delete[] this->paddress;
  			this->paddress = NULL;
  			this->m_rong = 0;
  			this->m_size = 0;
  		}
  		this->m_rong = arr.m_rong;
  		this->m_size = arr.m_size;
  		//深拷贝
  		this->paddress = new T[arr.m_rong];
  		for (int i = 0; i < this->m_size; i++) {
  			this->paddress[i] = arr.paddress[i];
  		}
  		return *this;
  	}
  	//通过下标获取元素
  	T& operator[](int index) {
  		return this->paddress[index];
  	}
  	//尾插法
  	void Push_back(const T&val) {
  		if (this->m_rong == this->m_size) {
  			return;
  		}
  		this->paddress[this->m_size] = val;
  		this->m_size++;
  	}
  	//尾删法
  	void Pop_back() {
  		//使用户访问不到最后一个元素
  		if (this->m_size == 0) {
  			return;
  		}
  		(this->m_size)--;
  	}
  	//获取长度
  	int getSize() {
  		return this->m_size;
  	}
  	//获取容量
  	int getrong() {
  		return this->m_rong;
  	}
  	
  	~Myarray() {
  		if (this->paddress != NULL) {
  			/*cout << "析构函数的调用" << endl;*/
  			delete[] this->paddress;
  			this->paddress = NULL;
  		}
  	}
  private:
  	T* paddress;
  	int m_rong;
  	int m_size;
  };
  ```

  text.cpp

  ```
  void printint(Myarray<int>&p) {
  	for (int i = 0; i < p.getSize(); i++) {
  		cout << p[i] << endl;
  	}
  }
  void text02() {
  	Myarray<int>arr(5);
  	for (int i = 0; i < 5; i++) {
  		arr.Push_back(i);
  	}
  	cout << "arr打印输出为" << endl;
  	printint(arr);
  	cout << "arr容量大小为：" << arr.getrong();
  	cout << "arr的大小为" << arr.getSize();
  	Myarray <int>arr2(arr);
  	cout << "arr2打印输出为" << endl;
  	printint(arr2);
  	cout<<arr2.getSize()<<arr2.getrong();
  	arr2.Pop_back();
  	cout << "arr2尾删后：" << endl;
  	printint(arr2);
  	cout << "arr2的容量大小为" << arr2.getrong() << endl;
  	cout << "arr2的长度为" << arr2.getSize() << endl;
  	//Myarray<int>arr2(arr);
  	//Myarray<int>arr3(100);
  	//arr3 = arr2;
  }
  //测试自定义数据类型
  class person {
  public:
  	person() {};
  	person(string name, int age) {
  		this->m_name = name;
  		this->m_age = age;
  	}
  	string m_name;
  	int m_age;
  };
  void personprint(Myarray<person>& p) {
  	for (int i = 0; i < p.getSize(); i++) {
  		cout << p[i].m_age << " " << p[i].m_name;
  	}
  }
  void text01(){
  	Myarray<person> arr(10);
  	person p1("孙悟空", 555);
  	person p2("wsw", 111);
  	person p3("aaa", 33);
  	arr.Push_back(p1);
  	arr.Push_back(p2);
  	arr.Push_back(p3);
  	personprint(arr);
  }
  ```

  

## 2.STL

### 2.1 诞生

面向对象和泛型编程的思想，目的是提升代码的复用性。

### 2.2 基本概念

- STL（标准模板库）
- STL从广义上分为：容器 算法 迭代器
- 容器和算法之间通过迭代器进行无缝衔接
- STL几乎所有代码都应用了模板类或者模板函数

### 2.3 STL六大组件

**容器，算法，迭代器，仿函数，适配器，空间配置器**

1.容器：各种数据结构  eg:vector,list,map,set等

2.算法：各种常用的算法，eg:sort,find,copy,for_each等

3.迭代器：容器和算法的胶合剂

4.仿函数：行为类似函数，可作为算法的某种策略

5.适配器：一种用来修饰容器或仿函数或迭代器接口的东西

6.空间配置器：负责空间的配置与管理

### 2.4 容器，算法，迭代器

**容器：**
序列式容器：强调值的排序，每个元素都有固定的位置

关联式容器：二叉树结构，各元素之间没有严格物理上的顺序关系

**迭代器：**

提供一种方法，使之能够依照次序访问容器的各元素，而又无需暴露容器的内部表示方式，每个容器都有自己专属的迭代器。

类似指针

**种类**

| 种类     | 功能                                             | 支持运算                      |
| -------- | ------------------------------------------------ | ----------------------------- |
| 输入     | 对数据只读访问                                   | ++，==，！=                   |
| 输出     | 对数据只写访问                                   | ++                            |
| 前向     | 读写操作，并能向前推进迭代器                     | ++，==，！=                   |
| 双向     | 读写操作，并能向前和向后操作                     | ++，--                        |
| 随机访问 | 读写操作，可以以跳跃的方式访问任意数据，功能最强 | ++，--，[n]，-n，<，<=，>，>= |

常用为双向和随机访问

#### 2.5 容器算法迭代器初识

#### 2.5.1 vector存放内置数据类型

迭代器 ：vector<int>::iterator

vector<int>::iterator itBegin = v.begin();//初始迭代器，指向第一个元素
vector<int>::iterator itEnd = v.end();//容器最后一个元素的下一个位置

```
void printmy(int val) {
	cout << val << endl;
}
void text01() {
	vector<int>v;
	v.push_back(10);
	v.push_back(20);
	v.push_back(30);
	v.push_back(40);
	v.push_back(50);
	//第一种遍历
	//通过迭代器访问容器中的数据
	//vector<int>::iterator itBegin = v.begin();//初始迭代器，指向第一个元素
	//vector<int>::iterator itEnd = v.end();//容器最后一个元素的下一个位置
	//while (itBegin!=itEnd) {
	//	cout << *itBegin << endl;
	//	itBegin++;
	//}
	//第二种遍历
	for (vector<int>::iterator it = v.begin(); it != v.end(); it++) {
		cout << *it << endl;
	}
	//第三种遍历
	for_each(v.begin(), v.end(),printmy);
}
```

#### 2.5.2 vector存放自定义数据类型

存放person类的数据类型

```
class person {
public:
	person(string name, int age) {
		this->m_name = name;
		this->m_age = age;
	}
	string m_name;
	int m_age;
};
void text01() {
	vector<person>v;
	person p1("aaa", 20);
	person p2("bbb", 30);
	person p3("ccc", 40);
	person p4("ddd", 50);
	v.push_back(p1);
	v.push_back(p2);
	v.push_back(p3);
	v.push_back(p4);
	//遍历容器数据
	for (vector<person>::iterator it = v.begin(); it != v.end(); it++) {
		//看括号数据类型就是*it
		cout << "姓名：" << (*it).m_name << " "
			<< "姓名：" << (*it).m_age << " " << endl;
		cout << "姓名：" << it->m_name << " "
			<< "姓名：" << it->m_age << " " << endl;
	}
}
```

2.5.3 vector容器嵌套容器

```
void text02() {
	vector<vector<int>>v;
	vector<int>p1;
	vector<int>p2;
	vector<int>p3;
	vector<int>p4;
	for (int i = 0; i < 4; i++) {
		p1.push_back(i + 1);
		p2.push_back(i + 2);
		p3.push_back(i + 3);
		p4.push_back(i + 4);
	}
	v.push_back(p1);
	v.push_back(p2);
	v.push_back(p3);
	v.push_back(p4);
	for (vector<vector<int>>::iterator it = v.begin(); it != v.end(); it++) {
		for (vector<int>::iterator mit = it->begin(); mit != it->end(); mit++) {
			cout << *mit << " ";
		}
		cout << endl;
	}
}
```

## 3.STL 常用容器

### 3.1 string容器

#### 3.1.1 string基本概念

**本质：**
c++风格的字符串，string实际上是一个类

**string 和char*的区别：**

- char* 是一个指针
- string 是一个类，类内部封装了char*，是一个char* *的容器

**特点：**

- string 内部封装了很多成员方法

- string 管理char*分配的内存，不用担心越界和取值越界

**构造函数：**
string();——空字符串

string(const string &s);——拷贝string

string(const char*s);——传入字符串

string(int n,char c);——n个c字符

#### 3.1.2 赋值操作

```
str1 = "hello world";
string str2;
str2 = str1;
string str3;
str3 = 'a';
string str4;
str4.assign("hello cc");
string str5;
str5.assign("hello cc", 5);//截取前五个字符
string str6;
str6.assign(str5);
string str7;
str7.assign(10, 'w');
```

#### 3.1.3 string拼接操作

+=相当于连接，可以连接字符串和单个字符

append函数可以连接字符串

str.append(const string &str,int pos,int n)从pos开始的n个字符

```
//string 字符串拼接操作
void text01() {
	string str1 = "我";
	str1 += "爱玩游戏";
	cout << str1 << endl;
	str1 += ";";
	cout << str1 << endl;

	string str2 = "LOL DNF";
	str1 += str2;
	cout << str1 << endl;
	string str3;
	str3.append("我太强了");
	cout << str3<<endl;
	str3.append("game", 4);
	cout << str3 << endl;
	str3.append(str2);
	cout << str3 << endl;
	str3.append(str2, 0, 3);//str.append(const string &str,int pos,int n)从pos开始的n个字符
	cout << str3 << endl;
}
```

#### 3.1.4 string 查找和替换

```
void text01() {
	/*find从左往右找*/
	string s="我是一个";
	int a=s.find("是",0);
	if (a == -1) {
		cout << "未找到字符串" << endl;
	}
	cout << a << endl;
	//rfind从右往左查找
	a = s.rfind("是");
	cout << a << endl;
}
//替换
void text02() {
	string str1 = "abcde";
	str1.replace(1, 3, "1111");//从1开始替换三个字符
	cout << str1 << endl;
	int b=str1.rfind("a1",0,1);//从pos开始查找s的前n个字符最后出现的位置
	cout << b << endl;

}
```

#### 3.1.5 string 字符串比较

ASCLL码值进行对比

```
void text03() {
	string name="aello";
	string str1 = "hello";
	if (name.compare(str1) == 0) {
		cout << "等于" << endl;
	}
	else if (name.compare(str1) > 0) {
		cout << "大于" << endl;
	}
	else {
		cout << "小于" << endl;
	}
}
```

#### 3.1.6 string字符串存取

方式有两种

- 下标
- at

```
void text03() {
	string str1 = "hello";
	for (int i = 0; i < str1.size(); i++) {
		cout << str1[i] << endl;
	}
	for (int i = 0; i < str1.size(); i++) {
		cout << str1.at(i) << " ";
	}
}
```

#### 3.1.7 string 插入和删除

插入和删除下标都是从零开始

```
void text03() {
	string str1 = "hello";
	str1.insert(0, "world");//插入字符串
	cout << str1 << endl;
	str1.insert(0, 3, 'c');//插入多个字符
	cout << str1 << endl;
	str1.erase(0, 3);
	cout << str1 << endl;//删除字符
}
```

#### 3.1.8 string 子串

从字符串中获取想要的字符串

```
void text03() {
	string str1 = "hello world";
	string str2 = str1.substr(1, 3);//从下标1开始，截取三个字符
	cout << str2 << endl;
}
//实际运用
void text02() {
	string str1 = "wushije5478@ccc";
	int pos = str1.find('@', 0);
	string str2 = str1.substr(0, pos);
	cout << str2 << endl;
}
```

### 3.2 vector容器

#### 3.2.1 基本概念

**功能：**
和数组很相似，成为单段数组

**与普通数组区别：**
数组是静态空间，vector可以动态扩展

**动态扩展：**

不是在后面续新空间，而是找一块更大的空间，将原数据拷贝，释放原空间

vector容器的迭代器是支持随机访问的迭代器，可以+3，+4等操作

#### 3.2.2 vector构造函数

创建vector容器

```
void printmy(vector<int> v) {
	for (vector<int>::iterator it = v.begin(); it < v.end(); it++) {
		cout << *it << " ";
	}
}
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	printmy(v);
	//通过区间方式进行构造
	vector<int>v1(v.begin(), v.end());
	printmy(v1);
	cout << endl;
	//n个数据进行构造
	vector<int>v2(10, 100);
	printmy(v2);
	cout << endl;
	//拷贝构造
	vector<int>v3(v2);
	printmy(v3);
}
```

#### 3.2.3 vector容器的赋值操作

```
void printmy(vector<int> &v) {
	for (vector<int>::iterator it = v.begin(); it < v.end(); it++) {
		cout << *it << " ";
	}
}
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	printmy(v);
	//赋值
	vector<int>v1;
	v1 = v;
	printmy(v1);
	vector<int>v2;
	//区间赋值
	v2.assign(v1.begin(), v1.end());
	printmy(v2);
	//n个数据赋值
	vector<int>v3;
	v3.assign(10, 100);
	printmy(v3);
}
```

#### 3.2.4 vector容量和大小

empty() 判断容器是否为空

size()元素个数

capacity() 容器的容量

resize(int size,int a)重新指定大小

```
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	printmy(v);
	if (v.empty())
	{
		cout << "容器为空" << endl;
	}//为真代表容器为空
	else {
		cout << "容器不为空" << endl;
		cout << "容器容量为" << v.capacity() << endl;
		cout << "大小" << v.size() << endl;
	}
	//重新制定大小
	v.resize(15,100);
	printmy(v);
	v.resize(5);
	printmy(v);
}
```

#### 3.2.5 插入和删除

```
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	//尾删
	v.pop_back();
	printmy(v);
	//插入 迭代器为第一个参数
	v.insert(v.begin(), 100);
	printmy(v);
	v.insert(v.begin(), 2, 1000);
	printmy(v);
	//删除
	v.erase(v.begin());
	printmy(v);
	//清空
	v.erase(v.begin(), v.end());
	printmy(v);
	v.clear();
}
```

#### 3.2.6 vector数据存取

下标，at

```
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	for (int i = 0; i < v.size(); i++) {
		cout << v[i] << " ";
	}
	cout << endl;
	for (int i = 0; i < v.size(); i++) {
		cout << v.at(i) << " ";
	}
	cout << endl;
	int a = v.front();
	int b = v.back();
	cout << a << b << endl;
}
```

#### 3.2.7 vector互换容器

swap(vec) //将vec与容器元素互换

```
void text02() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	printmy(v);
	vector<int>v1;
	for (int i = 10; i >0; i--) {
		v1.push_back(i);
	}
	printmy(v1);
	//互换容器
	v.swap(v1);
	printmy(v);
	printmy(v1);
}
//实际用途
void text01() {
	vector<int>v;
	for (int i = 0; i < 100000; i++) {
		v.push_back(i);
	}
	//容量和大小
	cout << v.capacity()<<endl;
	cout << v.size() << endl;
	v.resize(3);
	cout << v.capacity() << endl;
	cout << v.size() << endl;
	//巧用swap收缩内存
	vector<int>(v).swap(v);//用目前元素个数初始化匿名对象
	cout << v.capacity() << endl;
	cout << v.size() << endl;
}
```

#### 3.2.8 vector预留空间

减少vector动态扩展容量时的扩展次数

```
void text01() {
	vector<int>v;
	//利用reserve预留空间
	v.reserve(100000);
	int num = 0;
	int* p = 0;
	for (int i = 0; i < 100000; i++) {
		v.push_back(i);
		if (p != &v[0]) {
			p = &v[0];
			num++;
		}
	}
	cout << num << endl;
	
}
```

### 3.3 deque容器

#### 3.3.1 deque容器基本概念

双端数组，可以对头部进行插入操作

deque工作原理：

内部的中控器维护每段缓冲区的内容，缓冲区中存放真实数据，中控区维护缓冲区的地址，使得deque像一片连续的内存空间

#### 3.3.2 deque 容器的构造函数

```
void printmy(deque<int>& d) {
	for (deque<int>::const_iterator it = d.begin(); it < d.end(); it++) {
		cout << *it << " ";
	}
	cout << endl;
}
void text01() {
	deque<int>d1;
	for (int i = 0; i < 10; i++) {
		d1.push_back(i);
	}
	printmy(d1);
	deque<int>d2(d1.begin(),d1.end());
	printmy(d2);
	deque<int>d3(10, 100);
	printmy(d3);
	deque<int>d4(d3);
	printmy(d4);
}
```

#### 3.3.3 deque容器的赋值操作

同vector容器

#### 3.3.4 deque大小操作

deque.empty();

deque,size()

deque.resize(num)

deque.resize(num,elem)

deque容器没有容量的概念

#### 3.3.5 deque插入和删除

```
void text01() {
	deque<int>d1;
	//尾插
	for (int i = 0; i < 10; i++) {
		d1.push_back(i);
	}
	//头插
	d1.push_front(100);
	d1.push_front(200);
	printmy(d1);
	//尾删
	d1.pop_back();
	printmy(d1);
	//头删
	d1.pop_front();
	printmy(d1);
}
void text02() {
	deque<int>d1;
	for (int i = 0; i < 10; i++) {
		d1.push_back(i);
	}
	//insert插入
	d1.insert(d1.begin(), 100);
	printmy(d1);
	d1.insert(d1.begin(), 2, 200);
	printmy(d1);
	//按照区间插入
	deque<int>d2;
	d2.push_back(10);
	d2.push_back(20);
	d2.push_back(30);
	d1.insert(d1.begin(), d2.begin(), d2.end());
	printmy(d1);
}
void text03() {
	deque<int>d1;
	for (int i = 0; i < 10; i++) {
		d1.push_back(i);
	}
	//删除
	deque<int>::iterator it = d1.begin();
	it++;
	d1.erase(it);
	printmy(d1);
	//按照区间方式删除
	d1.erase(d1.begin(), d1.end());
	d1.clear();
	printmy(d1);
}
```

#### 3.3.6 deque数据存取

at,下标

front(),back()

#### 3.3.7 deque排序

sort(begin,end)

### 3.4 评委打分

```
//选手类
class person {
public:
	person(string name,int score) {
		m_name = name;
		m_score = score;
	}
	string m_name;
	int m_score;
};
void creatperson(vector<person> &v) {
	string nameseed = "ABCDE";
	for (int i = 0; i < 5; i++) {
		string name = "选手";
		name += nameseed[i];
		int score = 0;
		person p(name, score);
		v.push_back(p);
	}
}
void setscore(vector<person>& v) {
	for (vector<person>::iterator it = v.begin(); it != v.end(); it++) {
		//分数放到deque中
		deque<int>d1;
		for (int i = 0; i < 10; i++) {
			int score = rand()%41+60;
			d1.push_back(score);
		}
		cout << (*it).m_name << " ";
		//输出每个评委打分
		for (deque<int>::iterator dt = d1.begin(); dt != d1.end(); dt++) {
			cout << *dt << " ";
		}
		//排序
		sort(d1.begin(), d1.end());
		d1.pop_back();
		d1.pop_front();
		//取平均分
		int sum = 0;
		for (deque<int>::iterator mit = d1.begin(); mit != d1.end(); mit++) {
			sum += *mit;
		}
		int aver = sum / d1.size();
		it->m_score = aver;
		cout << it->m_score << endl;
	}
}
```

### 3.5 stack容器

#### 3.5.1 stack基本概念

先进后出的结构

#### 3.5.2 stack常用接口

构造函数：
拷贝构造 stack(const stack &stk)

数据存取；

push();

pop();

```
void text01() {
	stack<int>s;
	//入栈
	s.push(10);
	s.push(20);
	s.push(30);
	s.push(40);
	//栈不为空，看栈顶，并且出栈
	while (!s.empty()) {
		cout << "栈顶元素为：" << s.top() << endl;
		s. pop();
	}
	cout << "栈的大小" << s.size() << endl;
}
```



### 3.6 queue容器

#### 3.6.1 queue容器的概念

先进先出

队列容器只允许在一端新增元素，从另一端删除元素

队列容器不允许遍历

#### 3.6.2 queue容器常用接口

```
class person {
public:
	person(string name, int age) {
		m_name = name;
		m_age = age;
	}
	string m_name;
	int m_age;
};
void text01() {
	queue<person>q1;
	person p1("孙悟空", 22);
	person p2("唐山", 22);
	person p3("猪八戒", 33);
	person p4("沙僧", 44);
	q1.push(p1);
	q1.push(p2);
	q1.push(p3);
	q1.push(p4);
	cout << q1.size() << endl;
	while (!q1.empty()) {
		//队头
		cout << q1.front().m_name<<q1.front().m_age << endl;
		//队尾
		cout << q1.back().m_name << q1.back().m_age << endl;
		q1.pop();
	}
	cout << "队列大小为" << q1.size() << endl;
}
```

### 3.7 list容器

链表优点：可以对任意位置进行插入和删除元素

缺点：容器遍历速度没有数组快

占用空间比数组大

STL中的链表是一个**双向循环链表**

list容器的迭代器只能**前移和后移**，双向迭代器

#### 3.7.1构造函数

默认

区间

拷贝

n个数据

```
void printmy(list<int>& l) {
	for (list<int>::const_iterator it = l.begin(); it != l.end(); it++) {
		cout << *it << " ";
	}
	cout << endl;
}
void text01() {
	list<int>l;
	l.push_back(10);
	l.push_back(20);
	l.push_back(30);
	l.push_back(40);
	printmy(l);
	list<int>l1(l.begin(),l.end());
	printmy(l1);
	list<int>l2(l1);
	printmy(l2);
	list<int>l3(10,100);
	printmy(l3);
}
```

#### 3.7.2 list容器赋值和交换

```
void text01() {
	list<int>l;
	l.push_back(10);
	l.push_back(20);
	l.push_back(30);
	l.push_back(40);
	list<int>l1 = l;
	printmy(l1);
	l1.assign(10, 100);
	printmy(l1);
	list<int>l2(l1.begin(), l1.end());
	printmy(l2);
}
void text02() {
	//交换前
	list<int>l;
	l.push_back(10);
	l.push_back(20);
	l.push_back(30);
	l.push_back(40);
	list<int>l1 = l;
	printmy(l1);
	l1.assign(10, 100);
	printmy(l1);
	//交换后
	l.swap(l1);
	printmy(l);
	printmy(l1);
}
```

#### 3.7.3 list 容器的大小操作

size()

empty()

resize(num)//重新指定容器长为num，如果变长，填充默认值，如果变短，元素删除

resize(num,elem)

```
void text01() {
	list<int>l;
	l.push_back(10);
	l.push_back(20);
	l.push_back(30);
	l.push_back(40);
	list<int>l1 = l;
	printmy(l1);
	l1.assign(10, 100);
	printmy(l1);
	list<int>l2(l1.begin(), l1.end());
	printmy(l2);
}
void text02() {
	//交换前
	list<int>l;
	l.push_back(10);
	l.push_back(20);
	l.push_back(30);
	l.push_back(40);
	list<int>l1 = l;
	printmy(l1);
	l1.assign(10, 100);
	printmy(l1);
	//交换后
	l.swap(l1);
	printmy(l);
	printmy(l1);
}
```

#### 3.7.4 list容器的插入和删除

push_back(elem)

pop_back()

push_front(elem)

pop_front()

insert(pos,elem)

insert(pos,n,elem)

insert(pos,beg,end)

clear()

erase(beg,end)

erase(pos)

与vector,deque相似，新增：
remove(elem) //删除容器中所有与elem匹配的元素值

```
void text02() {
	list<int>l;
	//尾插
	for (int i = 0; i < 10; i++) {
		l.push_back(i);
	}
	//头插
	l.push_front(100);
	printmy(l);
	//尾删
	l.pop_back();
	printmy(l);
	cout << "容器大小为" << l.size() << endl;
	//头删
	l.pop_front();
	printmy(l);
	//insert插入
	l.insert(l.begin(), 10);
	printmy(l);
	l.insert(l.begin(), 2, 20);
	printmy(l);
	//删除
	l.remove(20);
	printmy(l);
	l.erase(l.begin(), l.end());
	printmy(l);
	l.clear();

}
```

#### 3.7.5 list容器的数据存取

front（）返回第一个元素

back（）返回最后一个元素

list本质是链表，不可以通过下标访问

#### 3.7.6 list容器反转和排序

```
bool temp(int a, int b) {
	return a > b;
}
void text02() {
	list<int>l;
	for (int i = 10; i >0; i--) {
		l.push_back(i);
	}
	printmy(l);
	//反转
	l.reverse();
	printmy(l);
	//排序
	//所有不支持随机访问迭代器的容器，不能用标准算法
	//不支持随机访问迭代器的容器内部提供对应的算法
	l.sort(temp);
	printmy(l);

}
```

### 3.8 set/multiset容器

所有元素都会在插入时自动被排序

关联式容器，用二叉树实现

#### 3.8.1 set容器的插入和构造

```
void text01() {
	set<int>s;
	s.insert(30);
	s.insert(40);
	s.insert(20);
	s.insert(50);
	s.insert(10);
	//set容器不允许插入重复值
	printset(s);
	//拷贝构造
	set<int>s1(s);
	printset(s1);
	//赋值
	set<int>s2;
	s2 = s1;
	printset(s2);
}
```

#### 3.8.2 set容器大小和交换

```
void text01() {
	set<int>s;
	s.insert(30);
	s.insert(40);
	s.insert(20);
	s.insert(50);
	s.insert(10);
	cout << "s的大小" << s.size() << endl;
	if (s.empty()) {
		cout << "容器为空" << endl;
	}
	else {
		cout << "s不为空" << endl;
	}
	set<int>s1;
	s1.insert(20);
	s1.insert(10);
	s1.insert(30);
	s1.insert(40);
	s1.insert(50);
	s1.swap(s);
	printset(s1);
	printset(s);
}
```

#### 3.8.3 set容器的插入和删除

insert(elem)

clear()

erase(pos)

erase(beg,end)

erase(elem)

#### 3.8.4 ser 容器查找和统计

find(key)  //查找key是否存在，返回该元素的迭代器，如果不存在，返回 set.end()

count(key) //统计key的元素个数

```
void text01() {
	set<int>s;
	s.insert(30);
	s.insert(40);
	s.insert(20);
	s.insert(50);
	s.insert(10);
	set<int>::iterator pos = s.find(20);
	if (pos != s.end()) {
		cout << "找到元素" << " ";
	}
	else {
		cout << "找到元素" << " ";
	}
	int num=s.count(20);

	cout << num;
}
```

#### 3.8.5 set和multiset区别

- 区别：
  set不可以重复插入数据，multiset可以
- set容器插入时返回插入结果，表示插入是否成功
- multiset不会检测数据，因此可以插入重复数据

```
set<int>s;
pair<set<int>::iterator, bool>ret = s.insert(10);
if (ret.second) {
	cout << "第一次插入成功" << endl;
}
else {
	cout << "失败" << endl;
}
```

#### 3.8.6 对组创建

```
void text01() {
	pair<int, string>p(2, "wss");
	cout << p.first << p.second << endl;
	pair<int, string>p1 = make_pair(2, "wza");
	cout << p.first << p.second << endl;
}
```

#### 3.8.7 set容器排序

set容器在插入数据后就排不了序了，所以要在之前进行排序

存放内置数据类型：

```
class mtcompare {
public:
	bool operator()( int  v1 , const int  v2 )const {
		return v1 > v2;
	}
};
void text01() {
	set<int>s;
	s.insert(10);
	s.insert(30);
	s.insert(20);
	s.insert(40);
	for (set<int>::iterator it = s.begin(); it != s.end(); it++) {
		cout << *it << " ";
	}
	cout << endl;
	set<int, mtcompare>s2;
	s2.insert(10);
	s2.insert(30);
	s2.insert(20);
	s2.insert(40);
	for (set<int,mtcompare>::iterator iat = s2.begin(); iat != s2.end(); iat++) {
		cout << *iat << " ";
	}
	

}
```

存放自定义数据类型：

```
class person {
public:
	person(string name, int age) {
		this->m_name = name;
		this->m_age = age;
	}
	string m_name;
	int m_age;
};
class temp {
public:
	bool operator()(person a, person b)const {
		return a.m_age > b.m_age;
	}
};
void text01() {
	set<person,temp>s;
	person p("张三", 22);
	person p1("李四", 21);
	person p2("王五", 23);
	person p3("赵六", 32);
	s.insert(p);
	s.insert(p1);
	s.insert(p2);
	s.insert(p3);
	for (set<person>::iterator it = s.begin(); it != s.end(); it++) {
		cout << it->m_name << " " << it->m_age;
	}
	cout << endl;
	
}
```

###  3.9 map/multimap容器

#### 3.9.1 map基本概念

关联式容器，二叉树结构

pair第一个元素为键值，起索引作用，第二个元素为value

所有元素会根据键值自动排序-------从小到大

**优点：**

可以根据key值快速找到value值

#### 3.9.2 map容器的构造和赋值

```
void printmy(map<int, int>& m) {
	for (map<int, int>::iterator it = m.begin(); it != m.end(); it++) {
		cout << it->first << " " << it->second<<" ";
		cout << endl;
	}
	cout << endl;
}
void text01() {
	map<int,int>m;
	m.insert(make_pair(1,10));
	m.insert(make_pair(2, 20));
	m.insert(make_pair(3, 30));
	m.insert(make_pair(4 ,40));
	m.insert(make_pair(5, 50));
	printmy(m);
	//拷贝
	map<int, int>m1(m);
	printmy(m1);
	//赋值
	map<int, int>m;
}
```

#### 3.9.3 map大小和交换

size()

empty()

swap(st)

#### 3.9.4 map容器的插入和删除

```
void text01() {
	map<int,int>m;
	//插入
	m.insert(make_pair(1,10));
	//可以通过下标遍历
	m[2] = 110;
	m.insert(make_pair(3, 30));
	m.insert(make_pair(4, 40));
	printmy(m);
	//删除
	m.erase(m.begin());
	m.erase(2);//按照key值删
	printmy(m);
	m.clear();
}
```

#### 3.9.4 查找和统计

如果key存在，返回迭代器，否则返回end()

find(key)

count(key)   //统计元素个数

#### 3.9.5 排序

```
class temp {
public:
	bool operator()(int v1, int v2)const {
		return v1 > v2;
	}
};
void text01() {
	map<int,int,temp>m;
	//插入
	m.insert(make_pair(1,10));
	//可以通过下标遍历
	m[2] = 110;
	m.insert(make_pair(3, 30));
	m.insert(make_pair(4, 40));
	for (map<int, int>::iterator it = m.begin(); it != m.end(); it++) {
		cout << it->first << " " << it->second << " ";
		cout << endl;
	}
	cout << endl;
	
}
```

#### 3.9.6 案例

利用vector容器对对员工进行存储，员工数据有名字和工资

再用muitmap容器为员工分配部门，再通过部门输出员工

```
class worker {
public:
	string m_name;
	int m_score;
};
void creatworker(vector<worker>& v) {
	string name="ABCDEFGHIJ";
	for (int i = 0; i < 10; i++) {
		worker *mworker=new worker;
		mworker->m_name = "员工";
		mworker->m_name += name[i];
		mworker->m_score = rand() % 10000 + 10000;
		v.push_back(*mworker);
		delete mworker;
	}
}
void setgroup(vector<worker>& v, multimap<int, worker>& m) {
	for (vector<worker>::iterator it = v.begin(); it != v.end(); it++) {
		int id = rand() % 3;
		m.insert(make_pair(id, *it));
	}
}
void showinfo(multimap<int, worker>& m) {
	cout << "0号部门" << endl;
	multimap<int, worker>::iterator pos = m.find(0);
	int count = m.count(0);
	int index = 0;
	for (; pos != m.end()&&index<count; pos++,index++) {
		cout << "名字" << pos->second.m_name << " 工资" << pos->second.m_score << endl;
	}
	cout << "1号部门" << endl;
	multimap<int, worker>::iterator mpos = m.find(1);
	int mcount = m.count(1);
	int mindex = 0;
	for (; pos != m.end() && mindex < mcount; mpos++, mindex++) {
		cout << "名字" << mpos->second.m_name << " 工资" << mpos->second.m_score << endl;
	}
	cout << "2号部门" << endl;
	multimap<int, worker>::iterator ipos = m.find(2);
	int icount = m.count(2);
	int iindex = 0;
	for (; pos != m.end() && iindex < icount; ipos++, iindex++) {
		cout << "名字" << ipos->second.m_name << " 工资" << ipos->second.m_score << endl;
	}
}
void text01() {
	//1.创建员工
	vector<worker>v;
	creatworker(v);
	/*for (vector<worker>::iterator it = v.begin(); it != v.end(); it++) {
		cout << it->m_name << " " << it->m_score << endl;
	}
	cout << endl;*/
	//2.员工分组
	multimap<int, worker>mworker;
	setgroup(v, mworker);
	for (multimap<int, worker>::iterator it = mworker.begin(); it != mworker.end(); it++) {
		cout << "部门 "<<it->first << " "<<" 名字 " << it->second.m_name <<"工资"<< it->second.m_score << endl;
	}
	//3.分组显示
	showinfo(mworker);

	
}
```

## 4.0 STL-函数对象

### 4.1 函数对象

#### 4.1.1 函数对象概念

重载函数调用操作符的类，其对象成为函数对象

函数对象使用重载的（）时，行为类似函数调用，也叫仿函数

本质：

是一个类

#### 4.1.2 函数对象的使用

使用时可以像函数一样调用，可以有参数，可以有返回值

可以作为函数参数传递

仿函数有自己的状态

```
class add {
public:
	int operator()(int a, int b)const {
		return a + b;
	}
};
void texy01() {
	add m;
	cout<<m(10, 20);
}
class persom{
public:
	persom() {
		this->count = 0;
	}
	void operator()(string name) {
		cout << name;
		this->count++;
	}
	int count;//内部自己的状态
};
void doprint(persom& p, string name) {
	p(name);
}
void text02() {
	persom p;
	doprint(p, "hell");

}
```

### 4.2 一元谓词

#### 4.2.1 概念

- 返回bool类型的仿函数
- 如果operator（）接受一个参数，叫一元谓词
- 如果operator（）接受两个参数，叫二元谓词

```
class person {
public:
	bool operator()(int a,int b) {
		return a > b;
	}
};
void text01() {
	vector<int>v;
	v.push_back(10);
	v.push_back(20);
	v.push_back(30);
	v.push_back(40);
	v.push_back(50);
	sort(v.begin(), v.end());
	for (vector<int>::iterator it = v.begin(); it != v.end(); it++) {
		cout << *it << endl;
	}
	sort(v.begin(), v.end(),person());
	for (vector<int>::iterator it = v.begin(); it != v.end(); it++) {
		cout << *it << endl;
	}
}
```

### 4. 3 内建函数对象

#### 4.3.1 内建函数对象意义

- 算数关系仿函数
- 关系仿函数
- 逻辑仿函数

仿函数所产生的对象，用法和一般函数完全相同

引入头文件<functional>

#### 4.3.2 算数仿函数

```
plus<T>   //加法
minux<T>  //减法
multiplies<T> //乘法
divides<T>//除法
modulus<T>//取模
negate<T>//取反
```

#### 4.3.3 关系仿函数

`equal_to<T> ` 等于

`not_equal_to<T> ` 不等于

`greater<T> ` 大于

`less<T> `小于

`greater_equal<T> ` 大于等于

`less_equal<T> ` 小于等于

#### 4.3.4 逻辑仿函数

bool logical_and<T>   逻辑与

bool logical_or<T>    逻辑或

bool logical_not<T>  逻辑非

## 5.STL常用算法

头文件：<algorithm> <functional><numeric>

### 5.1 常用遍历算法

#### 5.1.1 for_each

for_each(iterator beg,iterator end,_func);

//遍历算法 遍历容器元素

//beg 开始迭代器

//end结束迭代器

//--func 函数或函数对象

#### 5.1.2 transform

transform(iterator beg1,iterator end1,iterator beg2,_func)

- beg1 开始迭代器
- end1 结束迭代器
- beg2 目标容器开始迭代器
- _func 函数或仿函数

### 5.2 常用查找算法

find    查找元素

find_if    按条件查找元素

adjacent_find   查找相邻重复元素

binary_search  二分查找法

count   统计元素个数

count_if  按条件统计元素个数

#### 5.2.1 find

查找指定元素，找到时返回元素的迭代器，否则返回end()

**find(beg,end,value)**

```
class person {
public:
	person(string name, int age) {
		this->m_name = name;
		this->m_age = age;
	}
	//重载==号，使得find知道如何进行对比
	bool operator==(const person& p) {
		if (this->m_name == p.m_name && this->m_age == p.m_age) {
			return true;
		}
		else {
			return false;
		}
	}
	string m_name;
	int m_age;
};
class print1{
public:
	void operator()(int val) {
		cout<<val<<" ";
	}
};
void text01() {
	vector<int>v;
	for (int i = 0; i < 10; i++) {
		v.push_back(i);
	}
	vector<int>::iterator pos=find(v.begin(), v.end(), 5);
	if (pos != v.end()) {
		cout << "找到" << endl;
	}
	else {
		cout << "找不到" << endl;
	}
}
void text02() {
	vector<person>v1;
	person p1("张三", 22);
	person p2("李四", 32);
	person p3("王五", 42);
	person p4("赵六", 52);
	v1.push_back(p1);
	v1.push_back(p2);
	v1.push_back(p3);
	v1.push_back(p4);
	vector<person>::iterator pos = find(v1.begin(), v1.end(), p2);
	if (pos != v1.end()) {
		cout << "找到" << endl;
	}
	else {
		cout << "找不到" << endl;
	}
}
```

#### 5.2.2 find_if

find_if(iterator beg1,iterator end1,_func)

- beg1 开始迭代器
- end1 结束迭代器
- _func 函数或仿函数

#### 5.2.3 adjacent_find

adjacent_find(beg,end);

```
void text01() {
	vector<int>v;
	v.push_back(1);
	v.push_back(1);
	v.push_back(2);
	v.push_back(2);
	v.push_back(3);
	vector<int> ::iterator pos=adjacent_find(v.begin(), v.end());
	if (pos != v.end()) {
		cout << "找到" << endl;
	}
	else {
		cout << "找不到" << endl;
	}
}
```

#### 5.2.4 binary_search

**bool binary_search(bed,end,value)**

- 注意：在无序序列中不能用

#### 5.2.5 count

**count(beg,end,value)**

统计元素出现次数

#### 5.2.6 count_if

**count_if(iterator beg1,iterator end1,_func)**

### 5.3 常用排序算法

sort  //对容器元素进行排序

random_shuffle //洗牌，指定范围内元素进行随机排序

merge  //容器元素合并，并储存到另一个容器当中

reverse // 反转指定范围的元素

#### 5.3.1 sort

sort(beg,end,_pred)

#### 5.3.2 random_shuffle

random_shuffle(beg,end)

将范围内元素随机调整次序

```
void text01() {
	vector<int>v;
	v.push_back(1);
	v.push_back(1);
	v.push_back(2);
	v.push_back(2);
	v.push_back(3);
	random_shuffle(v.begin(), v.end());
	for (vector<int>::iterator it = v.begin(); it != v.end(); it++) {
		cout << *it << " ";
	}
}
```

#### 5.3.3 merge

merge(beg1,end1,beg2,end2,beg3)

beg1 容器1开始迭代器

end1 容器1结束迭代器

beg2 容器2开始迭代器

end2 容器2结束迭代器

beg3 目标容器开始迭代器

注意：两个源容器必须有序且顺序一致

```
void printmy(int val) {
	cout << val << " ";
}
void text01() {
	vector<int>v;
	vector<int>v1;
	for (int i = 0; i < 5; i++) {
		v.push_back(i);
		v1.push_back(i + 1);
	}
	vector<int>v2;
	v2.resize(10);
	merge(v.begin(), v.end(), v1.begin(), v1.end(), v2.begin());
	for_each(v2.begin(), v2.end(), printmy);
}
```

#### 5.3.4 reverse

reverse(beg,end)

范围内元素进行反转

### 5.4 常用拷贝和替换算法

copy 容器内指定元素拷贝到另一容器

replace  容器内指定范围内的旧元素改为新元素

replace_if  容器内指定范围满足条件的元素替换为新元素

 swap    互换两个容器的元素

#### 5.4.1 copy

copy(beg,end,dest)

开始迭代器，结束迭代器，目标起始迭代器

#### 5.4.2 replace

replace(beg,end,oldvalue,newvalue)

区间内旧元素替换为新元素

#### 5.4.3 replace_if

replace_if(beg,end,_func,newvalue)

```
void printmy(int val) {
	cout << val << " ";
}
class person {
public:
	bool operator()(int val) {
		return  val > 2;
	}
};
void text01() {
	vector<int>v;
	for (int i = 0; i < 5; i++) {
		v.push_back(i);
		
	}
	vector<int>v2;
	v2.resize(v.size());
	copy(v.begin(), v.end(), v2.begin());
	for_each(v2.begin(), v2.end(), printmy);
	replace(v2.begin(), v2.end(), 2, 200);
	for_each(v2.begin(), v2.end(), printmy);
	cout << endl;
	replace_if(v2.begin(), v2.end(), person(), 200);
	for_each(v2.begin(), v2.end(), printmy);
}
```

#### 5.4.4 swap

swap(c1,c2)

放入两个同类型容器

```
void text01() {
	vector<int>v;
	vector<int>v2;
	for (int i = 0; i < 5; i++) {
		v.push_back(i);
		v2.push_back(i + 1);
	}
	
	swap(v, v2);
	for_each(v.begin(), v.end(), printmy);
	for_each(v2.begin(), v2.end(), printmy);
}

```

### 5.5 常用算数生成算法

属于小型算法 头文件<numeric>

accmulate 计算容器元素累计总和

fill     向容器中添加元素

#### 5.5.1 accumulate

accumulate(beg,end,value)

计算容器内元素总和

#### 5.5.2 fill

fill(beg,end,value)

向容器内填充指定数据

### 5.6 常用集合算法

set_intersection //求两个容器的交集

set_union 求两个容器的并集

set_difference 求两个容器的差集

#### 5.6.1 set_intersection

set_intersection(beg1,end1,beg2,end2,dest)

```
void printmy(int val) {
	cout << val << " ";
}
class person {
public:
	bool operator()(int val) {
		return  val > 2;
	}
};
void text01() {
	vector<int>v;
	vector<int>v2;
	for (int i = 0; i < 5; i++) {
		v.push_back(i);
		v2.push_back(i + 1);
	}
	vector<int>v3;
	v3.resize(v.size() + v2.size());
	set_intersection(v.begin(), v.end(), v2.begin(), v2.end(), v3.begin());
	for_each(v3.begin(), v3.end(), printmy);
}

```

#### 5.6.2 set_union

set_union(beg,end,beg2,end2.dest)

注意：两个容器必须有序

#### 5.6.3 set_diffence

set_difference(beg,end,beg1,end1,dest)

注意：两个容器必须有序


## 相关条目
- [[c++核心编程]]
- [[红黑树]]
- [[平衡二叉树旋转机制]]
