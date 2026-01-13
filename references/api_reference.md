# Nano Banana API Reference

## GeminiAPIClient

Core client for image generation.

### Methods

#### generate_image(prompt, aspect_ratio, ...)

Generate a general-purpose image.

**Parameters:**
- `prompt` (str): Image description
- `aspect_ratio` (str): "1:1", "16:9", "9:16", "4:3", "3:4" (default: "1:1")
- `style` (str, optional): Art style
- `count` (int): Number of images (default: 1)

**Returns:** `GenerationResult`

---

#### generate_social_post(description, platform, style)

Generate social media post image.

**Parameters:**
- `description` (str): Content description
- `platform` (str): "instagram", "twitter", "youtube", "linkedin"
- `style` (str): Visual style (default: "modern")

**Returns:** `GenerationResult`

---

#### generate_thumbnail(title, style)

Generate YouTube thumbnail.

**Parameters:**
- `title` (str): Video title
- `style` (str): Visual style (default: "cinematic")

**Returns:** `GenerationResult` (16:9 aspect ratio)

---

#### generate_cover(title, subtitle, expression, ip_image_path, style_ref_path)

Generate blog/WeChat cover with Chinese text support.

**Parameters:**
- `title` (str): Main title (required)
- `subtitle` (str): Subtitle (optional)
- `expression` (str): Character expression - "思考", "惊讶", "开心", "托腮"
- `ip_image_path` (Path, optional): Custom IP character image
- `style_ref_path` (Path, optional): Style reference image

**Returns:** `GenerationResult` (16:9 aspect ratio)

---

#### generate_app_icon(description, style, remove_background, platform)

Generate app icon.

**Parameters:**
- `description` (str): App description
- `style` (str): "modern", "flat-design", "3d", "minimal", "gradient", "glassmorphism"
- `remove_background` (bool): Remove background (default: True)
- `platform` (str, optional): "ios" or "android" for size presets

**Returns:** `GenerationResult` (square)

---

#### generate_banner(description, style, aspect_ratio)

Generate wide banner.

**Parameters:**
- `description` (str): Banner content
- `style` (str): Visual style
- `aspect_ratio` (str): "16:9" or "21:9"

**Returns:** `GenerationResult`

---

## GenerationResult

Result object returned by all generation methods.

**Attributes:**
- `success` (bool): Whether generation succeeded
- `message` (str): Status message
- `images` (List[Path]): List of generated image paths
- `error` (str, optional): Error message if failed
- `prompt_used` (str, optional): The enhanced prompt used

---

## Aspect Ratios

| Value | Dimensions | Use Case |
|-------|------------|----------|
| `1:1` | 1024x1024 | Social posts, avatars, icons |
| `16:9` | 1664x928 | YouTube, banners, widescreen |
| `9:16` | 928x1664 | Stories, reels, mobile |
| `4:3` | 1472x1140 | Presentations |
| `3:4` | 1140x1472 | Product photos, portraits |
| `21:9` | 1792x768 | Ultra-wide banners |

---

## Image Styles

Common styles supported:
- `photorealistic` - Photo-like quality
- `cinematic` - Movie-style lighting
- `modern` - Clean contemporary look
- `minimalist` - Simple, clean
- `flat-design` - 2D flat graphics
- `3d-render` - 3D rendered
- `anime` - Anime style
- `watercolor` - Watercolor painting
- `digital-art` - Digital illustration

See `scripts/nano_banana/types.py` for full list.

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | - | Gemini API key |
| `NANOBANANA_OUTPUT_DIR` | No | `./nanobanana-output` | Output directory |
| `NANOBANANA_MODEL` | No | `gemini-3-pro-image-preview` | Model to use |
