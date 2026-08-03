"""SSH 连接命令 - 列出实例并快速 SSH 连接"""

import subprocess
import sys

from cfgpu_cli.api import CfgpuApiError, _request


def _format_size(size_bytes: int) -> str:
    """将字节数转换为可读格式"""
    if size_bytes <= 0:
        return "0 B"
    gb = size_bytes / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    mb = size_bytes / (1024 ** 2)
    return f"{mb:.0f} MB"


def _get_running_instances() -> list:
    """获取运行中的实例列表"""
    try:
        result = _request("/api/instance/page.json", payload={
            "pageNum": 1, "pageSize": 50, "statusCode": "RUNNING"
        }, auth=True)
        return result.get("records", []) if isinstance(result, dict) else []
    except CfgpuApiError as e:
        print(f"\n  错误: {e}")
        print("  请确认已登录: cfgpu login status")
        print()
        return []


def run(instance_id: str = None, show_list: bool = False):
    """SSH 连接到运行中的实例

    Args:
        instance_id: 实例 ID 或序号（可选，不指定则列出实例供选择）
        show_list: 是否只显示列表不连接
    """
    instances = _get_running_instances()

    if not instances:
        print("\n  没有运行中的实例。")
        print("  请先在网页端启动实例，然后重试。")
        print()
        return

    # 显示实例列表
    print(f"\n{'=' * 70}")
    print("  运行中的实例")
    print(f"{'=' * 70}")

    running = []
    for i, inst in enumerate(instances, 1):
        ssh_cmd = inst.get("sshCommand", "")
        if not ssh_cmd:
            continue

        inst_name = inst.get("instanceName") or inst.get("instanceId", "未知")
        gpu = inst.get("gpuName", "未知")
        gpus = inst.get("gpus", 0)
        region = inst.get("region", "未知")
        memory = _format_size(inst.get("memory", 0))
        jupyter = inst.get("jupyterLink", "")

        running.append({
            "index": i,
            "name": inst_name,
            "instance_id": inst.get("instanceId", ""),
            "gpu": f"{gpu} x{gpus}",
            "region": region,
            "memory": memory,
            "ssh": ssh_cmd,
            "jupyter": jupyter,
        })

        print(f"\n  [{i}] {inst_name}")
        print(f"      GPU: {running[-1]['gpu']} | 内存: {memory} | 区域: {region}")
        print(f"      SSH: {ssh_cmd}")
        if jupyter:
            print(f"      Jupyter: {jupyter}")

    if not running:
        print("\n  运行中的实例没有 SSH 连接信息。")
        print("  请确认实例已完全启动。")
        print()
        return

    print(f"\n{'=' * 70}")

    if show_list:
        print("\n  用法:")
        print(f"    cfgpu ssh <序号>      # 按序号连接 (如: cfgpu ssh 1)")
        print(f"    cfgpu ssh <实例ID>    # 按实例ID连接")
        print(f"    cfgpu ssh --jupyter <序号>  # 打开 Jupyter 链接")
        print()
        return

    # 选择实例
    target = None
    if instance_id:
        # 按序号
        if instance_id.isdigit():
            idx = int(instance_id)
            for r in running:
                if r["index"] == idx:
                    target = r
                    break
            if not target:
                print(f"\n  错误: 序号 {idx} 不存在，可选: 1-{len(running)}")
                print()
                return
        else:
            # 按实例 ID 匹配
            for r in running:
                if instance_id in r["instance_id"] or instance_id in r["name"]:
                    target = r
                    break
            if not target:
                print(f"\n  错误: 未找到匹配的实例: {instance_id}")
                print()
                return
    elif len(running) == 1:
        # 只有一个实例，直接连接
        target = running[0]
        print(f"\n  只有一个运行中的实例，自动选择: {target['name']}")
    else:
        # 多个实例，让用户选择
        print(f"\n  请选择要连接的实例 (输入序号 1-{len(running)}): ", end="", flush=True)
        try:
            choice = input().strip()
            idx = int(choice)
            for r in running:
                if r["index"] == idx:
                    target = r
                    break
        except (ValueError, EOFError):
            print("\n  已取消。")
            print()
            return

        if not target:
            print(f"\n  错误: 序号 {choice} 不存在。")
            print()
            return

    # 执行 SSH
    ssh_cmd = target["ssh"]
    print(f"\n  正在连接到: {target['name']} ({target['gpu']})")
    print(f"  命令: {ssh_cmd}")
    print(f"{'─' * 70}")
    print()

    # 解析 SSH 命令并执行
    # SSH 命令格式通常是: ssh -p <port> root@<host>
    try:
        # 使用 shell 执行 SSH 命令，这样终端交互正常
        subprocess.run(ssh_cmd, shell=True)
    except KeyboardInterrupt:
        print("\n\n  连接已断开。")
    except FileNotFoundError:
        print(f"\n  错误: 找不到 ssh 命令，请确认已安装 OpenSSH。")
    except Exception as e:
        print(f"\n  连接失败: {e}")

    print()
