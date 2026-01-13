"""Enhanced prompt templates for professional image generation.

Based on:
- Google's Gemini 2.5 Flash Image prompting guide
- Professional photography techniques (camera angles, lighting, composition)
- UI/UX design principles (Apple HIG, Material Design)
- Art direction and cinematography terminology
- Fine art movements and techniques
"""

from typing import Optional
from .types import (
    ImageRequest, ImagePurpose, ImageStyle, AspectRatio,
    CameraAngle, ShotType, LightingType, CompositionRule,
    TimeOfDay, Weather, Material, ArtMovement, ColorScheme, Mood,
    CameraType, LensType
)


class PromptBuilder:
    """Build optimized prompts for different image generation purposes."""
    
    # ============================================================
    # PURPOSE-SPECIFIC TEMPLATES
    # ============================================================
    
    TEMPLATES = {
        ImagePurpose.APP_ICON: {
            "prefix": "",
            "suffix": """Professional app icon design in {style} style. 
Create a single, centered iconic symbol with clean minimal design and perfect symmetry. 
The icon should feature smooth gradients, ultra crisp edges, and vector-like quality. 
Design for 1024x1024 resolution, optimized for Apple iOS App Store and Google Play Store. 
Use a solid color or subtle gradient background. 
The silhouette must be highly recognizable at small sizes (29x29 pixels). 
Employ flat design principles with bold shapes, no unnecessary details, consistent stroke weight. 
The icon should have emotional connection and be immediately identifiable.""",
            "default_style": ImageStyle.FLAT_DESIGN,
            "negative": "blurry, text, words, letters, typography, complex background, realistic photo, multiple objects, cluttered, low resolution, pixelated, busy design, 3D shadows, drop shadows, thin lines, intricate details"
        },
        
        ImagePurpose.FAVICON: {
            "prefix": "",
            "suffix": """Favicon icon design in {style} style. 
Create an extremely simple, bold symbol recognizable at 16x16 pixels. 
Use minimal details with high contrast, single focal point, and distinct shapes. 
The design must be readable at tiny sizes with clear silhouette. 
Employ thick strokes, solid fills, and maximum 2-3 colors.""",
            "default_style": ImageStyle.MINIMALIST,
            "negative": "complex, detailed, text, realistic, many elements, thin lines, gradients, shadows"
        },
        
        ImagePurpose.LOGO: {
            "prefix": "",
            "suffix": """Professional logo design in {style} style. 
Create a memorable, unique brand mark with clean lines and balanced composition. 
The logo must work on any background (light or dark) and scale from favicon to billboard. 
Design with timeless aesthetic, avoiding trendy effects. 
Use strategic negative space, harmonious proportions, and intentional color choices. 
Consider monochrome and reversed versions.""",
            "default_style": ImageStyle.MODERN,
            "negative": "busy, complex, realistic photo, too many colors, trendy effects, clip art, generic"
        },
        
        ImagePurpose.BANNER: {
            "prefix": "",
            "suffix": """Professional banner design in {style} style for {aspect_hint}. 
Create a wide composition with clear visual hierarchy and attention-grabbing focal point. 
Design with strategic negative space for text overlay on left or right third. 
Use dramatic lighting with cinematic atmosphere. 
Employ rule of thirds, leading lines, and depth layers (foreground, midground, background). 
The design should work as hero image with space for headline and CTA.""",
            "default_style": ImageStyle.CINEMATIC,
            "negative": "cluttered, centered subject blocking text space, low contrast, busy patterns"
        },
        
        ImagePurpose.THUMBNAIL: {
            "prefix": "",
            "suffix": """Eye-catching thumbnail in {style} style for YouTube/video content. 
Create a scroll-stopping composition with high contrast, vibrant saturated colors. 
Use dramatic rim lighting and chiaroscuro to make the subject pop. 
Design for immediate recognition at small sizes - bold shapes, exaggerated expressions, dynamic angles. 
Employ cinematic color grading (teal-orange, complementary colors). 
Include one dominant element that draws the eye within 0.5 seconds.""",
            "default_style": ImageStyle.CINEMATIC,
            "negative": "boring, low contrast, unclear subject, muted colors, static pose, cluttered"
        },
        
        ImagePurpose.PRODUCT: {
            "prefix": "",
            "suffix": """Professional product photography in {style} style. 
Create a high-resolution studio shot with three-point softbox lighting. 
Soft diffused highlights, minimal harsh shadows, 45-degree elevated camera angle. 
Position product on clean neutral background (white, gray gradient, marble, concrete). 
Ultra-sharp focus on product details with subtle depth of field. 
Soft reflections on surfaces, realistic materials, commercial e-commerce quality.""",
            "default_style": ImageStyle.STUDIO,
            "negative": "messy background, harsh shadows, poor lighting, amateur, distorted, unrealistic"
        },
        
        ImagePurpose.SOCIAL_POST: {
            "prefix": "",
            "suffix": """Engaging social media post image in {style} style. 
Create a scroll-stopping visual optimized for Instagram/Facebook feeds. 
Modern aesthetic, engaging composition, instantly shareable quality. 
Vibrant trending color palette with high saturation for feed impact. 
Visual breathing room, works in square and portrait crops. 
Evoke emotion, tell a micro-story, encourage engagement.""",
            "default_style": ImageStyle.MODERN,
            "negative": "boring, low quality, pixelated, dated aesthetic, muted colors"
        },
        
        ImagePurpose.STORY: {
            "prefix": "",
            "suffix": """Vertical story format image in {style} style for Instagram/TikTok. 
Mobile-first design for 9:16 vertical composition. 
Keep top 15% and bottom 20% clear for platform UI. 
Dynamic engaging visual capturing attention in first second. 
Bold colors, modern aesthetic, space for text overlays and stickers. 
Guide the eye vertically through the frame.""",
            "default_style": ImageStyle.MODERN,
            "negative": "horizontal, desktop-oriented, important content at edges, static"
        },
        
        ImagePurpose.HERO_IMAGE: {
            "prefix": "",
            "suffix": """Impactful website hero image in {style} style for {aspect_hint}. 
Wide-format visually stunning composition for above-the-fold placement. 
Significant negative space (left or right third) for headline text overlay. 
Cinematic lighting with atmospheric depth, dramatic gradients. 
Clear focal point that doesn't compete with overlaid text. 
Colors complement typical web UI (dark text on light, white on dark). 
Aspirational, professional mood aligned with brand storytelling.""",
            "default_style": ImageStyle.CINEMATIC,
            "negative": "cluttered center, no breathing room, competing focal points, harsh colors"
        },
        
        ImagePurpose.ILLUSTRATION: {
            "prefix": "",
            "suffix": """Artistic illustration in {style} style with expressive visual language. 
Unique illustration with intentional artistic choices in color, form, composition. 
Stylized rendering distinguishing from photography. 
Thoughtful color palette (complementary, analogous, or split-complementary). 
Clear visual hierarchy, balanced composition, emotional resonance. 
Consistent style throughout with harmonious line weights and fills.""",
            "default_style": ImageStyle.DIGITAL_ART,
            "negative": "photorealistic, stock photo look, inconsistent style, no focal point"
        },
        
        ImagePurpose.DIAGRAM: {
            "prefix": "",
            "suffix": """Technical diagram illustration in {style} style. 
Clear organized visual with logical hierarchy and clean connecting lines. 
Consistent iconography, aligned elements, strategic color coding. 
Generous whitespace, readable labels, clear flow direction. 
Visual grouping of related elements, professional documentation style. 
Flat design with minimal decorative elements.""",
            "default_style": ImageStyle.FLAT_DESIGN,
            "negative": "messy, unclear connections, artistic flourishes, overlapping, poor alignment"
        },
        
        ImagePurpose.PATTERN: {
            "prefix": "",
            "suffix": """Seamless tileable pattern in {style} style. 
Perfectly repeating design with no visible seams at tile edges. 
Balanced distribution of elements without clustering. 
Harmonious color palette with good contrast. 
Works at various scales. Rhythmic repetition with subtle variations.""",
            "default_style": ImageStyle.ABSTRACT,
            "negative": "non-repeating, visible edges, obvious seams, unbalanced, jarring"
        },
        
        ImagePurpose.AVATAR: {
            "prefix": "",
            "suffix": """Profile avatar image in {style} style for circular crop. 
Centered composition working in circular frame. 
Memorable, distinctive, recognizable at 32x32 pixels. 
Clear contrast between subject and background. 
Convey personality while remaining professional. 
Balanced lighting without harsh shadows.""",
            "default_style": ImageStyle.MODERN,
            "negative": "off-center, cropped poorly, busy background, forgettable"
        },
        
        ImagePurpose.MOCKUP: {
            "prefix": "",
            "suffix": """Professional product mockup in {style} style. 
Realistic scene showcasing product in context with authentic environment. 
Photorealistic rendering with accurate materials, lighting, reflections. 
Aspirational lifestyle setting elevating perceived value. 
Environmental storytelling with props and surfaces suggesting use case. 
Natural unforced composition like editorial photography.""",
            "default_style": ImageStyle.PHOTOREALISTIC,
            "negative": "fake looking, unrealistic lighting, floating objects, plastic, generic"
        },
        
        ImagePurpose.PORTRAIT: {
            "prefix": "",
            "suffix": """Professional portrait photography in {style} style. 
Flattering lighting with attention to facial features and skin texture. 
Natural skin tones, catch lights in eyes, dimensional lighting. 
Pleasing background separation with appropriate depth of field. 
Authentic expression capturing personality and emotion. 
85mm portrait lens equivalent with soft bokeh.""",
            "default_style": ImageStyle.PHOTOREALISTIC,
            "negative": "unflattering angle, harsh shadows on face, dead eyes, plastic skin, overprocessed"
        },
        
        ImagePurpose.LANDSCAPE: {
            "prefix": "",
            "suffix": """Stunning landscape photography in {style} style. 
Dramatic natural scenery with strong composition. 
Epic scale, atmospheric depth, compelling foreground interest. 
Dynamic sky, balanced exposure between land and sky. 
Sharp focus throughout with deep depth of field. 
Golden hour or blue hour lighting for maximum impact.""",
            "default_style": ImageStyle.PHOTOREALISTIC,
            "negative": "flat lighting, boring composition, no focal point, overexposed sky"
        },
        
        ImagePurpose.ARCHITECTURE: {
            "prefix": "",
            "suffix": """Professional architectural photography in {style} style. 
Clean lines, precise geometry, balanced perspective. 
Corrected verticals (no keystoning), symmetrical framing. 
Dramatic lighting emphasizing form and texture. 
Blue hour exterior or controlled interior lighting. 
Wide-angle perspective with minimal distortion.""",
            "default_style": ImageStyle.PHOTOREALISTIC,
            "negative": "distorted perspective, tilted verticals, cluttered, poor lighting"
        },
        
        ImagePurpose.FOOD: {
            "prefix": "",
            "suffix": """Appetizing food photography in {style} style. 
Mouthwatering presentation with fresh, vibrant colors. 
Natural or styled lighting from 45-degree angle. 
Shallow depth of field with hero item in sharp focus. 
Thoughtful props and garnishes enhancing composition. 
Textures visible, steam or moisture where appropriate.""",
            "default_style": ImageStyle.PHOTOREALISTIC,
            "negative": "unappetizing, cold looking, flat lighting, messy plating, dull colors"
        },
        
        ImagePurpose.FASHION: {
            "prefix": "",
            "suffix": """High-end fashion photography in {style} style. 
Editorial quality with dramatic poses and styling. 
Professional beauty lighting flattering model and garments. 
Strong composition with intentional negative space. 
Fabric textures visible, colors accurate. 
Aspirational mood aligned with brand aesthetic.""",
            "default_style": ImageStyle.FASHION,
            "negative": "amateur poses, poor fit, unflattering angles, cheap looking"
        },
        
        ImagePurpose.EDITORIAL: {
            "prefix": "",
            "suffix": """Magazine-quality editorial photography in {style} style. 
Storytelling composition with conceptual depth. 
Professional lighting, intentional styling, purposeful framing. 
Captures a moment or narrative beyond surface aesthetics. 
Print-ready quality with room for magazine text layouts.""",
            "default_style": ImageStyle.EDITORIAL,
            "negative": "generic, stock photo look, no narrative, poor composition"
        },
    }
    
    # ============================================================
    # STYLE MODIFIERS
    # ============================================================
    
    STYLE_MODIFIERS = {
        # Photography
        ImageStyle.PHOTOREALISTIC: "photorealistic, ultra realistic, 8K UHD, professional DSLR quality, RAW photo, accurate colors, natural textures, physically accurate lighting",
        ImageStyle.STUDIO: "professional studio photography, three-point lighting, softbox diffusion, neutral background, commercial quality, rim lighting separation",
        ImageStyle.CINEMATIC: "cinematic film quality, Hollywood production value, dramatic theatrical lighting, widescreen composition, film color grading, anamorphic lens, epic scope",
        ImageStyle.EDITORIAL: "editorial magazine quality, intentional artistic direction, storytelling composition, professional styling, high fashion aesthetic",
        ImageStyle.DOCUMENTARY: "documentary photography style, candid authentic moments, natural lighting, unstaged genuine emotion, photojournalistic approach",
        ImageStyle.FASHION: "high fashion photography, editorial quality, beauty lighting, designer aesthetic, model poses, aspirational luxury",
        
        # Traditional art
        ImageStyle.WATERCOLOR: "traditional watercolor painting, soft bleeding edges, transparent washes, visible paper texture, wet-on-wet technique, organic blending",
        ImageStyle.OIL_PAINTING: "classical oil painting, textured impasto brushstrokes, rich pigmented colors, canvas weave, painterly depth, old master technique",
        ImageStyle.ACRYLIC: "acrylic painting, bold colors, quick brushwork, versatile textures, contemporary art style",
        ImageStyle.SKETCH: "hand-drawn pencil sketch, graphite on paper, varied line weights, cross-hatching shadows, expressive strokes",
        ImageStyle.CHARCOAL: "charcoal drawing, rich blacks, expressive smudging, dramatic contrast, fine art quality",
        ImageStyle.INK_WASH: "ink wash painting, sumi-e style, flowing brushwork, gradual tonal values, East Asian aesthetic",
        ImageStyle.PASTEL: "soft pastel artwork, chalky texture, gentle blending, luminous colors, impressionistic quality",
        ImageStyle.GOUACHE: "gouache illustration, matte finish, opaque colors, flat color fields, vintage illustration style",
        
        # Digital art
        ImageStyle.DIGITAL_ART: "digital art, clean rendering, vibrant colors, professional illustration, modern digital painting",
        ImageStyle.CONCEPT_ART: "concept art, entertainment design, environmental storytelling, professional production quality",
        ImageStyle.MATTE_PAINTING: "digital matte painting, cinematic environment, photorealistic compositing, epic scale landscapes",
        ImageStyle.PIXEL_ART: "pixel art, retro 8-bit/16-bit aesthetic, limited color palette, deliberate pixelation, nostalgic gaming",
        ImageStyle.VOXEL: "voxel art, 3D pixel aesthetic, blocky forms, colorful cubic design, Minecraft-inspired",
        ImageStyle.LOW_POLY: "low poly 3D art, geometric faceted surfaces, minimal polygons, modern stylized aesthetic",
        
        # Illustration
        ImageStyle.ANIME: "anime style, Japanese animation aesthetic, cel-shaded, expressive features, vibrant colors, clean line art",
        ImageStyle.MANGA: "manga style, black and white, dynamic panel composition, expressive ink work, Japanese comic aesthetic",
        ImageStyle.COMIC_BOOK: "comic book art, bold outlines, dynamic action, halftone dots, superhero aesthetic",
        ImageStyle.CARTOON: "cartoon style, exaggerated features, bold colors, playful design, animated aesthetic",
        ImageStyle.CHILDRENS_BOOK: "children's book illustration, whimsical, friendly characters, soft colors, storybook quality",
        ImageStyle.STORYBOOK: "storybook illustration, fairy tale aesthetic, magical atmosphere, detailed backgrounds",
        
        # Design styles
        ImageStyle.MODERN: "contemporary modern design, clean minimalist aesthetic, current trends, sleek styling, refined palette",
        ImageStyle.MINIMALIST: "minimalist design, essential elements only, maximum negative space, intentional simplicity",
        ImageStyle.FLAT_DESIGN: "flat design, 2D graphic style, no shadows, bold solid colors, geometric shapes, vector illustration",
        ImageStyle.MATERIAL_DESIGN: "Material Design style, layered surfaces, subtle shadows, Google design language",
        ImageStyle.GLASSMORPHISM: "glassmorphism design, frosted glass effect, transparency, blur, modern UI aesthetic",
        ImageStyle.NEUMORPHISM: "neumorphism design, soft shadows, extruded elements, subtle 3D effect",
        ImageStyle.BRUTALIST: "brutalist design, raw concrete aesthetic, bold typography, stark minimalism",
        
        # 3D
        ImageStyle.THREE_D_RENDER: "3D CGI render, photorealistic ray tracing, subsurface scattering, ambient occlusion, global illumination",
        ImageStyle.ISOMETRIC: "isometric 3D perspective, 30-degree angles, technical illustration, geometric precision",
        ImageStyle.CLAY_RENDER: "clay render, smooth matte surfaces, soft studio lighting, sculptural forms",
        ImageStyle.WIREFRAME: "wireframe render, technical visualization, geometric mesh, blueprint aesthetic",
        
        # Aesthetic
        ImageStyle.VINTAGE: "vintage retro aesthetic, nostalgic color grading, film grain, faded tones, analog warmth",
        ImageStyle.RETRO: "retro design, throwback aesthetic, period-specific styling, nostalgic elements",
        ImageStyle.ABSTRACT: "abstract art, non-representational forms, expressive shapes, bold color fields",
        ImageStyle.SURREAL: "surrealist art, dreamlike imagery, impossible scenes, subconscious symbolism",
        ImageStyle.PSYCHEDELIC: "psychedelic art, vibrant swirling colors, trippy patterns, 1960s aesthetic",
        ImageStyle.VAPORWAVE: "vaporwave aesthetic, 80s/90s nostalgia, glitch art, neon colors, retro-futurism",
        ImageStyle.SYNTHWAVE: "synthwave aesthetic, neon grids, sunset gradients, retro-futuristic, 80s inspired",
        ImageStyle.CYBERPUNK: "cyberpunk aesthetic, neon-lit dystopia, high-tech low-life, rain-slicked streets",
        ImageStyle.STEAMPUNK: "steampunk aesthetic, Victorian era, brass gears, steam-powered machinery",
        ImageStyle.FANTASY: "fantasy art, magical realm, mythical creatures, epic adventure aesthetic",
        ImageStyle.SCI_FI: "science fiction art, futuristic technology, space exploration, advanced civilization",
        ImageStyle.NOIR: "film noir aesthetic, high contrast black and white, dramatic shadows, 1940s detective",
        ImageStyle.GOTHIC: "gothic aesthetic, dark romantic, ornate architecture, dramatic atmosphere",
    }
    
    # ============================================================
    # CAMERA ANGLES
    # ============================================================
    
    CAMERA_ANGLE_MODIFIERS = {
        CameraAngle.EYE_LEVEL: "eye-level camera angle, neutral balanced perspective, natural human viewpoint, relatable framing",
        CameraAngle.LOW_ANGLE: "low-angle shot looking upward, subject appears powerful and dominant, heroic imposing perspective, emphasizes strength",
        CameraAngle.HIGH_ANGLE: "high-angle shot looking downward, subject appears smaller and vulnerable, creates sense of overview or power dynamic",
        CameraAngle.BIRDS_EYE: "bird's-eye view directly overhead, top-down perspective, shows layout and geography, god's eye view",
        CameraAngle.WORMS_EYE: "worm's-eye view from ground level, extreme low angle, dramatic imposing perspective, architectural grandeur",
        CameraAngle.DUTCH_ANGLE: "Dutch angle tilted frame, creates unease tension and disorientation, dynamic diagonal lines, psychological unbalance",
        CameraAngle.OVER_SHOULDER: "over-the-shoulder shot, POV from behind subject, creates intimacy and perspective, conversational framing",
        CameraAngle.POV: "first-person POV perspective, viewer sees through character's eyes, immersive subjective viewpoint",
        CameraAngle.AERIAL: "aerial drone perspective, elevated bird's-eye with slight angle, sweeping landscape view",
        CameraAngle.FRONTAL: "straight-on frontal angle, direct symmetrical view, confrontational or iconic framing",
        CameraAngle.THREE_QUARTER: "three-quarter angle view, 45-degree perspective, classic portrait angle, dimensional depth",
    }
    
    # ============================================================
    # SHOT TYPES
    # ============================================================
    
    SHOT_TYPE_MODIFIERS = {
        ShotType.EXTREME_WIDE: "extreme wide shot, vast landscape dominates frame, subject tiny showing scale, establishing shot showing environment",
        ShotType.WIDE: "wide shot, full body and environment visible, context and setting clear, action fully readable",
        ShotType.FULL: "full shot, entire body from head to toe visible, body language readable, balanced framing",
        ShotType.MEDIUM: "medium shot, waist-up framing, conversational distance, gestures visible",
        ShotType.MEDIUM_CLOSE: "medium close-up, chest-up framing, emotional connection, facial expressions visible",
        ShotType.CLOSE_UP: "close-up shot, face fills frame, intimate emotional detail, eyes prominent and expressive",
        ShotType.EXTREME_CLOSE: "extreme close-up, macro detail shot, symbolic emphasis on specific feature, abstract intimacy",
        ShotType.TWO_SHOT: "two-shot framing, two subjects together, relationship dynamic visible, balanced composition",
        ShotType.GROUP: "group shot, multiple subjects framed together, social dynamics, ensemble composition",
        ShotType.DETAIL: "detail shot, specific object or texture focus, reveals important information, insert shot",
        ShotType.INSERT: "insert shot, cut-in to specific detail, narrative emphasis, storytelling element",
    }
    
    # ============================================================
    # LIGHTING TYPES
    # ============================================================
    
    LIGHTING_MODIFIERS = {
        # Studio
        LightingType.STUDIO: "professional three-point studio lighting, key fill and rim lights, controlled even illumination, commercial quality",
        LightingType.SOFTBOX: "softbox diffused lighting, soft even illumination, minimal shadows, beauty photography quality",
        LightingType.RING_LIGHT: "ring light illumination, even frontal lighting, catch lights in eyes, beauty/fashion aesthetic",
        LightingType.BEAUTY: "beauty lighting, butterfly/paramount setup, flattering facial illumination, glamour photography",
        
        # Dramatic
        LightingType.DRAMATIC: "dramatic chiaroscuro lighting, high contrast light and shadow, theatrical mood, bold light-dark interplay",
        LightingType.REMBRANDT: "Rembrandt lighting, triangular shadow on cheek, classic portrait technique, painterly quality",
        LightingType.SPLIT: "split lighting, half face in shadow, dramatic portrait, noir aesthetic, mysterious mood",
        LightingType.LOOP: "loop lighting, slight shadow under nose, flattering portrait light, professional headshot quality",
        LightingType.BUTTERFLY: "butterfly lighting, shadow under nose, glamour photography, beauty lighting setup",
        LightingType.BROAD: "broad lighting, light on wider side of face, flattering for narrow faces, classic portrait",
        LightingType.SHORT: "short lighting, light on narrow side of face, adds dimension and drama",
        
        # Natural
        LightingType.NATURAL: "natural daylight illumination, authentic outdoor lighting, realistic sun position, organic shadows",
        LightingType.GOLDEN_HOUR: "golden hour magic hour lighting, warm sunset/sunrise glow, long soft shadows, romantic amber tones",
        LightingType.BLUE_HOUR: "blue hour twilight lighting, cool ethereal atmosphere, soft ambient glow, magical quality",
        LightingType.OVERCAST: "overcast diffused daylight, soft even illumination, no harsh shadows, flattering natural light",
        LightingType.HARSH_SUNLIGHT: "harsh direct midday sun, strong shadows, high contrast, intense brightness",
        LightingType.DAPPLED: "dappled light through leaves, organic shadow patterns, natural filtered sunlight",
        LightingType.WINDOW: "soft window light, side illumination, natural portrait lighting, painterly quality",
        
        # Atmospheric
        LightingType.BACKLIT: "backlit silhouette lighting, rim light halo effect, sun behind subject, dramatic contrast",
        LightingType.RIM: "rim lighting, edge light separation from background, hair light, dimensional glow",
        LightingType.NEON: "neon light glow, cyberpunk aesthetic, colorful artificial illumination, electric atmosphere",
        LightingType.VOLUMETRIC: "volumetric lighting, visible light rays, god rays through atmosphere, dramatic shafts of light",
        LightingType.FOGGY: "foggy atmospheric lighting, diffused scattered light, mysterious mood, depth haze",
        LightingType.CANDLELIGHT: "warm candlelight illumination, flickering amber glow, intimate romantic atmosphere",
        LightingType.FIRELIGHT: "firelight illumination, orange dynamic glow, warm dancing shadows, campfire aesthetic",
        LightingType.MOONLIGHT: "cool moonlight illumination, blue night atmosphere, subtle luminance",
        
        # Cinematic
        LightingType.CINEMATIC: "cinematic movie lighting, dramatic production quality, motivated light sources, film aesthetic",
        LightingType.NOIR: "film noir lighting, high contrast shadows, dramatic venetian blind patterns, 1940s aesthetic",
        LightingType.LOW_KEY: "low-key lighting, predominantly dark, dramatic shadows, moody atmosphere",
        LightingType.HIGH_KEY: "high-key lighting, bright overall illumination, minimal shadows, optimistic feel",
    }
    
    # ============================================================
    # COMPOSITION RULES
    # ============================================================
    
    COMPOSITION_MODIFIERS = {
        CompositionRule.RULE_OF_THIRDS: "rule of thirds composition, subject at intersection points, balanced asymmetry, dynamic placement",
        CompositionRule.GOLDEN_RATIO: "golden ratio composition, Fibonacci spiral placement, naturally pleasing proportions",
        CompositionRule.CENTER: "centered symmetrical composition, balanced formal framing, direct powerful impact",
        CompositionRule.SYMMETRY: "symmetrical composition, mirror balance, architectural precision, formal elegance",
        CompositionRule.LEADING_LINES: "leading lines composition, visual pathways guiding eye to subject, dynamic depth",
        CompositionRule.FRAMING: "natural framing composition, elements create frame around subject, focused attention",
        CompositionRule.NEGATIVE_SPACE: "negative space emphasis, strategic emptiness, minimalist power, breathing room",
        CompositionRule.FILL_FRAME: "fill the frame composition, subject dominates, intimate detailed view, no wasted space",
        CompositionRule.DIAGONAL: "diagonal composition, dynamic energy, movement and tension, active framing",
        CompositionRule.TRIANGULAR: "triangular composition, stable pyramid arrangement, classical balanced structure",
        CompositionRule.LAYERED: "layered depth composition, distinct foreground midground background, dimensional space",
        CompositionRule.DEPTH: "strong depth perspective, three-dimensional spatial feeling, receding planes",
        CompositionRule.PATTERN_BREAK: "pattern with break composition, repetition disrupted by focal point, visual interest",
        CompositionRule.MINIMALIST: "minimalist composition, essential elements only, maximum simplicity, zen-like clarity",
    }
    
    # ============================================================
    # TIME OF DAY
    # ============================================================
    
    TIME_OF_DAY_MODIFIERS = {
        TimeOfDay.DAWN: "dawn early morning light, soft pink and purple sky, misty atmosphere, new day awakening",
        TimeOfDay.SUNRISE: "sunrise golden light emerging, warm orange and yellow glow, long shadows, hopeful atmosphere",
        TimeOfDay.MORNING: "bright morning daylight, fresh clear illumination, energetic atmosphere",
        TimeOfDay.MIDDAY: "harsh midday sun, strong overhead light, short shadows, high contrast",
        TimeOfDay.AFTERNOON: "warm afternoon light, angled golden illumination, relaxed atmosphere",
        TimeOfDay.GOLDEN_HOUR: "golden hour magic hour, warm amber sunset light, long soft shadows, romantic atmosphere",
        TimeOfDay.SUNSET: "dramatic sunset, orange red purple sky, silhouettes, emotional atmosphere",
        TimeOfDay.BLUE_HOUR: "blue hour twilight, cool blue atmosphere, city lights emerging, ethereal mood",
        TimeOfDay.DUSK: "dusk fading light, first stars appearing, transitional atmosphere",
        TimeOfDay.NIGHT: "nighttime scene, artificial lights, urban glow, nocturnal atmosphere",
        TimeOfDay.MIDNIGHT: "deep midnight, moonlit scene, quiet darkness, mysterious atmosphere",
        TimeOfDay.OVERCAST: "overcast diffused daylight, soft even lighting, moody grey sky",
    }
    
    # ============================================================
    # WEATHER CONDITIONS
    # ============================================================
    
    WEATHER_MODIFIERS = {
        Weather.CLEAR: "clear weather, blue sky, crisp visibility, perfect conditions",
        Weather.SUNNY: "sunny bright weather, strong sunlight, clear shadows, cheerful atmosphere",
        Weather.PARTLY_CLOUDY: "partly cloudy sky, dynamic clouds, interesting light variation",
        Weather.CLOUDY: "overcast cloudy sky, diffused soft light, moody atmosphere",
        Weather.FOGGY: "foggy misty atmosphere, limited visibility, mysterious mood, ethereal",
        Weather.RAINY: "rainy weather, falling rain, wet surfaces, reflections, moody atmosphere",
        Weather.STORMY: "stormy dramatic sky, dark threatening clouds, intense atmosphere",
        Weather.SNOWY: "snowy winter scene, falling snowflakes, white landscape, cold atmosphere",
        Weather.WINDY: "windy conditions, visible wind effects, movement in elements, dynamic atmosphere",
        Weather.HAZY: "hazy atmospheric conditions, soft distant visibility, dreamy quality",
        Weather.MISTY: "light misty atmosphere, subtle fog, soft diffusion, romantic mood",
        Weather.HUMID: "humid tropical atmosphere, visible moisture, lush environment",
    }
    
    # ============================================================
    # MATERIALS & TEXTURES
    # ============================================================
    
    MATERIAL_MODIFIERS = {
        # Metals
        Material.GOLD: "gold metallic surface, warm reflective shine, luxurious precious metal",
        Material.SILVER: "silver metallic surface, cool reflective shine, elegant precious metal",
        Material.COPPER: "copper metallic surface, warm reddish tone, antique patina possible",
        Material.BRONZE: "bronze metallic surface, warm brown tone, classical sculpture material",
        Material.CHROME: "chrome polished mirror surface, high reflectivity, modern industrial",
        Material.BRUSHED_METAL: "brushed metal texture, directional grain, matte metallic finish",
        Material.RUSTY: "rusty corroded metal, oxidized texture, weathered industrial aesthetic",
        
        # Glass
        Material.GLASS: "clear glass material, transparent, reflections and refractions, clean surface",
        Material.FROSTED_GLASS: "frosted glass material, translucent diffused, privacy glass aesthetic",
        Material.CRYSTAL: "crystal material, faceted cuts, light dispersion, luxury aesthetic",
        Material.ICE: "ice material, frozen water, cold translucent, crystalline structure",
        
        # Natural
        Material.WOOD: "wood material, natural grain patterns, organic warmth, varied species",
        Material.STONE: "stone material, natural texture, solid heavy, geological patterns",
        Material.MARBLE: "marble material, elegant veining, polished luxury, classical architecture",
        Material.GRANITE: "granite material, speckled texture, durable natural stone",
        Material.CONCRETE: "concrete material, industrial texture, modern brutalist aesthetic",
        Material.BRICK: "brick material, structured texture, architectural warmth",
        Material.SAND: "sand material, granular texture, beach or desert aesthetic",
        
        # Fabrics
        Material.SILK: "silk fabric, smooth lustrous sheen, luxurious drape, elegant flow",
        Material.VELVET: "velvet fabric, soft plush texture, rich depth, luxurious tactile",
        Material.LEATHER: "leather material, natural texture, warm patina, quality craftsmanship",
        Material.DENIM: "denim fabric, indigo weave, casual durable, classic American",
        Material.LINEN: "linen fabric, natural weave texture, breathable relaxed aesthetic",
        Material.WOOL: "wool fabric, soft fuzzy texture, warm cozy, natural material",
        Material.FUR: "fur material, soft fluffy texture, natural animal hair, luxurious",
        
        # Finishes
        Material.MATTE: "matte finish surface, non-reflective, soft light absorption",
        Material.GLOSSY: "glossy finish surface, high shine, reflective polished",
        Material.HOLOGRAPHIC: "holographic iridescent surface, rainbow color shift, futuristic",
        Material.IRIDESCENT: "iridescent surface, color-shifting sheen, pearl-like quality",
    }
    
    # ============================================================
    # ART MOVEMENTS
    # ============================================================
    
    ART_MOVEMENT_MODIFIERS = {
        ArtMovement.RENAISSANCE: "Renaissance art style, classical proportions, sfumato technique, Leonardo da Vinci, Michelangelo influence",
        ArtMovement.BAROQUE: "Baroque art style, dramatic chiaroscuro, rich ornamentation, Caravaggio, Rembrandt influence",
        ArtMovement.IMPRESSIONISM: "Impressionist style, visible brushstrokes, light and color emphasis, Monet, Renoir influence",
        ArtMovement.POST_IMPRESSIONISM: "Post-Impressionist style, bold colors, expressive brushwork, Van Gogh, Cézanne influence",
        ArtMovement.EXPRESSIONISM: "Expressionist style, emotional intensity, distorted forms, vivid colors, Munch, Kandinsky influence",
        ArtMovement.CUBISM: "Cubist style, fragmented geometric forms, multiple perspectives, Picasso, Braque influence",
        ArtMovement.SURREALISM: "Surrealist style, dreamlike imagery, subconscious symbolism, Dalí, Magritte influence",
        ArtMovement.POP_ART: "Pop Art style, bold colors, commercial imagery, Andy Warhol, Roy Lichtenstein influence",
        ArtMovement.ART_NOUVEAU: "Art Nouveau style, organic flowing lines, natural forms, decorative elegance, Mucha influence",
        ArtMovement.ART_DECO: "Art Deco style, geometric patterns, bold symmetry, 1920s glamour, luxurious elegance",
        ArtMovement.BAUHAUS: "Bauhaus style, functional minimalism, geometric forms, modernist design principles",
        ArtMovement.UKIYO_E: "Ukiyo-e Japanese woodblock style, flat colors, bold outlines, Hokusai, Hiroshige influence",
        ArtMovement.STREET_ART: "street art style, urban graffiti aesthetic, bold graphics, Banksy, Shepard Fairey influence",
    }
    
    # ============================================================
    # COLOR SCHEMES
    # ============================================================
    
    COLOR_SCHEME_MODIFIERS = {
        ColorScheme.WARM: "warm color palette, golden yellows, burnt oranges, rusty reds, cozy amber tones",
        ColorScheme.COOL: "cool color palette, ocean blues, forest greens, soft purples, calming serene tones",
        ColorScheme.NEUTRAL: "neutral color palette, grays, beiges, whites, sophisticated understated",
        ColorScheme.VIBRANT: "vibrant saturated colors, bold punchy hues, eye-catching intensity, maximum color",
        ColorScheme.MUTED: "muted desaturated tones, subtle sophisticated colors, refined palette",
        ColorScheme.PASTEL: "soft pastel colors, light gentle hues, dreamy aesthetic, delicate tones",
        ColorScheme.NEON: "neon fluorescent colors, electric bright palette, glowing saturated hues",
        ColorScheme.MONOCHROME: "monochromatic color scheme, single hue variations, unified tonal palette",
        ColorScheme.BLACK_AND_WHITE: "black and white, high contrast monochrome, dramatic grayscale",
        ColorScheme.SEPIA: "sepia toned, warm brown vintage aesthetic, nostalgic antique look",
        ColorScheme.EARTH_TONES: "earth tone palette, natural organic colors, terracotta olive sienna ochre",
        ColorScheme.CYBERPUNK: "cyberpunk color palette, neon pink blue purple, dark contrasting shadows",
        ColorScheme.VAPORWAVE: "vaporwave color palette, pink purple cyan, 80s/90s nostalgia, glitch aesthetic",
        ColorScheme.COMPLEMENTARY: "complementary color harmony, opposite colors for vibrance, dynamic tension",
        ColorScheme.ANALOGOUS: "analogous color harmony, adjacent colors, harmonious unified palette",
    }
    
    # ============================================================
    # MOOD / ATMOSPHERE
    # ============================================================
    
    MOOD_MODIFIERS = {
        Mood.CHEERFUL: "cheerful uplifting mood, bright optimistic atmosphere, joyful energy, warm inviting",
        Mood.JOYFUL: "joyful exuberant mood, pure happiness, celebratory atmosphere, radiant positivity",
        Mood.PEACEFUL: "peaceful serene mood, calm tranquil atmosphere, meditative stillness, harmony",
        Mood.SERENE: "serene quiet mood, gentle calm, undisturbed peace, contemplative beauty",
        Mood.ROMANTIC: "romantic mood, intimate atmosphere, soft lighting, love and connection",
        Mood.DREAMY: "dreamy ethereal mood, soft hazy atmosphere, fantasy-like quality, otherworldly",
        Mood.MAGICAL: "magical enchanting mood, wonder and awe, fantastical atmosphere, spellbinding",
        Mood.DRAMATIC: "dramatic intense mood, powerful emotional impact, theatrical tension",
        Mood.EPIC: "epic grand mood, monumental scale, heroic atmosphere, awe-inspiring",
        Mood.MYSTERIOUS: "mysterious enigmatic mood, intriguing atmosphere, subtle tension, curiosity",
        Mood.MELANCHOLIC: "melancholic wistful mood, gentle sadness, reflective atmosphere",
        Mood.DARK: "dark moody atmosphere, shadow and mystery, intense brooding quality",
        Mood.ELEGANT: "elegant sophisticated mood, refined luxury, tasteful opulence, polished",
        Mood.PROFESSIONAL: "professional corporate mood, business-appropriate, trustworthy polished",
        Mood.NOSTALGIC: "nostalgic wistful mood, sentimental warmth, memories evoked, timeless",
        Mood.FUTURISTIC: "futuristic forward-looking mood, cutting-edge aesthetic, tomorrow's vision",
    }
    
    # ============================================================
    # CAMERA TYPES
    # ============================================================
    
    CAMERA_TYPE_MODIFIERS = {
        CameraType.DSLR: "shot with professional DSLR camera, full-frame sensor quality, sharp detail",
        CameraType.MIRRORLESS: "shot with mirrorless camera, modern digital quality, clean rendering",
        CameraType.MEDIUM_FORMAT: "shot with medium format camera, exceptional detail and dynamic range",
        CameraType.LARGE_FORMAT: "shot with large format camera, ultra-high resolution, tilt-shift capable",
        CameraType.FILM_35MM: "shot on 35mm film, organic grain, classic analog aesthetic, warm tones",
        CameraType.FILM_120: "shot on medium format 120 film, beautiful depth, film color science",
        CameraType.POLAROID: "Polaroid instant film aesthetic, distinctive color cast, white border frame",
        CameraType.DISPOSABLE: "disposable camera aesthetic, lo-fi casual, flash-lit, nostalgic imperfection",
        CameraType.SMARTPHONE: "smartphone camera quality, modern computational photography, casual authentic",
        CameraType.DRONE: "drone aerial photography, elevated perspective, landscape sweep",
        CameraType.VHS: "VHS video aesthetic, scan lines, color bleeding, retro lo-fi",
    }
    
    # ============================================================
    # LENS TYPES
    # ============================================================
    
    LENS_TYPE_MODIFIERS = {
        LensType.WIDE_ANGLE: "wide-angle lens (14-35mm), expansive field of view, dramatic perspective distortion",
        LensType.STANDARD: "standard lens (35-50mm), natural perspective similar to human eye, versatile",
        LensType.PORTRAIT: "portrait lens (85mm), flattering compression, beautiful background blur, ideal for faces",
        LensType.TELEPHOTO: "telephoto lens (100-200mm), compressed perspective, subject isolation, distant reach",
        LensType.SUPER_TELEPHOTO: "super-telephoto lens (300mm+), extreme compression, wildlife/sports aesthetic",
        LensType.MACRO: "macro lens, extreme close-up capability, revealing tiny details, 1:1 reproduction",
        LensType.FISHEYE: "fisheye lens, ultra-wide 180-degree view, extreme barrel distortion, creative effect",
        LensType.TILT_SHIFT: "tilt-shift lens, selective focus plane, miniature effect, architectural correction",
        LensType.ANAMORPHIC: "anamorphic lens, cinematic widescreen, horizontal lens flares, oval bokeh",
        LensType.VINTAGE_LENS: "vintage lens character, soft glow, characterful aberrations, dreamy imperfection",
    }
    
    # ============================================================
    # QUALITY MODIFIERS
    # ============================================================
    
    QUALITY_MODIFIERS = {
        "low": "standard quality rendering",
        "medium": "good quality, detailed rendering, clear sharp output",
        "high": "high quality professional output, highly detailed, sharp focus, 4K quality",
        "ultra": "ultra-high quality masterpiece, extremely detailed, 8K UHD, award-winning caliber, perfect execution",
    }
    
    QUALITY_KEYWORDS = "high quality, professional rendering, detailed, sharp focus"
    
    # ============================================================
    # PROMPT BUILDING
    # ============================================================
    
    @classmethod
    def build_prompt(cls, request: ImageRequest) -> str:
        """Build an optimized prompt based on the request."""
        parts = []
        
        # 1. Shot type (if specified) - describes framing first
        if request.shot_type:
            shot_mod = cls.SHOT_TYPE_MODIFIERS.get(request.shot_type, "")
            if shot_mod:
                parts.append(shot_mod)
        
        # 2. Camera angle (if specified)
        if request.camera_angle:
            angle_mod = cls.CAMERA_ANGLE_MODIFIERS.get(request.camera_angle, "")
            if angle_mod:
                parts.append(angle_mod)
        
        # 3. Main subject/prompt
        base_prompt = request.prompt.strip()
        parts.append(base_prompt)
        
        # 4. Purpose-specific template
        if request.purpose:
            template = cls.TEMPLATES.get(request.purpose)
            if template:
                style = request.style or template.get("default_style", ImageStyle.MODERN)
                style_name = style.value if isinstance(style, ImageStyle) else style
                
                aspect_hint = ""
                if request.aspect_ratio in [AspectRatio.LANDSCAPE_16_9, AspectRatio.WIDE_21_9]:
                    aspect_hint = "wide landscape format, horizontal composition"
                elif request.aspect_ratio == AspectRatio.PORTRAIT_9_16:
                    aspect_hint = "vertical portrait format, tall composition"
                
                suffix = template["suffix"].format(style=style_name, aspect_hint=aspect_hint)
                parts.append(suffix)
        
        # 5. Style modifier
        if request.style:
            style_mod = cls.STYLE_MODIFIERS.get(request.style, "")
            if style_mod:
                parts.append(style_mod)
        
        # 6. Lighting
        if request.lighting:
            lighting_mod = cls.LIGHTING_MODIFIERS.get(request.lighting, "")
            if lighting_mod:
                parts.append(lighting_mod)
        
        # 7. Composition
        if request.composition:
            comp_mod = cls.COMPOSITION_MODIFIERS.get(request.composition, "")
            if comp_mod:
                parts.append(comp_mod)
        
        # 8. Time of day
        if request.time_of_day:
            time_mod = cls.TIME_OF_DAY_MODIFIERS.get(request.time_of_day, "")
            if time_mod:
                parts.append(time_mod)
        
        # 9. Weather
        if request.weather:
            weather_mod = cls.WEATHER_MODIFIERS.get(request.weather, "")
            if weather_mod:
                parts.append(weather_mod)
        
        # 10. Color scheme
        if request.color_scheme:
            color_mod = cls.COLOR_SCHEME_MODIFIERS.get(request.color_scheme, "")
            if color_mod:
                parts.append(color_mod)
        
        # 11. Mood
        if request.mood:
            mood_mod = cls.MOOD_MODIFIERS.get(request.mood, "")
            if mood_mod:
                parts.append(mood_mod)
        
        # 12. Art movement
        if request.art_movement:
            art_mod = cls.ART_MOVEMENT_MODIFIERS.get(request.art_movement, "")
            if art_mod:
                parts.append(art_mod)
        
        # 13. Material/texture
        if request.material:
            material_mod = cls.MATERIAL_MODIFIERS.get(request.material, "")
            if material_mod:
                parts.append(material_mod)
        
        # 14. Camera type
        if request.camera_type:
            camera_mod = cls.CAMERA_TYPE_MODIFIERS.get(request.camera_type, "")
            if camera_mod:
                parts.append(camera_mod)
        
        # 15. Lens type
        if request.lens_type:
            lens_mod = cls.LENS_TYPE_MODIFIERS.get(request.lens_type, "")
            if lens_mod:
                parts.append(lens_mod)
        
        # 16. Depth of field
        if request.depth_of_field:
            dof_map = {
                "shallow": "shallow depth of field, beautiful background blur, bokeh",
                "deep": "deep depth of field, sharp focus throughout, landscape-style clarity",
                "tilt-shift": "tilt-shift miniature effect, selective focus plane",
            }
            parts.append(dof_map.get(request.depth_of_field, ""))
        
        # 17. Visual effects
        effects = []
        if request.bokeh:
            effects.append("beautiful bokeh, creamy background blur")
        if request.film_grain:
            effects.append("subtle film grain texture, analog aesthetic")
        if request.vignette:
            effects.append("vignette darkening at corners")
        if request.lens_flare:
            effects.append("lens flare, light artifacts")
        if request.motion_blur:
            effects.append("motion blur, sense of movement and speed")
        if request.chromatic_aberration:
            effects.append("chromatic aberration, color fringing at edges")
        if effects:
            parts.append(", ".join(effects))
        
        # 18. Quality
        if request.quality:
            quality_mod = cls.QUALITY_MODIFIERS.get(request.quality, "")
            if quality_mod:
                parts.append(quality_mod)
        else:
            parts.append(cls.QUALITY_KEYWORDS)
        
        # 19. Negative prompt
        if request.negative_prompt:
            parts.append(f"Avoid: {request.negative_prompt}")
        
        # 20. Seed
        if request.seed is not None:
            parts.append(f"[seed:{request.seed}]")
        
        # 21. Resolution
        if request.width and request.height:
            parts.append(f"Output resolution: {request.width}x{request.height} pixels")
        
        # Combine with proper punctuation
        final_prompt = ". ".join(filter(None, parts))
        
        return final_prompt
    
    @classmethod
    def get_negative_prompt(cls, purpose: Optional[ImagePurpose]) -> Optional[str]:
        """Get negative prompt for a specific purpose."""
        if purpose:
            template = cls.TEMPLATES.get(purpose)
            if template:
                return template.get("negative")
        return None


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def app_icon_prompt(description: str, style: str = "flat-design") -> str:
    """Build optimized prompt for app icon."""
    from .types import ImageRequest, ImagePurpose, ImageStyle, AspectRatio
    request = ImageRequest(
        prompt=description,
        purpose=ImagePurpose.APP_ICON,
        style=ImageStyle(style) if style in [s.value for s in ImageStyle] else ImageStyle.FLAT_DESIGN,
        aspect_ratio=AspectRatio.SQUARE
    )
    return PromptBuilder.build_prompt(request)


def cinematic_prompt(
    description: str,
    shot_type: str = "wide",
    camera_angle: str = "eye-level",
    lighting: str = "cinematic",
    mood: str = "dramatic"
) -> str:
    """Build optimized prompt for cinematic scene."""
    from .types import ImageRequest, ImageStyle, AspectRatio, ShotType, CameraAngle, LightingType, Mood
    request = ImageRequest(
        prompt=description,
        style=ImageStyle.CINEMATIC,
        aspect_ratio=AspectRatio.LANDSCAPE_16_9,
        shot_type=ShotType(shot_type) if shot_type in [s.value for s in ShotType] else None,
        camera_angle=CameraAngle(camera_angle) if camera_angle in [s.value for s in CameraAngle] else None,
        lighting=LightingType(lighting) if lighting in [s.value for s in LightingType] else None,
        mood=Mood(mood) if mood in [s.value for s in Mood] else None,
        quality="ultra"
    )
    return PromptBuilder.build_prompt(request)


def portrait_prompt(
    description: str,
    lighting: str = "rembrandt",
    lens: str = "portrait"
) -> str:
    """Build optimized prompt for portrait."""
    from .types import ImageRequest, ImagePurpose, ImageStyle, AspectRatio, LightingType, LensType, ShotType
    request = ImageRequest(
        prompt=description,
        purpose=ImagePurpose.PORTRAIT,
        style=ImageStyle.PHOTOREALISTIC,
        aspect_ratio=AspectRatio.PORTRAIT_3_4,
        shot_type=ShotType.MEDIUM_CLOSE,
        lighting=LightingType(lighting) if lighting in [s.value for s in LightingType] else LightingType.REMBRANDT,
        lens_type=LensType(lens) if lens in [s.value for s in LensType] else LensType.PORTRAIT,
        bokeh=True,
        quality="ultra"
    )
    return PromptBuilder.build_prompt(request)
