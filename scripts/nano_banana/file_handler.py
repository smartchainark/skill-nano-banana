"""File handling utilities for Nano Banana MCP."""

import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class FileSearchResult:
    """Result of searching for an input file."""
    found: bool
    file_path: Optional[Path] = None
    searched_paths: List[Path] = None
    
    def __post_init__(self):
        if self.searched_paths is None:
            self.searched_paths = []


class FileHandler:
    """Handles file operations for image generation."""
    
    SEARCH_PATHS = [
        Path.cwd(),
        Path.cwd() / "images",
        Path.cwd() / "input",
        Path.cwd() / "nanobanana-output",
        Path.home() / "Downloads",
        Path.home() / "Desktop",
        Path.home() / "Pictures",
    ]
    
    @classmethod
    def find_input_file(cls, filename: str) -> FileSearchResult:
        """Search for an input file in common locations."""
        file_path = Path(filename)
        
        if file_path.is_absolute() and file_path.exists():
            return FileSearchResult(found=True, file_path=file_path)
        
        for search_path in cls.SEARCH_PATHS:
            full_path = search_path / filename
            if full_path.exists():
                return FileSearchResult(
                    found=True,
                    file_path=full_path,
                    searched_paths=cls.SEARCH_PATHS
                )
        
        return FileSearchResult(
            found=False,
            searched_paths=cls.SEARCH_PATHS
        )
    
    @staticmethod
    def generate_filename(
        prompt: str,
        extension: str = "png",
        index: int = 0
    ) -> str:
        """Generate a user-friendly filename from prompt."""
        base_name = prompt.lower()
        base_name = "".join(c if c.isalnum() or c.isspace() else "" for c in base_name)
        base_name = "_".join(base_name.split())[:32]
        
        if not base_name:
            base_name = "generated_image"
        
        if index > 0:
            base_name = f"{base_name}_{index}"
        
        return f"{base_name}.{extension}"
    
    @staticmethod
    def get_unique_filepath(directory: Path, filename: str) -> Path:
        """Get a unique filepath, adding counter if file exists."""
        filepath = directory / filename
        
        if not filepath.exists():
            return filepath
        
        stem = filepath.stem
        suffix = filepath.suffix
        counter = 1
        
        while filepath.exists():
            filepath = directory / f"{stem}_{counter}{suffix}"
            counter += 1
        
        return filepath
