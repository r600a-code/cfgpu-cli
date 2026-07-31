"""个人镜像管理命令 - 列出个人私有镜像"""

from cfgpu_cli.api import (
    CfgpuApiError,
    _request,
)


def _format_size(size_bytes: int) -> str:
    """将字节数转换为可读格式"""
    if size_bytes <= 0:
        return "0 B"
    gb = size_bytes / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    mb = size_bytes / (1024 ** 2)
    return f"{mb:.0f} MB"


def _format_time(timestamp_ms: int) -> str:
    """将毫秒时间戳转换为可读时间"""
    if not timestamp_ms:
        return "-"
    from datetime import datetime
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M")


def run(page: int = 1):
    """列出个人私有镜像

    Args:
        page: 页码，默认第1页
    """
    print(f"\n{'=' * 80}")
    print("  个人镜像列表")
    print(f"{'=' * 80}")

    try:
        result = _request("/api/image/page.json", payload={"pageNum": page, "pageSize": 50}, auth=True)
    except CfgpuApiError as e:
        print(f"  获取失败: {e}")
        return

    records = result.get("records", []) if isinstance(result, dict) else []
    total = result.get("total", 0) if isinstance(result, dict) else 0
    pages = result.get("pages", 0) if isinstance(result, dict) else 0

    if not records:
        print("  暂无镜像")
        return

    for i, img in enumerate(records, 1):
        image_id = img.get("imageId", "未知")
        name = img.get("name", "未知")
        size = _format_size(img.get("size", 0))
        region = img.get("region", "未知")
        os_type = img.get("os", "")
        arch = img.get("architecture", "")
        adapt_type = img.get("adaptType", "")
        source = img.get("sourceImageInfo", "")
        create_user = img.get("createUser", "")
        create_time = _format_time(img.get("gmtCreate", 0))
        shared = img.get("shared", False)
        be_shared = img.get("beShared", False)

        share_status = ""
        if shared:
            share_status = " [已分享]"
        elif be_shared:
            share_status = " [被分享]"
        else:
            share_status = " [私有]"

        print(f"\n  [{i}] {name}{share_status}")
        print(f"      ID: {image_id} | 区域: {region} | 大小: {size}")
        print(f"      系统: {os_type} | 架构: {arch} | 适配: {adapt_type}")
        print(f"      来源: {source}")
        print(f"      创建人: {create_user} | 创建时间: {create_time}")

    print(f"\n{'=' * 80}")
    print(f"  共 {total} 个镜像 (第 {page}/{pages} 页)")
    print(f"{'=' * 80}\n")
