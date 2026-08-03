"""登录命令 - 引导用户获取并保存登录凭证"""

import os
import sys
import webbrowser


COOKIE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cookies")
LOGIN_URL = "https://www.cfgpu.com/login"


def _save_cookie(cookie_str: str):
    """保存 cookie 到本地文件"""
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        f.write(cookie_str)
    print(f"\n  Cookie 已保存到: {COOKIE_FILE}")


def _load_cookie() -> str:
    """从文件加载 cookie"""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def _check_login() -> bool:
    """检查是否已登录"""
    cookie = _load_cookie()
    if not cookie:
        return False
    # 简单检查：cookie 中应该包含 satoken
    return "satoken=" in cookie


def run(action: str = None, cookie_value: str = None):
    """登录管理命令

    Args:
        action: 操作类型 (status|guide|save|open)
        cookie_value: cookie 字符串（用于 save 操作）
    """
    if action == "status":
        # 检查登录状态
        if _check_login():
            print("\n  登录状态: 已登录")
            print(f"  Cookie 文件: {COOKIE_FILE}")
            print(f"  提示: Cookie 有时效性，如遇到 401 错误请重新登录\n")
        else:
            print("\n  登录状态: 未登录")
            print(f"  Cookie 文件: {COOKIE_FILE} (不存在或无效)")
            print("\n  请运行以下命令获取登录引导:")
            print("    cfgpu login guide")
            print()
        return

    if action == "save":
        # 保存 cookie
        if not cookie_value:
            print("\n  用法: cfgpu login save <cookie字符串>")
            print("\n  获取 cookie 的方法:")
            print("    1. 运行: cfgpu login open")
            print("    2. 在浏览器中登录")
            print("    3. 按 F12 打开开发者工具")
            print("    4. 在 Console 中执行: document.cookie")
            print("    5. 复制输出结果，运行: cfgpu login save \"<复制的内容>\"")
            print()
            return

        _save_cookie(cookie_value)
        print("\n  登录成功！现在可以使用需要登录的命令了。")
        print("\n  可用命令:")
        print("    cfgpu dashboard          # 查看个人空间")
        print("    cfgpu instance           # 查看实例列表")
        print("    cfgpu generate-image     # 调用 API 生图")
        print("    cfgpu open-model         # 打开模型体验页")
        print()
        return

    if action == "open":
        # 打开登录页面
        print(f"\n  正在打开登录页面: {LOGIN_URL}")
        print("  请在浏览器中完成登录，然后运行:")
        print("    cfgpu login guide")
        print()
        try:
            webbrowser.open(LOGIN_URL)
        except Exception:
            print(f"  无法自动打开浏览器，请手动访问: {LOGIN_URL}\n")
        return

    if action == "guide" or action is None:
        # 显示登录引导
        print(f"\n{'=' * 60}")
        print("  登录引导 - 获取骋风算力登录凭证")
        print(f"{'=' * 60}")
        print("""
  本工具需要登录凭证才能访问个人空间和调用模型 API。

  步骤 1: 打开登录页面
  ─────────────────────────────────────────
    运行命令:
      cfgpu login open

    或手动访问:
      https://www.cfgpu.com/login

  步骤 2: 在浏览器中登录
  ─────────────────────────────────────────
    使用手机号和密码登录，或使用微信扫码登录。

  步骤 3: 获取 Cookie
  ─────────────────────────────────────────
    登录成功后，按 F12 打开浏览器开发者工具，
    切换到 Console (控制台) 标签，输入:

      document.cookie

    按回车，复制输出的完整字符串。

  步骤 4: 保存 Cookie
  ─────────────────────────────────────────
    回到终端，运行:

      cfgpu login save "<复制的cookie字符串>"

    注意: 整个字符串要用双引号包裹。

  步骤 5: 验证登录
  ─────────────────────────────────────────
    运行:
      cfgpu login status

    如果显示"已登录"，就可以使用所有功能了。

  常见问题
  ─────────────────────────────────────────
  Q: Cookie 什么时候会过期？
  A: 通常 7-30 天，取决于平台设置。遇到 401 错误时
     需要重新登录。

  Q: 如何更新 Cookie？
  A: 重复上述步骤 1-4 即可。

  Q: Cookie 文件存在哪里？
  A: {cookie_file}
     该文件已加入 .gitignore，不会被提交到 Git。

  Q: 哪些命令需要登录？
  A: dashboard, instance, my-images, file-storage,
     api-token, generate-image, open-model 等。
""".format(cookie_file=COOKIE_FILE))
        print(f"{'=' * 60}\n")
        return

    # 未知操作
    print(f"\n  未知操作: {action}")
    print("  可用操作: status, guide, open, save")
    print()
