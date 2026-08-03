## Judge0的部署

按照官网上的来

[judge0/CHANGELOG.md at master · judge0/judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md#deployment-procedure)

```
Download and extract the release archive:
下载并解压发布存档：
wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
unzip judge0-v1.13.1.zip
Visit this website to generate a random password.
请访问此网站以生成随机密码。
Use the generated password to update the variable REDIS_PASSWORD in the judge0.conf file.
使用生成的密码更新<；b1></b1>；文件中的变量<；b0></b0>；。
Visit again this website to generate another random password.
再次访问此网站以生成另一个随机密码。
Use the generated password to update the variable POSTGRES_PASSWORD in the judge0.conf file.
使用生成的密码更新<；b1></b1>；文件中的变量<；b0></b0>；。
Run all services and wait a few seconds until everything is initialized:
运行所有服务并等待几秒钟，直到所有服务都初始化：
cd judge0-v1.13.1
docker-compose up -d db redis
sleep 10s
docker-compose up -d
sleep 5s
Your instance of Judge0 CE v1.13.1 is now up and running; visit docs at http://<IP ADDRESS OF YOUR SERVER>:2358/docs.
您的Judge0 CE v1.13.1实例现在已经启动并运行；访问文档：<；b0></b0>；
```

这里主要讲一下我遇到的问题

按照官网配置好进行数据的测试

发送请求获取token

```
curl -X POST http://localhost:2358/submissions \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "print(\"Hello, Judge0!\")",
    "language_id": 71
  }'
```

根据token查询结果

```
curl -X GET http://localhost:2358/submissions/你的token
```

但是结果却是这样的：显示无法找到文件

```
{"stdout":null,"time":null,"memory":null,"stderr":null,"token":"920c64d5-352a-4ab9-8fff-5d5bc74b0531","compile_output":null,"message":"No such file or directory @ rb_sysopen - /box/script.py","status":{"id":13,"description":"Internal Error"}}
```

造成这个错误的根本原因就是 **cgroup 版本不兼容**。

Judge0 底层依赖的 `isolate` 沙盒环境，是为传统的 cgroup v1 设计的，而现代 Linux 系统（如 Ubuntu 21.10+、RHEL 9+、Amazon Linux 2023 等）默认启用的是 cgroup v2 。这两者的核心差异导致 Judge0 无法正常工作。

我们可以检查一下cgroup版本

```
# 查看当前cgroup版本
mount | grep cgroup
stat -fc %T /sys/fs/cgroup/

# 如果看到"cgroup2fs"，说明是cgroups v2，需要切换到v1
```

切换cgroups v1

```
# 编辑GRUB配置
sudo nano /etc/default/grub

# 找到 GRUB_CMDLINE_LINUX 行，修改为：
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"

# 更新GRUB
sudo update-grub

# 重启系统
sudo reboot
```

验证

```
# 确认cgroup版本
mount | grep cgroup
# 应该看到多个cgroup v1挂载，没有cgroup2
```

这时再重新启动容器进行测试，就可以正确获取到测试结果了

## 相关条目
- [[1-概述：开源在线代码执行系统]]
- [[2-快速启动：Docker Compose 部署指南]]
- [[5-系统架构设计]]
- [[Linux操作系统]]
