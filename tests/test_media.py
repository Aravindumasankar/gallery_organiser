import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from gallery_organiser import media, database


def setup_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "db.sqlite")
    database.init_db()


def test_scan_media(tmp_path, monkeypatch):
    setup_db(tmp_path, monkeypatch)
    (tmp_path / "image.jpg").write_text("a")
    (tmp_path / "video.mp4").write_text("a")
    (tmp_path / "photo.heic").write_text("a")
    (tmp_path / "doc.txt").write_text("a")

    monkeypatch.setattr(media, "classify_image", lambda p: "label")
    files, skipped, logs, _ = media.scan_media(tmp_path)
    names = sorted(Path(f["path"]).name for f in files)
    labels = [f.get("label") for f in files if f.get("label")]
    assert names == ["image.jpg", "photo.heic", "video.mp4"]
    assert labels == ["label", "label"]
    assert skipped == 0
    assert any("Found" in log for log in logs)


def test_scan_media_skips_inaccessible(tmp_path, monkeypatch):
    setup_db(tmp_path, monkeypatch)
    bad = tmp_path / "bad.jpg"
    bad.write_text("a")

    def bad_classify(path: Path) -> str:
        raise PermissionError

    monkeypatch.setattr(media, "classify_image", bad_classify)
    files, skipped, logs, _ = media.scan_media(tmp_path)
    assert files == []
    assert skipped == 1
    assert any("Skipped" in log for log in logs)
