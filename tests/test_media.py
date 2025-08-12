import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser import media


def test_scan_media(tmp_path, monkeypatch):
    (tmp_path / "image.jpg").write_text("a")
    (tmp_path / "video.mp4").write_text("a")
    (tmp_path / "photo.heic").write_text("a")
    (tmp_path / "doc.txt").write_text("a")

    monkeypatch.setattr(media, "classify_image", lambda p: "label")
    files, skipped = media.scan_media(tmp_path)
    names = sorted(Path(f["path"]).name for f in files)
    labels = [f.get("label") for f in files if f.get("label")]
    assert names == ["image.jpg", "photo.heic", "video.mp4"]
    assert labels == ["label", "label"]
    assert skipped == 0


def test_scan_media_skips_inaccessible(tmp_path, monkeypatch):
    bad = tmp_path / "bad.jpg"
    bad.write_text("a")

    def bad_classify(path: Path) -> str:
        raise PermissionError

    monkeypatch.setattr(media, "classify_image", bad_classify)
    files, skipped = media.scan_media(tmp_path)
    assert files == []
    assert skipped == 1
