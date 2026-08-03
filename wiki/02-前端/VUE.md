

## Vue常用指令

指令：HTML标签上带有v-前缀的特殊属性，不同的指令具有不同的含义，可以实现不同的功能

### v-for

作用：列表渲染，遍历容器的元素或者对象的属性

语法：

```
<tr v-for="(item,index) in items":key="item.id">{{item}}</tr>
```

items:要遍历的数组

item:为遍历出来的元素

index:索引/下标，从0开始；

key:

作用：为元素添加唯一标识，便于vue进行列表项的正确排序复用，提升渲染性能

推荐使用id作为key(唯一)

### v-bind

作用：动态为HTML标签绑定属性值，如设置href,src,style样式等

语法：v-bind:属性名="属性值"

简化：：属性名=“属性值”

### v-if &v-show

作用：这两类指令，都是用来控制元素的显示与隐藏的

v-if

- 语法v-if="表达式"，表达式的值为true，显示：false，隐藏
- 原理：基于条件判断，来控制创建或移除元素节点
- 场景：要么显示，要么不显示， 不频繁切换的场景

v-show

- 语法：v-show="表达式",表达式的值为true，显示：false，隐藏
- 原理：基于CSS样式display来控制显示与隐藏
- 场景：频繁切换显示隐藏的场景

### v-on

作用：为html标签绑定事件（添加事件监听）

语法：

v-on：事件名=“方法名”

简写为 @事件名="..."

### v-model

- v-model指令可以在表单 input、textarea以及select元素上创建双向数据绑定；
- 它会根据控件类型自动选取正确的方法来更新元素；
- 尽管如此， v-model 本质上是语法糖，它负责监听用户的输入事件来更新数据，并在某种极端场景下进行一些特殊处理；

## Ajax

作用：

数据交换：通过Ajax可以给服务器发送请求，并获取服务器响应的数据

异步交互：可以在不重新加载整个页面的情况下，与服务器交换数据并更新部分网页的技术，如：搜索联想，用户名是否可用的校验等等

### 同步与异步

同步：客户端发起请求服务器，服务器处理，客户端等待，处理后返回客户端，客户端解除等待

异步：客户端发出请求后可以执行其他操作，服务器处理后返回

### Axios

对原生的Ajax进行了封装，简化书写，快速开发

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ajax</title>
</head>
<body>
    <input type="button" value="获取数据CET" id="btnGet">
    <input type="button" value="操作数据POST" id="btnPost">

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        //发送GET请求
        document.querySelector('#btnGet').addEventListener('click',()=>{
            //axios发布异步请求
            axios({
                url:'https://mock.apifox.cn/m1/3083103-0-default/emps/list',
                method:'GET'
            }).then((result)=>{//成功回调函数
                console.log(result);
            }).catch((err)=>{//失败回调函数
                console.log(err);
            })
    
        })
        //发送POST请求
        document.querySelector('#btnPost').addEventListener('click',()=>{
            axios({
                url:'https://mock.apifox.cn/m1/3083103-0-default/emps/upda',
                method:'POST',
                data:{id:1}//Post请求方式
            }).then((result)=>{//成功回调函数
                console.log(result);
            }).catch((err)=>{//失败回调函数
                console.log(err);
            })
        })
    </script>
</body>
</html>

## 项目结构

根组件

```
<script setup>

</script>

<template>
  <ElementDemo></ElementDemo>
  
</template>

<style scoped>

</style>

```

**index.html**

1. - 这是项目的入口HTML文件
   - 包含基本的HTML结构和元信息
   - 通过 `<script type="module" src="/src/main.js"></script>` 引入了 [main.js](javascript:void(0)) 文件
   - 提供了一个挂载点 `<div id="app"></div>` 用于渲染Vue应用
2. **src/main.js**
   - 这是Vue应用的入口JavaScript文件
   - 使用 `createApp` 创建Vue应用实例
   - 导入并挂载 [App.vue](javascript:void(0)) 组件到 `#app` 元素上
   - 导入全局样式文件 `./assets/main.css`
3. **src/App.vue**
   - 这是Vue应用的根组件
   - 使用 `<script setup>` 语法定义组件逻辑
   - 包含一个响应式数据 [message](javascript:void(0))
   - 在 `<template>` 中显示 [message](javascript:void(0)) 的值
   - 通过 [main.js](javascript:void(0)) 被挂载到页面上

整体流程：[index.html](javascript:void(0)) 加载 [main.js](javascript:void(0)) → [main.js](javascript:void(0)) 创建Vue应用并挂载 [App.vue](javascript:void(0)) → [App.vue](javascript:void(0)) 组件被渲染到 [index.html](javascript:void(0)) 的 `#app` 容器中。

只有在需要字符串插值或换行时才会使用反引号（模板字符串）。

### API

### 组合式API

```
<template>
  <div>
    <p>{{ count }}</p>
    <p>{{ doubledCount }}</p>
    <button @click="increment">增加</button>
    <button @click="decrement">减少</button>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// 响应式数据
const count = ref(0)
const message = ref('Hello')

// 计算属性
const doubledCount = computed(() => count.value * 2)

// 方法
const increment = () => {
  count.value++
}

const decrement = () => {
  count.value--
}

// 生命周期
onMounted(() => {
  console.log('组件已挂载')
})

// 监听器
watch(count, (newVal, oldVal) => {
  console.log(`count从${oldVal}变为${newVal}`)
})
</script>
```

### 选项式API

```
<template>
  <div>
    <p>{{ count }}</p>
    <p>{{ doubledCount }}</p>
    <button @click="increment">增加</button>
    <button @click="decrement">减少</button>
  </div>
</template>

<script>
export default {
  // 数据选项
  data() {
    return {
      count: 0,
      message: 'Hello'
    }
  },
  
  // 计算属性
  computed: {
    doubledCount() {
      return this.count * 2
    }
  },
  
  // 方法
  methods: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    }
  },
  
  // 生命周期
  mounted() {
    console.log('组件已挂载')
  },
  
  // 监听器
  watch: {
    count(newVal, oldVal) {
      console.log(`count从${oldVal}变为${newVal}`)
    }
  }
}
</script>
```

为了避免出现域名问题，需要在配置文件中指定访问的IP和端口号，且需要在请求路径前加前缀，避免访问到静态资源

```
server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        secure: false,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  }
```

### 发送请求和响应请求的逻辑以及结构

1. #### **请求发送流程**

- 使用 `axios` 创建 [request](javascript:void(0)) 实例，设置基础URL为 `/api`
- 通过 [request](javascript:void(0)) 实例的 HTTP 方法（get/post/put/delete）发送请求
- 请求会自动加上 `/api` 前缀，例如 `request.get('/depts')` 实际访问 `/api/depts`

2. #### **响应处理流程**

- `request.interceptors.response.use()` 设置了响应拦截器
- 成功响应时，拦截器直接返回 `response.data`，即只返回实际数据部分
- 失败响应时，拦截器将错误通过 `Promise.reject(error)` 向上抛出

3. #### **API 调用示例**

以 [queryAllApi](javascript:void(0)) 为例：

- 调用 `request.get('/depts')` 发送 GET 请求

- 请求地址实际为 `/api/depts`

- 响应拦截器处理后，只返回数据部分给调用方

  处理数据部分时，在代码中采用async和await进行数据接收，对接受过来的数据进行处理，如果返回状态吗正确，输出相应提示信息

## ElementPlus组件

参考文档

[一个 Vue 3 UI 框架 | Element Plus](https://element-plus.org/zh-CN/)

表格组件

```
<el-table :data="tableData" border style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" align="center" />
    <el-table-column prop="name" label="Name" width="180" align="center" />
    <el-table-column prop="address" label="Address" align="center"/>
  </el-table>
```

prop为列属性，label为标签名字

弹窗表格

```
<div class="button-row">
    <el-button plain @click="dialogVisible = true"> Click to open the Dialog</el-button>
    <el-dialog v-model="dialogVisible" title="收获表格" width="800">
    <el-table :data="tableData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-dialog>
```

分页组件

```
<div class="button-row">
    <el-pagination
      v-model:current-page="currentPage4"
      v-model:page-size="pageSize4"
      :page-sizes="[100, 200, 300, 400]"
      
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="400"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
   </div>
```

## Vue Router

Vue Router 是 Vue 官方的客户端路由解决方案。

客户端路由的作用是在单页应用 (SPA) 中将浏览器的 URL 和用户看到的内容绑定起来。当用户在应用中浏览不同页面时，URL 会随之更新，但页面不需要从服务器重新加载。

Vue Router 基于 Vue 的组件系统构建，你可以通过配置**路由**来告诉 Vue Router 为每个 URL 路径显示哪些组件。

1. **Route**
   - `route` 指的是单个路由规则，即你在 `routes` 数组里定义的对象
   - 每个 route 包含 `path`(路径)、`name`(名称)、`component`(对应渲染的组件) 等属性
   - 例如 `{path: '/login', name: 'login', component: LoginView}` 就是一个具体的 route 配置
2. **Router View**
   - `<router-view>` 是一个 Vue 组件，作为路由出口，用来显示当前路由匹配到的组件
   - 当 URL 改变时，`<router-view>` 会自动更新为对应的组件内容
   - 在嵌套路由中（如你配置中的 children），子组件也会渲染在父级的 `<router-view>` 内
3. **Router Link**
   - `<router-link>` 是一个特殊的组件，用于创建导航链接
   - 使用它可以在不重新加载整个页面的情况下切换不同的路由
   - 典型用法是设置 `to` 属性指向目标路由的路径或命名路由，例如 `<router-link to="/login">Login</router-link>`

### 嵌套路由

```
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
     path: '/', 
     name: '',
     component: LayoutView,
     redirect: '/index', //重定向
     children: [
      {path: 'index', name: 'index', component: IndexView},
      {path: 'clazz', name: 'clazz', component: ClazzView},
      {path: 'stu', name: 'stu', component: StuView},
      {path: 'dept', name: 'dept', component: DeptView},
      {path: 'emp', name: 'emp', component: EmpView},
      {path: 'log', name: 'log', component: LogView},
      {path: 'empReport', name: 'empReport', component: EmpReportView},
      {path: 'stuReport', name: 'stuReport', component: StuReportView}
     ]
    },
    {path: '/login', name: 'login', component: LoginView}
  ]
})
```

设置子路由实现路径映射，显示对应的组件

在对应组件通过link标签跳转对应的路径

在布局页面中对应的区域（比如左侧菜单）设置视图展示

```
<el-main class="main-content">
          <div class="content-wrapper">
            <router-view></router-view>
          </div>
        </el-main>
```

## Vuex

## TypeScript

### 介绍

是js的超集

在js基础上加入了类型支持

在编译期进行类型检查，减少找bug，改bug的时间

### 类型

#### 字符串，布尔，数字类型

```
//字符串类型
let str: string ='hello world'

//数字类型
let num: number=123

//布尔类型
let bool: boolean=true



console.log(str,num,bool)
```

#### 字面量类型

在指定数据中进行选择

```
function pringttest(s : string ,alignment: 'left' | 'center' | 'right'){
    console.log(s,alignment)
}
```

#### 接口和接口实现

```
//接口
interface Animal{
    name:string,
    age?:number
}

const a:Animal={
    name:'dog',
    age:12
}
console.log(a)
```

```
class Dog implements Animal{ 
    name:string;
    age:number;
    constructor(name:string,age:number){
        this.name=name,
        this.age=age
    }
}
const d=new Dog('小花',12)
console.log(d.name)
```

类的定义和继承

```
class User{
    name:string;
    age:number;
    constructor(name:string,age:number){
        this.name=name,
        this.age=age
    }
    study(){
        console.log(`[${this.name}]正在学习...`)
    }
}
const u=new User('张三',18)
u.study()
```

```
//继承
class Cat extends User{
    say(){
        console.log(`[${this.name}]正在说话...`)
    }
}

const c=new Cat('小猫',12)
c.study()
c.say()
```



## watch

Watch监听函数主要用于：

- 在数据变化时执行异步操作
- 在数据变化时执行开销较大的操作
- 监听特定数据的变化并执行相应逻辑
- 实现数据验证、数据联动等复杂业务逻辑

基本语法

```
// 选项式API
watch: {
  // 简单监听
  被监听的数据(newValue, oldValue) {
    // 响应数据变化的逻辑
  },
  
  // 深度监听
  被监听的数据: {
    handler(newValue, oldValue) {
      // 响应数据变化的逻辑
    },
    deep: true, // 深度监听对象内部值的变化
    immediate: true // 立即执行一次handler
  }
}

// 组合式API
import { watch } from 'vue'

watch(
  被监听的数据,
  (newValue, oldValue) => {
    // 响应数据变化的逻辑
  },
  {
    deep: true,
    immediate: true
  }
)
```

## 1. Vue 3 Composition API 核心概念

### `setup` 语法糖

javascript

```
<script setup>
// 所有内容都在setup中，无需return
import { ref, watch, onMounted } from 'vue'
```



- **原理**：`<script setup>` 是编译时语法糖，内部声明的变量、函数自动暴露给模板
- **优势**：代码更简洁，无需手动返回响应式数据

### 响应式系统

javascript

```
const empList = ref([])
const searchEmp = ref({ name: '', gender: '' })
```



**原理分析**：

- `ref()` 将基本类型包装为响应式对象，通过 `.value` 访问
- 在模板中自动解包，无需 `.value`
- Vue 3 使用 Proxy 实现响应式，比 Vue 2 的 Object.defineProperty 更强大

## 2. 生命周期管理

javascript

```
onMounted(() => {
  search()           // 初始化数据
  queryAllDepts()    // 加载部门数据
  getToken()         // 获取认证token
})
```



**生命周期流程**：

1. `onMounted` → 组件挂载完成后执行
2. 异步加载初始数据
3. 确保DOM已渲染，可以安全操作DOM

## 3. 数据侦听器 (Watch)

### 简单侦听

javascript

```
watch(() => searchEmp.value.date, (newValue, oldValue) => {
  // 处理日期范围变化
})
```



### 深度侦听

javascript

```
watch(() => employee.value.exprList, (newValue, oldValue) => {
  // deep: true 启用深度侦听
  employee.value.exprList.forEach(item => {
    item.begin = item.exprDate[0]
    item.end = item.exprDate[1]
  })
}, { deep: true })
```



**侦听器原理**：

- 第一个参数：要侦听的响应式数据
- 第二个参数：回调函数，数据变化时执行
- 第三个参数：配置选项（deep, immediate等）

## 4. 异步编程与 API 调用

### async/await 模式

javascript

```
const search = async () => {
  const result = await queryPageApi(
    searchEmp.value.name, 
    searchEmp.value.gender,
    searchEmp.value.begin,
    searchEmp.value.end,
    currentPage.value,
    pageSize.value
  )
  if (result.code) {
    empList.value = result.data.rows
    total.value = result.data.total
  }
}
```



**异步编程知识点**：

- `async` 函数返回 Promise
- `await` 暂停异步函数执行，等待 Promise 完成
- 错误处理通过 try-catch 或条件判断

## 5. 数组操作与函数式编程

### 数组方法应用

javascript

```
// 1. map - 数据转换
selectIds.value = val.map((item) => item.id)

// 2. forEach - 遍历操作
employee.value.exprList.forEach(item => {
  item.begin = item.exprDate[0]
  item.end = item.exprDate[1]
})

// 3. splice - 删除数组元素
employee.value.exprList.splice(index, 1)

// 4. push - 添加数组元素
employee.value.exprList.push({company:'', job:'', begin:'', end:'', exprDate:[]})
```



## 6. 表单处理与验证

### Element Plus 表单验证

javascript

```
const rules = ref({
  username: [
    { required: true, message: '用户名是必填项', trigger: 'blur' },
    { min: 2, max: 10, message: '用户名的长度应该在2-10位之间', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
  ]
})
```



**验证规则详解**：

- `required`: 必填字段
- `min/max`: 长度限制
- `pattern`: 正则表达式验证
- `trigger`: 触发时机（blur、change）

### 表单提交验证

javascript

```
const save = async () => {
  empFormRef.value.validate(async (valid) => {
    if (valid) {
      // 验证通过，提交数据
      let result = employee.value.id 
        ? await updateApi(employee.value)
        : await addApi(employee.value)
      
      if (result.code) {
        ElMessage.success('保存成功')
        dialogVisible.value = false
        search()
      }
    } else {
      ElMessage.error('请填写必要的表单数据！')
    }
  })
}
```



## 7. 文件上传处理

javascript

```
// 上传成功回调
const handleAvatarSuccess = (response) => {
  employee.value.image = response.data
}

// 上传前验证
const beforeAvatarUpload = (rawFile) => {
  // 文件类型验证
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('只支持上传图片')
    return false
  }
  // 文件大小验证
  else if (rawFile.size / 1024 / 1024 > 10) {
    ElMessage.error('只能上传10M以内图片')
    return false
  }
  return true
}
```



## 8. 条件渲染与列表渲染

### 动态样式类

vue

```
<el-icon class="avatar-uploader-icon">
  <Plus />
</el-icon>
```



### 条件渲染

vue

```
<img v-if="employee.image" :src="employee.image" class="avatar">
<el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
```



### 列表渲染

vue

```
<el-option v-for="g in genders" :key="g.value" :label="g.name" :value="g.value"></el-option>

<el-row v-for="(expr, index) in employee.exprList" :key="index">
  <!-- 动态生成工作经历表单项 -->
</el-row>
```



## 9. 事件处理

### 方法定义与调用

javascript

```
// 方法定义
const remove = (index) => {
  employee.value.exprList.splice(index, 1)
}

// 事件绑定
<el-button @click="remove(index)">- 删除</el-button>
```



### 事件修饰符

- `@click` - 点击事件
- `@change` - 值变化事件
- `@success` - 成功事件（上传组件）

## 10. 组件通信与引用

### 模板引用

javascript

```
const empFormRef = ref()  // 创建引用

<el-form ref="empFormRef">  // 绑定引用
```



### 通过 ref 操作子组件

javascript

```
empFormRef.value.validate((valid) => {
  // 调用子组件方法
})
```



## 11. 本地存储操作

javascript

```
const getToken = async () => { 
  const loginToken = JSON.parse(localStorage.getItem('loginUser'))
  if (loginToken && loginToken.token) { 
    token.value = loginToken.token
  }
}
```



**localStorage 操作**：

- `getItem(key)` - 获取存储数据
- `setItem(key, value)` - 设置存储数据
- `JSON.parse()` - 解析JSON字符串
- `JSON.stringify()` - 转换为JSON字符串

## 12. 弹窗与用户交互

### 确认对话框

javascript

```
const deleteID = async (id) => { 
  ElMessageBox.confirm(
    '您确认删除该部门吗?',
    '提示',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    // 用户确认
    const result = await deleteApi(id)
    if (result.code) {
      ElMessage.success("删除成功")
      search()
    }
  }).catch(() => {
    // 用户取消
    ElMessage.info('您已经取消删除')
  })
}
```



## 关键 JavaScript 知识点总结

1. **ES6+ 语法**：箭头函数、解构赋值、模板字符串
2. **模块化**：import/export 模块导入导出
3. **Promise 和异步编程**：async/await 错误处理
4. **数组方法**：map、forEach、splice、push
5. **对象操作**：属性访问、方法调用
6. **条件判断**：if/else、三元运算符
7. **函数作用域**：闭包、this 指向
8. **事件循环**：宏任务、微任务执行顺序

这个组件展示了现代前端开发的典型模式：响应式数据绑定、组件化开发、异步数据流、表单处理等核心概念。


## 相关条目
- [[Day01]]
- [[Layui表格和表单]]
- [[javaweb]]
