# TDL - 测试描述语言
> Tests Description Language or Tests Design Language。

TDL旨在提供通用的测试套件、测试用例、测试步骤及测试报告等描述方法及固定格式。
已实现跨编程语言的测试统一，以及清晰可自动化的测试描述。

TDL是另一款关键字驱动测试框架，或者类似BDD的测试框架。
不同于Robot Framework测试框架，及Cucumber采用的Gerkin等领域专用语言格式，
TDL基于广泛使用的JSON格式并推荐使用YAML文件格式来描述测试用例或测试套件。
一方面是方便解析及二次开发，另一方面也旨在兼容基于文件系统的测试框架及基于数据库的测试平台的需求，方便二者的融合。

TDL除提供基础的协议（格式规范）之外，还致力于提供完整的集成测试及系统测试自动化解决方案。
包括接口测试、WebUI测试、AppUI测试、性能测试等测试框架及测试平台，以及不同编程语言的生态组件。


```yaml
name: 接口测试套件示例
config:     # 临时环境配置
  Http: {base_url: http://postman-echo.com}  # Http库配置
setups:     # 测试准备步骤
  - Http.post /post data={"username":"kevin","password":"123456"}

tests:      
  - name: 测试Get接口
    steps:  # 测试步骤
      - Http.get /get params={"a":"1","b":"2"}
      - Assert.contains $step1.url /get
      - Assert.str_eq $step1.status_code 200
```
