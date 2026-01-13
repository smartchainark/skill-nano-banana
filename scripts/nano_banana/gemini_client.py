"""Gemini API client wrapper for image generation using official google-genai SDK."""

import logging
import os
from typing import Optional, List
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from .config import APIConfig, ServerConfig
from .types import (
    ImageRequest,
    GenerationResult,
    AspectRatio,
    ImagePurpose,
    ImageStyle,
    PURPOSE_ASPECT_RATIOS,
    PURPOSE_STYLES,
)
from .prompt_templates import PromptBuilder

logger = logging.getLogger(__name__)


class GeminiAPIClient:
    """Wrapper for official Gemini API for image generation."""

    # Aspect ratio to dimension mapping
    ASPECT_DIMENSIONS = {
        AspectRatio.SQUARE: (1024, 1024),
        AspectRatio.LANDSCAPE_16_9: (1664, 928),
        AspectRatio.PORTRAIT_9_16: (928, 1664),
        AspectRatio.LANDSCAPE_4_3: (1472, 1140),
        AspectRatio.PORTRAIT_3_4: (1140, 1472),
        AspectRatio.WIDE_21_9: (1792, 768),
    }

    def __init__(self, api_config: APIConfig = None, server_config: ServerConfig = None):
        self.api_config = api_config or APIConfig.from_env()
        self.server_config = server_config or ServerConfig.from_env()

        # Set API key in environment for google-genai
        os.environ["GOOGLE_API_KEY"] = self.api_config.api_key

        # Initialize client
        self._client = genai.Client()
        self._model = self.server_config.model

        logger.info(f"Gemini API client initialized with model: {self._model}")

    def _build_aspect_ratio_hint(self, aspect_ratio: AspectRatio) -> str:
        """Build aspect ratio hint for the prompt."""
        hints = {
            AspectRatio.SQUARE: "IMPORTANT: Generate image in SQUARE format (1:1 aspect ratio)",
            AspectRatio.LANDSCAPE_16_9: "IMPORTANT: Generate image in WIDE LANDSCAPE format (16:9 aspect ratio)",
            AspectRatio.PORTRAIT_9_16: "IMPORTANT: Generate image in TALL PORTRAIT format (9:16 aspect ratio)",
            AspectRatio.LANDSCAPE_4_3: "IMPORTANT: Generate image in LANDSCAPE format (4:3 aspect ratio)",
            AspectRatio.PORTRAIT_3_4: "IMPORTANT: Generate image in PORTRAIT format (3:4 aspect ratio)",
            AspectRatio.WIDE_21_9: "IMPORTANT: Generate image in ULTRA-WIDE PANORAMIC format (21:9 aspect ratio)",
        }
        return hints.get(aspect_ratio, "")

    def _save_image_from_response(self, response, output_path: Path, prefix: str = "generated") -> List[Path]:
        """Extract and save images from API response."""
        saved_files = []

        for i, part in enumerate(response.parts):
            if hasattr(part, 'inline_data') and part.inline_data:
                # Get image from response
                image = part.as_image()
                filename = f"{prefix}_{i}.png"
                filepath = output_path / filename

                # Handle filename collision
                counter = 1
                while filepath.exists():
                    filename = f"{prefix}_{i}_{counter}.png"
                    filepath = output_path / filename
                    counter += 1

                image.save(str(filepath))
                saved_files.append(filepath)
                logger.info(f"Saved image: {filepath}")

        return saved_files

    def generate_from_request(self, request: ImageRequest) -> GenerationResult:
        """Generate image from structured request."""
        output_path = self.server_config.ensure_output_dir()

        try:
            # Auto-set aspect ratio and style based on purpose if not specified
            if request.purpose:
                if request.aspect_ratio == AspectRatio.SQUARE:
                    request.aspect_ratio = PURPOSE_ASPECT_RATIOS.get(
                        request.purpose,
                        AspectRatio.SQUARE
                    )
                if not request.style:
                    request.style = PURPOSE_STYLES.get(request.purpose)

            # Build optimized prompt
            enhanced_prompt = PromptBuilder.build_prompt(request)

            # Add aspect ratio hint at the BEGINNING
            aspect_hint = self._build_aspect_ratio_hint(request.aspect_ratio)
            if aspect_hint:
                enhanced_prompt = f"{aspect_hint}. {enhanced_prompt}"

            logger.info(f"Enhanced prompt: {enhanced_prompt[:200]}...")

            generated_files: List[Path] = []

            for i in range(request.count):
                response = self._client.models.generate_content(
                    model=self._model,
                    contents=[enhanced_prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                    ),
                )

                # Save images from response
                purpose_prefix = request.purpose.value if request.purpose else "generated"
                files = self._save_image_from_response(response, output_path, f"{purpose_prefix}_{i}")
                generated_files.extend(files)

            if not generated_files:
                return GenerationResult(
                    success=False,
                    message="No images generated",
                    error="API returned no image data"
                )

            return GenerationResult(
                success=True,
                message=f"Generated {len(generated_files)} image(s)",
                images=generated_files,
                prompt_used=enhanced_prompt
            )

        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return GenerationResult(
                success=False,
                message="Image generation failed",
                error=str(e)
            )

    def generate_image(
        self,
        prompt: str,
        purpose: Optional[str] = None,
        aspect_ratio: str = "1:1",
        style: Optional[str] = None,
        lighting: Optional[str] = None,
        mood: Optional[str] = None,
        color_palette: Optional[str] = None,
        count: int = 1,
        output_dir: Optional[Path] = None,
        filename_prefix: str = "generated",
        quality: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> GenerationResult:
        """Generate image with full options."""
        # Convert string parameters to enums
        purpose_enum = None
        if purpose:
            try:
                purpose_enum = ImagePurpose(purpose)
            except ValueError:
                pass

        style_enum = None
        if style:
            try:
                style_enum = ImageStyle(style)
            except ValueError:
                pass

        aspect_enum = AspectRatio.from_string(aspect_ratio)

        request = ImageRequest(
            prompt=prompt,
            purpose=purpose_enum,
            aspect_ratio=aspect_enum,
            style=style_enum,
            lighting=lighting,
            mood=mood,
            color_palette=color_palette,
            count=count,
            quality=quality,
            negative_prompt=negative_prompt,
            seed=seed,
            width=width,
            height=height
        )

        return self.generate_from_request(request)

    def generate_app_icon(
        self,
        description: str,
        style: str = "flat-design",
        remove_background: bool = True,
        generate_sizes: Optional[List[int]] = None,
        platform: Optional[str] = None,
        background_color: Optional[str] = None,
        shape: str = "squircle",
    ) -> GenerationResult:
        """Generate app icon with optimized settings and optional background removal."""
        # Add style-specific prompt enhancements
        style_prompts = {
            "gradient": "smooth gradient background, vibrant colors",
            "glassmorphism": "glassmorphism effect, frosted glass, blur, transparency",
        }
        extra_prompt = style_prompts.get(style, "")
        enhanced_description = f"{description}, {extra_prompt}" if extra_prompt else description

        request = ImageRequest(
            prompt=enhanced_description,
            purpose=ImagePurpose.APP_ICON,
            aspect_ratio=AspectRatio.SQUARE,
            style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.FLAT_DESIGN,
        )

        result = self.generate_from_request(request)

        # Post-process: remove background and generate sizes
        if result.success and result.images:
            try:
                from .image_processing import (
                    remove_background as remove_bg,
                    generate_icon_sizes,
                    add_background_to_icon,
                    PLATFORM_SIZES
                )

                # Determine sizes to generate
                sizes_to_generate = generate_sizes
                if platform and platform in PLATFORM_SIZES:
                    sizes_to_generate = PLATFORM_SIZES[platform]

                processed_images = []
                for img_path in result.images:
                    if sizes_to_generate:
                        # Generate multiple sizes with background removal and shape
                        icon_paths = generate_icon_sizes(
                            img_path,
                            sizes=sizes_to_generate,
                            remove_bg=remove_background,
                            shape=shape,
                            platform=platform
                        )

                        # Add background color if specified
                        if background_color:
                            for icon_path in icon_paths:
                                add_background_to_icon(icon_path, background_color, icon_path)

                        processed_images.extend(icon_paths)
                    elif remove_background:
                        # Just remove background
                        nobg_path = remove_bg(img_path)
                        if background_color:
                            add_background_to_icon(nobg_path, background_color, nobg_path)
                        processed_images.append(nobg_path)
                    else:
                        processed_images.append(img_path)

                if processed_images:
                    result.images = processed_images
                    platform_info = f" for {platform}" if platform else ""
                    result.message = f"Generated {len(processed_images)} icon(s){platform_info}"
            except ImportError:
                logger.warning("rembg not installed, skipping background removal")
            except Exception as e:
                logger.warning(f"Background removal failed: {e}")

        return result

    def generate_banner(
        self,
        description: str,
        style: str = "modern",
        aspect_ratio: str = "16:9",
    ) -> GenerationResult:
        """Generate banner with optimized settings."""
        request = ImageRequest(
            prompt=description,
            purpose=ImagePurpose.BANNER,
            aspect_ratio=AspectRatio.from_string(aspect_ratio),
            style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.MODERN,
        )
        return self.generate_from_request(request)

    def generate_product_photo(
        self,
        description: str,
        style: str = "studio",
        lighting: str = "studio",
    ) -> GenerationResult:
        """Generate product photo with optimized settings."""
        request = ImageRequest(
            prompt=description,
            purpose=ImagePurpose.PRODUCT,
            aspect_ratio=AspectRatio.PORTRAIT_3_4,
            style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.STUDIO,
            lighting=lighting,
        )
        return self.generate_from_request(request)

    def generate_thumbnail(
        self,
        description: str,
        style: str = "cinematic",
    ) -> GenerationResult:
        """Generate YouTube thumbnail with optimized settings."""
        request = ImageRequest(
            prompt=description,
            purpose=ImagePurpose.THUMBNAIL,
            aspect_ratio=AspectRatio.LANDSCAPE_16_9,
            style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.CINEMATIC,
            mood="energetic",
        )
        return self.generate_from_request(request)

    def generate_social_post(
        self,
        description: str,
        platform: str = "instagram",
        style: str = "modern",
    ) -> GenerationResult:
        """Generate social media post image."""
        # Determine aspect ratio based on platform
        if platform.lower() in ["instagram", "facebook"]:
            aspect = AspectRatio.SQUARE
            purpose = ImagePurpose.SOCIAL_POST
        elif platform.lower() in ["story", "tiktok", "reels"]:
            aspect = AspectRatio.PORTRAIT_9_16
            purpose = ImagePurpose.STORY
        elif platform.lower() in ["twitter", "linkedin"]:
            aspect = AspectRatio.LANDSCAPE_16_9
            purpose = ImagePurpose.SOCIAL_POST
        else:
            aspect = AspectRatio.SQUARE
            purpose = ImagePurpose.SOCIAL_POST

        request = ImageRequest(
            prompt=description,
            purpose=purpose,
            aspect_ratio=aspect,
            style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.MODERN,
        )
        return self.generate_from_request(request)

    def generate_cover(
        self,
        title: str,
        subtitle: str = "",
        expression: str = "思考",
        ip_image_path: Optional[Path] = None,
        style_ref_path: Optional[Path] = None,
    ) -> GenerationResult:
        """
        生成博客/公众号封面图（支持多参考图）。

        使用 IP 形象图片和风格参考图生成带中文标题的封面图。

        Args:
            title: 主标题（必填）
            subtitle: 副标题
            expression: 人物表情描述，如：思考、惊讶、开心、托腮
            ip_image_path: IP 形象图片路径，默认使用内置图片
            style_ref_path: 风格参考图片路径，默认使用内置图片

        Returns:
            GenerationResult 包含生成的图片路径
        """
        output_path = self.server_config.ensure_output_dir()

        # 使用默认资源图片
        assets_dir = Path(__file__).parent / "assets"
        ip_path = Path(ip_image_path) if ip_image_path else assets_dir / "default_ip.png"
        style_path = Path(style_ref_path) if style_ref_path else assets_dir / "default_style_ref.jpeg"

        # 验证图片存在
        if not ip_path.exists():
            return GenerationResult(
                success=False,
                message=f"IP 形象图片不存在: {ip_path}",
                error="File not found"
            )
        if not style_path.exists():
            return GenerationResult(
                success=False,
                message=f"风格参考图片不存在: {style_path}",
                error="File not found"
            )

        # 加载图片
        style_image = Image.open(style_path)
        ip_image = Image.open(ip_path)

        # 构建提示词
        prompt = f"""参考图片中这些视频的封面制作风格，UP主抠图照片、大字主题（有一定表达风格）、体现主题的背景，绘制一张使用图二人物形象（UP主）的封面图。

要求：
- 人物表现一种{expression}的姿态
- 注意表情也需要契合主题
- 围绕主题确定封面文字表述
- 主题：「{title}」
"""
        if subtitle:
            prompt += f"- 副标题：{subtitle}\n"

        prompt += """- 比例：16:9 横版
- 风格：现代科技博客封面，专业、吸引眼球
- 中文文字必须清晰准确渲染"""

        logger.info(f"Cover prompt: {prompt[:100]}...")

        try:
            # 调用 API - 多参考图：图1=风格参考，图2=IP形象
            response = self._client.models.generate_content(
                model=self._model,
                contents=[
                    "图一（风格参考）：",
                    style_image,
                    "图二（UP主形象）：",
                    ip_image,
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            # 保存生成的图片
            generated_files = self._save_image_from_response(response, output_path, "cover")

            if not generated_files:
                # 获取文本响应
                text_response = None
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        text_response = part.text
                        break

                return GenerationResult(
                    success=False,
                    message="未生成封面图",
                    text=text_response,
                    error="API returned no image data"
                )

            return GenerationResult(
                success=True,
                message=f"封面图已生成",
                images=generated_files,
                prompt_used=prompt
            )

        except Exception as e:
            logger.error(f"Cover generation failed: {e}")
            return GenerationResult(
                success=False,
                message="封面图生成失败",
                error=str(e)
            )

    def edit_image(
        self,
        prompt: str,
        input_image_path: Path,
        output_dir: Optional[Path] = None,
        filename_prefix: str = "edited"
    ) -> GenerationResult:
        """Edit an existing image based on prompt."""
        output_path = output_dir or self.server_config.ensure_output_dir()

        if not input_image_path.exists():
            return GenerationResult(
                success=False,
                message=f"Input image not found: {input_image_path}",
                error="File not found"
            )

        try:
            # Load input image
            input_image = Image.open(input_image_path)

            edit_prompt = f"Edit this image: {prompt}"

            response = self._client.models.generate_content(
                model=self._model,
                contents=[
                    "Original image:",
                    input_image,
                    edit_prompt,
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            generated_files = self._save_image_from_response(response, output_path, filename_prefix)

            if not generated_files:
                # Get text response if no images
                text_response = None
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        text_response = part.text
                        break

                return GenerationResult(
                    success=False,
                    message="No edited images returned",
                    text=text_response,
                    error="API returned no image data"
                )

            return GenerationResult(
                success=True,
                message=f"Edited image saved",
                images=generated_files
            )

        except Exception as e:
            logger.error(f"Image editing failed: {e}")
            return GenerationResult(
                success=False,
                message="Image editing failed",
                error=str(e)
            )

    def chat(self, message: str) -> GenerationResult:
        """Send a chat message to Gemini."""
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=[message],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            generated_files: List[Path] = []
            text_response = None

            # Extract text and images
            for part in response.parts:
                if hasattr(part, 'text') and part.text:
                    text_response = part.text
                elif hasattr(part, 'inline_data') and part.inline_data:
                    output_path = self.server_config.ensure_output_dir()
                    files = self._save_image_from_response(response, output_path, "chat")
                    generated_files.extend(files)
                    break

            return GenerationResult(
                success=True,
                message="Chat response received",
                text=text_response,
                images=generated_files
            )

        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return GenerationResult(
                success=False,
                message="Chat failed",
                error=str(e)
            )


# Convenience function to get a shared client instance
_client_instance: Optional[GeminiAPIClient] = None


def get_client() -> GeminiAPIClient:
    """Get or create a shared client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = GeminiAPIClient()
    return _client_instance
