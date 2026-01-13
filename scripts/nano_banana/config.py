"""Configuration for Nano Banana MCP using official Gemini API."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIConfig:
    """Gemini API authentication."""
    api_key: str

    @classmethod
    def from_env(cls) -> "APIConfig":
        """Load API key from environment variables."""
        api_key = os.getenv("GOOGLE_API_KEY", "")

        if not api_key:
            raise ValueError(
                "Missing GOOGLE_API_KEY environment variable.\n"
                "Please set your Gemini API key:\n"
                "1. Get API key from https://aistudio.google.com/apikey\n"
                "2. Set: export GOOGLE_API_KEY='your_api_key'"
            )

        return cls(api_key=api_key)


@dataclass
class ServerConfig:
    """MCP Server configuration."""
    output_dir: Path = Path("./nanobanana-output")
    model: str = "gemini-3-pro-image-preview"
    timeout: int = 60
    auto_refresh: bool = True
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Load server config from environment."""
        output_dir = Path(os.getenv("NANOBANANA_OUTPUT_DIR", "./nanobanana-output"))
        model = os.getenv("NANOBANANA_MODEL", "models/gemini-3-pro-image-preview")
        timeout = int(os.getenv("NANOBANANA_TIMEOUT", "60"))
        
        return cls(
            output_dir=output_dir,
            model=model,
            timeout=timeout
        )
    
    def ensure_output_dir(self) -> Path:
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
