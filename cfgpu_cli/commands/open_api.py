"""开放 API 文档命令 - 列出所有可用的开放 API 端点"""


# 开放 API 端点定义
OPEN_API_ENDPOINTS = [
    {
        "category": "区域与资源",
        "endpoints": [
            {
                "method": "POST",
                "path": "/userapi/v1/region/list",
                "description": "获取可用区域列表",
                "auth": True,
            },
            {
                "method": "POST",
                "path": "/userapi/v1/gpu/list",
                "description": "获取 GPU 型号列表",
                "auth": True,
            },
        ],
    },
    {
        "category": "镜像管理",
        "endpoints": [
            {
                "method": "POST",
                "path": "/userapi/v1/image/privateList",
                "description": "获取私有镜像列表",
                "auth": True,
            },
        ],
    },
    {
        "category": "实例管理",
        "endpoints": [
            {
                "method": "POST",
                "path": "/userapi/v1/instance/status",
                "description": "获取实例状态",
                "auth": True,
            },
            {
                "method": "POST",
                "path": "/userapi/v1/instance/page",
                "description": "获取实例列表（分页）",
                "auth": True,
            },
        ],
    },
]


def run():
    """列出所有可用的开放 API 端点"""
    print(f"\n{'=' * 80}")
    print("  开放 API 端点列表")
    print(f"{'=' * 80}")

    print("""
  使用说明:
    1. 在请求 Header 中添加 Authorization 参数进行鉴权
    2. Authorization 值为 API Token 的完整值
    3. 使用 API Token 调用时，将使用 Token 创建人的身份和权限
    4. 如果 Token 创建人权限被撤销，API 调用也会返回无权限

  鉴权示例:
    curl -X POST "https://www.cfgpu.com/userapi/v1/region/list" \\
         -H "Content-Type: application/json" \\
         -H "Authorization: <your-api-token>"
""")

    total = 0
    for category_info in OPEN_API_ENDPOINTS:
        category = category_info["category"]
        endpoints = category_info["endpoints"]

        print(f"\n  === {category} ===")
        for ep in endpoints:
            method = ep["method"]
            path = ep["path"]
            desc = ep["description"]
            auth = "需要认证" if ep["auth"] else "公开"

            print(f"\n  [{method}] {path}")
            print(f"      说明: {desc}")
            print(f"      认证: {auth}")
            total += 1

    print(f"\n{'=' * 80}")
    print(f"  共 {total} 个 API 端点")
    print(f"{'=' * 80}\n")
