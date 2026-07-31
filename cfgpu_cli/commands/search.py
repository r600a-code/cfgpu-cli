"""搜索命令 - 按关键词搜索GPU资源、镜像市场和模型平台"""

import json
import os

from cfgpu_cli.api import list_resources, CfgpuApiError
from cfgpu_cli.commands.images import _load_images


def _load_json_models(filename: str) -> list:
    """加载JSON模型数据文件"""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        filename
    )
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])


def run(keyword: str):
    """按关键词搜索GPU资源、镜像市场和模型平台"""
    keyword_lower = keyword.lower()
    print(f"\n{'=' * 60}")
    print(f"  搜索: \"{keyword}\"")
    print(f"{'=' * 60}")

    found_gpu = []
    for rtype in ["container", "vm", "bare_metal"]:
        type_label = {"container": "容器", "vm": "虚拟机", "bare_metal": "裸金属"}.get(rtype, rtype)
        try:
            items = list_resources(rtype)
        except CfgpuApiError:
            continue

        for item in items:
            title = item.get("title", "")
            attrs_text = " ".join(
                f"{a.get('key', '')} {a.get('value', '')}"
                for a in item.get("attribute", [])
            )
            searchable = f"{title} {attrs_text}".lower()
            if keyword_lower in searchable:
                found_gpu.append((type_label, item))

    # 搜索镜像市场
    found_images = []
    images = _load_images()
    for img in images:
        name = img.get("name", "")
        desc = img.get("description", "")
        category = img.get("category", "")
        searchable = f"{name} {desc} {category}".lower()
        if keyword_lower in searchable:
            found_images.append(img)

    # 搜索大语言模型
    found_llm = []
    llm_models = _load_json_models("llm_models.json")
    for model in llm_models:
        name = model.get("name", "")
        provider = model.get("provider", "")
        desc = model.get("description", "")
        tags = " ".join(model.get("tags", []))
        searchable = f"{name} {provider} {desc} {tags}".lower()
        if keyword_lower in searchable:
            found_llm.append(("LLM", model))

    # 搜索视频模型
    found_video = []
    video_models = _load_json_models("video_models.json")
    for model in video_models:
        name = model.get("name", "")
        provider = model.get("provider", "")
        desc = model.get("description", "")
        tags = " ".join(model.get("tags", []))
        searchable = f"{name} {provider} {desc} {tags}".lower()
        if keyword_lower in searchable:
            found_video.append(("视频", model))

    # 搜索图像模型
    found_image = []
    image_models = _load_json_models("image_models.json")
    for model in image_models:
        name = model.get("name", "")
        provider = model.get("provider", "")
        desc = model.get("description", "")
        tags = " ".join(model.get("tags", []))
        searchable = f"{name} {provider} {desc} {tags}".lower()
        if keyword_lower in searchable:
            found_image.append(("生图", model))

    # 搜索语音模型
    found_voice = []
    voice_models = _load_json_models("voice_models.json")
    for model in voice_models:
        name = model.get("name", "")
        provider = model.get("provider", "")
        desc = model.get("description", "")
        tags = " ".join(model.get("tags", []))
        searchable = f"{name} {provider} {desc} {tags}".lower()
        if keyword_lower in searchable:
            found_voice.append(("语音", model))

    has_results = any([found_gpu, found_images, found_llm, found_video, found_image, found_voice])
    if not has_results:
        print("  未找到匹配结果")
    else:
        if found_gpu:
            print("\n  === GPU资源 ===")
            for idx, (type_label, item) in enumerate(found_gpu, 1):
                title = item.get("title", "?")
                price = item.get("price", "?")
                unit = item.get("priceUnit", "")
                print(f"\n  [{idx}] [{type_label}] {title} - {price} {unit}")
                for attr in item.get("attribute", []):
                    print(f"      {attr.get('key', '')}: {attr.get('value', '')}")

        if found_images:
            print("\n  === 镜像市场 ===")
            for idx, img in enumerate(found_images, 1):
                name = img.get("name", "?")
                img_type = img.get("type", "")
                category = img.get("category", "")
                runtime = img.get("runtime", "")
                desc = img.get("description", "").split("\n")[0][:50]
                print(f"\n  [{idx}] {name}")
                print(f"      类型: {img_type} | 分类: {category}")
                print(f"      运行时长: {runtime}")
                print(f"      简介: {desc}")

        if found_llm:
            print("\n  === 大语言模型 ===")
            for idx, (cat, model) in enumerate(found_llm, 1):
                name = model.get("name", "?")
                provider = model.get("provider", "")
                price = model.get("output_price", "")
                desc = model.get("description", "").split("\n")[0][:50]
                print(f"\n  [{idx}] {name}")
                print(f"      提供商: {provider} | 价格: {price}")
                print(f"      简介: {desc}")

        if found_video:
            print("\n  === 视频模型 ===")
            for idx, (cat, model) in enumerate(found_video, 1):
                name = model.get("name", "?")
                provider = model.get("provider", "")
                price = model.get("output_price", "")
                desc = model.get("description", "").split("\n")[0][:50]
                print(f"\n  [{idx}] {name}")
                print(f"      提供商: {provider} | 价格: {price}")
                print(f"      简介: {desc}")

        if found_image:
            print("\n  === 图像模型 ===")
            for idx, (cat, model) in enumerate(found_image, 1):
                name = model.get("name", "?")
                provider = model.get("provider", "")
                price = model.get("output_price", "")
                desc = model.get("description", "").split("\n")[0][:50]
                print(f"\n  [{idx}] {name}")
                print(f"      提供商: {provider} | 价格: {price}")
                print(f"      简介: {desc}")

        if found_voice:
            print("\n  === 语音模型 ===")
            for idx, (cat, model) in enumerate(found_voice, 1):
                name = model.get("name", "?")
                provider = model.get("provider", "")
                price = model.get("output_price", "")
                desc = model.get("description", "").split("\n")[0][:50]
                print(f"\n  [{idx}] {name}")
                print(f"      提供商: {provider} | 价格: {price}")
                print(f"      简介: {desc}")

    total = len(found_gpu) + len(found_images) + len(found_llm) + len(found_video) + len(found_image) + len(found_voice)
    print(f"\n  共找到 {total} 个结果")
    print(f"  (GPU: {len(found_gpu)}, 镜像: {len(found_images)}, LLM: {len(found_llm)}, 视频: {len(found_video)}, 生图: {len(found_image)}, 语音: {len(found_voice)})")
    print(f"{'=' * 60}\n")
