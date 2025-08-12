from gallery_organiser import server, database
from PIL import Image


def setup_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "db.sqlite")
    database.init_db()


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
    setup_db(tmp_path, monkeypatch)

    def fake_scan_media(path):
        return ([{"path": str(tmp_path / "img.jpg"), "label": "cat"}], 0, ["log"])

    monkeypatch.setattr(server, "scan_media", fake_scan_media)
    client = server.app.test_client()
    resp = client.get("/api/media", query_string={"path": str(tmp_path)})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["files"][0]["label"] == "cat"
    assert data["skipped"] == 0
    assert data["logs"] == ["log"]


def test_tag_and_search(monkeypatch, tmp_path):
    setup_db(tmp_path, monkeypatch)

    def fake_detect(path):
        return [(0, 0, 10, 10)]

    monkeypatch.setattr(server, "detect_faces", fake_detect)
    client = server.app.test_client()
    img_path = tmp_path / "a.jpg"
    img_path.write_text("a")
    resp = client.post("/api/tag", json={"path": str(img_path), "name": "Bob"})
    assert resp.status_code == 200
    resp = client.get("/api/search", query_string={"name": "Bob"})
    assert resp.status_code == 200
    assert resp.get_json()[0]["path"] == str(img_path)


def test_run_server_uses_public_host(monkeypatch):
    called = {}

    def fake_run(*args, **kwargs):
        called.update(kwargs)

    monkeypatch.setattr(server.app, "run", fake_run)
    server.run_server()
    assert called.get("host") == "0.0.0.0"
