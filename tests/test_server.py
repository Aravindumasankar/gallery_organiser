from gallery_organiser import server
from PIL import Image

def test_api_dirs(tmp_path):
    (tmp_path / "sub").mkdir()
    client = server.app.test_client()
    resp = client.get("/api/dirs", query_string={"path": str(tmp_path)})
    assert resp.status_code == 200
    assert str(tmp_path / "sub") in resp.get_json()


def test_api_file(tmp_path):
    img_path = tmp_path / "pic.png"
    Image.new("RGB", (1, 1)).save(img_path)
    client = server.app.test_client()
    resp = client.get("/api/file", query_string={"path": str(img_path)})
    assert resp.status_code == 200
    assert resp.mimetype == "image/png"


def test_api_media(monkeypatch, tmp_path):
    def fake_scan_media(path):
        return [{"path": str(tmp_path / "img.jpg"), "label": "cat"}]

    monkeypatch.setattr(server, "scan_media", fake_scan_media)
    client = server.app.test_client()
    resp = client.get("/api/media", query_string={"path": str(tmp_path)})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data[0]["label"] == "cat"
