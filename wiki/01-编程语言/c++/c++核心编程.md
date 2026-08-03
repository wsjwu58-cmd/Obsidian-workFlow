# c++核心编程

## 1.内存分区模型

代码区:存放函数体的二进制代码，有操作系统进行管理的。

全局区:存放全局变量和静态变量以及常量。

栈区:由编译器自动分配和释放，存放函数的参数值，局部变量。

堆区:由程序员分配和释放，存放函数的参数值。(主要利用new在堆区开辟内存)

### 1.1new运算符

```
#include<iostream>
using namespace std;
int* func() {
	int* a = new int(10);
	return a;
}
int main() {
	int* p = func();
	cout << *p << endl;
	return 0;
}
```

如果想释放堆区的数据，用delete。

## 2.引用

### 2.1引用的基本使用

语法:数据类型 & 别名=原名

### 2.2引用注意事项

引用必须初始化

引用在初始化后，不可以更改

```
int main() {
	int a = 10;
	int b = 20;
	int& c = a;
	c = b;
	cout << c << a << b;
	return 0;
}
```

### 2.3引用做函数返回值

注意：不要返回局部变量引用

用法:函数调用作为左值

```
int& text01() {
	int static a=10;
	return a;
}
int& text02() {
	int b = 20;
	return b;//不能返回临时变量
}
int main() {
	int& ref = text01();
	cout << ref << endl;
	cout << ref << endl;
	text01() = 1000;//如果函数返回值是引用，则函数可以做左值
	cout << text01() << endl;
	int& ref1 = text02();
	cout << ref1 << endl;
	cout << ref1 << endl;
	return 0;
}
```

### 2.4引用的本质

本质:指针常量

```
void func(int& ref) {
	ref = 100;
}
int main() {
	int a = 10;
	int& ref = a;//制度转换为 int* const ref=&a,指针常量不可更改
	ref = 20;//转换为 *ref=20
	cout << ref << endl;
	cout << a << endl;
	func(a);
	return 0;
}
```

## 3.类和对象

c++面向对象的三大特性：封装，继承，多态

c++认为万事万物都有对象，对象上有其属性和行为

### 3.1封装

```
const double pi = 3.14;
class circle{
public://权限
	int r;//属性
	double zhouchang() {
		return 2 * pi * r;//行为
	}
};
int main() {
	circle a;
	a.r = 10;
	cout<<a.zhouchang();
	return 0;
}
```

封装意义二：

类在设计时，可以把属性和行为放在不同的权限下，加以控制

访问权限：

**公共权限 public--->成员类内可以访问，类外可以访问**

**保护权限 protected-->成员类内可以访问，类外不可以访问，儿子可以访问父亲保护的内容**

**私有权限private----> 成员类内可以访问，类外不可以访问  儿子不可以访问父亲的私有内容**

```
class preson {
public:
	string m_name;

protected:
	string m_car;
public:
	void func() {
		m_name="杭三";
		m_car="皮卡"; //类内可以访问
	}
};

int main() {
	preson p1;
	p1.m_name = "李四";
	p1.func();
	//p1.car="宝马",私有权限类外不可以访问
	return 0;
}
```

#### 3.1.2 struct和class的区别

唯一区别:默认访问权限不同

struct:默认公共权限

class:默认私有权限

#### 3.1.3 成员属性设置私有

```
class student{
public:
	void getname(string id) {
		name = id;
	}
	string printname() {
		return name;
	}
	int getage() {
		return age;
	}
	void getidole(string s) {
		idole = s;
	}
protected:
	string name;//可读可写
	int age=18;//只读
	string idole;//只写
};
int main() {
	student a;
	a.getname("张三");
	cout << a.printname()<< endl;
	cout << a.getage() << endl;
	a.getidole("李四");
	return 0;
}
```

### 3.2 对象的初始化和清理

#### 3.2.1 构造函数和析构函数

这两个函数会被编译器自动调用，完成对象的初始化和清理工作。

构造函数：创建对象时为对象的成员赋值，编译器自动调用

析构函数：在对象销毁前自动调用。

**构造函数语法：类名(){}**

1.没有返回值

2.函数名称与类名相同

3.可以重载

4，只能调用一次。

**析构函数：~类名(){}**

1.没有返回值

2.函数名称与类名相同，在名称前加上符号~

3.不可以有参数，不能发生重载

4.只会调用一次

#### 3.2.2 函数分类以及调用

```
class person {
public:
	person() {
		cout << "无参构造函数的调用" << endl;
	}
	person(int a) {
		age = a;
		cout << "有参构造函数调用" << endl;
	}
	person(const person &p) {
		age = p.age;
		cout << "person的拷贝构造函数的调用" << endl;
	}
	~person() {
		cout << "析构函数的调用" << endl;
	}
	int age;
};
void text01() {
	//括号法
	//person p1;
	//person p2(10);
	//person p3(p2);
	//显示法
	person p1;
	person p2 = person(10);
	person p3 = person(p2);
	//隐式转换法
	person p4 = 10;
	person p5 = p4;
}
```

#### 3.2.3 拷贝构造函数的调用时机

- 使用一个创建完毕的对象来初始化一个新对象
- 通过值传递的方式给函数参数传值
- 以值方式返回局部对象

```
void dowork(person 
p) {
}
void text02() {
	person p;
	dowork(p);
} //值传递，拷贝和默认构造函数
```

#### 3.2.4 构造函数的调用规则

如果我们写了有参构造函数，系统不会提供默认构造，但依然会提供拷贝构造函数

如果写了拷贝构造函数，那么编译器不再提供其他的函数。

#### 3.2.5 深拷贝与浅拷贝

![image-20250615115225382](https://gitee.com/Wsj123789/wsj/raw/master/img/20250615120638547.png)

浅拷贝带来的问题是堆区内存重复释放

```
person(const person& p) {
	cout << "person拷贝构造函数的调用" << endl;
	m_age = p.m_age;
	//深拷贝操作
	m_height=new int(*p.m_height);
}
```

#### 3.2.6 初始化列表

```
class person {
public:
	person(int a,int b) :m_a(a), m_b(b){}
	int m_a, m_b;
};
int main() {
	person p(20,10);
	cout << p.m_a << p.m_b;
	return 0;
}
```

#### 3.2.7 类对象作为类成员



```
class phone {
public:
	phone(string pname) {
		m_pname = pname;
		cout << "phone的构造函数调用" << endl;
	}
	~phone() {
		cout << "phone析构函数的调用" << endl;
	}
	string m_pname;
};
class person {
public:
	person(string name,string Pname ):m_name(name),m_phone(Pname){
		cout << "person函数构造调用" << endl;
	}
	~person() {
		cout << "person析构函数的调用" << endl;
	}
string m_name;
phone m_phone;
};
//当其他类函数作为一个类的成员时，优先调用其他类的构造函数，析构函数则相反
void text01() {
	person p("张三", "苹果max");
	cout << p.m_name << p.m_phone.m_pname;
}
```

#### 3.2.8 静态成员

- 静态成员变量：所有对象共享一份数据，在编译阶段分配内存，类内声明，类外初始化（有访问权限）
- 静态成员函数：所有对象共享同一个函数，静态成员函数只能访问

```
class person{
public:
	static int m_a;
};
int person::m_a = 100;
void text01() {
	person p;
	cout << p.m_a << endl;//直接访问
	cout << person::m_a << endl;//间接访问
}
```

```
class person {
public:
	static void func() {
		a = 100;//静态成员函数可以访问
		//b = 2000 静态成员函数不能访问非静态常量，无法区分是哪个对象的
		cout << "静态函数调用" << endl;
	}
	static int a;
	int b;
	//静态函数有访问权限
};
void text01() {
	person p;
	p.func();
	person::func();
}
```

### 3.3 c++对象模型和this指针

```
class person {
	int m_a;
	static int m_b;//不属于类的对象
	void func() {//非静态成员函数不属于类的对象
	}
	static void func1() {};//静态成员函数不属于类的对象
};
int person::m_b = 100;
void text01() {
	person p;
	//c++编译器会给每个空对象分配一个字节空间，是为了区分空对象占内存的位置
	//每个空对象也应该有一个独一无二的内存地址
	cout << sizeof(p) << endl;
};
```

#### 3.3.1 this 指针

```
class person {
public:
	person(int age) {
		//this指针指向的是被调用的成员函数所属的对象
		this->age = age;
	}
	person& personage(person &p) {//用引用做函数返回值，返回类本身
		this->age += p.age;//若返回值，则会拷贝一个新的person类型，无法对原类成员进行修改
		return *this;
	}
	int age;
};
void text01() {
	person p(18);
	cout << p.age;
};
void text02() {
	person p1(19);
	person p2(10);
	//链式编程思想
	p2.personage(p1).personage(p1).personage(p1);
	cout << p2.age << endl;
}
```

#### 3.3.2 空指针访问成员函数

#### 3.3.3 const指针修饰成员函数

常函数：

- 在成员函数后加const，修饰this指针，使得它指向的值不可以修改
- 常函数内不能修改成员属性
- 成员属性声明时加关键字mutable后，在常函数中依然可以修改

常对象：

- 声明对象前加const为常对象
- 常对象只能调用常函数

```
class person{
public:
	void func() {
		cout << "调用" << endl;

	}
	void func1(int age) const{
		m_abs = age;
	}
	int m_age;
	mutable int m_abs;//特殊变量，在常函数中可以修改值
};
//常对象只能调用常函数
void text01() {
	const person p;
	p.m_abs = 199;
	p.func1(10);
	cout << p.m_abs << endl;
}
```

### 3.4 友元

友元的目的是让一个函数或类访问另一个类中的私有成员

#### 3.4.1全局函数做友元

在类中定义全局函数并在前加上friend

```
class person {
	friend void goodway(person build);
public:
	string building;
private:
	string address;
};
void goodway(person build) {
	cout <<"成功访问" << build.address << endl;
}
```

#### 3.4.2 类做友元

```
class Building;
class goodway {
public:
	goodway();
	void visit();//参观函数访问Building中的属性
	Building* building;
};
class Building{
	friend class goodway;//使得class可以访问building中的private成员
public:
	Building();
public:
	string m_sitroom;
private:
	string m_redroom;
};
Building::Building() {
	m_sitroom = "客厅";
	m_redroom = "卧室";
}
goodway::goodway() {
	building = new Building;
}
void goodway::visit() {
	cout << building->m_sitroom << endl;//调用building构造函数，给成员赋值
	cout << building->m_redroom << endl;
}
```

#### 3.4.3 成员函数做友元

```
class goodway {
public:
	goodway();
	void visit();//让visit函数访问Building中的私有成员
	void visit2();//让visit2函数不可以访问Building私有成员
	Building* building;
};
class Building{
	friend void goodway::visit();
public:
	Building();
public:
	string m_sitroom;
private:
	string m_bedroom;
};
```

### 3.5运算符重载

#### 3.5.1加号运算符重载

```
class person {
public:
	person operator+(person a) {
		person temp;
		temp.m_a = this->m_a + a.m_a;
		temp.m_b=this->m_b + a.m_b;
		return temp;
	}
	int m_a;
	int m_b;
};
void text01() {
	person p1;
	p1.m_a = 10;
	p1.m_b = 10;
	person p2;
	p2.m_a = 10;
	p2.m_b = 10;
	person p3 = p1 + p2;
	cout << p3.m_a << p3.m_b;
}
person operator+(person a,person b){
	person temp;
	temp.m_a = b.m_a + a.m_a;
	temp.m_b = b.m_b + a.m_b;
	return temp;
}
```

#### 3.5.2 左移运算符重载

```
class person {
	friend ostream& operator<<(ostream& cout, person& p);
public:
	person() {
		m_a = 10;
		m_b = 20;
	}
private:
	int m_a;
	int m_b;
	//void operator<<(ostream& cout)
	//本质：p.operator<<(cout)-->p<<cout 不符合规范
};
ostream & operator<<(ostream &cout, person &p) {//本质：operator<<(cout,p)-->cout<<p;
	cout << p.m_a;
	cout << p.m_b;
	return cout;
}
void text01() {
	person p;
	cout << p <<"www" << endl;//链式编程思想，返回cout
}
```

#### 3.5.3 递增/减运算符重载

```
class person {
	friend ostream& operator<<(ostream &cout, const person &p);
public:
	person(int a, int b) {
		m_a = a;
		m_b = b;
	}
	person & operator--() {
		m_a --;
		m_b--;
		return *this;
	}
	const  person operator--(int) {
		person temp = *this;
		m_a--;
		m_b--;
		return temp;
	}
private:
	int m_a;
	int m_b;
};
ostream & operator<<(ostream &cout, const person &p) {
	cout << p.m_a << endl;
	cout << p.m_b << endl;
	return cout;
}
void text01() {
	person p1(10, 20);
	cout << p1--;
	cout << p1;
	cout << --(--p1);
}
```

以引用为返回值的函数，可以通过值传递，可以通过引用传递。

以值为返回值的函数，通过引用传递时，必须在引用前加const，因为非const的引用不能绑定临时对象

#### 3.5.4 赋值运算符重载

c++编译器给一个类添加四个函数：构造，析构，拷贝构造，赋值运算符 operator=对属性值拷贝

```
class person {
public:
	person(int age) {
		m_age=new int(age);
	}
	person & operator=(person &p) {
		//先判断是否有属性在堆区，如果有先释放干净，然后再深拷贝
		if (m_age == NULL) {
			delete m_age;
			m_age = NULL;
		}
		m_age = new int(*p.m_age);
		return *this;
	}
	~person(){
		if (m_age != NULL) {
			delete m_age;
			m_age = NULL;
		}
		cout << "析构函数的调用" << endl;
	}
	int *m_age;
};
void text02() {
	person p2(10);
	person p3(29);
	person p4(39);
	p2 = p3 = p4;
	cout << *p2.m_age << *p3.m_age << *p4.m_age << endl;
}
```

编译器默认提供的赋值运算符是m_age=p.age的浅拷贝,在释放内存时会重复释放。

#### 3.5.5  关系运算符重载

让两个自定义对象进行对比

```
class person {
public:
	person(string name, int age) {
		m_name = name;
		m_age = age;
	}
	bool operator==(person &p) {
		if (this->m_name == p.m_name && this->m_age == p.m_age) {
			return true;
		}
		return false;
	}
	string m_name;
	int m_age;
};
```

#### 3.5.6 函数调用运算符重载

仿函数

```
class person {
public:
	//仿函数，重载小括号，形式不唯一
	int operator()(int a,int b) {
		return a + b;
	}
};
void text1() {
	person p1;
	int ret = p1(10, 20);
	cout << ret << endl;
	//匿名函数对象，用完释放
	cout << person()(10, 20);
}
```

### 3.6 继承

定义类时，下级成员会有上级成员的一些共性以及自己的特性

可以用继承来减少重复代码

#### 3.6.1 继承的基本语法

class 子类 :继承方式 父亲

#### 3.6.2 继承方式

不管哪种继承方式，都不能访问私有成员

- 公共继承：父类中公共权限成员和保护权限成员到子类中依然相同
- 保护继承：父类中公共权限成员和保护权限成员到子类中成为保护权限
- 私有继承：父类中公共权限成员和保护权限成员到子类中成为私有权限

#### 3.6.3 继承中的对象模型

父类中所有非静态成员属性都会被子类继承下去，父类中私有属性被编译器隐藏，所以不能访问

利用开发人员命令提示工具查看对象模型

跳转盘符  D： 跳转文件路径 cd

查看命名：dir

cl /d1 reportSingleClassLayoutson .\text1.cpp

#### 3.6.4 继承中构造和析构顺序

先构造父类，再构造子类

析构与构造顺序相反

#### 3.6.5 继承同名成员的处理方式

```
class base {
public:
	base() {
		m_a = 100;
	}
	void func() {
		cout << "base" << endl;
	}
	void func(int a) {
		cout << "base1" << endl;
	}
	int m_a;
};
class son : public base {
public:
	son() {
		m_a = 200;
	}
	void func() {
		cout << "son" << endl;
	}
	int m_a;
};
void texy01() {
	son s1;
	cout << s1.m_a;
	cout << s1.base::m_a;
}
void text02() {
	son s2;
	s2.func();
	//如果子类中函数名与父类相同，则会隐藏所有父类同名函数，如果要调用需要加作用域
	s2.base::func(100);
}
```

#### 3.6.6 继承同名静态成员处理

静态成员有两种访问方式

```
void text01() {
	son s1;
	cout << s1.m_a;
	cout << s1.base::m_a;
	//通过类名的方式进行访问
	cout << son::m_a << endl;
	cout << son::base::m_a << endl;
}
```

#### 3.6.7 菱形继承

两个类继承同一个类

有一个类同时继承这两个类

![image-20250627183808576](https://gitee.com/Wsj123789/wsj/raw/master/img/20250822094226104.png)

```
class animal{//虚基类
public:
	int m_a;
};
class sheep:virtual public animal{};//虚继承
class tuo:virtual public animal{};
class yt:public sheep,public tuo{};
void text01() {
	yt s1;
	s1.sheep::m_a = 18;
	s1.tuo::m_a = 28;
	cout << s1.sheep::m_a << endl;
	cout << s1.tuo::m_a << endl;//输出28
}
```

虚继承只有一份数据

### 3.7 多态

#### 3.7.1 基本概念

- 静态多态：函数重载和运算符重载，复用函数名
- 动态多态：派生类和虚函数实现运行多态

静态多态和动态多态的区别：

- 静态多态分函数地址早绑定--编译阶段确定函数地址
- 动态多态的函数地址晚绑定--运行阶段确定函数地址

```
class animal {
public:
//虚函数
	virtual void speak() {
		cout << "动物在说话" << endl;
	}
};
class cat :public animal {
//重写：函数返回值类型，函数名，参数列表完全相同
	public:
		void speak() {
			cout << "小猫在说话" << endl;
		}
};
class dog:public animal {
	void speak() {
		cout << "小狗在说话" << endl;
	}
};
//地址早绑定 在编译阶段确定函数地址
//如果想执行猫说话,地址晚执行
//动态多态满足条件：
//1.有继承关系
//2.子类重写父类中的虚函数
void dospeak(animal& manimal) {
	manimal.speak();
}
void text01() {
	cat mcat;
	dospeak(mcat);
	dog mdog;
	dospeak(mdog);
}
```

vfptr----虚函数指针（指向虚函数表，表内部记录虚函数的地址 Animal&animal）

子类重写时，指向子类的虚函数表

#### 3.7.2 案例：计算器(普通和多态)

```

class calculator {
public:
	int getresult(string oper) {
		if (oper == "+") {
			return m_num1 + m_num2;
		}
		else if (oper == "-") {
			return m_num1 + m_num2;
		}
		else if (oper == "*") {
			return m_num1 * m_num2;
		}
	}
	int m_num1;
	int m_num2;
};
void text01() {
	calculator c;
	c.m_num1 = 10;
	c.m_num2 = 10;
	cout << c.m_num1 << "+" << c.m_num2 << "=" << c.getresult("+") << endl;
}
//利用多态实现计算器
//组织结构清晰
//可读性强
//前期和后期拓展以及维护性高
class basscalculator {
public:
	virtual int getresult() {
		return 0;
	}
	int m_num1;
	int m_num2;
};
//加法计算器
class jia :public basscalculator {
public:
	int getresult() {
		return m_num1 + m_num2;
	}
};
//乘法计算器
class cheng :public basscalculator {
public:
	int getresult() {
		return m_num1 * m_num2;
	}
};
void text02() {
	basscalculator* p = new jia;
	p->m_num1 = 10;
	p->m_num2 = 10;
	cout << p->getresult() << endl;
	p = new cheng;
	p->m_num1 = 10;
	p->m_num2 = 10;
	cout << p->getresult() << endl;
}
```

#### 3.7.3 纯虚函数和抽象类

virtual 返回值类型 函数名 （参数列表）=0

#### 3.7.4 多态案例：制作饮品

```
class drink {
public:
	virtual void boil() = 0;
	virtual void brew() = 0;
	virtual void pour() = 0;
	virtual void fuzhu() = 0;
	void makedrink() {
		boil();
		brew();
		pour();
		fuzhu();
	}
};
class coffee :public drink {
public:
	virtual void boil() {
		cout << "农夫山泉" << endl;
	}
	virtual void brew() {
		cout << "冲泡" << endl;
	}
	virtual void pour() {
		cout << "倒入杯中" << endl;
	}
	virtual void fuzhu() {
		cout << "加入糖和牛奶" << endl;
	}
};
class cha :public drink {
public:
	virtual void boil() {
		cout << "农夫山泉" << endl;
	}
	virtual void brew() {
		cout << "冲泡" << endl;
	}
	virtual void pour() {
		cout << "倒入杯中" << endl;
	}
	virtual void fuzhu() {
		cout << "加入枸杞" << endl;
	}
};
void dowork(drink* abs) {
	abs->makedrink();
}
void text02() {
	dowork(new coffee);
}
```

#### 3.7.5 虚析构和纯虚析构

多态中如果子类中有属性开辟到堆区，那么父类指针无法释放

虚析构和纯虚析构解决了这个问题

```
class animal {
public:
	animal() {
		cout << "animal构造函数的调用" << endl;
	}
	//解决父类指针释放子类对象不干净的问题
	//virtual ~animal() {
		//cout << "aniaml析构函数的调用" << endl;
	//}
	//有纯虚析构这个类成为抽象类
	virtual ~animal() = 0;
	virtual void speak() = 0;

};
//需要声明也需要实现
animal::~animal() {
	cout << "纯虚析构函数的调用" << endl;
}
class cat :public animal {
public:
	cat(string name) {
		cout << "cat构造函数的调用" << endl;
		m_name = new string(name);
	}
	~cat() {
		if (m_name != NULL) {
			delete m_name;
			cout << "cat析构函数的调用" << endl;
			m_name = NULL;
		}
	}
	virtual void speak() {
		cout <<*m_name<< "小猫在说话" << endl;
	}
	string* m_name;
};
void text01() {
	animal* p = new cat("tom");
	p->speak();
	//父类指针在析构时候不会调用子类析构，会导致堆区的内存无法释放
	delete p;
}
```

#### 3.7.6 电脑组装具体实现

```
class cpu {
public:
	virtual void carculate() = 0;
	virtual ~cpu() {

	}
};
class xianka {
public:
	virtual void display() = 0;
	virtual ~xianka() {

	}
};
class memory {
public:
	virtual void storage() = 0;
	virtual ~memory() {

	}
};
class internet :public cpu {
public:
	void carculate() {
		cout << "internet的cpu开始计算了" << endl;
	}
	~internet() {
		
	}
};
class internet1 :public xianka {
public:
	void display() {
		cout << "internet的xianka开始运行了" << endl;
	}
};
class internet2 :public memory {
public:
	void storage(){
		cout << "internet的memory开始存储了" << endl;
	}
};
class lenovo :public cpu {
public:
	void carculate() {
		cout << "lenovo的cpu开始计算了" << endl;
	}
	
};
class lenovo1 :public xianka {
public:
	void display() {
		cout << "lenovo的xianka开始运行了" << endl;
	}
};
class lenovo2 :public memory {
public:
	void storage() {
		cout << "lenovo的memory开始存储了" << endl;
	}
};
class computer {
public:
	computer(cpu* CPU, xianka* XK, memory* MM) {
		mcpu = CPU;
		myxianka = XK;
		mymemory = MM;
	}
	void work() {
		mcpu->carculate();
		myxianka->display();
		mymemory->storage();
	}
	~computer() {
		if (mcpu != NULL) {
			delete mcpu;
			mcpu = NULL;
		}
		if (myxianka != NULL) {
			delete myxianka;
			myxianka = NULL;
		}
		if (mymemory != NULL) {
			delete mymemory;
			mymemory = NULL;
		}
	}
private:
	cpu* mcpu;
	xianka* myxianka;
	memory* mymemory;
};
void text01() {
	cpu* a = new internet;
	xianka* b = new internet1;
	memory* c = new internet2;
	computer* computer1 = new computer(a, b, c);
	computer1->work();
	delete computer1;
	computer* computer2 = new computer(new internet, new lenovo1, new lenovo2);
	computer2->work();
	delete computer2;

}
```

## 4.文件操作

头文件<fstream>

文本文件：文件以文本的ASCII码存储

二进制文件：文件以二进制形式存储，用户一般不能直接读懂

操作文件三大类：

1.ofstream:写操作

2.ifstream:读操作

3.fstream:读写操作

### 4.1文本文件

#### 4.1.1 写文件

1.头文件

2.创建流对象

ofstream ofs;

3.打开文件

ofs.open("文件路径",打开方式)

4.写数据

ofs<<"写入的数据";

5.关闭文件

ofs.close()



打开方式

| 打开方式    | 解释                         |
| ----------- | ---------------------------- |
| ios::in     | 为读文件而打开文件           |
| ios::out    | 为写文件而打开文件           |
| ios::ate    | 初始位置：文件尾             |
| ios::app    | 追加方式写文件               |
| ios::trunc  | 如果文件存在，先删除，再创建 |
| ios::binary | 二进制方式                   |

如果打开方式要配合使用，利用|操作符

```
void text01() {
	ofstream ofs;
	ofs.open("test.txt", ios::out);
	ofs << "姓名：张三" << endl;
	ofs << "年龄：10" << endl;
	ofs << "性别：男" << endl;
	ofs.close();
}
```

#### 4.1.2 读文件

1.头文件

2.创建流对象

ifstream ifs;

3.打开文件

ifs.open("文件路径",打开方式)

4.读数据

四种方式读取

5.关闭文件

ifs.close()

```
void text01() {
	//创建流对象
	ifstream ifs;
	//打开文件，并且判断是否打开成功
	ifs.open("test.txt", ios::in);
	if (!ifs.is_open()) {
		cout << "文件打开失败" << endl;
		return;
	}
	//第一种
	//char buf[1024] = { 0 };
	//while (ifs >> buf) {
	//	cout << buf << endl;
	//}
	//读数据
	// 第二种
	//char buf[1024] = {0};
	//while (ifs.getline(buf, sizeof(buf))) {
	//	cout << buf << endl;
	//}
	// 第三种
	//string buf;
	//while (getline(ifs, buf)) {
	//	cout << buf << endl;
	//}
	char c;
	while ((c = ifs.get()) != EOF) {
		cout << c;
	}

	ifs.close();
}
```

### 4.2 二进制文件

打开方式 ios::binary

#### 4.2.1 写文件

通过write函数，以二进制方式写数据

```
class person {
public:
	char m_name[64];
	int m_age;
};
void text01() {
	//包含头文件
	//创建流对象
	ofstream ofs;
	//打开文件
	ofs.open("text.txt", ios::out | ios::binary);
	//写文件
	person p = {"张三",19};
	ofs.write((const char*)&p, sizeof(person));
	ofs.close();
}
```

#### 4.2.2 读文件

```
public:
	char name[64];
	int m_age;
};
void text01() {
	ifstream ifs;
	ifs.open("text.txt", ios::in|ios::binary);
	if (!ifs.is_open()) {
		cout << "文件打开失败" << endl;
		return;
	}
	person p;
	ifs.read((char*)&p, sizeof(person));
	cout << p.name << p.m_age << endl;
	ifs.close();
}
```



## 相关条目
- [[C++模板和STL]]
- [[面向对象]]
