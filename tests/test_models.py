import sys
from pathlib import Path

# Ensure the package root is on the path when running tests directly
sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser.models import Artwork, Gallery


def test_add_and_list_artwork():
    gallery = Gallery(name="Test")
    art = Artwork(title="Mona Lisa", artist="Leonardo da Vinci", year=1503)
    gallery.add_artwork(art)

    artworks = gallery.list_artworks()
    assert len(artworks) == 1
    assert artworks[0].title == "Mona Lisa"
    assert artworks[0].artist == "Leonardo da Vinci"
    assert artworks[0].year == 1503
