"""Data models for the gallery organiser."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Artwork:
    """Represents a piece of art."""

    title: str
    artist: str
    year: int | None = None


@dataclass
class Gallery:
    """A simple in-memory gallery."""

    name: str
    artworks: List[Artwork] = field(default_factory=list)

    def add_artwork(self, artwork: Artwork) -> None:
        """Add an artwork to the gallery."""
        self.artworks.append(artwork)

    def list_artworks(self) -> List[Artwork]:
        """Return the artworks currently stored."""
        return list(self.artworks)
