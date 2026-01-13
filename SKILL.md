---
name: nano-banana
description: |
  This skill should be used when the user asks to "生成图片", "生成封面",
  "生成配图", "生成缩略图", "nano banana", or "API 生图".
  Provides fast image generation via Gemini API for social posts, thumbnails,
  blog covers, app icons, and banners. Faster than browser-based alternatives
  but requires GOOGLE_API_KEY environment variable.
---

# Nano Banana - Gemini API Image Generation

Generate images via Gemini API with optimized presets for common use cases.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# CORRECT - Always use run.py:
python scripts/run.py generate.py image "A cute robot"
python scripts/run.py generate.py cover "Blog Title"

# WRONG - Never call directly (may fail without venv):
python scripts/generate.py image "..."
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Executes script with correct environment

## Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `image` | General image | `generate.py image "A cute robot"` |
| `social` | Social media post | `generate.py social "AI tips" --platform youtube` |
| `thumbnail` | YouTube thumbnail | `generate.py thumbnail "10 Python Tips"` |
| `cover` | Blog/WeChat cover | `generate.py cover "Title" --subtitle "Subtitle"` |
| `icon` | App icon | `generate.py icon "Music app" --style flat-design` |
| `banner` | Wide banner | `generate.py banner "Welcome" --aspect-ratio 16:9` |

## Usage Examples

### General Image
```bash
python scripts/run.py generate.py image "A futuristic city at sunset" --aspect-ratio 16:9
```

### Social Media Post
```bash
python scripts/run.py generate.py social "AI productivity tips" --platform youtube --style modern
```

### YouTube Thumbnail
```bash
python scripts/run.py generate.py thumbnail "10 Python Tips You Must Know" --style cinematic
```

### Blog/WeChat Cover (Chinese Support)
```bash
python scripts/run.py generate.py cover "Claude Code 升级指南" --subtitle "踩坑总结" --expression "思考"
```

Expression options: 思考 (thinking), 惊讶 (surprised), 开心 (happy), 托腮 (chin rest)

### App Icon
```bash
python scripts/run.py generate.py icon "Music streaming app" --style flat-design
```

Style options: modern, flat-design, 3d, minimal

### Banner
```bash
python scripts/run.py generate.py banner "Welcome to my channel" --aspect-ratio 16:9
```

## Environment Setup

Required environment variable:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

Get API key from: https://aistudio.google.com/apikey

## Output

Generated images saved to `./nanobanana-output/` directory.
File naming format: `{type}_{index}.png`

## Comparison with Other Skills

| Skill | Method | Speed | Cost | Chinese Text |
|-------|--------|-------|------|--------------|
| nano-banana | Gemini API | Fast (5-10s) | Requires API Key | Via thinking mode |
| agent-image-generator | Playwright browser | Slow (20-40s) | Free | Native support |

**Recommendation:**
- Fast batch generation → nano-banana
- Free with Chinese text → agent-image-generator
- Blog covers only → nano-banana `cover` command

## Script Reference

### generate.py

Full command syntax:

```bash
# image
python scripts/run.py generate.py image <prompt> [--aspect-ratio 1:1|16:9|9:16|4:3|3:4] [--output PATH]

# social
python scripts/run.py generate.py social <description> [--platform instagram|twitter|youtube|linkedin] [--style STYLE] [--output PATH]

# thumbnail
python scripts/run.py generate.py thumbnail <title> [--style STYLE] [--output PATH]

# cover
python scripts/run.py generate.py cover <title> [--subtitle TEXT] [--expression TEXT] [--output PATH]

# icon
python scripts/run.py generate.py icon <description> [--style modern|flat-design|3d|minimal] [--output PATH]

# banner
python scripts/run.py generate.py banner <description> [--style STYLE] [--aspect-ratio RATIO] [--output PATH]
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Missing API key | Set `GOOGLE_API_KEY` environment variable |
| Rate limit | Wait or check API quota |
| Image not generated | Check error message, verify prompt |

## Resources

- `scripts/nano_banana/` - Core library code
- `scripts/nano_banana/assets/` - Reference images for cover generation
- `references/api_reference.md` - Detailed API documentation
