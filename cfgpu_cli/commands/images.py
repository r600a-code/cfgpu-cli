"""镜像市场命令 - 列出镜像市场中的AI模型"""

import json
import os
from typing import Optional


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


def run(category: Optional[str] = None, page: int = 1):
    """列出镜像市场中的AI模型
    
    Args:
        category: 可选分类筛选 (如: 大语言模型, 图像生成, 语音合成, 3D生成, AI Agent等)
        page: 页码，默认第1页
    """
    images = _load_images()
    
    # 按分类筛选
    if category:
        category_lower = category.lower()
        images = [
            img for img in images
            if category_lower in img.get("category", "").lower()
            or category_lower in img.get("name", "").lower()
        ]
    
    # 分页
    page_size = 10
    total = len(images)
    total_pages = (total + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_images = images[start_idx:end_idx]
    
    print(f"\n{'=' * 70}")
    if category:
        print(f"  镜像市场 - {category} (第 {page}/{total_pages} 页)")
    else:
        print(f"  镜像市场 - AI模型列表 (第 {page}/{total_pages} 页)")
    print(f"{'=' * 70}")
    
    if not page_images:
        print("  暂无镜像")
        return
    
    for i, img in enumerate(page_images, start_idx + 1):
        name = img.get("name", "未知")
        img_type = img.get("type", "未知")
        img_category = img.get("category", "")
        runtime = img.get("runtime", "0 h")
        desc = img.get("description", "").split("\n")[0][:60]
        
        print(f"\n  [{i}] {name}")
        print(f"      类型: {img_type} | 分类: {img_category}")
        print(f"      运行时长: {runtime}")
        print(f"      简介: {desc}")
    
    print(f"\n{'=' * 70}")
    print(f"  共 {total} 个镜像 (当前显示第 {page}/{total_pages} 页)")
    print(f"  可用分类: 大语言模型, 图像生成, 语音合成, 3D生成, AI Agent,")
    print(f"           视频生成, 目标检测, 模型训练, AI助手, 数字人, 科学计算")
    print(f"{'=' * 70}\n")
