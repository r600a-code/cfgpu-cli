# CFGPU 骋风算力 - 网站分析报告

## 一、网站概况

- **名称**: 骋风算力 (CFGPU)
- **网址**: https://www.cfgpu.com/
- **定位**: GPU算力租赁平台，提供云容器、虚拟机、裸金属三种形态的GPU资源
- **技术栈**: React (UmiJS) 单页应用，前端资源托管在 cdn.chengfengerlai.com
- **特点**: 无状态页面，所有数据通过API动态加载，无需登录即可浏览资源列表

## 二、页面结构

### 首页 (SPA 单页)
- Banner轮播区（活动/广告）
- 资源展示区（Tab切换：云容器 / 虚拟机 / 裸金属）
- "租算力，快人一步" 引导区
- 页脚（公司信息、联系方式、二维码）

### 隐藏/需点击的页面
- 登录页: /login
- ECS市场: /ecs/market
- 控制台: 需登录后访问

## 三、API 结构

所有API均为 POST 请求，Base URL: https://www.cfgpu.com

| API 路径 | 功能 | 是否需要登录 |
|---------|------|------------|
| /api/main/header/menu.json | 获取导航菜单 | 否 |
| /api/main/header/platform.json | 获取平台信息 | 否 |
| /api/main/header/isLogin.json | 检查登录状态 | 否 |
| /api/cpi/container/list.json | 云容器资源列表 | 否 |
| /api/cpi/vm/list.json | 虚拟机资源列表 | 否 |
| /api/cpi/bare_metal/list.json | 裸金属资源列表 | 否 |

### API 响应格式
```json
{
  "success": true,
  "content": [...],
  "errorCode": null,
  "errorMsg": null
}
```

## 四、资源数据

### 云容器 (5个)
| GPU | 显存 | 内存 | CPU | 价格 |
|-----|------|------|-----|------|
| A100-PCIE | 40GB | 85GB/卡 | 11核 Xeon Gold 6248R | 1.79/卡/小时 |
| RTX 4090 | 24GB | 60GB/卡 | 17核 Platinum 8352V | 1.89/卡/小时 |
| L40S | 48GB | 117GB/卡 | 13核 Xeon Gold 6348 | 2.99/卡/小时 |
| RTX 3080 | 10GB | 48GB/卡 | 60核 ARM | 0.59/卡/小时 |
| HGX H800 | 80GB | 243GB/卡 | 22核 Platinum 8468 | 12.99/卡/小时 |

### 虚拟机 (2个)
| GPU | 显存 | 内存 | CPU | 价格 |
|-----|------|------|-----|------|
| RTX 4090 | 24GB | 60GB/卡 | 17核 Platinum 8352V | 1.89/卡/小时 |
| A100-PCIE-40GB | 40GB | 85GB/卡 | 11核 Xeon Gold 6248R | 1.99/卡/小时 |

### 裸金属 (10个)
| GPU | 显存 | 内存 | CPU | 价格 |
|-----|------|------|-----|------|
| RTX 4090 | 24G | 512GB | EPYC 7513*2 | 6xxx/台/月 |
| A100-40G-pcie | 40G | 640GB | Xeon Gold 6248R 80核 | 1xxxx/台/月 |
| H800-80G-nvlink | 80G | 64G DDR5*32 | Platinum 8468*2 | 5xxxx/台/月 |
| H100-80G-nvlink | 80G | 64G DDR5*32 | Platinum 8468*2 | 5xxxx/台/月 |
| h200-141G-nvlink | 141G | 64GB DDR5*32 | 8468*2 | 6xxxx/台/月 |
| A800-80G-nvlink | 80G | 2048G | 8336c | 2xxxx/台/月 |
| H20-96G-nvlink | 96G | 1960GB | 8457c*2 | 2xxxx/台/月 |
| h100-80G-nvlink | 80G | 64GB DDR5*32 | Platinum 8468*2 | 6xxxx/台/月 |
| L40 | 48G | 32GB DDR4*32 | Xeon 6348*2 | 9xxx/台/月 |
| A100-80G-nvlink | 80G | 1960 GiB | 8336c*2 | 2xxxx/台/月 |

## 五、网站痛点分析

1. **信息分散**: 三种资源类型需要切换Tab才能看到，无法一目了然
2. **价格不透明**: 裸金属价格用"6xxx"这种模糊表示
3. **对比困难**: 同一GPU在不同类型下的配置差异无法直观对比
4. **搜索缺失**: 没有搜索功能，找特定GPU型号需要手动浏览
5. **数据无法导出**: 无法将资源信息导出做进一步分析

## 六、CLI工具解决方案

详见 cfgpu-cli/ 目录，提供以下命令：
- `list` - 列出指定类型资源
- `menu` - 查看导航菜单
- `compare` - 跨类型对比GPU
- `price` - 价格速查表
- `search` - 关键词搜索
- `export` - 导出JSON数据
- `all` - 列出全部资源
