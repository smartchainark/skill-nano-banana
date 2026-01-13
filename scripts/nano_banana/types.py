"""Type definitions for Nano Banana MCP - Enhanced with professional photography & art parameters."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from pathlib import Path


# ============================================================
# ASPECT RATIOS
# ============================================================

class AspectRatio(str, Enum):
    """Supported aspect ratios for image generation."""
    SQUARE = "1:1"           # 1024x1024 - Social media posts, profile pics, app icons
    LANDSCAPE_16_9 = "16:9"  # 1664x928 - YouTube thumbnails, banners, widescreen
    PORTRAIT_9_16 = "9:16"   # 928x1664 - Stories, reels, mobile wallpapers
    LANDSCAPE_4_3 = "4:3"    # 1472x1140 - Traditional photo, presentations
    PORTRAIT_3_4 = "3:4"     # 1140x1472 - Product photos, portraits
    WIDE_21_9 = "21:9"       # 1792x768 - Ultra-wide banners, cinematic
    LANDSCAPE_3_2 = "3:2"    # Classic 35mm film ratio
    PORTRAIT_2_3 = "2:3"     # Classic portrait ratio
    
    @classmethod
    def from_string(cls, value: str) -> "AspectRatio":
        """Get aspect ratio from string."""
        for ratio in cls:
            if ratio.value == value:
                return ratio
        return cls.SQUARE


# ============================================================
# QUALITY LEVELS
# ============================================================

class ImageQuality(str, Enum):
    """Image quality levels."""
    LOW = "low"           # Faster generation, standard quality
    MEDIUM = "medium"     # Balanced speed/quality
    HIGH = "high"         # High detail, slower
    ULTRA = "ultra"       # Maximum quality, professional output


# ============================================================
# ART STYLES
# ============================================================

class ImageStyle(str, Enum):
    """Predefined artistic styles."""
    # Photography styles
    PHOTOREALISTIC = "photorealistic"
    STUDIO = "studio"
    CINEMATIC = "cinematic"
    EDITORIAL = "editorial"
    DOCUMENTARY = "documentary"
    FASHION = "fashion"
    
    # Traditional art
    WATERCOLOR = "watercolor"
    OIL_PAINTING = "oil-painting"
    ACRYLIC = "acrylic"
    SKETCH = "sketch"
    CHARCOAL = "charcoal"
    INK_WASH = "ink-wash"
    PASTEL = "pastel"
    GOUACHE = "gouache"
    
    # Digital art
    DIGITAL_ART = "digital-art"
    CONCEPT_ART = "concept-art"
    MATTE_PAINTING = "matte-painting"
    PIXEL_ART = "pixel-art"
    VOXEL = "voxel"
    LOW_POLY = "low-poly"
    
    # Illustration styles
    ANIME = "anime"
    MANGA = "manga"
    COMIC_BOOK = "comic-book"
    CARTOON = "cartoon"
    CHILDRENS_BOOK = "childrens-book"
    STORYBOOK = "storybook"
    
    # Design styles
    MODERN = "modern"
    MINIMALIST = "minimalist"
    FLAT_DESIGN = "flat-design"
    MATERIAL_DESIGN = "material-design"
    GLASSMORPHISM = "glassmorphism"
    NEUMORPHISM = "neumorphism"
    BRUTALIST = "brutalist"
    
    # 3D styles
    THREE_D_RENDER = "3d-render"
    ISOMETRIC = "isometric"
    CLAY_RENDER = "clay-render"
    WIREFRAME = "wireframe"
    
    # Aesthetic styles
    VINTAGE = "vintage"
    RETRO = "retro"
    ABSTRACT = "abstract"
    SURREAL = "surreal"
    PSYCHEDELIC = "psychedelic"
    VAPORWAVE = "vaporwave"
    SYNTHWAVE = "synthwave"
    CYBERPUNK = "cyberpunk"
    STEAMPUNK = "steampunk"
    FANTASY = "fantasy"
    SCI_FI = "sci-fi"
    NOIR = "noir"
    GOTHIC = "gothic"


# ============================================================
# IMAGE PURPOSE
# ============================================================

class ImagePurpose(str, Enum):
    """Purpose-specific image types with optimized prompts."""
    APP_ICON = "app-icon"
    FAVICON = "favicon"
    LOGO = "logo"
    BANNER = "banner"
    THUMBNAIL = "thumbnail"
    PRODUCT = "product"
    SOCIAL_POST = "social-post"
    STORY = "story"
    HERO_IMAGE = "hero-image"
    ILLUSTRATION = "illustration"
    DIAGRAM = "diagram"
    PATTERN = "pattern"
    AVATAR = "avatar"
    MOCKUP = "mockup"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    ARCHITECTURE = "architecture"
    FOOD = "food"
    FASHION = "fashion"
    EDITORIAL = "editorial"


# ============================================================
# CAMERA ANGLES (Cinematography)
# ============================================================

class CameraAngle(str, Enum):
    """Camera angles for composition control."""
    EYE_LEVEL = "eye-level"           # Neutral, natural perspective
    LOW_ANGLE = "low-angle"           # Looking up, subject appears powerful
    HIGH_ANGLE = "high-angle"         # Looking down, subject appears smaller
    BIRDS_EYE = "birds-eye"           # Directly above, top-down view
    WORMS_EYE = "worms-eye"           # Extreme low, from ground level
    DUTCH_ANGLE = "dutch-angle"       # Tilted frame, creates tension
    OVER_SHOULDER = "over-shoulder"   # POV from behind a subject
    POV = "pov"                       # First-person perspective
    AERIAL = "aerial"                 # Drone/helicopter view
    FRONTAL = "frontal"               # Straight-on, symmetrical
    THREE_QUARTER = "three-quarter"   # 45-degree angle, classic portrait


# ============================================================
# SHOT TYPES (Framing)
# ============================================================

class ShotType(str, Enum):
    """Shot types for framing control."""
    EXTREME_WIDE = "extreme-wide"     # Vast landscape, subject tiny
    WIDE = "wide"                     # Full environment visible
    FULL = "full"                     # Full body visible
    MEDIUM = "medium"                 # Waist up
    MEDIUM_CLOSE = "medium-close"     # Chest up
    CLOSE_UP = "close-up"             # Face/detail focus
    EXTREME_CLOSE = "extreme-close"   # Macro detail
    TWO_SHOT = "two-shot"             # Two subjects framed together
    GROUP = "group"                   # Multiple subjects
    DETAIL = "detail"                 # Specific object/texture focus
    INSERT = "insert"                 # Cut-in of specific detail


# ============================================================
# LIGHTING TYPES
# ============================================================

class LightingType(str, Enum):
    """Professional lighting setups."""
    # Studio lighting
    STUDIO = "studio"                 # Three-point professional setup
    SOFTBOX = "softbox"               # Soft diffused light
    RING_LIGHT = "ring-light"         # Even frontal lighting
    BEAUTY = "beauty"                 # Flattering portrait light
    
    # Dramatic lighting
    DRAMATIC = "dramatic"             # High contrast chiaroscuro
    REMBRANDT = "rembrandt"           # Triangle shadow on cheek
    SPLIT = "split"                   # Half face in shadow
    LOOP = "loop"                     # Slight shadow under nose
    BUTTERFLY = "butterfly"           # Shadow under nose, glamour
    BROAD = "broad"                   # Light on wider side of face
    SHORT = "short"                   # Light on narrow side of face
    
    # Natural lighting
    NATURAL = "natural"               # Outdoor daylight
    GOLDEN_HOUR = "golden-hour"       # Warm sunset/sunrise
    BLUE_HOUR = "blue-hour"           # Cool twilight
    OVERCAST = "overcast"             # Soft diffused daylight
    HARSH_SUNLIGHT = "harsh-sunlight" # Direct midday sun
    DAPPLED = "dappled"               # Light through leaves
    WINDOW = "window"                 # Soft side window light
    
    # Atmospheric
    BACKLIT = "backlit"               # Subject silhouetted
    RIM = "rim"                       # Edge/hair light
    NEON = "neon"                     # Colorful artificial glow
    VOLUMETRIC = "volumetric"         # Visible light rays
    FOGGY = "foggy"                   # Diffused atmospheric
    CANDLELIGHT = "candlelight"       # Warm flickering
    FIRELIGHT = "firelight"           # Orange dynamic glow
    MOONLIGHT = "moonlight"           # Cool blue night
    
    # Cinematic
    CINEMATIC = "cinematic"           # Movie-quality lighting
    NOIR = "noir"                     # High contrast shadows
    LOW_KEY = "low-key"               # Mostly dark, dramatic
    HIGH_KEY = "high-key"             # Bright, minimal shadows


# ============================================================
# COMPOSITION RULES
# ============================================================

class CompositionRule(str, Enum):
    """Composition guidelines."""
    RULE_OF_THIRDS = "rule-of-thirds"         # Subject at intersection points
    GOLDEN_RATIO = "golden-ratio"             # Fibonacci spiral placement
    CENTER = "center"                         # Symmetrical centered
    SYMMETRY = "symmetry"                     # Mirror balance
    LEADING_LINES = "leading-lines"           # Lines guide to subject
    FRAMING = "framing"                       # Natural frame around subject
    NEGATIVE_SPACE = "negative-space"         # Emphasis through emptiness
    FILL_FRAME = "fill-frame"                 # Subject fills entire frame
    DIAGONAL = "diagonal"                     # Dynamic diagonal composition
    TRIANGULAR = "triangular"                 # Stable triangle arrangement
    LAYERED = "layered"                       # Foreground/mid/background
    DEPTH = "depth"                           # Strong sense of 3D space
    PATTERN_BREAK = "pattern-break"           # Breaking repetition for interest
    MINIMALIST = "minimalist"                 # Essential elements only


# ============================================================
# TIME OF DAY
# ============================================================

class TimeOfDay(str, Enum):
    """Time of day for lighting and atmosphere."""
    DAWN = "dawn"                   # Early morning, soft pink/purple
    SUNRISE = "sunrise"             # Golden warm light emerging
    MORNING = "morning"             # Bright fresh daylight
    MIDDAY = "midday"               # Harsh overhead sun
    AFTERNOON = "afternoon"         # Warm angled light
    GOLDEN_HOUR = "golden-hour"     # Hour before sunset, magical
    SUNSET = "sunset"               # Dramatic orange/red sky
    BLUE_HOUR = "blue-hour"         # After sunset, cool blue
    DUSK = "dusk"                   # Fading light, first stars
    NIGHT = "night"                 # Dark with artificial lights
    MIDNIGHT = "midnight"           # Deep night, moonlight
    OVERCAST = "overcast"           # Cloudy, diffused light


# ============================================================
# WEATHER CONDITIONS
# ============================================================

class Weather(str, Enum):
    """Weather conditions for atmosphere."""
    CLEAR = "clear"                 # Blue sky, no clouds
    SUNNY = "sunny"                 # Bright sunlight
    PARTLY_CLOUDY = "partly-cloudy" # Some clouds
    CLOUDY = "cloudy"               # Overcast sky
    FOGGY = "foggy"                 # Misty atmosphere
    RAINY = "rainy"                 # Rain falling
    STORMY = "stormy"               # Dark dramatic clouds
    SNOWY = "snowy"                 # Snow falling
    WINDY = "windy"                 # Visible wind effects
    HAZY = "hazy"                   # Atmospheric haze
    MISTY = "misty"                 # Light fog
    HUMID = "humid"                 # Tropical moisture


# ============================================================
# MATERIALS & TEXTURES
# ============================================================

class Material(str, Enum):
    """Surface materials and textures."""
    # Metals
    GOLD = "gold"
    SILVER = "silver"
    COPPER = "copper"
    BRONZE = "bronze"
    CHROME = "chrome"
    BRUSHED_METAL = "brushed-metal"
    RUSTY = "rusty"
    
    # Glass & Crystal
    GLASS = "glass"
    FROSTED_GLASS = "frosted-glass"
    CRYSTAL = "crystal"
    ICE = "ice"
    
    # Natural
    WOOD = "wood"
    STONE = "stone"
    MARBLE = "marble"
    GRANITE = "granite"
    CONCRETE = "concrete"
    BRICK = "brick"
    SAND = "sand"
    
    # Fabrics
    SILK = "silk"
    VELVET = "velvet"
    LEATHER = "leather"
    DENIM = "denim"
    LINEN = "linen"
    WOOL = "wool"
    FUR = "fur"
    
    # Organic
    SKIN = "skin"
    WATER = "water"
    FIRE = "fire"
    SMOKE = "smoke"
    CLOUD = "cloud"
    
    # Synthetic
    PLASTIC = "plastic"
    RUBBER = "rubber"
    CERAMIC = "ceramic"
    PORCELAIN = "porcelain"
    MATTE = "matte"
    GLOSSY = "glossy"
    HOLOGRAPHIC = "holographic"
    IRIDESCENT = "iridescent"


# ============================================================
# ART MOVEMENTS & ARTISTS (Reference styles)
# ============================================================

class ArtMovement(str, Enum):
    """Art movements and influential styles."""
    # Historical movements
    RENAISSANCE = "renaissance"
    BAROQUE = "baroque"
    ROCOCO = "rococo"
    NEOCLASSICAL = "neoclassical"
    ROMANTICISM = "romanticism"
    REALISM = "realism"
    IMPRESSIONISM = "impressionism"
    POST_IMPRESSIONISM = "post-impressionism"
    EXPRESSIONISM = "expressionism"
    FAUVISM = "fauvism"
    CUBISM = "cubism"
    FUTURISM = "futurism"
    DADA = "dada"
    SURREALISM = "surrealism"
    ABSTRACT_EXPRESSIONISM = "abstract-expressionism"
    POP_ART = "pop-art"
    MINIMALISM = "minimalism"
    PHOTOREALISM = "photorealism"
    
    # Contemporary
    STREET_ART = "street-art"
    GRAFFITI = "graffiti"
    LOWBROW = "lowbrow"
    DIGITAL_SURREALISM = "digital-surrealism"
    AFROFUTURISM = "afrofuturism"
    
    # Regional
    UKIYO_E = "ukiyo-e"           # Japanese woodblock
    ART_NOUVEAU = "art-nouveau"
    ART_DECO = "art-deco"
    BAUHAUS = "bauhaus"


# ============================================================
# COLOR SCHEMES
# ============================================================

class ColorScheme(str, Enum):
    """Color palette options."""
    # Temperature
    WARM = "warm"
    COOL = "cool"
    NEUTRAL = "neutral"
    
    # Saturation
    VIBRANT = "vibrant"
    MUTED = "muted"
    PASTEL = "pastel"
    NEON = "neon"
    
    # Special
    MONOCHROME = "monochrome"
    BLACK_AND_WHITE = "black-and-white"
    SEPIA = "sepia"
    DUOTONE = "duotone"
    
    # Nature
    EARTH_TONES = "earth-tones"
    OCEAN = "ocean"
    FOREST = "forest"
    SUNSET = "sunset"
    AUTUMN = "autumn"
    SPRING = "spring"
    
    # Aesthetic
    CYBERPUNK = "cyberpunk"
    VAPORWAVE = "vaporwave"
    SYNTHWAVE = "synthwave"
    NOIR = "noir"
    VINTAGE = "vintage"
    
    # Color theory
    COMPLEMENTARY = "complementary"
    ANALOGOUS = "analogous"
    TRIADIC = "triadic"
    SPLIT_COMPLEMENTARY = "split-complementary"
    TETRADIC = "tetradic"


# ============================================================
# MOOD / ATMOSPHERE
# ============================================================

class Mood(str, Enum):
    """Emotional atmosphere."""
    # Positive
    CHEERFUL = "cheerful"
    JOYFUL = "joyful"
    PEACEFUL = "peaceful"
    SERENE = "serene"
    HOPEFUL = "hopeful"
    ROMANTIC = "romantic"
    WHIMSICAL = "whimsical"
    PLAYFUL = "playful"
    DREAMY = "dreamy"
    MAGICAL = "magical"
    
    # Intense
    DRAMATIC = "dramatic"
    EPIC = "epic"
    POWERFUL = "powerful"
    ENERGETIC = "energetic"
    DYNAMIC = "dynamic"
    INTENSE = "intense"
    
    # Dark
    MYSTERIOUS = "mysterious"
    MELANCHOLIC = "melancholic"
    SOMBER = "somber"
    EERIE = "eerie"
    HAUNTING = "haunting"
    OMINOUS = "ominous"
    DARK = "dark"
    GRITTY = "gritty"
    
    # Neutral
    PROFESSIONAL = "professional"
    ELEGANT = "elegant"
    SOPHISTICATED = "sophisticated"
    MINIMALIST = "minimalist"
    CALM = "calm"
    CONTEMPLATIVE = "contemplative"
    NOSTALGIC = "nostalgic"
    FUTURISTIC = "futuristic"


# ============================================================
# CAMERA & LENS SIMULATION
# ============================================================

class CameraType(str, Enum):
    """Camera/lens simulation for specific looks."""
    DSLR = "dslr"                   # Professional digital camera
    MIRRORLESS = "mirrorless"       # Modern mirrorless
    MEDIUM_FORMAT = "medium-format" # High-end detail
    LARGE_FORMAT = "large-format"   # Ultra-high resolution
    FILM_35MM = "film-35mm"         # Classic 35mm film
    FILM_120 = "film-120"           # Medium format film
    POLAROID = "polaroid"           # Instant film look
    DISPOSABLE = "disposable"       # Lo-fi casual
    SMARTPHONE = "smartphone"       # Modern phone camera
    DRONE = "drone"                 # Aerial photography
    CCTV = "cctv"                   # Surveillance aesthetic
    WEBCAM = "webcam"               # Low quality intentional
    VHS = "vhs"                     # Retro video tape


class LensType(str, Enum):
    """Lens types for specific effects."""
    WIDE_ANGLE = "wide-angle"       # 14-35mm, expansive view
    STANDARD = "standard"           # 35-50mm, natural perspective
    PORTRAIT = "portrait"           # 85mm, flattering compression
    TELEPHOTO = "telephoto"         # 100-200mm, compressed background
    SUPER_TELEPHOTO = "super-telephoto"  # 300mm+, extreme compression
    MACRO = "macro"                 # Extreme close-up detail
    FISHEYE = "fisheye"             # Ultra-wide distorted
    TILT_SHIFT = "tilt-shift"       # Miniature effect
    ANAMORPHIC = "anamorphic"       # Cinematic widescreen
    VINTAGE_LENS = "vintage-lens"   # Soft, characterful


# ============================================================
# GEMINI MODELS
# ============================================================

class GeminiModel(str, Enum):
    """Available Gemini models for image generation."""
    GEMINI_2_0_FLASH_EXP = "gemini-2.0-flash-exp"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_IMAGE = "gemini-2.5-flash-image"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_3_PRO_IMAGE = "gemini-3-pro-image-preview"


# ============================================================
# IMAGE REQUEST (Enhanced)
# ============================================================

@dataclass
class ImageRequest:
    """Enhanced request for image generation with full control."""
    # Required
    prompt: str
    
    # Purpose & basic settings
    purpose: Optional[ImagePurpose] = None
    aspect_ratio: AspectRatio = AspectRatio.SQUARE
    style: Optional[ImageStyle] = None
    model: GeminiModel = GeminiModel.GEMINI_2_5_PRO
    count: int = 1
    
    # Photography controls
    camera_angle: Optional[CameraAngle] = None
    shot_type: Optional[ShotType] = None
    lighting: Optional[LightingType] = None
    composition: Optional[CompositionRule] = None
    
    # Environment
    time_of_day: Optional[TimeOfDay] = None
    weather: Optional[Weather] = None
    
    # Artistic controls
    mood: Optional[Mood] = None
    color_scheme: Optional[ColorScheme] = None
    art_movement: Optional[ArtMovement] = None
    material: Optional[Material] = None
    
    # Camera simulation
    camera_type: Optional[CameraType] = None
    lens_type: Optional[LensType] = None
    depth_of_field: Optional[str] = None  # "shallow", "deep", "tilt-shift"
    
    # Additional modifiers
    negative_prompt: Optional[str] = None
    reference_style: Optional[str] = None  # Artist or specific reference
    
    # Quality and generation control
    quality: Optional[str] = None  # "low", "medium", "high", "ultra"
    seed: Optional[int] = None     # For reproducible generation
    
    # Size control (pixels)
    width: Optional[int] = None    # Custom width in pixels
    height: Optional[int] = None   # Custom height in pixels
    
    # Advanced
    bokeh: bool = False           # Background blur
    film_grain: bool = False      # Add film grain texture
    vignette: bool = False        # Dark corners
    lens_flare: bool = False      # Light flares
    motion_blur: bool = False     # Movement blur
    chromatic_aberration: bool = False  # Color fringing


# ============================================================
# GENERATION RESULT
# ============================================================

@dataclass
class GenerationResult:
    """Result of image generation."""
    success: bool
    message: str
    images: List[Path] = field(default_factory=list)
    text: Optional[str] = None
    error: Optional[str] = None
    prompt_used: Optional[str] = None  # The final enhanced prompt


# ============================================================
# PURPOSE MAPPINGS (Auto-settings based on purpose)
# ============================================================

PURPOSE_ASPECT_RATIOS = {
    ImagePurpose.APP_ICON: AspectRatio.SQUARE,
    ImagePurpose.FAVICON: AspectRatio.SQUARE,
    ImagePurpose.LOGO: AspectRatio.SQUARE,
    ImagePurpose.BANNER: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.THUMBNAIL: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.PRODUCT: AspectRatio.PORTRAIT_3_4,
    ImagePurpose.SOCIAL_POST: AspectRatio.SQUARE,
    ImagePurpose.STORY: AspectRatio.PORTRAIT_9_16,
    ImagePurpose.HERO_IMAGE: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.ILLUSTRATION: AspectRatio.LANDSCAPE_4_3,
    ImagePurpose.DIAGRAM: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.PATTERN: AspectRatio.SQUARE,
    ImagePurpose.AVATAR: AspectRatio.SQUARE,
    ImagePurpose.MOCKUP: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.PORTRAIT: AspectRatio.PORTRAIT_3_4,
    ImagePurpose.LANDSCAPE: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.ARCHITECTURE: AspectRatio.LANDSCAPE_16_9,
    ImagePurpose.FOOD: AspectRatio.SQUARE,
    ImagePurpose.FASHION: AspectRatio.PORTRAIT_9_16,
    ImagePurpose.EDITORIAL: AspectRatio.PORTRAIT_3_4,
}

PURPOSE_STYLES = {
    ImagePurpose.APP_ICON: ImageStyle.FLAT_DESIGN,
    ImagePurpose.FAVICON: ImageStyle.MINIMALIST,
    ImagePurpose.LOGO: ImageStyle.MODERN,
    ImagePurpose.PRODUCT: ImageStyle.STUDIO,
    ImagePurpose.DIAGRAM: ImageStyle.FLAT_DESIGN,
    ImagePurpose.ILLUSTRATION: ImageStyle.DIGITAL_ART,
    ImagePurpose.PORTRAIT: ImageStyle.PHOTOREALISTIC,
    ImagePurpose.FASHION: ImageStyle.FASHION,
    ImagePurpose.FOOD: ImageStyle.PHOTOREALISTIC,
    ImagePurpose.ARCHITECTURE: ImageStyle.PHOTOREALISTIC,
}

PURPOSE_LIGHTING = {
    ImagePurpose.PORTRAIT: LightingType.REMBRANDT,
    ImagePurpose.PRODUCT: LightingType.STUDIO,
    ImagePurpose.FOOD: LightingType.NATURAL,
    ImagePurpose.FASHION: LightingType.BEAUTY,
    ImagePurpose.THUMBNAIL: LightingType.DRAMATIC,
}

PURPOSE_SHOT_TYPE = {
    ImagePurpose.PORTRAIT: ShotType.MEDIUM_CLOSE,
    ImagePurpose.PRODUCT: ShotType.DETAIL,
    ImagePurpose.LANDSCAPE: ShotType.WIDE,
    ImagePurpose.ARCHITECTURE: ShotType.WIDE,
    ImagePurpose.AVATAR: ShotType.CLOSE_UP,
}
