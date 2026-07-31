# CFGPU CLI - 骋风算力命令行工具

## 为什么要做这个工具

骋风算力（cfgpu.com）是一个 GPU 算力租赁平台，但它的网页端存在以下问题：

1. **功能藏得深**：镜像市场、模型聚合平台、视频/图像/语音模型等功能入口不明显，需要多次点击才能找到
2. **操作链路长**：查看价格需要切换 Tab → 找 GPU 型号 → 看配置 → 记价格，对比不同型号要反复切换
3. **信息分散**：余额、实例、镜像、存储、API Token 散落在控制台的不同页面，每次都要逐个打开
4. **无法批量操作**：管理 API Token（创建/启用/禁用/删除）只能在网页上逐个点击，没有批量能力
5. **不利于脚本化**：想写自动化脚本调用平台 API，但文档藏在前端代码里，需要自己逆向

### 目标用户的工作习惯

AIGC 技术人员（算法工程师、AI 研究员、GPU 算力用户）的工作特点是：

- **习惯终端环境**：日常在命令行中操作，输入命令 → 立即得到结果，而不是在网页上层层点击
- **追求效率**：选 GPU、查价格、看配置是高频操作，需要快速得到结构化信息，而不是在 UI 中反复切换
- **需要脚本化能力**：想用 Python/Shell 脚本批量处理数据、自动化管理资源，但网页无法提供 API 入口
- **反感"游戏化"交互**：如果找功能的过程像玩游戏（点菜单 → 找子菜单 → 再点 → 再找），会觉得很烦，因为这是用来干活的工具，不是娱乐产品

这个 CLI 工具把上面所有问题一次性解决：**一个命令替代十次点击**，让 AIGC 人员用他们最熟悉的方式高效工作。

## 它能做什么

### 一、资源发现与选型决策

| 能力 | 解决了什么问题 | 对应命令 |
|------|--------------|---------|
| 列出全部 GPU 资源 | 网页上三种资源类型（容器/虚拟机/裸金属）分三个 Tab，要逐个切换才能看全 | `list` |
| GPU 型号横向对比 | 同一 GPU 在不同资源类型下价格不同，网页无法并排对比 | `compare` |
| 价格速查表 | 网页上价格信息分散在配置详情里，需要点开才能看到 | `price` |
| 全局关键词搜索 | 网页搜索只能搜 GPU 资源，搜不到镜像和模型 | `search` |

### 二、AI 模型平台速查

| 能力 | 解决了什么问题 | 对应命令 |
|------|--------------|---------|
| 镜像市场 AI 模型列表 | 37 个 AI 模型镜像混在一起，按分类筛选需要手动找 | `images` |
| 大语言模型广场 | 35+ 大模型，网页上需要滚动 + 筛选才能找到目标模型 | `llm` |
| 视频生成模型列表 | 22 个视频模型（Kling/万相/HappyHorse/字节跳动），网页上信息分散 | `video-models` |
| 图像生成模型列表 | 9 个生图模型的价格和能力标签一目了然 | `image-models` |
| 语音合成模型列表 | 3 个 TTS 模型的价格对比 | `voice-models` |

### 三、个人空间一站式管理

| 能力 | 解决了什么问题 | 对应命令 |
|------|--------------|---------|
| 余额与存储概览 | 余额、代金券、实例数、镜像容量、文件存储分散在 4 个页面 | `dashboard` |
| 实例列表与连接信息 | 9 个实例的 SSH 命令、Jupyter 链接、GPU/CPU 配置一次全看到 | `instance` |
| 个人私有镜像管理 | 9 个镜像的大小、区域、来源、分享状态集中展示 | `my-images` |
| 文件存储用量查看 | 各区域存储容量、已用空间、日费用一目了然 | `file-storage` |
| API Token 全生命周期管理 | 创建/编辑/启用/禁用/删除 Token，不用打开网页逐个操作 | `api-token` |
| 开放 API 端点文档 | API 文档藏在前端 JS 里，逆向出来整理成可读文档 | `open-api` |

### 四、开发与集成

| 能力 | 解决了什么问题 | 对应命令 |
|------|--------------|---------|
| 全量数据导出 JSON | 想用脚本处理平台数据，但网页无法批量导出 | `export` |
| 导航菜单与平台信息 | 快速了解平台有哪些功能入口 | `menu` |

## 快速开始

```bash
# 查看所有命令
python3 -m cfgpu_cli

# 查看 GPU 价格速查表
python3 -m cfgpu_cli price

# 搜索资源
python3 -m cfgpu_cli search "4090"

# 查看个人空间概览（需要登录）
python3 -m cfgpu_cli dashboard
```

## 命令总览

### 公共资源（无需登录）

| 命令 | 功能 | 示例 |
|------|------|------|
| `list <type>` | 列出资源 | `list container` |
| `compare` | GPU 型号对比 | `compare` |
| `price` | 价格速查表 | `price` |
| `search <关键词>` | 全局搜索 | `search "deepseek"` |
| `all` | 列出所有资源 | `all` |
| `export [file]` | 导出为 JSON | `export data.json` |
| `menu` | 导航菜单 | `menu` |

### 模型平台（本地数据）

| 命令 | 功能 | 示例 |
|------|------|------|
| `images [分类]` | 镜像市场 AI 模型 | `images 大语言模型` |
| `llm [提供商]` | 大语言模型 | `llm 深度求索` |
| `video-models [提供商]` | 视频生成模型 | `video-models Kling` |
| `image-models [提供商]` | 图像生成模型 | `image-models 字节跳动` |
| `voice-models [提供商]` | 语音合成模型 | `voice-models MiniMax` |

### 个人空间（需要登录）

| 命令 | 功能 | 示例 |
|------|------|------|
| `dashboard` | 个人空间概览 | `dashboard` |
| `instance [状态]` | 实例列表 | `instance RUNNING` |
| `my-images` | 个人私有镜像 | `my-images` |
| `file-storage` | 文件存储信息 | `file-storage` |
| `api-token [操作]` | API Token 管理 | `api-token list` |
| `open-api` | 开放 API 文档 | `open-api` |

## 项目结构

```
cfgpu-cli/
├── README.md                          # 本文档
├── analysis/                          # 分析过程产物
│   ├── website-analysis.md            # 网站逆向分析报告
│   └── resources.json                 # 原始 API 响应数据
├── cfgpu_cli/
│   ├── __main__.py                    # CLI 入口，命令路由
│   ├── api.py                         # API 客户端（核心）
│   ├── .cookies                       # 登录凭证（已脱敏，勿提交）
│   ├── commands/                      # 命令模块（每个命令一个文件）
│   │   ├── resources.py               # list 命令
│   │   ├── compare.py                 # compare 命令
│   │   ├── price.py                   # price 命令
│   │   ├── search.py                  # search 命令
│   │   ├── export.py                  # export 命令
│   │   ├── menu.py                    # menu 命令
│   │   ├── images.py                  # images 命令
│   │   ├── llm.py                     # llm 命令
│   │   ├── video_models.py            # video-models 命令
│   │   ├── image_models.py            # image-models 命令
│   │   ├── voice_models.py            # voice-models 命令
│   │   ├── dashboard.py               # dashboard 命令
│   │   ├── instance.py                # instance 命令
│   │   ├── console_image.py           # my-images 命令
│   │   ├── file_storage.py            # file-storage 命令
│   │   ├── api_token.py               # api-token 命令
│   │   └── open_api.py                # open-api 命令
│   └── data/                          # 本地数据文件
│       ├── images.json                # 镜像市场数据
│       ├── llm_models.json            # 大语言模型数据
│       ├── video_models.json          # 视频模型数据
│       ├── image_models.json          # 图像模型数据
│       └── voice_models.json          # 语音模型数据
```

## 架构设计

### 三层架构

```
┌─────────────────────────────────────────────┐
│  __main__.py  (命令路由层)                    │
│  解析命令行参数，分发到对应命令模块             │
├─────────────────────────────────────────────┤
│  commands/*.py  (命令逻辑层)                  │
│  每个文件一个命令，负责数据格式化和终端输出     │
─────────────────────────────────────────────┤
│  api.py  (API 客户端层)                       │
│  封装所有 HTTP 请求，统一错误处理              │
└─────────────────────────────────────────────┘
```

### 数据获取策略

项目采用两种数据获取方式，根据 API 是否需要登录区分：

**方式一：直接 API 调用（无需登录）**

公共资源（GPU 列表、价格、菜单等）的 API 不需要认证，直接通过 `urllib` 发送 POST 请求即可获取。

```python
# api.py 中的核心请求函数
def _request(path: str, payload: dict = None, auth: bool = False) -> dict:
    """发送 POST 请求到 CFGPU API"""
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload or {}).encode("utf-8")
    headers = {"Content-Type": "application/json", ...}
    if auth:
        headers["Cookie"] = _load_cookies()
    # ... 发送请求，解析响应
```

**方式二：Cookie 认证（需要登录）**

个人空间相关 API 需要登录态。通过浏览器登录后提取 cookie 字符串，保存到 `.cookies` 文件，后续请求自动携带。

```bash
# 首次使用需要登录
# 1. 在浏览器中登录 cfgpu.com
# 2. 在浏览器控制台执行: document.cookie
# 3. 将结果保存到 cfgpu_cli/.cookies 文件
```

**方式三：本地 JSON 数据（无法通过 API 获取）**

部分数据（如 LLM 模型广场、视频/图像/语音模型列表）的 API 需要特殊权限或前端渲染后才有数据。通过浏览器 agent 提取页面内容后，整理为本地 JSON 文件。

### 命令模块规范

每个命令文件遵循统一结构：

```python
"""命令描述"""

from cfgpu_cli.api import CfgpuApiError, _request

def run(param1: str = None, param2: int = 1):
    """命令入口函数

    Args:
        param1: 参数说明
        param2: 参数说明
    """
    # 1. 调用 API 获取数据
    # 2. 格式化输出到终端
    # 3. 打印统计信息
```

## 已发现的 API 端点

### 公开 API（无需认证）

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/main/header/menu.json` | POST | 导航菜单 |
| `/api/main/header/platform.json` | POST | 平台信息 |
| `/api/main/header/isLogin.json` | POST | 登录状态检查 |
| `/api/cpi/container/list.json` | POST | 云容器列表 |
| `/api/cpi/vm/list.json` | POST | 虚拟机列表 |
| `/api/cpi/bare_metal/list.json` | POST | 裸金属列表 |
| `/api/openModel/page.json` | POST | 模型聚合平台列表 |
| `/api/openModel/modelTypeSelect.json` | POST | 模型类型筛选 |
| `/api/openModel/manufacturerSelect.json` | POST | 制造商筛选 |
| `/api/openModel/tagSelect.json` | POST | 标签筛选 |

### 认证 API（需要 Cookie）

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/authToken/list.json` | POST | API Token 列表 |
| `/api/authToken/create.json` | POST | 创建 API Token |
| `/api/authToken/update.json` | POST | 编辑 Token 备注 |
| `/api/authToken/enable.json` | POST | 启用 Token |
| `/api/authToken/disable.json` | POST | 禁用 Token |
| `/api/authToken/delete.json` | POST | 删除 Token |
| `/api/recharge/balanceQuery.json` | POST | 余额查询 |
| `/api/instance/page.json` | POST | 实例列表（分页） |
| `/api/instance/expiredConfig.json` | POST | 到期配置 |
| `/api/image/overview.json` | POST | 镜像存储概览 |
| `/api/image/page.json` | POST | 个人镜像列表 |
| `/api/filesystem/list.json` | POST | 文件存储列表 |
| `/api/team/info.json` | POST | 团队/空间信息 |
| `/api/team/selectAll.json` | POST | 团队列表 |

### 开放 API（使用 API Token 认证）

| 端点 | 方法 | 功能 |
|------|------|------|
| `/userapi/v1/region/list` | POST | 可用区域列表 |
| `/userapi/v1/gpu/list` | POST | GPU 型号列表 |
| `/userapi/v1/image/privateList` | POST | 私有镜像列表 |
| `/userapi/v1/instance/status` | POST | 实例状态 |
| `/userapi/v1/instance/page` | POST | 实例列表 |

## 如何演化为可复用的 CLI Skill

本项目的核心方法论可以复用到任何 Web 应用的 CLI 化工具开发中。以下是通用流程：

### 第一步：网站逆向分析

1. **识别技术栈**：通过浏览器开发者工具确认前端框架（React/Vue/SPA 等）
2. **抓取网络请求**：在浏览器中操作页面，记录所有 XHR/Fetch 请求
3. **分析 API 结构**：整理端点路径、请求方法、参数格式、响应结构
4. **区分认证级别**：标记哪些 API 需要登录、哪些公开

产出文件：`analysis/website-analysis.md`

### 第二步：构建 API 客户端

1. 用 Python 标准库（`urllib`）实现 HTTP 请求封装
2. 统一响应解析和错误处理
3. 实现 Cookie 管理（登录态持久化）
4. 为每个 API 端点创建对应的函数

关键文件：`api.py`

### 第三步：实现命令模块

1. 每个命令一个独立文件，放在 `commands/` 目录
2. 统一入口函数签名：`def run(*args)`
3. 命令内部调用 API 客户端获取数据
4. 格式化输出到终端（表格、列表、树形结构）

### 第四步：处理无法 API 化的数据

对于需要前端渲染或特殊权限才能获取的数据：

1. 使用浏览器自动化工具（如 browser-use agent）提取页面内容
2. 整理为本地 JSON 数据文件
3. 命令模块从本地文件加载数据

### 第五步：命令行路由

在 `__main__.py` 中实现命令分发：

```python
def main():
    command = sys.argv[1]
    if command == "xxx":
        from cfgpu_cli.commands.xxx import run
        run(*sys.argv[2:])
```

### 复用到其他网站

将上述流程应用到任何 Web 应用时，只需：

1. 替换 `BASE_URL` 为目标网站域名
2. 重新执行第一步的逆向分析
3. 更新 `api.py` 中的端点函数
4. 添加对应的命令模块

核心架构（三层架构 + Cookie 认证 + 本地数据兜底）保持不变。

## 注意事项

- `.cookies` 文件包含登录凭证，已加入 `.gitignore`，切勿提交到版本库
- Cookie 有时效性，过期后需要重新登录并更新 `.cookies` 文件
- 本地 JSON 数据文件（`data/*.json`）需要定期从网站同步更新
- 所有 API 均为 POST 请求，即使只是获取数据
