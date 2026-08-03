"""菜单命令 - 展示网站导航结构和CLI命令帮助"""

from cfgpu_cli.api import get_menu, get_platform, CfgpuApiError


def _print_tree(data, indent=0):
    """递归打印树形结构"""
    prefix = "  " * indent
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                name = item.get("name", item.get("label", ""))
                path = item.get("path", item.get("url", ""))
                children = item.get("children", [])
                if path:
                    print(f"{prefix}- {name}  -> {path}")
                else:
                    print(f"{prefix}- {name}")
                if children:
                    _print_tree(children, indent + 1)
            else:
                print(f"{prefix}- {item}")
    elif isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, (dict, list)):
                print(f"{prefix}{key}:")
                _print_tree(val, indent + 1)
            else:
                print(f"{prefix}{key}: {val}")


def run():
    """展示导航菜单、平台信息和CLI命令帮助"""
    print(f"\n{'=' * 60}")
    print("  骋风算力 (CFGPU) - 导航菜单")
    print(f"{'=' * 60}")

    try:
        menu = get_menu()
        print("\n  导航菜单:")
        _print_tree(menu)
    except CfgpuApiError as e:
        print(f"  菜单获取失败: {e}")

    try:
        platform = get_platform()
        print("\n  平台信息:")
        _print_tree(platform)
    except CfgpuApiError as e:
        print(f"  平台信息获取失败: {e}")

    print(f"\n{'=' * 60}")
    print("  CLI 命令帮助")
    print(f"{'=' * 60}")
    print("""
  资源管理:
    list <type>              列出资源 (container | vm | bare_metal)
    compare                  对比所有GPU型号
    price                    价格速查表
    all                      列出所有资源

  模型平台:
    llm [provider]           大语言模型 (如: 深度求索, 千问, 字节跳动)
    video-models [provider]  视频生成模型 (如: Kling, 万相, 字节跳动)
    image-models [provider]  图像生成模型 (如: 字节跳动, OpenAI)
    voice-models [provider]  语音合成模型 (如: MiniMax, 字节跳动)

  模型体验 (需要登录):
    generate-image <描述>    调用API生图
      --model <模型>         模型简称 (默认: seedream-5.0-lite)
      --resolution <分辨率>  分辨率: 2K, 3K, 4K (默认: 2K)
      --ratio <宽高比>       宽高比: 1:1, 16:9, 9:16 等 (默认: 1:1)
      --output <路径>        输出文件路径 (默认: 自动生成)

  镜像市场:
    images [category]        镜像市场AI模型 (如: 大语言模型, 图像生成, 语音合成)

  个人空间 (需要登录):
    dashboard                个人空间概览 (余额、实例、镜像、存储)
    instance [status]        个人实例列表 (可选状态: RUNNING, CLOSED)
    my-images                个人私有镜像列表
    file-storage             个人文件存储信息
    api-token [action]       管理API Token (list|create|edit|enable|disable|delete)
    open-api                 列出开放API端点文档

  搜索与导出:
    search <关键词>          搜索GPU资源、镜像和模型
    export [file]            导出所有数据为JSON

  其他:
    menu                     显示此帮助菜单
    help                     显示命令帮助
""")
    print(f"{'=' * 60}\n")
