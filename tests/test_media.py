import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser.media import scan_media


def test_scan_media(tmp_path):
    (tmp_path / "image.jpg").write_text("a")
    (tmp_path / "video.mp4").write_text("a")
    (tmp_path / "photo.heic").write_text("a")
    (tmp_path / "doc.txt").write_text("a")

    files = scan_media(tmp_path)
    names = sorted(p.name for p in files)
    assert names == ["image.jpg", "photo.heic", "video.mp4"]
