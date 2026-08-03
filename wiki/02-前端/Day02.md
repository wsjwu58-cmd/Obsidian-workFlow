# Day02

## img

img标签是HTML中用来显示图片的标签

它有两个主要的属性：

- src图片的来源
- width:图片的外观大小

```
    <style>
        .myimg{
            width:1000px;
            height: 1000px;
        }
    </style>
</head>
<body>
    <!--src插入图片并设置宽高-->
    <img src="./img/1.png" class="myimg">
</body>
```

## 链接

<a><a>标签

a标签用来跳转定位资源

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图片</title>
    <style>
        .myimg{
            width:600px;
            height: 300px;
        }
    </style>
</head>
<body>
    <!--src插入图片并设置宽高-->
    <img src="./img/1.png" class="myimg">
    <!--href指定了链接的资源位置-->
    <!--a标签是显示的文字-->
    <a href="https://www.baidu.com/index.php?tn=68018901_58_oem_dg">百度</a>
    <a href="https://www.nuc.edu.cn/index.htm">中北大学</a>
    <a href="#position1">去位置1</a>
    <a href="#position2">去位置2</a>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <!--定义锚点可以让链接快速定位-->
    <a name="position1">位置1</a>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <a name="position2">位置2</a>
</body>
</html>
```

## 表格

\<table>

```
     <table border="1">
     <tr>
         <td>第一列</td>
         <td>第二列</td>
         <td>第三列</td>
        </tr>
        <tr>
            <td>第一列</td>
            <td>第二列</td>
            <td>第三列</td>
        </tr>
        <tr>
            <td>第一列</td>
            <td>第二列</td>
            <td>第三列</td>
        </tr>
     </table>
```

border属性：指定表格和它的单元格边框的线条的宽度，border=1是一个像素宽

tr:table row 表格的行

td:table data 表格的数据

## 列表

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <!--无序列表-->
    <ul>
        <li>苹果</li>
        <li>梨</li>
        <li>香蕉</li>
    </ul>
    <!--有序列表-->
    <ol>
         <li>苹果</li>
        <li>梨</li>
        <li>香蕉</li>
    </ol>
    <h2>基本信息</h2>
    <ul>
        <li>姓名：张三</li>
        <li>性别：男</li>
        <li>出生日期：2006-8-02</li>
    </ul>
    <ol>
         <li>Java</li>
        <li>c</li>
        <li>python</li>
    </ol>
</body>
</html>
```

## 区块

\<div>

块、层，可以作为HTML元素的容器使用，在现代网页设计中是最主要的元素，现代网页设计模式是：DIV+CSS

一个div占一行，自动占满一行

```
<div style="background-color:aqua">1</div>
```

## 实体引用

实体引用也叫转义，是把一个字符串转换为特殊对象，如：&nbsp代表了空格（前面加反斜杠）

这些字符串都是以&开头，以分号结尾

一个例子，在中和国之间写空格

在网页中显示一个版权信息

在文本框中显示一个双引号

```
  <div style="background-color:aqua">1</div>
    <div>大宝&reg;中&nbsp;&nbsp;&nbsp;&nbsp;国&copy;
        <input value="123&quot;">
        <input value="我是一个&quot;超人&quot;">
        <input value='我是一个“超人”'>
    </div>
```

## 视频播放

```
   <div>
        <video src="./img/3.mp4"  width="400" controls autoplay></video>
    </div>
```

## 音频播放

```
    <div>
           <audio src="./img/4.mp3" controls></audio>
        </div>
```

embed和object会自动播放，audio可以手动播放


## 相关条目
- [[Day01]]
- [[Day03]]
