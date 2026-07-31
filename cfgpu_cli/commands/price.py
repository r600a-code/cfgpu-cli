"""价格命令 - 以表格形式展示价格对比"""

from cfgpu_cli.api import list_resources, CfgpuApiError


def run():
    """以表格形式展示所有资源价格"""
    print(f"\n{'=' * 80}")
    print("  骋风算力 - GPU 价格速查表")
    print(f"{'=' * 80}")

    # 表头
    header = f"{'类型':<8} {'GPU型号':<22} {'显存':<10} {'内存':<14} {'CPU':<30} {'价格':<14}"
    print(f"\n  {header}")
    print(f"  {'-' * 78}")

    for rtype in ["container", "vm", "bare_metal"]:
        type_label = {"container": "容器", "vm": "虚拟机", "bare_metal": "裸金属"}.get(rtype, rtype)
        try:
            items = list_resources(rtype)
        except CfgpuApiError as e:
            print(f"  {rtype} 获取失败: {e}")
            continue

        for item in items:
            title = item.get("title", "?")
            price = item.get("price", "?")
            unit = item.get("priceUnit", "")
            attrs = item.get("attribute", [])

            vram = ""
            memory = ""
            cpu = ""
            for attr in attrs:
                key = attr.get("key", "")
                val = attr.get("value", "")
                if "显存" in key:
                    vram = val
                elif "内存" in key:
                    memory = val
                elif "CPU" in key:
                    cpu = val[:28]

            row = f"{type_label:<8} {title:<22} {vram:<10} {memory:<14} {cpu:<30} {price}{unit:<6}"
            print(f"  {row}")

    print(f"\n{'=' * 80}\n")
