"""实例管理命令 - 列出、查看个人实例"""

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


def run(status: str = None, page: int = 1):
    """列出个人实例

    Args:
        status: 可选的状态筛选 (RUNNING | CLOSED)
        page: 页码，默认第1页
    """
    print(f"\n{'=' * 80}")
    print("  个人实例列表")
    print(f"{'=' * 80}")

    try:
        payload = {"pageNum": page, "pageSize": 20}
        if status:
            payload["statusCode"] = status
        result = _request("/api/instance/page.json", payload=payload, auth=True)
    except CfgpuApiError as e:
        print(f"  获取失败: {e}")
        return

    records = result.get("records", []) if isinstance(result, dict) else []
    total = result.get("total", 0) if isinstance(result, dict) else 0
    pages = result.get("pages", 0) if isinstance(result, dict) else 0

    if not records:
        print("  暂无实例")
        return

    for i, inst in enumerate(records, 1):
        inst_id = inst.get("instanceId", "未知")
        inst_name = inst.get("instanceName") or inst_id
        region = inst.get("region", "未知")
        node = inst.get("node", "")
        status_text = inst.get("status", "未知")
        gpu_name = inst.get("gpuName", "未知")
        gpus = inst.get("gpus", 0)
        cpu_name = inst.get("cpuName", "")
        cpus = inst.get("cpus", 0)
        memory = _format_size(inst.get("memory", 0))
        price = inst.get("price", "0")
        price_unit = inst.get("priceUnit", "")
        consume_type = inst.get("consumeType", "")
        create_time = _format_time(inst.get("createTime", 0))
        expire_time = _format_time(inst.get("expireTime", 0))
        ssh_cmd = inst.get("sshCommand", "")
        jupyter = inst.get("jupyterLink", "")
        source_image = inst.get("sourceImageInfo", "")

        status_icon = "[运行]" if inst.get("statusCode") == "RUNNING" else "[关机]"
        print(f"\n  [{i}] {status_icon} {inst_name}")
        print(f"      ID: {inst_id} | 区域: {region} | 节点: {node}")
        print(f"      GPU: {gpu_name} x{gpus} | CPU: {cpu_name} {cpus}核 | 内存: {memory}")
        print(f"      计费: {consume_type} | 价格: ¥{price}/{price_unit}")
        print(f"      镜像: {source_image}")
        print(f"      创建: {create_time} | 到期: {expire_time}")
        if ssh_cmd:
            print(f"      SSH: {ssh_cmd}")
        if jupyter:
            print(f"      Jupyter: {jupyter}")

    print(f"\n{'=' * 80}")
    print(f"  共 {total} 个实例 (第 {page}/{pages} 页)")
    print(f"  筛选: 全部 | RUNNING(运行中) | CLOSED(已关机)")
    print(f"{'=' * 80}\n")
