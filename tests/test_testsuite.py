from pprint import pprint

import yaml

from tdl import TestSuite


def test_test_suite(env):
    data = {
        "name": "testsuite_01",
        "description": "testsuite description",
        "tags": ["api-test"],
        "priority": 1,
        "tests": [
            {
                "name": "test_api_demo_1",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                    {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
                     "set": {"url": "$.url"}, "verify": [{"eq": ["$url", "/get"]}]}
                ]
            },
            {
                "name": "test_api_demo_2",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                ]
            }
        ]
    }

    testsuite = TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    pprint(result.data)
    assert result.is_success is True


def test_test_suite2(env):
    data = {
        "name": "testsuite_01",
        "description": "testsuite description",
        "tags": ["api-test"],
        "priority": 1,
        "setups": [],
        "teardowns": [],
        "tests": [
            {
                "name": "test_api_demo_1",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                    {"name": "步骤3", "method": "Http.get", "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}},
                     "set": {"url": "$.url"}, "verify": [{"eq": ["$url", "/get"]}]}
                ]
            },
            {
                "name": "test_api_demo_2",
                "description": "test description",
                "steps": [
                    {"name": "步骤1", "method": "Http.get",
                     "args": {"url": "/get", "params": {"a": 1, "b": 2, "c": 3}}},
                    {"name": "步骤2", "method": "Http.post", "args": {"url": "/post", "json": {"name": "Kevin"}}},
                ]
            }
        ]
    }

    testsuite = TestSuite.load(data)
    # print(testsuite.__dict__)
    result = testsuite.run(env)
    print()
    pprint(result.data)


def test_chainmaker_testsuite(env):  # Fixme
    raw = '''name: access_control_of_permissioned_with_cert  
desc: 验证PermissionedWithCert模式默认权限  
owner: debbyszhang  
timeout: 1  
tags: [ ac,cert ]  
priority: High  

variables:  
  ANY_ADMIN:  
    - user: client1  
      endorsers: [ ]  
    - user: admin2  
      endorsers: [ ]  
    - user: light3  
      endorsers: [ ]  
    - user: consensus4  
      endorsers: [ ]  
    - user: common4  
      endorsers: [ ]  

  contract_name: counter  
  byte_code_path: ./testdata/rust-counter-2.0.0.wasm  
  runtime_type: WASMER  

tests:  
  - name: cert_manage_certs_freeze  
    description: 验证CERT_MANAGE-CERTS_FREEZE权限(ANY-ADMIN)  
    data: ${ANY_ADMIN}  
    variables:  
      a: 1  
    steps:  
      - Chainmaker.FreezeContract contract_name=${contract_name}  
  - name: t02_cert_manage_certs_freeze  
    desc: 验证CERT_MANAGE-CERTS_FREEZE权限(ANY-ADMIN)  
    variables:  
    steps:  
      - Chainmaker.FreezeContract contract_name=${contract_name}
    '''
    data = yaml.safe_load(raw)
    testsuite = TestSuite.load(data)
    result = testsuite.run(env)
    pprint(result.data)
    # assert result[0].status == TestCaseStatus.PASSED


def test_get_api_testsuite():
    raw = '''
    name: 接口测试套件示例
    config:     # 临时环境配置
      Http: {base_url: http://postman-echo.com}  # Http库配置
    setups:     # 测试准备步骤
      - Http.post /post data={"username":"kevin","password":"123456"}
    
    tests:      
      - name: 测试Get接口
        steps:  # 测试步骤
          - Http.get /get params={"a":"1","b":"2"}
          - Assert.contains $result.url /get
          - Assert.str_eq $result.status_code 200
    '''
    data = yaml.safe_load(raw)
    testsuite = TestSuite.load(data)
    result = testsuite.run()
    pprint(result.data)


def test_get_api_testsuite_with_prefix_step():
    raw = '''
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
    '''
    data = yaml.safe_load(raw)
    testsuite = TestSuite.load(data)
    result = testsuite.run()
    pprint(result.data)
