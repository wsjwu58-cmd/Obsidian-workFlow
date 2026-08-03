# 一、前端开发工具介绍

1. 前端怎么理解？前端就是软件的界面。
2. 前端开发工具有若干种

- HBuilderX：免费的,中国人开发的，非常优秀的前端与APP、小程序开发工具，来自中国公司DCloud
- WebStorm: 付费的,捷克的产品, JetBrains公司的产品;用来开发企业级项目前端,非常棒; 课后学习它
- VS Code: 免费的,美国微软的,万金油,啥都能开发;多数人用它开发前端,但非企业级。使用它需要安相应的插件。

# 二、商业项目解析

1. 商业项目的分层 = 前端 + 后端 + 数据库
2. 以12306为例：

- 用户看到的网页和APP属于:前端
- 查票、退票、选座：后端实现的
- 票的信息和交易数据：数据库里

# 三、企业项目开发流程（面试题）

1. 招投标
2. 签合同（岗位：商务、售前工程师）
3. 建立项目组（岗位：项目经理PM）
4. 需求调研与分析（岗位：需求分析工程师、需求管理工程师）
5. 架构设计（岗位：架构师，技术狂人）
6. 详细设计（岗位：系统分析师，侧重设计软件代码）
7. 数据库设计（岗位：DBA）
8. 开发（岗位：初级、中级、高级开发工程师）
9. 测试（岗位：测试工程师）
10. 实施部署（岗位：实施工程师）
11. 验收
12. 维护（岗位：技术支持工程师）

# 四、HTML技术

## 1.HTML介绍

- HTML是一种语言，它是用来做网页的
- 全称：HyperText Markup Language
- 它是W3C的标准（国际万维网联盟）
- HTML代码由浏览器执行
- 浏览器有哪些：Edge、Firefox、Chrome、Opera、Safari

## 2.网页结构

- head
- body

## 3.网页标题

- 共6级标题，从h1-h6

## 4.表单

- 文本框
- 密码框
- 单选按钮
- 复选框
- 下拉列表
- 文本域
- 文件上传
- 提交按钮

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>软件实践第一天</title>
</head>
<body>
    <h1>中北大学软件学院</h1>
    <h2>英才公司</h2>
    <h2>用户注册</h2>
    <form action="getinfo.html"> 
        用户名：<input type="text" placeholder="用户名设置不能更改">
        <br><br>
        密码：<input type="password" placeholder="请输入内容"> 
        <br><br>
        性别：<input type="radio" name="gender"> 男
        <input type="radio" name="gender"> 女
        <input type="radio" name="gender"> 保密
        <br><br>
        籍贯：<select>
            <option>山西大同</option>
            <option>河北沧州</option>
            <option>山西太原</option>
        </select>
        <br><br>
        爱好：<input type="checkbox">钓鱼
        <input type="checkbox">打篮球
        <input type="checkbox">骑行
        <input type="checkbox">旅行
        <br><br>
        自我介绍
        <textarea></textarea>
        <br>
        简历上传<input type="file">
        <br><br>
        <input type="submit" >我已阅读并遵守<p></p>
    </form>
</body>
</html>
```



## 相关条目
- [[Day02]]
- [[VUE]]
