"""生图命令 - 通过 API 调用图像生成模型"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from typing import Optional


BASE_URL = "https://www.cfgpu.com"
COOKIE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cookies")

# 默认生图模型
DEFAULT_MODEL_ID = "doubao-seedream-5-0-260128"

# 可用生图模型列表
IMAGE_MODELS = {
    "seedream-5.0-pro": "doubao-seedream-5-0-pro",
    "seedream-5.0-lite": "doubao-seedream-5-0-260128",
    "seedream-5.0": "doubao-seedream-5-0",
    "seedream-4.5": "doubao-seedream-4.5",
    "seedream-4.0": "doubao-seedream-4.0",
    "gpt-image-1": "gpt-image-1",
    "gpt-image-1-mini": "gpt-image-1-mini",
    "imagen-3": "imagen-3-generate-002",
}


def _load_cookies() -> str:
    """从文件加载 cookie 字符串"""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def _llm_request(path: str, payload: dict) -> dict:
    """发送 POST 请求到 LLM 体验 API

    Args:
        path: API 路径（相对于 BASE_URL）
        payload: 请求体数据
    """
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "language": "zh-CN",
        "User-Agent": "CFGPU-CLI/1.0",
    }
    cookie = _load_cookies()
    if cookie:
        headers["Cookie"] = cookie

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  HTTP 错误 {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"  网络错误: {e.reason}")
        sys.exit(1)

    return body


def _create_image(model_id: str, prompt: str, resolution: str,
                  aspect_ratio: str) -> dict:
    """调用生图 API 创建图片

    Args:
        model_id: 模型 ID
        prompt: 图片描述
        resolution: 分辨率 (2K, 1K)
        aspect_ratio: 宽高比 (1:1, 16:9, 9:16, 4:3, 3:4)
    """
    payload = {
        "modelId": model_id,
        "generationMode": "IMAGE_TO_IMAGE",
        "params": {
            "prompt": prompt,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
            "watermark": True,
            "webSearch": False,
        },
    }
    return _llm_request("/llmExperience/v1/image/create", payload)


def _poll_image(biz_id: str, max_wait: int = 60) -> Optional[dict]:
    """轮询等待图片生成完成

    Args:
        biz_id: 业务 ID（create 接口返回的 bizId）
        max_wait: 最大等待时间（秒）
    """
    payload = {"bizIds": [biz_id]}
    start = time.time()

    while time.time() - start < max_wait:
        result = _llm_request("/llmExperience/v1/image/batchGet", payload)
        records = result if isinstance(result, list) else result.get("content", [])
        if records:
            record = records[0]
            status = record.get("status", "")
            if status in ("succeeded", "SUCCESS"):
                return record
            elif status in ("failed", "FAILED"):
                print(f"\n  生成失败: {record.get('errorMessage', '未知原因')}")
                return None
        time.sleep(2)
        print(".", end="", flush=True)

    print(f"\n  超时：{max_wait} 秒内未完成")
    return None


def _download_image(url: str, output_path: str) -> bool:
    """下载生成的图片到本地

    Args:
        url: 图片 URL
        output_path: 本地保存路径
    """
    req = urllib.request.Request(url, headers={"User-Agent": "CFGPU-CLI/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False


def run(prompt: Optional[str] = None, model: Optional[str] = None,
        resolution: str = "2K", aspect_ratio: str = "1:1",
        output: Optional[str] = None):
    """通过 API 调用图像生成模型

    Args:
        prompt: 图片描述（必填）
        model: 模型简称（可选，默认 seedream-5.0-lite）
        resolution: 分辨率，可选 2K/1K（默认 2K）
        aspect_ratio: 宽高比，可选 1:1/16:9/9:16/4:3/3:4（默认 1:1）
        output: 输出文件路径（可选，默认自动生成）
    """
    if not prompt:
        print("\n  用法: cfgpu generate-image <图片描述> [选项]")
        print("\n  选项:")
        print("    --model <模型>      模型简称 (默认: seedream-5.0-lite)")
        print("    --resolution <分辨率> 分辨率: 2K, 1K (默认: 2K)")
        print("    --ratio <宽高比>     宽高比: 1:1, 16:9, 9:16, 4:3, 3:4 (默认: 1:1)")
        print("    --output <路径>      输出文件路径 (默认: 自动生成)")
        print("\n  可用模型:")
        for short, full in IMAGE_MODELS.items():
            print(f"    {short}")
        print(f"\n  示例:")
        print(f"    cfgpu generate-image \"一只橘猫坐在窗台上看夕阳\"")
        print(f"    cfgpu generate-image \"赛博朋克城市夜景\" --model gpt-image-1 --ratio 16:9")
        print(f"    cfgpu generate-image \"水墨山水画\" --resolution 1K --output ./art.png")
        print()
        return

    # 解析模型 ID
    model_id = IMAGE_MODELS.get(model, model) if model else DEFAULT_MODEL_ID

    print(f"\n{'=' * 60}")
    print(f"  生图任务")
    print(f"{'=' * 60}")
    print(f"  模型: {model_id}")
    print(f"  描述: {prompt}")
    print(f"  分辨率: {resolution} | 宽高比: {aspect_ratio}")
    print(f"{'=' * 60}")

    # 检查登录
    cookie = _load_cookies()
    if not cookie:
        print("\n  错误: 未登录。请先在浏览器登录 cfgpu.com，")
        print("  然后运行: cfgpu save-cookie <cookie字符串>")
        print()
        return

    # 创建生图任务
    print("\n  正在提交生图任务...")
    result = _create_image(model_id, prompt, resolution, aspect_ratio)

    if not result.get("success"):
        print(f"  提交失败: {result.get('errorMsg', '未知错误')}")
        return

    content = result.get("content", {})
    task_id = content.get("bizId") or content.get("taskId")
    if not task_id:
        print(f"  未获取到任务 ID，响应: {json.dumps(content, ensure_ascii=False)}")
        return

    print(f"  任务 ID: {task_id}")
    print(f"  等待生成中...", end="", flush=True)

    # 轮询等待
    record = _poll_image(task_id)
    if not record:
        return

    # 下载图片
    image_url = record.get("ossUrl", "")
    if not image_url:
        print(f"\n  生成完成但未获取到图片 URL")
        return

    # 确定输出路径
    if not output:
        output_dir = os.getcwd()
        output = os.path.join(output_dir, f"generated_{task_id[:8]}.jpg")

    print(f"\n  正在下载图片...")
    if _download_image(image_url, output):
        print(f"\n  图片已保存到: {output}")
    else:
        print(f"\n  图片 URL: {image_url}")

    print(f"\n{'=' * 60}\n")
