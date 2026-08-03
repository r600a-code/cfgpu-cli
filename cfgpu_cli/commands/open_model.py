"""打开模型体验页面 - 在浏览器中打开指定模型的体验界面"""

import subprocess
import sys
import webbrowser


BASE_URL = "https://www.cfgpu.com"

# 模型体验页面路径
MODEL_PAGES = {
    # 生图模型
    "seedream-5.0-pro": "/llm/experience/image?modelId=doubao-seedream-5-0-pro",
    "seedream-5.0-lite": "/llm/experience/image?modelId=doubao-seedream-5-0-260128",
    "seedream-5.0": "/llm/experience/image?modelId=doubao-seedream-5-0",
    "seedream-4.5": "/llm/experience/image?modelId=doubao-seedream-4.5",
    "seedream-4.0": "/llm/experience/image?modelId=doubao-seedream-4.0",
    "gpt-image-1": "/llm/experience/image?modelId=gpt-image-1",
    "gpt-image-1-mini": "/llm/experience/image?modelId=gpt-image-1-mini",
    "imagen-3": "/llm/experience/image?modelId=imagen-3-generate-002",
    # 对话模型
    "deepseek": "/llm/experience/chat?modelId=deepseek-v3",
    "qwen": "/llm/experience/chat?modelId=qwen-plus",
    # 视频模型
    "kling": "/llm/experience/video?modelId=kling-v2",
    # 通用入口
    "image": "/llm/experience/image",
    "video": "/llm/experience/video",
    "chat": "/llm/experience/chat",
    "square": "/llm/square",
}


def run(model: str = None, list_models: bool = False):
    """在浏览器中打开模型体验页面

    Args:
        model: 模型简称或页面类型 (image/video/chat/square)
        list_models: 列出所有可用的模型简称
    """
    if list_models:
        print("\n  可用模型简称:")
        print(f"\n  {'生图模型':^20}")
        print(f"  {'─' * 40}")
        for name in ["seedream-5.0-pro", "seedream-5.0-lite", "seedream-5.0",
                      "seedream-4.5", "seedream-4.0", "gpt-image-1",
                      "gpt-image-1-mini", "imagen-3"]:
            print(f"    {name}")
        print(f"\n  {'通用入口':^20}")
        print(f"  {'─' * 40}")
        for name in ["image", "video", "chat", "square"]:
            print(f"    {name}")
        print()
        return

    if not model:
        print("\n  用法: cfgpu open-model <模型简称> [--list]")
        print("\n  在浏览器中打开模型体验页面")
        print("\n  示例:")
        print("    cfgpu open-model seedream-5.0-lite    # 打开 Seedream 生图")
        print("    cfgpu open-model gpt-image-1          # 打开 GPT 生图")
        print("    cfgpu open-model image                # 打开生图模型选择页")
        print("    cfgpu open-model square               # 打开模型广场")
        print("    cfgpu open-model --list               # 列出所有可用模型")
        print()
        return

    # 查找 URL
    if model in MODEL_PAGES:
        path = MODEL_PAGES[model]
    else:
        # 尝试作为完整 URL 或模型 ID
        if model.startswith("http"):
            path = model.replace(BASE_URL, "")
        else:
            # 默认当作生图模型 ID
            path = f"/llm/experience/image?modelId={model}"

    url = f"{BASE_URL}{path}"
    print(f"\n  正在打开: {url}")

    try:
        webbrowser.open(url)
        print(f"  已在浏览器中打开\n")
    except Exception:
        # 降级到系统命令
        try:
            subprocess.run(["open", url], check=False)
            print(f"  已在浏览器中打开\n")
        except Exception:
            print(f"  无法自动打开浏览器，请手动访问:")
            print(f"  {url}\n")
