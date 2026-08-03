# Day03

## 样式CSS

CSS：Cascading Style Sheets

用来设计界面的外观，起美化的作用

HTML+CSS+JavaAScript构成前端网页

HTML负责显示的内容

CSS是风格，是外观

JavaScript负责与用户交互

## 使用CSS

-可以使用style属性

-可以使用style标签

比如让一个列表项显示蓝色背景，白色文字

```html
	<ul>
			<li style="background-color: skyblue;">新闻</li>
			<li>产品</li>
			<li>促销</li>
		</ul>
```

设计一个表格的外观

```html
ul>
			<li style="background-color: skyblue;">新闻</li>
			<li>产品</li>
			<li>促销</li>
		</ul>
		<table>
			<tr>
				<td>1行1列</td><td>1行2列</td><td>1行3列</td><td>1行4列</td>

			</tr>
			<tr>
				<td>2行1列</td><td>2行2列</td><td>2行3列</td><td>2行4列</td>	
			</tr>
			<tr>
				<td>3行1列</td><td>3行2列</td><td>3行3列</td><td>3行4列</td>
			</tr>
			

```

## 定位

定位可以控制页面元素在页面上的位置

三种定位：

-相对定位：所控制元素相对它在父元素的位置

-绝对定位：所控制元素相对父元素的位置

固定定位：所控制元素的位置不随窗口滚动而变化，是相对于浏览器窗口的位置

### 选择器

-ID选择器，可以精准的控制页面上的每一个元素，该选择器用#开头定义样式，同时页面上的元素要用id属性来定义元素的id

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<style>
			div{}
			#div1{
				width: 200px;
				height: 200px;
				border: 1px solid red;
				position: relative;/*相对定位*/
				top: 50px;/*当前div的左上角位于它父对象的50px处，相当于y坐标*/
				left: 50px;/*相当与x坐标*/
			}
			#div2{
				width: 200px;
				height: 200px;
				border: 1px solid red;
				position: absolute;/*绝对定位*/
				top: 100px;/*当前div的左上角位于它父对象的50px处，相当于y坐标*/
				left: 100px;/*相当与x坐标*/
			}
			#div3{
				width: 200px;
				height: 200px;
				border: 1px solid red;
				position: fixed;/*相对定位*/
				top: 50px;/*当前div的左上角位于它浏览器窗口的50px处，相当于y坐标*/
				left: 50px;/*相当与x坐标*/
			}
		</style>
	</head>
	<body>
		<div style="width: 400px;height:400px;border:1px solid gray;
			position:relative;top:50px;left:50px;">
			<div id="div1">相对定位</div>
			<div id="div2">绝对定位</div>
			<div id="div3">固定定位</div>
		</div>
		<div style="height: 800px;"></div>
	</body>
</html>
```



## 选择器

作用：用来选中页面上的元素，可以是选中单个元素，也可以是选中一类元素，还可以是选中所有元素。

-ID选择器，可以选中单个元素，用id属性来控制

-类选择器：在样式定义中以“.”点开头的样式，同时页面元素要用class属性来指定类名。

-标签选择器：使用HTML元素的标签定义

-伪类选择器：动态响应文档结构变化或用户交互行为



```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<style>
		li{background-color: aqua;
		   width: 200px;
		}	/*类选择器  */
			.myLi{
				border:1px solid #cccccc;/*#ccccc十六进制的颜色值*/
				
			}
			/* 伪类选择器,鼠标悬停 */
			.myLi:hover{
				background-color: blueviolet;
				color: #ffffff;
			}
			table{
				width: 80%;
				border-collapse: collapse;
			}
			td{
				border:1px solid lightgray;
				text-align: center;
				
			}
			tr:hover{
				background-color: chartreuse;
				
			}
			
		</style>
	</head>
	<body>
		<u1>
			<li class="myLi">Java</li>
			<li class="myLi">JavaWEB</li>
			<li class="myLi">MySQL</li>
			
		</u1>
		
		<table>
			<tr>
				<td>1行1列</td><td>1行2列</td><td>1行3列</td><td>1行4列</td>
		
			</tr>
			<tr>
				<td>2行1列</td><td>2行2列</td><td>2行3列</td><td>2行4列</td>	
			</tr>
			<tr>
				<td>3行1列</td><td>3行2列</td><td>3行3列</td><td>3行4列</td>
			</tr>
			
			
	</body>
</html>
```



## 背景

背景可以设置背景色，还可以设置背景图片

```html
	body{background-image: url(img/img_flwr.gif),url(img/paper.gif);
			     background-position: right bottom,left top;
			     background-repeat: no-repeat,repeat;
			}
```



## 练习

-ul列表显示4个列表项，当鼠标经过列表项时，显示orange背景，字体白色

-table表格，4行4列，奇数行显示skyblue背景色，偶数行显示orange背景色

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        li{
            background-color:red;
        }
        .my:hover{
            background-color:orange;
            color:#ffffff;
        }
        .my1:hover{
            background-color:skyblue;
            color:#ffffff;
        }
        .my2:hover{
            background-color:orange;
            color:#ffffff;
        }
        table{
            width:80%;
            border-collapse:collapse;
        }
        td{
            border:1px solid lightgray;
            text-align:center;
        }
    </style>
</head>
<body>
    <ul>
        <li class="my">第一项</li>
        <li class="my">第二项</li>
        <li class="my">第三项</li>
        <li class="my">第四项</li>
    </ul>
    <table>
         <tr class="my1">
            <td class="my2">1行1列</td>
            <td>1行2列</td>
            <td>1行3列</td>
            <td>1行4列</td>
        </tr>
        <tr class="my2">
            <td>2行1列</td>
            <td>2行2列</td>
            <td>2行3列</td>
            <td>2行4列</td>
        </tr>
        <tr class="my1">
            <td>3行1列</td>
            <td>3行2列</td>
            <td>3行3列</td>
            <td>3行4列</td>
        </tr>
        <tr class="my2">
            <td>4行1列</td>
            <td>4行2列</td>
            <td>4行3列</td>
            <td>4行4列</td>
        </tr>
    </table>
</body>
</html>
```



## 文字效果

可以指定文字的阴影效果，4个参数：

- 水平方向的阴影
- 垂直方向的阴影
- 阴影的程序
- 阴影的颜色

```
h1{
           /* border:1px solid black; */
          text-align:center;
            text-shadow:10px 10px 5px #9b1b1b;
        }
        ul{
            box-shadow:5px 5px 5px ;
            width:200px;
        }
```

## 链接样式

链接是a标签

它的默认样式是带下划线，点击前和点击后文字颜色不一样

```
a{
            text-decoration:none;/* 去掉下划线 */
            color:gray;
        }
        a:hover{
            color:red;
        }
```

## 盒子模型

用来布局页面

是样式的核心技术

它的思想是把页面的每一个元素看成一个盒子

每个盒子有宽高，盒子边框的厚度，盒子中内容和盒子边框的距离（padding）内边距

两个盒子之间的距离，外边距（marging）

通过盒子大小和内外边距设计页面


## 相关条目
- [[Day02]]
- [[Day04]]
