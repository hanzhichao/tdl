# TDL
Tests Description Language 
测试描述语言， 用于描述测试用例，测试步骤等

## 目标特性
- [ ] 支持接口测试、WebUI测试、AppUI测试
- [ ] 支持BDD、数据驱动、关键字驱动
- [ ] 自带Dashboard
- [ ] 支持Python、Go、Java、JavaScript
- [ ] 支持单元测试
- [ ] 支持性能测试
- [ ] 支持执行Shell、SQL
- [ ] 支持二次开发
- [ ] 结构清晰、灵活
- [ ] 支持定时任务
- [ ] 支持Form表单、支持RPA
- [ ] 支持Stage
- [ ] 支持多环境切换

## Schema 0.1

一个脚本一个Suite/Module/Epic
- 引用: 
  - 变量引用: $var或${var}
  - 函数引用: $func()或${func()}
  - 计算: ${var+1}、${func()+1}
- 文件导入
  - 绝对路径: /tmp/tmp.log
  - 项目路径: @/utils/utils.py
  - 相对路径: ./db.py

  

```yaml
# 配置<dict>
config: 
  base_url: 

# 用例<list>
tests:  
  - name: 用例描述
    tags: 用例标签 <list>
    skip: true
    xfail: true
```


## 模型设计
- TestCase
- Step
- Data
- TestSuite
- TestReport

```json
{
  "name": "testsuite_01",
  "description": "testsuite description",
  "filter": {
    "tags": [],
    "priorities": [],
    "status": [],
    "owner": []
  },
  "tags": [],
  "priority": 0,
  "setup": [],
  "teardown": [],
  "setup_suite": [],
  "teardown_suite": [],
  "tests": [
    {"id": "testsuite_01", "name": "testcase_01"},
    {"id": "testsuite_02", "name": "testcase_02"},
    {"id": "testsuite_03", "name": "testcase_03"}
  ]
}


```


### 测试用例
TestCase
- feature
- title/ scenario / summary
- description: Optional[str]
- tags
- priority
- status: 实现中/Ready 当前状态
- timeout: 可继承运行参数
- owner
- ddt：可继承运行参数
- setup
- teardown
- skip: 跳过条件
- xfail：预期失败
- rerun / retry/ repeat /times: 失败重试/无条件重试(repeat) 可继承运行参数
- 上次运行状态/时间 总体状态 / 平均执行时间
- state: 关联阶段 Prod/Test/Stage
- type: 用例类型 接口/性能/WebUI/AppUI
- related_requirement：关联需求
- order执行顺序

## 用例
```json
{
  "name": "test_api_demo",
  "description": "test description",
  "priority": 1,
  "tags": ["http", "api-test"],
  "timeout": 100,
  "setup": [
    {"method": "Http.Get", "args": {"url": "/get","params":  {"a": 1, "b": 2, "c": 3}}}
  ],
  "teardown": [
     {"method": "Http.Get", "args": {"url": "/get","params":  {"a": 1, "b": 2, "c": 3}}}
  ],
  "steps": [
    {"method": "Http.Get", "args": {"url": "/get","params":  {"a": 1, "b": 2, "c": 3}}},
    {"method": "Http.Post", "args": {"url": "/post", "json":  {"name": "Kevin"}}},
    {"method": "Http.Get", "args": {"url": "/get", "params":  {"a": 1, "b": 2, "c": 3}}, 
      "store": {"url": "$.url"}, "excepted": {"eq": ["$url", "/get"]}}
  ]
}

```
```json
{
  "name": "test_web_ui_demo",
  "description": "test description",
  "steps": [
    {"method": "Page.Open", "args": ["https://www.baidu.com/"]},
    {"method": "Page.InputTo", "args": ["id","kw", "helloworld"], "register": {"value1": "//[@id=\"kw\"]/@value"}},
    {"method": "Page.Click", "args": ["id","su"]}
  ]
}

```

```json
{
  "name": "test_ssh_demo",
  "description": "test description",
  "steps": [
    {"method": "SSH.Execute", "args": "echo hello"},
    {"method": "SSH.GET", "args": ["/path/a.txt", "/local_path/a.txt"]}
  ]
}

```
```json
{
  "name": "test_mysql_demo",
  "description": "test description",
  "steps": [
    {"method": "MySQL.Query", "args": "SELECT * FROM `users`"},
    {"method": "MySQL.Execute", "args": "INSERT INTO `users` (\"name\") VALUES(\"KEVIN\")"}
  ]
}

```

## TestReport
```json
{
  "name": "test_report",
  "summary": {
    "start_at": "2015-02-03 12:00:00.000",
    "end_at": "2015-02-03 12:01:00.00",
    "total": 12
  },
  "details": [
    {}
  ]
  
}
```



RF TestCase
[Documentation]	Used for specifying a test case documentation.
[Tags]	Used for tagging test cases.
[Setup]	Used for specifying a test setup.
[Teardown]	Used for specifying a test teardown.
[Template]	Used for specifying a template keyword.
[Timeout]

## 测试步骤
TestStep
- 所属用例
- 顺序 order
- 执行动作
- wait_for: 等待某一条件达到再开始执行
- skip: 跳过条件
- ignore_error: 忽略异常
- except_error: 期望异常
- on_error: continue / warn / raise
- on_fail: continue / warn / fail
- rurun / retry/ repeat / times / loop_util: 失败/永远 执行次数 /直到
- timeout: 超时时间
- validate/ verify / check /assert
- extract/ register / log  打印其中信息

并行和串行
steps
  - step1
  - step2 # 串行
  - [step3, step4]  # 并行

- [ ] 支持基本的关联及断言
- [ ] 支持

## 问题
- 一个文件 一个**特性**？一个套件？一个用例？


## 参考
- [runnerz](https://github.com/hanzhichao/runnerz)
- [robotframework](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- [djaong-zendao](https://github.com/hanzhichao/django_zendao/blob/main/apps/mtest/models.py)
- [qtaf](https://qta-testbase.readthedocs.io/zh/latest/testcheck.html#id4)
