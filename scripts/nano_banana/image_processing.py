"""Image post-processing utilities."""

import asyncio
import logging
import threading
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Tuple, Literal, Union
from PIL import Image, ImageDraw, ImageFilter
import io
import numpy as np

logger = logging.getLogger(__name__)

# Session cache
_rembg_session = None
_rmbg2_model = None
_session_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="bg_removal")

# Available rembg models with characteristics
REMBG_MODELS = {
    "u2netp": {"size": "4.7MB", "quality": "good", "speed": "fast", "best_for": "general"},
    "u2net": {"size": "176MB", "quality": "excellent", "speed": "slow", "best_for": "complex"},
    "isnet-general-use": {"size": "170MB", "quality": "excellent", "speed": "medium", "best_for": "objects"},
    "isnet-anime": {"size": "170MB", "quality": "excellent", "speed": "medium", "best_for": "anime/icons"},
    "silueta": {"size": "43MB", "quality": "good", "speed": "very fast", "best_for": "silhouettes"},
    "birefnet-general": {"size": "900MB", "quality": "best", "speed": "slow", "best_for": "high-quality"},
}

# Background removal engines
ENGINES = ["rembg", "rmbg2"]

# Default settings
DEFAULT_ENGINE = os.environ.get("BG_REMOVAL_ENGINE", "rembg")
DEFAULT_MODEL = os.environ.get("REMBG_MODEL", "isnet-general-use")

# Platform-specific icon sizes
PLATFORM_SIZES = {
    "ios": [20, 29, 40, 60, 76, 83, 1024],
    "android": [48, 72, 96, 144, 192, 512],
    "web": [16, 32, 180, 192, 512],
    "macos": [16, 32, 64, 128, 256, 512, 1024],
    "all": [16, 20, 29, 32, 40, 48, 60, 64, 72, 76, 83, 96, 128, 144, 180, 192, 256, 512, 1024]
}

# Check available libraries
try:
    from rembg import remove as rembg_remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    new_session = None
    rembg_remove = None

try:
    import torch
    from torchvision import transforms
    from transformers import AutoModelForImageSegmentation
    RMBG2_AVAILABLE = True
except ImportError:
    RMBG2_AVAILABLE = False
    torch = None
    transforms = None
    AutoModelForImageSegmentation = None


def _get_rembg_session(model: str = None):
    """Get or create a reusable rembg session."""
    global _rembg_session
    model = model or DEFAULT_MODEL
    
    with _session_lock:
        if _rembg_session is None and REMBG_AVAILABLE:
            logger.info(f"Creating rembg session with {model} model...")
            try:
                _rembg_session = new_session(model)
                logger.info(f"Rembg session created with {model}")
            except Exception as e:
                logger.warning(f"Failed to load {model}, falling back to u2netp: {e}")
                _rembg_session = new_session("u2netp")
        return _rembg_session


def _get_rmbg2_model():
    """Get or create RMBG 2.0 model (best quality)."""
    global _rmbg2_model
    
    with _session_lock:
        if _rmbg2_model is None and RMBG2_AVAILABLE:
            logger.info("Loading RMBG 2.0 model (briaai/RMBG-2.0)...")
            try:
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                _rmbg2_model = AutoModelForImageSegmentation.from_pretrained(
                    'briaai/RMBG-2.0',
                    trust_remote_code=True
                ).eval().to(device)
                logger.info(f"RMBG 2.0 loaded on {device}")
            except Exception as e:
                logger.error(f"Failed to load RMBG 2.0: {e}")
                _rmbg2_model = None
        return _rmbg2_model


def preload_model(engine: str = None, model: str = None):
    """Pre-load model to avoid cold start delay."""
    engine = engine or DEFAULT_ENGINE
    if engine == "rmbg2" and RMBG2_AVAILABLE:
        _get_rmbg2_model()
    elif REMBG_AVAILABLE:
        _get_rembg_session(model)


async def remove_background(
    image_path: Path, 
    output_path: Optional[Path] = None,
    timeout: float = 120.0,
    engine: Optional[str] = None,
    model: Optional[str] = None,
    alpha_matting: bool = False,
    alpha_matting_foreground_threshold: int = 240,
    alpha_matting_background_threshold: int = 10,
    post_process: bool = True,
) -> Path:
    """
    Remove background from an image with multiple engine options.
    
    Args:
        image_path: Path to input image
        output_path: Optional output path
        timeout: Maximum time in seconds
        engine: 'rembg' (fast) or 'rmbg2' (best quality - BRIA RMBG 2.0)
        model: rembg model (only used if engine='rembg')
        alpha_matting: Enable alpha matting (rembg only)
        post_process: Apply post-processing to clean up edges
    
    Returns:
        Path to processed image
    """
    engine = engine or DEFAULT_ENGINE
    
    # Auto-select best available engine
    if engine == "rmbg2" and not RMBG2_AVAILABLE:
        logger.warning("RMBG 2.0 not available, falling back to rembg")
        engine = "rembg"
    
    if engine == "rembg" and not REMBG_AVAILABLE:
        raise RuntimeError(
            "No background removal library available. "
            "Install with: pip install rembg[cpu] or pip install transformers torch"
        )
    
    if output_path is None:
        output_path = image_path.parent / f"{image_path.stem}_nobg.png"
    
    loop = asyncio.get_running_loop()
    try:
        await asyncio.wait_for(
            loop.run_in_executor(
                _executor, 
                _remove_bg_sync, 
                image_path, 
                output_path,
                engine,
                model,
                alpha_matting,
                alpha_matting_foreground_threshold,
                alpha_matting_background_threshold,
                post_process
            ),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        logger.error(f"Background removal timed out after {timeout}s")
        raise RuntimeError(f"Background removal timed out after {timeout} seconds")
    
    return output_path


def _remove_bg_sync(
    input_path: Path, 
    output_path: Path,
    engine: str = "rembg",
    model: Optional[str] = None,
    alpha_matting: bool = False,
    fg_threshold: int = 240,
    bg_threshold: int = 10,
    post_process: bool = True
):
    """Synchronous background removal with multiple engines."""
    
    if engine == "rmbg2" and RMBG2_AVAILABLE:
        output_image = _remove_bg_rmbg2(input_path)
    else:
        output_image = _remove_bg_rembg(
            input_path, model, alpha_matting, fg_threshold, bg_threshold
        )
    
    # Post-processing
    if post_process and output_image:
        output_image = _post_process_alpha(output_image)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_image.save(output_path, "PNG", optimize=True)


def _remove_bg_rmbg2(input_path: Path) -> Image.Image:
    """Remove background using BRIA RMBG 2.0 (best quality)."""
    model = _get_rmbg2_model()
    if model is None:
        raise RuntimeError("RMBG 2.0 model failed to load")
    
    device = next(model.parameters()).device
    
    # Prepare image
    image = Image.open(input_path).convert("RGB")
    original_size = image.size
    
    # Transform
    transform_image = transforms.Compose([
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    input_tensor = transform_image(image).unsqueeze(0).to(device)
    
    # Inference
    with torch.no_grad():
        preds = model(input_tensor)[-1].sigmoid().cpu()
    
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(original_size, Image.Resampling.LANCZOS)
    
    # Apply mask
    image = Image.open(input_path).convert("RGBA")
    image.putalpha(mask)
    
    return image


def _remove_bg_rembg(
    input_path: Path,
    model: Optional[str] = None,
    alpha_matting: bool = False,
    fg_threshold: int = 240,
    bg_threshold: int = 10
) -> Image.Image:
    """Remove background using rembg library."""
    session = _get_rembg_session(model)
    
    input_image = Image.open(input_path)
    original_size = input_image.size
    
    # Optimize: resize large images
    max_size = 1024
    resized = False
    if max(original_size) > max_size:
        ratio = max_size / max(original_size)
        new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
        input_image = input_image.resize(new_size, Image.Resampling.LANCZOS)
        resized = True
    
    if input_image.mode != 'RGBA':
        input_image = input_image.convert('RGBA')
    
    output_image = rembg_remove(
        input_image, 
        session=session,
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=fg_threshold,
        alpha_matting_background_threshold=bg_threshold,
    )
    
    if resized:
        output_image = output_image.resize(original_size, Image.Resampling.LANCZOS)
    
    return output_image


def _post_process_alpha(image: Image.Image) -> Image.Image:
    """Post-process alpha channel for cleaner edges."""
    if image.mode != 'RGBA':
        return image
    
    r, g, b, a = image.split()
    a_np = np.array(a)
    
    # Clean up noise
    a_np = np.where(a_np < 20, 0, a_np)
    a_np = np.where(a_np > 235, 255, a_np)
    
    a_clean = Image.fromarray(a_np.astype(np.uint8))
    a_clean = a_clean.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return Image.merge('RGBA', (r, g, b, a_clean))


async def resize_image(
    image_path: Path,
    size: tuple[int, int],
    output_path: Optional[Path] = None,
    keep_aspect: bool = True
) -> Path:
    """
    Resize an image.
    
    Args:
        image_path: Path to input image
        size: Target size (width, height)
        output_path: Optional output path
        keep_aspect: Whether to maintain aspect ratio
    
    Returns:
        Path to resized image
    """
    if output_path is None:
        output_path = image_path.parent / f"{image_path.stem}_resized{image_path.suffix}"
    
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _resize_sync, image_path, size, output_path, keep_aspect)
    
    return output_path


def _resize_sync(input_path: Path, size: tuple[int, int], output_path: Path, keep_aspect: bool):
    """Synchronous image resize."""
    image = Image.open(input_path)
    
    if keep_aspect:
        image.thumbnail(size, Image.Resampling.LANCZOS)
    else:
        image = image.resize(size, Image.Resampling.LANCZOS)
    
    image.save(output_path)


async def generate_icon_sizes(
    input_path: Path,
    sizes: list[int],
    remove_bg: bool = True,
    output_dir: Optional[Path] = None,
    timeout: float = 60.0,
    shape: str = "squircle",
    platform: Optional[str] = None
) -> list[Path]:
    """
    Generate multiple icon sizes from a single image.
    
    Args:
        input_path: Path to input image
        sizes: List of icon sizes (e.g., [16, 32, 64, 128, 256, 512])
        remove_bg: Whether to remove background first
        output_dir: Output directory (defaults to input directory)
        timeout: Maximum time for background removal
        shape: Icon shape mask (rounded, squircle, circle, square)
        platform: Platform preset (ios, android, web, macos, all)
    
    Returns:
        List of paths to generated icons
    """
    if output_dir is None:
        output_dir = input_path.parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get sizes from platform preset if specified
    if platform and platform in PLATFORM_SIZES:
        sizes = PLATFORM_SIZES[platform]
    
    # Remove background if requested
    source_image = input_path
    if remove_bg and REMBG_AVAILABLE:
        try:
            logger.info(f"Removing background from {input_path}")
            source_image = await remove_background(input_path, timeout=timeout)
            logger.info(f"Background removed successfully: {source_image}")
        except Exception as e:
            logger.warning(f"Background removal failed: {e}, using original image")
            source_image = input_path
    elif remove_bg and not REMBG_AVAILABLE:
        logger.warning("rembg not available, skipping background removal")
    
    # Generate all sizes with shape mask
    output_paths = []
    for size in sizes:
        output_path = output_dir / f"{input_path.stem}_{size}x{size}.png"
        await resize_image(source_image, (size, size), output_path, keep_aspect=False)
        
        # Apply shape mask
        if shape and shape != "square":
            apply_shape_mask(output_path, shape)
        
        output_paths.append(output_path)
    
    return output_paths


def apply_shape_mask(image_path: Path, shape: str = "squircle"):
    """Apply shape mask to icon (rounded, squircle, circle)."""
    img = Image.open(image_path).convert("RGBA")
    size = img.size[0]
    
    # Create mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    if shape == "circle":
        draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    elif shape == "rounded":
        radius = size // 6
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    elif shape == "squircle":
        # iOS-style superellipse approximation
        radius = size // 4
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    
    # Apply mask
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    output.save(image_path, "PNG")


def parse_background_color(color_str: str) -> Tuple[int, int, int, int]:
    """Parse background color string to RGBA tuple."""
    if not color_str:
        return (0, 0, 0, 0)  # Transparent
    
    color_str = color_str.lower().strip()
    
    # Named colors
    named_colors = {
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "red": (255, 0, 0, 255),
        "green": (0, 255, 0, 255),
        "blue": (0, 0, 255, 255),
        "transparent": (0, 0, 0, 0),
    }
    
    if color_str in named_colors:
        return named_colors[color_str]
    
    # Hex color
    if color_str.startswith("#"):
        hex_color = color_str[1:]
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            return (r, g, b, a)
    
    return (0, 0, 0, 0)


async def add_background_to_icon(
    image_path: Path,
    background_color: str,
    output_path: Optional[Path] = None
) -> Path:
    """Add solid background color to transparent icon."""
    if output_path is None:
        output_path = image_path.parent / f"{image_path.stem}_bg.png"
    
    img = Image.open(image_path).convert("RGBA")
    color = parse_background_color(background_color)
    
    # Create background
    background = Image.new("RGBA", img.size, color)
    
    # Composite
    result = Image.alpha_composite(background, img)
    result.save(output_path, "PNG")
    
    return output_path
