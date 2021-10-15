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




