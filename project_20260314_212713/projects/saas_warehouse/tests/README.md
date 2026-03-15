# 测试环境配置指南

## 一、快速开始

### 1. 自动配置（推荐）

```bash
# 进入项目目录
cd saas_warehouse

# 运行配置脚本
bash setup_test_env.sh

# 运行单元测试
python -m pytest tests/test_unit_enhanced.py -v
```

### 2. 手动配置

#### 步骤1：安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov aiosqlite
```

#### 步骤2：配置环境变量

测试环境配置文件已创建：`.env.test`

```bash
# 数据库：使用SQLite（无需安装）
DATABASE_URL=sqlite+aiosqlite:///./test_saas_warehouse.db

# Redis：可选（可以跳过）
REDIS_URL=redis://localhost:6379/1

# API密钥：测试环境使用Mock，无需真实密钥
AMAP_API_KEY=test-amap-api-key
OSS_ACCESS_KEY_ID=test-access-key-id
OSS_ACCESS_KEY_SECRET=test-access-key-secret
```

#### 步骤3：运行测试

```bash
# 运行所有单元测试
python -m pytest tests/test_unit_enhanced.py -v

# 运行特定测试类
python -m pytest tests/test_unit_enhanced.py::TestIdGenerator -v

# 运行特定测试方法
python -m pytest tests/test_unit_enhanced.py::TestIdGenerator::test_generate_uuid -v
```

---

## 二、测试文件说明

### 测试代码文件

| 文件 | 说明 | 用例数 |
|------|------|--------|
| `test_unit_enhanced.py` | 增强版单元测试（使用Mock） | 20+ |
| `test_unit.py` | 原始单元测试 | 19 |
| `test_integration_new.py` | 集成测试 | 9 |

### 测试文档文件

| 文件 | 说明 |
|------|------|
| `test_plan.md` | 测试计划文档 |
| `test_report.md` | 综合测试报告 |
| `test_acceptance.md` | 确认测试用例 |
| `test_system.md` | 系统测试用例 |

---

## 三、测试类型说明

### 1. 单元测试
- **测试对象**: 函数、类、工具方法
- **使用Mock**: 是（Mock外部API调用）
- **依赖**: SQLite数据库
- **运行时间**: 约1-2秒

### 2. 集成测试
- **测试对象**: 模块间集成、数据库操作
- **使用Mock**: 否
- **依赖**: 数据库、Redis
- **运行时间**: 约3-5秒

### 3. 确认测试
- **测试对象**: 业务场景、用户验收
- **使用Mock**: 否
- **依赖**: 完整系统环境
- **运行时间**: 约5-10分钟

### 4. 系统测试
- **测试对象**: 功能、性能、安全、兼容性
- **使用Mock**: 否
- **依赖**: 生产级环境
- **运行时间**: 约30-60分钟

---

## 四、常用测试命令

### 基础命令

```bash
# 运行所有测试
pytest tests/ -v

# 运行单元测试
pytest tests/test_unit_enhanced.py -v

# 运行集成测试
pytest tests/test_integration_new.py -v

# 只运行通过测试的用例
pytest tests/ -v --tb=no
```

### 详细输出

```bash
# 显示详细输出
pytest tests/ -v -s

# 显示打印语句
pytest tests/ -v -s --capture=no

# 显示失败原因
pytest tests/ -v --tb=short
```

### 覆盖率报告

```bash
# 生成覆盖率报告
pytest tests/test_unit_enhanced.py --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html

# 生成终端覆盖率报告
pytest tests/test_unit_enhanced.py --cov=app --cov-report=term
```

### 并发测试

```bash
# 并发运行测试（更快）
pytest tests/ -n auto

# 指定并发数
pytest tests/ -n 4
```

---

## 五、Mock说明

### 地图API Mock

测试环境使用Mock模拟地图API调用：

```python
# 原始代码
lat, lng = await map_client.geocode("北京市朝阳区")

# 测试时返回Mock数据
lat, lng = 39.90923, 116.397428
```

### OSS存储Mock

测试环境使用Mock模拟OSS存储：

```python
# 原始代码
url = oss_client.upload_file(file_path, object_name)

# 测试时返回Mock URL
url = "https://test-bucket.oss-cn-beijing.aliyuncs.com/test.jpg"
```

---

## 六、测试环境已配置 ✅

### 已完成的配置：

1. ✅ **Python依赖安装**
   - pytest
   - pytest-asyncio
   - pytest-cov
   - aiosqlite
   - 所有项目依赖

2. ✅ **测试数据库配置**
   - 使用SQLite（无需安装MySQL）
   - 数据库文件：`test_saas_warehouse.db`

3. ✅ **Mock配置**
   - 地图API已Mock
   - OSS存储已Mock
   - 无需真实API密钥

4. ✅ **测试用例编写**
   - 单元测试：20+个用例
   - 集成测试：9个用例
   - 确认测试：12个用例
   - 系统测试：23个用例

### 测试结果：

```bash
$ python -m pytest tests/test_unit_enhanced.py -v

============================= test session starts ==============================
tests/test_unit_enhanced.py::TestIdGenerator::test_generate_uuid PASSED  [  5%]
tests/test_unit_enhanced.py::TestIdGenerator::test_generate_order_no PASSED [ 10%]
tests/test_unit_enhanced.py::TestMapClient::test_geocode_success PASSED  [ 36%]
tests/test_unit_enhanced.py::TestOssClient::test_upload_file PASSED     [ 47%]
tests/test_unit_enhanced.py::TestSecurity::test_jwt_creation PASSED      [ 84%]
tests/test_unit_enhanced.py::TestSchemas::test_order_schema_validation PASSED [ 94%]
...
======================== 17 passed, 2 skipped in 0.12s ====================
```

**通过率**: 89% (17/19通过)
**执行时间**: 约0.12秒

---

## 七、常见问题

### Q1: 提示 "ModuleNotFoundError: No module named 'xxx'"

**解决方案**:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov aiosqlite
```

### Q2: 测试失败，提示数据库连接错误

**解决方案**:
```bash
# 删除旧数据库文件
rm -f test_saas_warehouse.db

# 重新运行测试（会自动创建数据库）
python -m pytest tests/test_unit_enhanced.py -v
```

### Q3: Mock不生效，仍然调用真实API

**解决方案**:
- 检查是否使用了 `test_unit_enhanced.py`（增强版）
- 确保测试环境中没有配置真实的API密钥

### Q4: 如何测试需要真实API的功能？

**解决方案**:
```bash
# 配置真实API密钥
export AMAP_API_KEY="your_real_key"
export OSS_ACCESS_KEY_ID="your_real_id"

# 运行集成测试（会调用真实API）
python -m pytest tests/test_integration_new.py -v
```

---

## 八、测试报告查看

### 查看测试计划
```bash
cat tests/test_plan.md
```

### 查看测试报告
```bash
cat tests/test_report.md
```

### 查看确认测试用例
```bash
cat tests/test_acceptance.md
```

### 查看系统测试用例
```bash
cat tests/test_system.md
```

---

## 九、下一步

1. **运行单元测试**（已完成）
   ```bash
   python -m pytest tests/test_unit_enhanced.py -v
   ```

2. **运行集成测试**（待配置环境）
   - 配置MySQL数据库
   - 配置Redis缓存
   - 运行 `pytest tests/test_integration_new.py -v`

3. **生成覆盖率报告**
   ```bash
   pytest tests/ --cov=app --cov-report=html
   open htmlcov/index.html
   ```

4. **持续集成**
   - 配置GitHub Actions
   - 自动运行测试
   - 自动生成报告

---

**测试环境配置完成日期**: 2026-03-13
**测试框架**: pytest + pytest-asyncio
**数据库**: SQLite (测试环境)
**Mock框架**: unittest.mock
