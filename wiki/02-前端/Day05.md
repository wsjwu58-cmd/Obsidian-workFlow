## JavaScript

脚本语言，是一边解释，一边执行

HTML负责内容，CSS负责美化，JavaScript负责互动

- 可以校验表单内容的合法性：是不是空内容，是不是数字，是不是格式完整等
- 动态获取后台数据，以及动态提交后台数据
- 页面动态效果展示，如动画等

简称JS，JS的代码可以在元素的属性中，也可以在<script>标签中，也可以定义在专门的js文件中

<button onclick="alert()">弹出对话框</button>

onclick是按钮中的一个点击事件，单击，所有事件都以on开头

alert 是弹窗

console.log 是在控制台输出内容

function 定义函数

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        a{
            display:block;
            border:1px solid gray;
            width:80px;
            text-decoration:none;
            color:gray;
            background-color:skyblue;
        }
    </style>
</head>
<body>
    <button onclick="alert()">弹出对话框</button>
    <input type="button" value="显示年龄" onclick="showage()">
    <a href="javascript:showage()">显示年龄</a>
</body>
<script>
        // alert("HELLO ");弹窗
        console.log("hello world"); //在控制台输出内容
        let age=19;
        console.log("你的年龄是："+  age);
    //定义函数
    function showage(){
        alert("你的年龄是："+age);
    }
    </script>
</html>
```

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        a{
            display:block;
            border:1px solid gray;
            width:80px;
            text-decoration:none;
            color:gray;
            background-color:skyblue;
        }
    </style>
    <script>
        // let obj=11;
        // obj="cat";
        // obj=[1,2,3];
        let n =prompt("请输入一个数字",8);
        if(n){
            alert("你输入的数字是："+n);
        }
        else
            alert("你没有输入数字");
        for(let i=0;i<10;i++){
            //alter("i="+i);
            let n=Math.random();
            alert(n);
        }
        while(1){
            let m=prompt("请输入");
            if(m){
                if(m>n){
                    alert("大了");
                }
                if(m<n){
                    alert("小了");
                }
                if(m==n){
                    alert("恭喜你猜对了");
                    break;
                }
            }
            else{
                alter("你输入发无效");
            }
        }
    </script>
 </head>



<body>
    <button onclick="alert(obj)">弹出对话框</button>
    <input type="button" value="显示年龄" onclick="showage()">
    <a href="javascript:showage()">显示年龄</a>
    <input type="button" value="加法" onclick="plus()">
</body>



<script>
        // alert("HELLO ");弹窗
        console.log("hello world"); //在控制台输出内容
        let age=19;
        console.log("你的年龄是："+  age);
    //定义函数
        function showage(){
        alert("你的年龄是："+age);
        }
    function plus(){
        let n1=prompt("请输入第一个数");
        let n2=prompt("请输入第二个数");
        let n3;
        if(n1&&n2){
            n3=Number(n1)+Number(n2);
            alert(n1+"+"+n2+"="+n3);
        }
        else
            alert("输入的数字无效")
    }
    </script>
</html>
```

## 练习：计算器

用table 表格布局实现一个计算器

用三个变量分别存储第一个数，第二个数，运算符，在点“=”按钮时弹出运算的结果

## DOM

文档对象模型，javascript的核心对象

通过DOM对象可以操作页面内容

把整个网页作为一个文档，页面上的每个元素都是这个文档的一部分

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .op{
            width:100%;
        }
        .op1{
            width:100%;
            background-color:red;
            color:white;
        }
        .second{
            color:white;
            background-color:blue;
        }
        .table{
            width:1000px;
            margin:auto;
        }
    </style>
</head>
<body>
    <h1 style="text-align:center">个人社保计算器</h1>
    <table class="table table-bordered  table-hover ">
        <tr>
            <td>工资</td>
            <td colspan="3"><input id="salary" placeholder="请输入工资" class="op"></td>
            <td><button onclick="calc()" class="op1">计算</button></td>
        </tr>
        <tr class="second">
            <td>险种</td>
            <td>个人%</td>
            <td>个人</td>
            <td>公司%</td>
            <td>公司</td>
        </tr>
        <tr>
        <td>养老</td>
        <td class="per">8%</td>
        <td></td>
        <td class="per1">20%</td>
        <td></td>
        </tr>
        <tr>
            <td>医保</td>
            <td class="per">2%</td>
            <td></td>
            <td class="per1">6%</td>
            <td></td>
        </tr>
        <tr>
            <td>失业</td>
            <td class="per">0.5%</td>
            <td></td>
            <td class="per1">1.5%</td>
            <td></td>
        </tr>
        <tr>
            <td>工伤</td>
            <td></td>
            <td></td>
            <td class="per1">0.5%</td>
            <td></td>
        </tr>
        <tr>
            <td>生育</td>
            <td ></td>
            <td></td>
            <td class="per1">0.8%</td>
            <td></td>
        </tr>
        <tr>
            <td>公积金</td>
            <td class="per">12%</td>
            <td></td>
            <td class="per1">12%</td>
            <td></td>
        </tr>
        <tr>
            <td>合计</td>
            <td class="per">个人合计</td>
            <td></td>
            <td class="per1">公司合计</td>
            <td></td>
        </tr>
        <tr>
            
            <td class="zong">总额</td>
            <td  colspan="4"></td>
        </tr>
    </table>
</body>
<script>
    function calc(){
        let salary=document.getElementById("salary").value;
        // alert(salary);
        let pers=document. getElementsByClassName("per");
        // alert(pers.length);
        let per2=document.getElementsByClassName("per1");
        let persontotal=0;
        let gongtotal=0;
        let total=0;
        let per3=document.getElementsByClassName("zong");
        for(let i=0;i<pers.length-1;i++){
            let per=parseFloat(pers[i].innerHTML);
            per=per/100;
            let result=per*salary;
            result=result.toFixed(2);
            // alert(salary*per);
            // document.getElementById("old").innerHTML=salary*per;
            pers[i].nextElementSibling.innerHTML=result;
            persontotal=parseFloat(persontotal)+parseFloat(result);
        }
        pers[pers.length-1].nextElementSibling.innerHTML=persontotal;
        for(let i=0;i<per2.length-1;i++){
            let myper=parseFloat(per2[i].innerHTML);
            myper=myper/100;
            let result=myper*salary;
            result=result.toFixed(2);
            // alert(salary*per);
            // document.getElementById("old").innerHTML=salary*per;
            per2[i].nextElementSibling.innerHTML=result;
            gongtotal=parseFloat(gongtotal)+parseFloat(result);
        }
        per2[per2.length-1].nextElementSibling.innerHTML=gongtotal;
        per3[0].nextElementSibling.innerHTML=gongtotal+persontotal;

    }
</script>
</html>
```



## 相关条目
- [[Day04]]
- [[Day06]]
