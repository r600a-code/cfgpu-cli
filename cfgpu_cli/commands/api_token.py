"""API Token 管理命令 - 列出、创建、编辑、启用、禁用、删除 API Token"""

from typing import Optional

from cfgpu_cli.api import (
    CfgpuApiError,
    list_api_tokens,
    create_api_token,
    update_api_token,
    enable_api_token,
    disable_api_token,
    delete_api_token,
)


def run(action: Optional[str] = None, token_id: Optional[str] = None, note: Optional[str] = None):
    """管理 API Token

    Args:
        action: 操作类型 (list | create | edit | enable | disable | delete)
        token_id: Token ID（用于 edit/enable/disable/delete）
        note: 备注（用于 create/edit）
    """
    if not action or action == "list":
        _list_tokens()
    elif action == "create":
        if not note:
            print("  用法: cfgpu api-token create <备注>")
            return
        _create_token(note)
    elif action == "edit":
        if not token_id or not note:
            print("  用法: cfgpu api-token edit <token_id> <备注>")
            return
        _edit_token(token_id, note)
    elif action == "enable":
        if not token_id:
            print("  用法: cfgpu api-token enable <token_id>")
            return
        _enable_token(token_id)
    elif action == "disable":
        if not token_id:
            print("  用法: cfgpu api-token disable <token_id>")
            return
        _disable_token(token_id)
    elif action == "delete":
        if not token_id:
            print("  用法: cfgpu api-token delete <token_id>")
            return
        _delete_token(token_id)
    else:
        print(f"  未知操作: {action}")
        print("  可用操作: list, create, edit, enable, disable, delete")


def _list_tokens():
    """列出所有 API Token"""
    print(f"\n{'=' * 80}")
    print("  API Token 列表")
    print(f"{'=' * 80}")

    try:
        tokens = list_api_tokens()
    except CfgpuApiError as e:
        print(f"  获取失败: {e}")
        print("  提示: 请先登录并保存 cookie")
        return

    if not tokens:
        print("  暂无 API Token")
        return

    print(f"\n  {'ID':<20} {'状态':<6} {'创建时间':<20} {'备注':<20}")
    print(f"  {'-' * 76}")

    for token in tokens:
        token_id = token.get("bizId", "")
        status = "禁用" if token.get("disable") else "启用"
        create_time = token.get("createTimeStr", "")
        note = token.get("note", "")[:18]

        print(f"  {token_id:<20} {status:<6} {create_time:<20} {note:<20}")

    enabled_count = sum(1 for t in tokens if not t.get("disable"))
    disabled_count = sum(1 for t in tokens if t.get("disable"))

    print(f"\n{'=' * 80}")
    print(f"  共 {len(tokens)} 个 Token (启用: {enabled_count}, 禁用: {disabled_count})")
    print(f"{'=' * 80}\n")


def _create_token(note: str):
    """创建新的 API Token"""
    print(f"\n  正在创建 API Token...")

    try:
        result = create_api_token(note)
        print(f"  创建成功!")
        print(f"  Token ID: {result.get('bizId', '')}")
        print(f"  Token: {result.get('token', '')}")
        print(f"  备注: {note}")
        print(f"\n  请妥善保存 Token，它只会显示一次!")
    except CfgpuApiError as e:
        print(f"  创建失败: {e}")


def _edit_token(token_id: str, note: str):
    """编辑 API Token 备注"""
    print(f"\n  正在编辑 API Token {token_id}...")

    try:
        update_api_token(token_id, note)
        print(f"  编辑成功! 新备注: {note}")
    except CfgpuApiError as e:
        print(f"  编辑失败: {e}")


def _enable_token(token_id: str):
    """启用 API Token"""
    print(f"\n  正在启用 API Token {token_id}...")

    try:
        enable_api_token(token_id)
        print(f"  启用成功!")
    except CfgpuApiError as e:
        print(f"  启用失败: {e}")


def _disable_token(token_id: str):
    """禁用 API Token"""
    print(f"\n  正在禁用 API Token {token_id}...")

    try:
        disable_api_token(token_id)
        print(f"  禁用成功!")
    except CfgpuApiError as e:
        print(f"  禁用失败: {e}")


def _delete_token(token_id: str):
    """删除 API Token"""
    print(f"\n  正在删除 API Token {token_id}...")
    print(f"  警告: 此操作不可恢复!")

    try:
        delete_api_token(token_id)
        print(f"  删除成功!")
    except CfgpuApiError as e:
        print(f"  删除失败: {e}")
