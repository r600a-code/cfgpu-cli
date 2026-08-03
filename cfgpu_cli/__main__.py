#!/usr/bin/env python3
"""CFGPU CLI - 骋风算力命令行工具

Usage:
    python -m cfgpu_cli <command> [options]

Commands:
    list <type>         列出资源 (container | vm | bare_metal)
    menu                查看导航菜单和平台信息
    compare             对比所有GPU型号
    price               价格速查表
    search <key>        按关键词搜索GPU资源
    export [file]       导出所有资源数据为JSON
    all                 列出所有资源

  登录管理:
    login [action]      登录引导 (guide|status|open|save)

  模型平台:
    images [category]   列出镜像市场AI模型 (可选分类: 大语言模型, 图像生成, 语音合成等)
    llm [provider]      列出模型聚合平台的大语言模型 (可选提供商: DeepSeek, 阿里云等)
    video-models [provider]  列出视频生成模型 (可选提供商: 字节跳动, Kling, 万相等)
    image-models [provider]  列出图像生成模型 (可选提供商: 字节跳动, OpenAI等)
    voice-models [provider]  列出语音合成模型 (可选提供商: MiniMax, 字节跳动等)

  模型体验 (需要登录):
    generate-image <描述>  调用 API 生图 (--model/--resolution/--ratio/--output)
    open-model <模型>      在浏览器打开模型体验页面 (--list 列出可用模型)

  个人空间 (需要登录):
    dashboard           个人空间概览 (余额、实例、镜像、存储)
    instance [status]   个人实例列表 (可选状态: RUNNING, CLOSED)
    ssh [序号|实例ID]   SSH 连接到运行中的实例 (--list 查看列表)
    my-images           个人私有镜像列表
    file-storage        个人文件存储信息
    api-token [action]  管理API Token (list|create|edit|enable|disable|delete)
    open-api            列出开放API端点文档
"""

import sys


def print_usage():
    print(__doc__)


def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        sys.exit(0)

    command = args[0]

    if command == "list":
        if len(args) < 2:
            print("用法: cfgpu list <container|vm|bare_metal>")
            sys.exit(1)
        from cfgpu_cli.commands.resources import run
        run(args[1])

    elif command == "menu":
        from cfgpu_cli.commands.menu import run
        run()

    elif command == "compare":
        from cfgpu_cli.commands.compare import run
        run()

    elif command == "export":
        from cfgpu_cli.commands.export import run
        output = args[1] if len(args) > 1 else None
        run(output)

    elif command == "price":
        from cfgpu_cli.commands.price import run
        run()

    elif command == "search":
        if len(args) < 2:
            print("用法: cfgpu search <关键词>")
            sys.exit(1)
        from cfgpu_cli.commands.search import run
        run(args[1])

    elif command == "all":
        from cfgpu_cli.commands.resources import run
        for rtype in ["container", "vm", "bare_metal"]:
            run(rtype)

    elif command == "login":
        from cfgpu_cli.commands.login import run
        action = args[1] if len(args) > 1 else "guide"
        cookie_value = args[2] if len(args) > 2 else None
        run(action, cookie_value)

    elif command == "images":
        from cfgpu_cli.commands.images import run
        category = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(category, page)

    elif command == "llm":
        from cfgpu_cli.commands.llm import run
        provider = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(provider, page)

    elif command == "video-models":
        from cfgpu_cli.commands.video_models import run
        provider = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(provider, page)

    elif command == "image-models":
        from cfgpu_cli.commands.image_models import run
        provider = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(provider, page)

    elif command == "voice-models":
        from cfgpu_cli.commands.voice_models import run
        provider = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(provider, page)

    elif command == "generate-image":
        from cfgpu_cli.commands.generate_image import run
        # Parse options from remaining args
        prompt = None
        model = None
        resolution = "2K"
        ratio = "1:1"
        output = None
        i = 1
        while i < len(args):
            if args[i] == "--model" and i + 1 < len(args):
                model = args[i + 1]
                i += 2
            elif args[i] == "--resolution" and i + 1 < len(args):
                resolution = args[i + 1]
                i += 2
            elif args[i] == "--ratio" and i + 1 < len(args):
                ratio = args[i + 1]
                i += 2
            elif args[i] == "--output" and i + 1 < len(args):
                output = args[i + 1]
                i += 2
            elif not args[i].startswith("--"):
                if prompt is None:
                    prompt = args[i]
                else:
                    prompt += " " + args[i]
                i += 1
            else:
                i += 1
        run(prompt, model, resolution, ratio, output)

    elif command == "open-model":
        from cfgpu_cli.commands.open_model import run
        model = args[1] if len(args) > 1 and not args[1].startswith("--") else None
        list_models = "--list" in args
        run(model, list_models)

    elif command == "api-token":
        from cfgpu_cli.commands.api_token import run
        action = args[1] if len(args) > 1 else "list"
        token_id = args[2] if len(args) > 2 else None
        note = args[3] if len(args) > 3 else None
        run(action, token_id, note)

    elif command == "open-api":
        from cfgpu_cli.commands.open_api import run
        run()

    elif command == "dashboard":
        from cfgpu_cli.commands.dashboard import run
        run()

    elif command == "instance":
        from cfgpu_cli.commands.instance import run
        status = args[1] if len(args) > 1 else None
        page = int(args[2]) if len(args) > 2 else 1
        run(status, page)

    elif command == "ssh":
        from cfgpu_cli.commands.ssh import run
        instance_id = None
        show_list = False
        for arg in args[1:]:
            if arg == "--list":
                show_list = True
            else:
                instance_id = arg
        run(instance_id, show_list)

    elif command == "my-images":
        from cfgpu_cli.commands.console_image import run
        page = int(args[1]) if len(args) > 1 else 1
        run(page)

    elif command == "file-storage":
        from cfgpu_cli.commands.file_storage import run
        run()

    elif command in ("-h", "--help", "help"):
        print_usage()

    else:
        print(f"未知命令: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
