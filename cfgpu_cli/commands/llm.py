"""模型聚合平台命令 - 列出可用的大语言模型"""

import json
import os
from typing import Optional


def _load_llm_models() -> list:
    """加载大语言模型数据"""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "llm_models.json"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])


def run(provider: Optional[str] = None, page: int = 1):
    """列出模型聚合平台的大语言模型
    
    Args:
        provider: 可选的模型提供商筛选 (如: DeepSeek, 阿里云, 智谱AI, Meta, OpenAI, Google等)
        page: 页码，默认第1页
    """
    models = _load_llm_models()
    
    # 按提供商筛选
    if provider:
        provider_lower = provider.lower()
        models = [
            m for m in models
            if provider_lower in m.get("provider", "").lower()
            or provider_lower in m.get("name", "").lower()
        ]
    
    # 分页
    page_size = 10
    total = len(models)
    total_pages = (total + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_models = models[start_idx:end_idx]
    
    print(f"\n{'=' * 70}")
    if provider:
        print(f"  模型聚合平台 - {provider} (第 {page}/{total_pages} 页)")
    else:
        print(f"  模型聚合平台 - 大语言模型 (第 {page}/{total_pages} 页)")
    print(f"{'=' * 70}")
    
    if not page_models:
        print("  暂无模型")
        return
    
    for i, model in enumerate(page_models, start_idx + 1):
        name = model.get("name", "未知")
        model_provider = model.get("provider", "未知")
        model_type = model.get("type", "")
        parameters = model.get("parameters", "")
        context_length = model.get("context_length", "")
        pricing = model.get("pricing", {})
        desc = model.get("description", "").split("\n")[0][:60]
        
        print(f"\n  [{i}] {name}")
        print(f"      提供商: {model_provider} | 类型: {model_type}")
        print(f"      参数量: {parameters} | 上下文长度: {context_length}")
        if pricing:
            input_price = pricing.get("input", "")
            output_price = pricing.get("output", "")
            print(f"      价格: 输入 {input_price} | 输出 {output_price}")
        print(f"      简介: {desc}")
    
    print(f"\n{'=' * 70}")
    print(f"  共 {total} 个模型 (当前显示第 {page}/{total_pages} 页)")
    print(f"  可用提供商: DeepSeek, 阿里云, 智谱AI, Meta, Anthropic, OpenAI, Google")
    print(f"{'=' * 70}\n")
