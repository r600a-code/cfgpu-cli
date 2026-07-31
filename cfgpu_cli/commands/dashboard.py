"""控制台概览命令 - 显示个人空间余额、实例、镜像、存储概览"""

from cfgpu_cli.api import (
    CfgpuApiError,
    _request,
)


def run():
    """显示个人空间概览信息"""
    print(f"\n{'=' * 70}")
    print("  个人空间概览")
    print(f"{'=' * 70}")

    # 余额信息
    try:
        balance = _request("/api/recharge/balanceQuery.json", auth=True)
        print(f"\n  === 账户余额 ===")
        print(f"  可用总额: ¥{balance.get('total', '0')}")
        print(f"  余额:     ¥{balance.get('balance', '0')}")
        print(f"  代金券:   ¥{balance.get('voucherAmount', '0')}")
        print(f"  信用额度: ¥{balance.get('creditLimitNum', '0')}")
    except CfgpuApiError as e:
        print(f"\n  余额获取失败: {e}")

    # 团队信息
    try:
        team = _request("/api/team/info.json", auth=True)
        print(f"\n  === 空间信息 ===")
        print(f"  空间名称: {team.get('tenantName', '未知')}")
        print(f"  空间类型: {'个人空间' if team.get('type') == 0 else '团队空间'}")
    except CfgpuApiError as e:
        print(f"\n  空间信息获取失败: {e}")

    # 实例概览
    try:
        instances = _request("/api/instance/page.json", payload={"pageNum": 1, "pageSize": 50}, auth=True)
        records = instances.get("records", []) if isinstance(instances, dict) else []
        total = instances.get("total", 0) if isinstance(instances, dict) else 0

        running = sum(1 for r in records if r.get("statusCode") == "RUNNING")
        closed = sum(1 for r in records if r.get("statusCode") == "CLOSED")

        print(f"\n  === 实例概览 ===")
        print(f"  总实例数: {total}")
        print(f"  运行中:   {running}")
        print(f"  已关机:   {closed}")
    except CfgpuApiError as e:
        print(f"\n  实例信息获取失败: {e}")

    # 镜像概览
    try:
        overview = _request("/api/image/overview.json", auth=True)
        max_usage = int(overview.get("maxUsage", 0))
        usage = int(overview.get("usage", 0))
        free_usage = int(overview.get("freeUsage", 0))
        charge = overview.get("charge", "0")
        price = overview.get("price", "0")

        max_gb = max_usage / (1024 ** 3)
        usage_gb = usage / (1024 ** 3)
        free_gb = free_usage / (1024 ** 3)

        print(f"\n  === 镜像存储 ===")
        print(f"  总容量:   {max_gb:.1f} GB")
        print(f"  已使用:   {usage_gb:.1f} GB")
        print(f"  免费额度: {free_gb:.1f} GB")
        print(f"  计费容量: {charge} GB")
        print(f"  存储费用: ¥{price}/GB/天")
    except CfgpuApiError as e:
        print(f"\n  镜像存储信息获取失败: {e}")

    # 文件存储概览
    try:
        filesystems = _request("/api/filesystem/list.json", auth=True)
        print(f"\n  === 文件存储 ===")
        if isinstance(filesystems, list):
            for fs in filesystems:
                region = fs.get("regionName", "未知")
                init = fs.get("init", False)
                if not init:
                    print(f"\n  [{region}] 未初始化")
                    continue
                limit_size = fs.get("limitSize", "0")
                usage_size = fs.get("usageSize", "0")
                free_size = fs.get("freeSize", "0")
                pay_amount = fs.get("payAmount", "0")
                print(f"\n  [{region}]")
                print(f"      总容量: {limit_size} GB")
                print(f"      已使用: {usage_size} GB")
                print(f"      免费额度: {free_size} GB")
                print(f"      存储费用: ¥{pay_amount}/天")
        else:
            print("  暂无文件存储数据")
    except CfgpuApiError as e:
        print(f"\n  文件存储信息获取失败: {e}")

    print(f"\n{'=' * 70}\n")
