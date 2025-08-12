"""Command line interface for the gallery organiser."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .models import Artwork, Gallery

DATA_FILE = Path("gallery_data.json")


def build_parser() -> argparse.ArgumentParser:
    """Create an argument parser for the CLI.

    Split out for easier testing and to avoid global parser state.
    """
    parser = argparse.ArgumentParser(description="Gallery organiser CLI")
    parser.add_argument("command", choices=["add", "list", "serve"])
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--name", default="My Gallery")
    parser.add_argument("--title")
    parser.add_argument("--artist")
    parser.add_argument("--year", type=int)
    return parser


def load_gallery(name: str) -> Gallery:
    """Load gallery data from disk if available."""
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text())
        artworks = [Artwork(**a) for a in data.get("artworks", [])]
        return Gallery(name=name, artworks=artworks)
    return Gallery(name=name)


def save_gallery(gallery: Gallery) -> None:
    """Persist gallery data to disk."""
    data = {
        "name": gallery.name,
        "artworks": [a.__dict__ for a in gallery.artworks],
    }
    DATA_FILE.write_text(json.dumps(data, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"add", "list"}:
        gallery = load_gallery(args.name)

    if args.command == "add":
        if not args.title or not args.artist:
            parser.error("add requires --title and --artist")
        artwork = Artwork(title=args.title, artist=args.artist, year=args.year)
        gallery.add_artwork(artwork)
        save_gallery(gallery)
        print(f"Added artwork '{artwork.title}' by {artwork.artist}")
    elif args.command == "list":
        for art in gallery.list_artworks():
            yr = art.year if art.year is not None else "Unknown year"
            print(f"{art.title} by {art.artist} ({yr})")
    else:
        from .server import run_server
        run_server()


if __name__ == "__main__":  # pragma: no cover
    main()
