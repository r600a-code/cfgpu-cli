"""对比命令 - 对比不同GPU型号"""

from cfgpu_cli.api import list_resources, CfgpuApiError


def run():
    """对比所有GPU型号资源"""
    print(f"\n{'=' * 70}")
    print("  GPU 型号对比 (所有资源类型)")
    print(f"{'=' * 70}")

    all_items = []
    for rtype in ["container", "vm", "bare_metal"]:
        try:
            items = list_resources(rtype)
            for item in items:
                item["_type"] = rtype
            all_items.extend(items)
        except CfgpuApiError as e:
            print(f"  {rtype} 获取失败: {e}")

    if not all_items:
        print("  无数据")
        return

    # 按标题分组（同一GPU可能出现在不同类型中）
    gpu_map = {}
    for item in all_items:
        title = item.get("title", "未知")
        if title not in gpu_map:
            gpu_map[title] = []
        gpu_map[title].append(item)

    for idx, (title, variants) in enumerate(gpu_map.items(), 1):
        print(f"\n  [{idx}] {title}")
        for v in variants:
            rtype = v.get("_type", "")
            type_label = {"container": "容器", "vm": "虚拟机", "bare_metal": "裸金属"}.get(rtype, rtype)
            price = v.get("price", "?")
            unit = v.get("priceUnit", "")
            print(f"      [{type_label}] 价格: {price} {unit}")

            attrs = v.get("attribute", [])
            for attr in attrs:
                key = attr.get("key", "")
                val = attr.get("value", "")
                print(f"        {key}: {val}")

    print(f"\n{'=' * 70}")
    print(f"  共 {len(gpu_map)} 种GPU型号，{len(all_items)} 个资源条目")
    print(f"{'=' * 70}\n")
