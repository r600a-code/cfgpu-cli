"""文件存储管理命令 - 列出个人文件存储信息"""

from cfgpu_cli.api import (
    CfgpuApiError,
    _request,
)


def run():
    """列出个人文件存储信息"""
    print(f"\n{'=' * 70}")
    print("  文件存储")
    print(f"{'=' * 70}")

    try:
        filesystems = _request("/api/filesystem/list.json", auth=True)
    except CfgpuApiError as e:
        print(f"  获取失败: {e}")
        return

    if not filesystems or not isinstance(filesystems, list):
        print("  暂无文件存储数据")
        return

    for fs in filesystems:
        region = fs.get("regionName", "未知")
        region_code = fs.get("regionCode", "")
        init = fs.get("init", False)
        host = fs.get("filebrowserHost", "")

        print(f"\n  === {region} ({region_code}) ===")

        if not init:
            print("  状态: 未初始化")
            continue

        limit_size = fs.get("limitSize", "0")
        usage_size = fs.get("usageSize", "0")
        free_size = fs.get("freeSize", "0")
        pay_size = fs.get("paySize", "0")
        price = fs.get("price", "0")
        pay_amount = fs.get("payAmount", "0")

        print(f"  状态:     已初始化")
        print(f"  总容量:   {limit_size} GB")
        print(f"  已使用:   {usage_size} GB")
        print(f"  免费额度: {free_size} GB")
        print(f"  付费容量: {pay_size} GB")
        print(f"  单价:     ¥{price}/GB/天")
        print(f"  日费用:   ¥{pay_amount}")
        if host:
            print(f"  访问地址: {host}")

    print(f"\n{'=' * 70}\n")
