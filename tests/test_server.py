from gallery_organiser import server, database, tasks, media
from gallery_organiser import server, database, tasks, media
from gallery_organiser import server, database, tasks, media
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


def test_scan_endpoint(monkeypatch, tmp_path):
    setup_db(tmp_path, monkeypatch)
    tasks.celery_app.conf.task_always_eager = True

    def fake_classify(path):
        return "cat"

    monkeypatch.setattr(media, "classify_image", fake_classify)
    img = tmp_path / "a.jpg"
    Image.new("RGB", (1, 1)).save(img)
    client = server.app.test_client()
    resp = client.post("/api/scan", json={"path": str(tmp_path)})
    assert resp.status_code == 200
    task_id = resp.get_json()["task_id"]
    resp = client.get(f"/api/scan/{task_id}")
    data = resp.get_json()
    assert data["state"] == "SUCCESS"
    assert data["files"][0]["path"] == str(img)
    assert data["summary"]["cat"] == 1


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
