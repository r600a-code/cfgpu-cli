"""JSON导出命令 - 将所有资源数据和模型数据导出为JSON"""

import json
import os

from cfgpu_cli.api import list_resources, CfgpuApiError


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


def _load_images() -> list:
    """加载镜像市场数据"""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "images.json"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("images", [])


def run(output: str = None):
    """导出所有资源数据和模型数据为JSON"""
    data = {}

    # GPU资源
    for rtype in ["container", "vm", "bare_metal"]:
        try:
            data[rtype] = list_resources(rtype)
        except CfgpuApiError as e:
            data[rtype] = {"error": str(e)}

    # 镜像市场
    data["images"] = _load_images()

    # 模型平台
    data["llm_models"] = _load_json_models("llm_models.json")
    data["video_models"] = _load_json_models("video_models.json")
    data["image_models"] = _load_json_models("image_models.json")
    data["voice_models"] = _load_json_models("voice_models.json")

    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"  已导出到: {output}")
    else:
        print(json_str)
