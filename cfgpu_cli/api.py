"""CFGPU API 客户端 - 封装所有骋风算力API调用"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional


BASE_URL = "https://www.cfgpu.com"
COOKIE_FILE = os.path.join(os.path.dirname(__file__), ".cookies")


class CfgpuApiError(Exception):
    """API 调用异常"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


def _load_cookies() -> str:
    """从文件加载 cookie 字符串"""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def _save_cookies(cookie_str: str):
    """保存 cookie 字符串到文件"""
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        f.write(cookie_str)


def _request(path: str, payload: Optional[dict] = None, auth: bool = False) -> dict:
    """发送 POST 请求到 CFGPU API

    Args:
        path: API 路径
        payload: 请求体数据
        auth: 是否需要登录认证
    """
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload or {}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "CFGPU-CLI/1.0",
    }
    if auth:
        cookie = _load_cookies()
        if cookie:
            headers["Cookie"] = cookie

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise CfgpuApiError(f"HTTP_{e.code}", f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise CfgpuApiError("NETWORK", f"网络错误: {e.reason}")

    if not body.get("success"):
        raise CfgpuApiError(
            body.get("errorCode", "UNKNOWN"),
            body.get("errorMsg", "未知错误"),
        )
    return body.get("content", {})


def get_menu() -> dict:
    """获取导航菜单"""
    return _request("/api/main/header/menu.json")


def get_platform() -> dict:
    """获取平台信息"""
    return _request("/api/main/header/platform.json")


def check_login() -> dict:
    """检查登录状态"""
    return _request("/api/main/header/isLogin.json")


def list_resources(resource_type: str) -> list:
    """
    获取资源列表
    resource_type: container | vm | bare_metal
    """
    valid = {"container", "vm", "bare_metal"}
    if resource_type not in valid:
        raise ValueError(f"资源类型无效: {resource_type}，可选: {', '.join(valid)}")
    return _request(f"/api/cpi/{resource_type}/list.json")


def list_containers() -> list:
    """获取云容器列表"""
    return list_resources("container")


def list_vms() -> list:
    """获取虚拟机列表"""
    return list_resources("vm")


def list_bare_metal() -> list:
    """获取裸金属列表"""
    return list_resources("bare_metal")


def list_api_tokens() -> list:
    """获取 API Token 列表（需要登录认证）"""
    return _request("/api/authToken/list.json", auth=True)


def create_api_token(note: str) -> dict:
    """创建 API Token（需要登录认证）"""
    return _request("/api/authToken/create.json", payload={"note": note}, auth=True)


def update_api_token(token_id: str, note: str) -> dict:
    """编辑 API Token 备注（需要登录认证）"""
    return _request("/api/authToken/update.json", payload={"id": token_id, "note": note}, auth=True)


def enable_api_token(token_id: str) -> dict:
    """启用 API Token（需要登录认证）"""
    return _request("/api/authToken/enable.json", payload={"id": token_id}, auth=True)


def disable_api_token(token_id: str) -> dict:
    """禁用 API Token（需要登录认证）"""
    return _request("/api/authToken/disable.json", payload={"id": token_id}, auth=True)


def delete_api_token(token_id: str) -> dict:
    """删除 API Token（需要登录认证）"""
    return _request("/api/authToken/delete.json", payload={"id": token_id}, auth=True)


def save_cookie(cookie_str: str):
    """保存 cookie 到本地文件"""
    _save_cookies(cookie_str)
