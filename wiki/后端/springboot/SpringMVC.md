# SpringMVC
## 配置

基本配置文件：扫描组件，视图解析器，view-controller，default-servlet-handler，MVC注解驱

动，文件上传解析器，异常处理，拦截器 web.xml

```
<?xml version="1.0" encoding="UTF-8"?>  
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"  
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"  
         version="4.0">  
<!--    // 解决乱码-->  
    <filter>  
        <filter-name>CharacterEncodingFilter</filter-name>  
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>  
        <init-param>            <param-name>encoding</param-name>  
            <param-value>UTF-8</param-value>  
        </init-param>        <init-param>            <param-name>forceResponseEncoding</param-name>  
            <param-value>true</param-value>  
        </init-param>    </filter>    <!--    配置HiddenHttpMethodFilter-->  
    <filter>  
        <filter-name>HiddenHttpMethodFilter</filter-name>  
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>  
    </filter>    <filter-mapping>        <filter-name>HiddenHttpMethodFilter</filter-name>  
        <url-pattern> /*</url-pattern>  
    </filter-mapping>    <filter-mapping>        <filter-name>CharacterEncodingFilter</filter-name>  
        <url-pattern> /*</url-pattern>  
    </filter-mapping><!--    配置springmvc的前端控制器，对浏览器发送的请求进行统一处理-->  
    <servlet>  
        <servlet-name>SpringMVC</servlet-name>  
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>  
<!--        初始化参数-->  
        <init-param>  
            <param-name>contextConfigLocation</param-name>  
            <param-value>classpath:SpringMVC.xml</param-value>  
        </init-param><!--        将前端控制器的初始化时间提前的=到服务器启动时-->  
        <load-on-startup>1</load-on-startup>  
    </servlet>    <servlet-mapping>        <servlet-name>SpringMVC</servlet-name>  
        <url-pattern>/</url-pattern>  
    </servlet-mapping></web-app>
```

bean.xml

```
<?xml version="1.0" encoding="UTF-8"?>  
<beans xmlns="http://www.springframework.org/schema/beans"  
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
       xmlns:context="http://www.springframework.org/schema/context"  
       xmlns:mvc="http://www.springframework.org/schema/mvc"  
       xsi:schemaLocation="http://www.springframework.org/schema/beans  
                           http://www.springframework.org/schema/beans/spring-beans.xsd                           http://www.springframework.org/schema/context                           http://www.springframework.org/schema/context/spring-context.xsd                           http://www.springframework.org/schema/mvc                           http://www.springframework.org/schema/mvc/spring-mvc.xsd">  
  
  
    <!-- 组件扫描 -->  
    <context:component-scan base-package="com.wsj.mvc.cotroller"/>  
  
<!--    开放对静态资源的访问-->  
    <mvc:default-servlet-handler />  
    <!-- 注解驱动 -->  
    <mvc:annotation-driven/>  
  
  
  
  
  
  
    <!-- 视图解析器 - Thymeleaf -->    <bean id="templateResolver" class="org.thymeleaf.spring6.templateresolver.SpringResourceTemplateResolver">  
<!--        模板路径-->  
        <property name="prefix" value="/WEB-INF/templates/"/>  
        <property name="suffix" value=".html"/>  
        <property name="templateMode" value="HTML"/>  
        <property name="characterEncoding" value="UTF-8"/>  
        <property name="cacheable" value="false"/>  
    </bean>  
    <bean id="templateEngine" class="org.thymeleaf.spring6.SpringTemplateEngine">  
        <property name="templateResolver" ref="templateResolver"/>  
        <property name="enableSpringELCompiler" value="true"/>  
    </bean>  
    <bean class="org.thymeleaf.spring6.view.ThymeleafViewResolver">  
        <property name="templateEngine" ref="templateEngine"/>  
        <property name="characterEncoding" value="UTF-8"/>  
        <property name="order" value="1"/>  
    </bean>  
    <mvc:view-controller path="/" view-name="index"></mvc:view-controller>  
  
    <!-- 文件上传配置 -->  
    <bean id="multipartResolver" class="org.springframework.web.multipart.support.StandardServletMultipartResolver"/>  
  
    <!-- 拦截器配置（可选） -->  
    <mvc:interceptors>  
        <bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor">  
            <property name="paramName" value="lang"/>  
        </bean>    </mvc:interceptors>  
  
<!--    配置异常处理-->  
    <bean class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">  
        <property name="exceptionMappings">  
            <props>                <prop key="java.lang.ArithmeticException">error</prop>  
            </props>        </property>        <property name="defaultErrorView" value="error"/>  
  
<!--        设置将异常信息共享在请求域中的键-->  
  
        <property name="exceptionAttribute" value="ex"/>  
    </bean>  
  
  
</beans>
```

## 工作流程

浏览器发送请求，请求地址符合url-pattern，请求会被DispatcherServlet处理，前端控制器读取核心配置文件，扫描组件找到控制器，将请求地址和控制器的value属性进行匹配，如果匹配成功，视图名称被视图解析器解析，加上前缀和后缀组成路径，转发到视图对应页面

## @RequestMapping

将请求和处理请求的控制器方法关联起来，建立映射

### @Value属性

![](/attachments/Pasted%20image%2020251120111521.png)

可以在value中写多个请求地址，满足其中一个即可

### @Method属性

指定请求方式

get-->@GetMapping

post-->@PostMapping

put-->@PutMapping

delete-->@DeleteMapping

### params属性

params通过设定参数，使得请求在发送时必须携带指定的参数

```
@RequestMapping(value = "/target",params = "username")  
public String target(){  
    return "target";  
}
```

## 获取请求参数

### 原生Servlet Api

```
@RequestMapping(value = "/target1")  
public String target2(HttpServletRequest request){  
    String username=request.getParameter("username");  
    String password=request.getParameter("password");  
    System.out.println( username+ password);  
    return "target";  
}
```

## 域对象获取数据

**域对象** 指的是那些可以在**特定范围（域）** 内存储和共享数据的对象。你可以把它们想象成一个个具有不同“作用域”的储物箱，你可以在一个地方（比如一个 Servlet）把数据放进这个箱子，然后在另一个地方（比如另一个 Servlet 或 JSP 页面）从同一个箱子里把数据取出来。

在 Java Web 中，主要有四个域对象，按作用域**从小到大**排列：

1.  **PageContext** - 页面域
2.  **HttpServletRequest** - 请求域
3.  **HttpSession** - 会话域
4.  **ServletContext** - 应用域

### 一、request域对象共享数据

ServletAPI/ModelAndView

```
    @RequestMapping("/servletAPI")
    public String servletAPI(HttpServletRequest request){
        request.setAttribute("requestAttribute","helloworld");
        return "servletAPI";
    }

```

```
    /**
     * ModelAndView有model和view的功能
     * @return 返回值为ModelAndView对象，交给前端处理器处理
     */
    @RequestMapping("/testModelAndView")
    public ModelAndView testModelAndView(){
        //new一个ModelAndView对象
        ModelAndView modelAndView = new ModelAndView();
        //向请求域中共享数据
        modelAndView.addObject("requestAttribute","helloworld,modelandview");
        //设置视图名称，由thymeleaf解析
        modelAndView.setViewName("testModelAndView");
        return modelAndView;
    }

```

Model、ModelMap和Map

```
    /**
     *
     * @param model 传入Model对象，以便向request中共享数据
     * @return 返回视图名称
     */
    @RequestMapping("/testModel")
    public String testModel(Model model){
        //向request中共享数据
        model.addAttribute("requestAttribute","helloworld,Model");
        return "testModel";
    }

```

### 二、session域对象共享数据

```
    @RequestMapping("/testSession")
    public String testSession(HttpSession session){
        session.setAttribute("sessionAttribute","helloworld,session");
        return "testSession";
    }
```

### 三、context域对象共享数据

```
    @RequestMapping("/testContext")
    public String testContext(HttpServletRequest request){
        ServletContext application = request.getServletContext();
        application.setAttribute("contextAttribute","helloworld,context");
        return "testContext";
    }
```

## 视图

### ThymeleafView

#### 整体流程与 ThymeleafView 的创建

现在，我们把“转发视图”放到完整的请求处理流程中，来看 `ModelAndView` 和 `ThymeleafView` 是如何协作的：

1.  `**DispatcherServlet**` **接收请求**：它是前端控制器，是所有请求的入口。
2.  **调用控制器方法**：`DispatcherServlet` 找到对应的 `@Controller` 和方法并调用它。
3.  **构建** `**ModelAndView**`：如上所述，无论控制器方法如何声明，最终都会返回一个 `ModelAndView` 实例给 `DispatcherServlet`。这个实例包含了：
    *   `View` 信息（可能是一个视图名 `"hello"`，也可能是一个视图对象）。
    *   `Model` 数据（一个包含键值对的 Map）。
4.  **解析视图名称 -** `**ViewResolver**`：
    *   `DispatcherServlet` 拿到 `ModelAndView` 后，发现里面只是一个视图名 `"hello"`，而不是一个具体的 `View` 对象。
    *   它开始询问所有配置的 `**ViewResolver**`（视图解析器）：“谁能解析这个名叫 `‘hello’` 的视图？”
    *   `**ThymeleafViewResolver**`（Spring 为 Thymeleaf 提供的集成类）会站出来说：“我能！”。它根据前缀（`classpath:/templates/`）和后缀（`.html`）将视图名 `"hello"` 解析为一个具体的 `**ThymeleafView**` 对象。这个对象知道模板文件的实际位置（`/templates/hello.html`）。
5.  **渲染视图 -** `**View.render()**`：
    *   `DispatcherServlet` 现在有了完整的 `ModelAndView`（其中 `View` 部分已经是具体的 `ThymeleafView` 对象）。
    *   它调用 `ThymeleafView.render(model, request, response)` 方法。
    *   **这就是 Thymeleaf 引擎工作的时刻**：
        *   `ThymeleafView` 委托内部的 `TemplateEngine` 去处理。
        *   `TemplateEngine` 通过 `TemplateResolver` 找到模板文件。
        *   引擎将 `Model` 中的数据与模板文件合并，执行所有的 `th:*` 指令，生成最终的 HTML。
        *   将生成的 HTML 写入 `HttpServletResponse` 对象。

## 返回视图底层调用

HTTP Request ↓ DispatcherServlet ↓ HandlerMapping (找到控制器方法) ↓ HandlerAdapter (执行控制器方法) ↓ 控制器方法执行 ↓ 返回值处理 ←--- ModelAndView 封装过程 ↓ ViewResolver (解析视图) ↓ 视图渲染 ↓ HTTP Response

核心：ModelAndView

### HiddenHttpMethodFilter处理put/delete请求核心

```
protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {  
    HttpServletRequest requestToUse = request;  
    if ("POST".equals(request.getMethod()) && request.getAttribute("jakarta.servlet.error.exception") == null) {  
        String paramValue = request.getParameter(this.methodParam);  
        if (StringUtils.hasLength(paramValue)) {  
            String method = paramValue.toUpperCase(Locale.ROOT);  
            if (ALLOWED_METHODS.contains(method)) {  
                requestToUse = new HttpMethodRequestWrapper(request, method);  
            }  
        }  
    }  
  
    filterChain.doFilter(requestToUse, response);  
}
```

拦截器拦截request，如果请求中携带POST方法，进行下一步判断：获取方法请求参数,修改原始方法，模拟delete,put请求，放行

### 转发视图

前缀forward:

一次请求（浏览器），服务器内部发出另一次请求

### 重定向视图

前缀：redirect

两次请求

## HttpMessageConverter

对报文信息进行转换，转换为java格式，再将java格式转换为报文信息

@RequestBody:在形参处进行标识

@ResponseBody:在方法上方进行标识，将返回数据转化为保温信息

### 返回json格式数据

导入相关依赖

```
<!--        json依赖-->  
        <dependency>  
            <groupId>com.fasterxml.jackson.core</groupId>  
            <artifactId>jackson-databind</artifactId>  
            <version>2.19.2</version>  
        </dependency>
```

### ResponseEntity

文件上传解析器

```
<!-- 文件上传配置 -->  
<bean id="multipartResolver" class="org.springframework.web.multipart.support.StandardServletMultipartResolver"/>
```

通过MultipartFile类型的参数接收，建立HttpSession类型的session对象，获取服务器路径

## 拦截器

若配置多个拦截器，prehandle（）执行顺序为在配置文件中的顺序，底层将自定义的拦截器和SpringMVC自带的拦截器按照顺序放在一个数组中，依靠循环输出拦截器中的prehandle()方法， 而对于拦截器后面的两个方法，则是在循环中通过将索引递减的方式进行遍历，所以输出方法的顺序和第一个不同

![](/attachments/Pasted%20image%2020251124173855.png)