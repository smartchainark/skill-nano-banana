#!/usr/bin/env python3
"""
Nano Banana - Gemini API 图片生成脚本

用法：
  python generate.py image "A cute robot"
  python generate.py social "AI tips" --platform youtube
  python generate.py thumbnail "10 Python Tips"
  python generate.py cover "博客标题" --subtitle "副标题"
  python generate.py icon "Music app" --style flat-design
  python generate.py banner "Welcome" --aspect-ratio 16:9
"""

import argparse
import os
import sys
from pathlib import Path

# Add nano_banana library path (relative to this script)
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from nano_banana.gemini_client import GeminiAPIClient
except ImportError as e:
    print(f"Error: Cannot import nano_banana library: {e}")
    print(f"Script directory: {SCRIPT_DIR}")
    print("Please run via: python scripts/run.py generate.py ...")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana - Gemini API 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="生成类型")

    # image 命令
    image_parser = subparsers.add_parser("image", help="通用图片生成")
    image_parser.add_argument("prompt", help="图片描述")
    image_parser.add_argument("--aspect-ratio", "-a", default="1:1",
                              help="宽高比 (1:1, 16:9, 9:16, 4:3, 3:4)")
    image_parser.add_argument("--output", "-o", help="输出路径")

    # social 命令
    social_parser = subparsers.add_parser("social", help="社交媒体配图")
    social_parser.add_argument("description", help="内容描述")
    social_parser.add_argument("--platform", "-p", default="instagram",
                               choices=["instagram", "twitter", "youtube", "linkedin"],
                               help="平台")
    social_parser.add_argument("--style", "-s", default="modern", help="风格")
    social_parser.add_argument("--output", "-o", help="输出路径")

    # thumbnail 命令
    thumb_parser = subparsers.add_parser("thumbnail", help="YouTube 缩略图")
    thumb_parser.add_argument("title", help="视频标题")
    thumb_parser.add_argument("--style", "-s", default="modern", help="风格")
    thumb_parser.add_argument("--output", "-o", help="输出路径")

    # cover 命令
    cover_parser = subparsers.add_parser("cover", help="博客/公众号封面")
    cover_parser.add_argument("title", help="主标题")
    cover_parser.add_argument("--subtitle", "-s", default="", help="副标题")
    cover_parser.add_argument("--expression", "-e", default="思考",
                              help="人物表情 (思考/惊讶/开心/托腮)")
    cover_parser.add_argument("--output", "-o", help="输出路径")

    # icon 命令
    icon_parser = subparsers.add_parser("icon", help="App 图标")
    icon_parser.add_argument("description", help="应用描述")
    icon_parser.add_argument("--style", "-s", default="modern",
                             choices=["modern", "flat-design", "3d", "minimal"],
                             help="风格")
    icon_parser.add_argument("--output", "-o", help="输出路径")

    # banner 命令
    banner_parser = subparsers.add_parser("banner", help="横幅")
    banner_parser.add_argument("description", help="横幅描述")
    banner_parser.add_argument("--style", "-s", default="modern", help="风格")
    banner_parser.add_argument("--aspect-ratio", "-a", default="16:9", help="宽高比")
    banner_parser.add_argument("--output", "-o", help="输出路径")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 检查 API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("错误: 请设置环境变量 GOOGLE_API_KEY")
        sys.exit(1)

    # 初始化客户端
    print("初始化 Gemini API 客户端...")
    client = GeminiAPIClient()

    # 执行生成
    result = None

    if args.command == "image":
        print(f"生成图片: {args.prompt}")
        result = client.generate_image(
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
        )

    elif args.command == "social":
        print(f"生成 {args.platform} 配图: {args.description}")
        result = client.generate_social_post(
            description=args.description,
            platform=args.platform,
            style=args.style,
        )

    elif args.command == "thumbnail":
        print(f"生成 YouTube 缩略图: {args.title}")
        result = client.generate_thumbnail(
            title=args.title,
            style=args.style,
        )

    elif args.command == "cover":
        print(f"生成封面图: {args.title}")
        result = client.generate_cover(
            title=args.title,
            subtitle=args.subtitle,
            expression=args.expression,
        )

    elif args.command == "icon":
        print(f"生成 App 图标: {args.description}")
        result = client.generate_app_icon(
            description=args.description,
            style=args.style,
        )

    elif args.command == "banner":
        print(f"生成横幅: {args.description}")
        result = client.generate_banner(
            description=args.description,
            style=args.style,
            aspect_ratio=args.aspect_ratio,
        )

    # 输出结果
    if result and result.success:
        print(f"生成成功!")
        for img_path in result.images:
            print(f"  {img_path}")

        # 如果指定了输出路径，复制文件
        if args.output and result.images:
            import shutil
            src = result.images[0]
            shutil.copy(src, args.output)
            print(f"已复制到: {args.output}")
    else:
        print(f"生成失败: {result.message if result else '未知错误'}")
        if result and result.error:
            print(f"  错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
