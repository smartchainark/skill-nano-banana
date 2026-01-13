# Nano Banana

> Fast image generation via Gemini API for Claude Code

[English](#english) | [中文](#中文)

---

## English

### What is Nano Banana?

A Claude Code skill that generates images using Google's Gemini API. Optimized presets for:
- General images
- Social media posts (Instagram, Twitter, YouTube, LinkedIn)
- YouTube thumbnails
- Blog/WeChat covers (with Chinese text support)
- App icons
- Banners

### Quick Start

1. **Clone to Claude Code skills directory:**
   ```bash
   cd ~/.claude/skills
   git clone https://github.com/smartchainark/skill-nano-banana.git nano-banana
   ```

2. **Set API key:**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   Get key from: https://aistudio.google.com/apikey

3. **Use in Claude Code:**
   Say "生成图片" or "nano banana" to trigger the skill.

### Usage

```bash
# General image
python scripts/run.py generate.py image "A cute robot in space"

# YouTube thumbnail
python scripts/run.py generate.py thumbnail "10 Python Tips"

# Blog cover (Chinese)
python scripts/run.py generate.py cover "Claude Code 指南" --subtitle "入门到精通"

# App icon
python scripts/run.py generate.py icon "Music app" --style flat-design

# Social media
python scripts/run.py generate.py social "AI tips" --platform youtube
```

### Features

| Command | Purpose | Output |
|---------|---------|--------|
| `image` | General image | Any aspect ratio |
| `social` | Social media post | Platform-optimized |
| `thumbnail` | YouTube thumbnail | 16:9 |
| `cover` | Blog cover | 16:9 with Chinese text |
| `icon` | App icon | Square |
| `banner` | Wide banner | 16:9 or 21:9 |

### Examples

| YouTube Thumbnail | Blog Cover |
|-------------------|------------|
| ![thumbnail](images/thumbnail_0_0.png) | ![cover](images/cover_0.png) |

| Social Media Post | App Icon |
|-------------------|----------|
| ![social](images/social-post_0_0.png) | ![icon](images/app-icon_0_0.png) |

### vs Other Skills

| Skill | Speed | Cost | Chinese Text |
|-------|-------|------|--------------|
| nano-banana | Fast (5-10s) | API Key | Via thinking mode |
| agent-image-generator | Slow (20-40s) | Free | Native |

---

## 中文

### Nano Banana 是什么？

一个使用 Google Gemini API 生成图片的 Claude Code 技能。支持：
- 通用图片生成
- 社交媒体配图（Instagram、Twitter、YouTube、LinkedIn）
- YouTube 缩略图
- 博客/公众号封面（支持中文）
- App 图标
- 横幅

### 快速开始

1. **克隆到 Claude Code 技能目录：**
   ```bash
   cd ~/.claude/skills
   git clone https://github.com/smartchainark/skill-nano-banana.git nano-banana
   ```

2. **设置 API Key：**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   获取地址：https://aistudio.google.com/apikey

3. **在 Claude Code 中使用：**
   说 "生成图片" 或 "nano banana" 即可触发技能。

### 使用示例

```bash
# 通用图片
python scripts/run.py generate.py image "太空中的可爱机器人"

# YouTube 缩略图
python scripts/run.py generate.py thumbnail "10个Python技巧"

# 博客封面
python scripts/run.py generate.py cover "Claude Code 指南" --subtitle "入门到精通"

# App 图标
python scripts/run.py generate.py icon "音乐应用" --style flat-design

# 社交媒体
python scripts/run.py generate.py social "AI技巧分享" --platform youtube
```

### 功能对比

| 命令 | 用途 | 输出 |
|------|------|------|
| `image` | 通用图片 | 任意比例 |
| `social` | 社交媒体 | 平台优化 |
| `thumbnail` | YouTube 缩略图 | 16:9 |
| `cover` | 博客封面 | 16:9 带中文 |
| `icon` | App 图标 | 正方形 |
| `banner` | 横幅 | 16:9 或 21:9 |

### 效果展示

| YouTube 缩略图 | 博客封面 |
|----------------|----------|
| ![thumbnail](images/thumbnail_0_0.png) | ![cover](images/cover_0.png) |

| 社交媒体配图 | App 图标 |
|--------------|----------|
| ![social](images/social-post_0_0.png) | ![icon](images/app-icon_0_0.png) |

### 与其他技能对比

| 技能 | 速度 | 成本 | 中文支持 |
|------|------|------|----------|
| nano-banana | 快 (5-10s) | 需 API Key | 思考模式 |
| agent-image-generator | 慢 (20-40s) | 免费 | 原生支持 |

---

## License

MIT License - See [LICENSE](LICENSE) for details.
