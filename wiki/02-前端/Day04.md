## Bootstrap

一个前端的框架，集合了样式和HTML以及JAVAScript的内容

用少量代码实现丰富的效果

前端组件库，可以轻松实现移动设备的web页面，可以跨不同平台使用

container容器样式类，默认在容器和窗口间留有一定间距

container-fluld流动的可变的容器样式类，可以填充窗口宽度

```
<!DOCTYPE html>
<html>
<head>
  <title>Bootstrap5 实例</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="./bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="./bootstrap/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>

<div style="border:1px solid red" class="container">
  <h1>我的第一个 Bootstrap 页面</h1>
  <p>这是一些文本。</p> 
</div>
<div style="border:1px solid red" class="container-fluid">
  <h1>我的第一个 Bootstrap 页面</h1>
  <p>使用了 .container-fluid，100% 宽度，占据全部视口（viewport）的容器。</p> 
</div>

</body>
</html>
```

## 网格

把页面水平分为12份，也就是12列，可以指定元素占多少列

## 表格

```
<!DOCTYPE html>
<html>
<head>
  <title>Bootstrap5 实例</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="./bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="./bootstrap/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>

<div style="border:1px solid red" class="container">
  <h1>我的第一个 Bootstrap 页面</h1>
  <p>这是一些文本。</p> 
</div>
<div style="border:1px solid red" class="container-fluid">
  <h1>我的第一个 Bootstrap 页面</h1>
  <p>使用了 .container-fluid，100% 宽度，占据全部视口（viewport）的容器。</p> 
</div>
<div class="container-fluid mt-3">
  <h1>创建相等宽度的列</h1>
  <p>创建三个相等宽度的列! 尝试在 class="row" 的 div 中添加新的 class="col" div，会显示四个等宽的列。</p>
  <div class="row">
    <div class="col">4</div>
    <div class="col">4</div>
    <div class="col">4</div>
  </div>
  <div class="row">
  <div class="col">6</div>
  <div class="col">6</div>
</div>
<div class="row">
    <div class="col-sm-3 ">.col</div>
    <div class="col-sm-3 ">.col</div>
    <div class="col-sm-3">.col</div>
    <div class="col-sm-3 ">.col</div>
  </div>
  <div class="row">
    <div class="col-xl-3 ">.col</div>
    <div class="col-xl-3 ">.col</div>
    <div class="col-xl-3">.col</div>
    <div class="col-xl-3 ">.col</div>
  </div>
</div>
<div class="container mt-3"> <!--container固定宽度并居中 mt是间距类-->
  <h2>基础表格</h2>
  <p>.table 类来设置基础表格的样式:</p>            
  <table class="table table-bordered  table-hover table-striped ">
    <thead>
      <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>John</td>
        <td>Doe</td>
        <td>john@example.com</td>
      </tr>
      <tr>
        <td>Mary</td>
        <td>Moe</td>
        <td>mary@example.com</td>
      </tr>
      <tr>
        <td>July</td>
        <td>Dooley</td>
        <td>july@example.com</td>
      </tr>
    </tbody>
  </table>
</div>
</body>
</html>
```

## 表单

学习使用Bootstrap 的类来设计表单页面

```
<div class="container mt-3">
  <h2>复选框</h2>
  <p>.form-check-label 类添加到标签元素，.form-check 容器内添加 .form-check-input 类来设置复选框的样式。</p>
  <p>以下三个复选框，第一个默认选中，最后一个禁止选择：</p>
  <form action="/action_page.php">
    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="check1" name="option1" value="something" checked>
      <label class="form-check-label" for="check1">Option 1</label>
    </div>
    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="check2" name="option2" value="something">
      <label class="form-check-label" for="check2">Option 2</label>
    </div>
    <div class="form-check">
      <input type="checkbox" class="form-check-input" disabled>
      <label class="form-check-label">Option 3</label>
    </div>
    <button type="submit" class="btn btn-primary mt-3">Submit</button>
  </form>
</div>
```

## 按钮

可以从大小，颜色，风格上区分

普通按钮，小按钮，大按钮

默认颜色，蓝色，绿色，红色

## 练习

两个页面：

add.html

list.html

add.html是一个表单页面，用来填写产品信息，并提交，提交后转到list.html

list.html是一个表格页面，显示所有产品信息，可以自拟一些数据

产品的数据有：

- id:编号
- name:名称
- price:价格
- number:数量
- unit单位(盒，箱)
- data_time 生产日期（使用Bootstrap的日期组件选择日期）
- batch:批次

在add.html的action属性填写list.html就可以实现页面跳转

list.html的页面表格使用Bootstrap的表格

## 相关条目
- [[Day03]]
- [[Day05]]
