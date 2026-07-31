"""资源列表命令 - 展示云容器/虚拟机/裸金属"""

from cfgpu_cli.api import list_resources, CfgpuApiError

TYPE_LABELS = {
    "container": "云容器",
    "vm": "虚拟机",
    "bare_metal": "裸金属",
}


def run(resource_type: str):
    """列出指定类型的资源"""
    label = TYPE_LABELS.get(resource_type, resource_type)
    print(f"\n{'=' * 60}")
    print(f"  {label} 资源列表")
    print(f"{'=' * 60}")

    try:
        items = list_resources(resource_type)
    except CfgpuApiError as e:
        print(f"  获取失败: {e}")
        return

    if not items:
        print("  暂无资源")
        return

    for i, item in enumerate(items, 1):
        title = item.get("title", "未知")
        price = item.get("price", "?")
        price_unit = item.get("priceUnit", "/卡/小时")
        attrs = item.get("attribute", [])

        print(f"\n  [{i}] {title}")
        print(f"      价格: {price} {price_unit}")

        if attrs:
            print(f"      配置:")
            for attr in attrs:
                key = attr.get("key", "")
                val = attr.get("value", "")
                print(f"        {key}: {val}")

    print(f"\n{'=' * 60}")
    print(f"  共 {len(items)} 个{label}资源")
    print(f"{'=' * 60}\n")
